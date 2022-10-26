import email
import json
from msilib.schema import Class
from multiprocessing import context
from django.forms import ValidationError
from django.shortcuts import render
from django.urls import reverse
from pytz import timezone, utc
from requests import Session, request, session
from yaml import serialize
import razorpay
from django.views.generic import View
from datetime import datetime , timedelta
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK , HTTP_404_NOT_FOUND
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import views
from .models import SubscriptionPlan,User,UserSubscription,SubscriptionOrder,SubscriptionPayment
from resources.api.serializers import CheckoutSubscriptionDataSerializer, SubscriptionPaymentSerializer,UserSubscriptionSerializer,SubscriptionOrderSerializer
# Create your views here.

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

class Payment(generics.ListAPIView):
    queryset = SubscriptionOrder.objects.all()
    serializer_class = SubscriptionOrderSerializer
    '''def get_serializer_context(self):
        context = super().get_serializer_context()
        context['message'] = "Successfully Paid!"
        return context'''
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = SubscriptionOrderSerializer(queryset, many=True)

        # append serializer's data with some additional value
        response_list = serializer.data 
        response_list.append({"Status":"Successfully Paid!"})
        return Response(response_list)

    def get_queryset(self):
        user = self.request.user
        upd_status = SubscriptionOrder.objects.get(order_by = user,created_at__date=datetime.today().strftime('%Y-%m-%d'))
        upd_status.status = "confirmed"
        upd_status.save()
        return SubscriptionOrder.objects.filter(order_by = user,created_at__date=datetime.today().strftime('%Y-%m-%d'))

class CheckoutSubscriptionData(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = CheckoutSubscriptionDataSerializer
    api_views = ["POST"]

    def post(self, request):
        try:
            subscription_plan_id = request.data.get('subscription_plan_id')
            subscription_plan_obj = SubscriptionPlan.objects.get(pk=subscription_plan_id)
            amount = subscription_plan_obj.plan_amount
            amount = amount * 100
            amount = amount + ((amount * subscription_plan_obj.tax)/100)
            currency = subscription_plan_obj.currency
            user_prof = User.objects.get(email=request.user)
            user_exist = SubscriptionOrder.objects.filter(order_by=request.user).last()
            print(user_exist)
            if user_exist:
                if UserSubscription.objects.filter(user_id=request.user,is_expired=False).last():
                    return Response({'Status':'Failed', 'Reason':'Already have active plan.'})

            order_dict = {'amount':amount , 'currency':currency , 'payment_capture':'0', 'notes':{'plan_id':subscription_plan_id , 'order_by':user_prof.id}}
            razorpay_order = razorpay_client.order.create(order_dict)
            
            if request.is_secure():
                request_method = "https"
            else:
                request_method = "http"
            
            request_host = request.get_host()
            full_host = request_method + "://" + request_host +"/api/"
            print(full_host)
            #callback_url =  full_host + reverse('callback')
            callback_url = "http://" + "127.0.0.1:8000" + "/api/callback/"
            data = {
                'key': settings.RAZOR_KEY_ID,
                'amount': amount,
                'currency': currency,
                'name': 'Resolab Pvt. Ltd.',
                'callback_url': callback_url,
                'order_id': razorpay_order.get('id')
            }
            
            return render(request,"payment.html",data)
           
        except Exception as error:
            return Response({'response': str(error)}, 401)
            #return render(request, "payment.html")



@method_decorator(csrf_exempt, name='dispatch')
class SubscriptionCallbackEndpoint(View):
    def post(self, request):
        
        '''if 'razorpay_payment_id' in request.POST:
            print('Signature present')
            return render(request, "callback.html", context={"status": "Success"})
        else:
            print('Signature Not present')
            return render(request, "callback.html", context={"status": "Signature Not present"})'''
        try:
           
            
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            print(result)

            if result is True:
                print("signature verify")
                amount = razorpay_client.order.fetch(razorpay_order_id).get('amount')
                order_notes = razorpay_client.order.fetch(razorpay_order_id).get('notes')
                plan_id = order_notes.get('plan_id')  
                user_id = order_notes.get('order_by')  
                epoch_time = razorpay_client.order.fetch(razorpay_order_id).get('created_at')
                created_at = datetime.fromtimestamp(epoch_time)
                
                order_data = {
                    'order_id': razorpay_order_id,
                    'plan_id': plan_id,
                    'amount': amount,
                    'currency': 'INR',
                    'amount_unit': 'paise',
                    'status': 'pending',
                    'order_by': user_id,
                    'created_at': created_at,
                    'updated_at': datetime.now(),
                }
                
                order_serializer = SubscriptionOrderSerializer(data=order_data)
                
                if order_serializer.is_valid():
                    order_serializer.save()
                    print("subscription Order Save")
                else:
                    return render(request, "callback.html", context={"status": "Failure"})
                
                try:
                    razorpay_response =  razorpay_client.payment.capture(payment_id, amount)
                    card = razorpay_response.pop('card')
                    new_card_dict = dict()
                    [new_card_dict.update({"card_"+key: i}) for key, i in card.items()]

                    razorpay_response.update(new_card_dict)
                    razorpay_response['amount_unit'] = 'paise'
                    razorpay_response['payment_id'] = razorpay_response['id']


                    if razorpay_response.get('notes'):
                        notes_list = [str(j) for i, j  in razorpay_response.get('notes').items()]
                        razorpay_response['notes'] = ", ".join(notes_list)
                    else:
                        razorpay_response['notes'] = ""
                        
                    epoch_time = razorpay_response.get('created_at')
                    created_at = datetime.fromtimestamp(epoch_time)
                    razorpay_response['created_at'] = created_at
                    razorpay_serializer = SubscriptionPaymentSerializer(data=razorpay_response)
                    
                    if razorpay_serializer.is_valid():
                        razorpay_serializer.save()    
                        plan = SubscriptionPlan.objects.get(pk=plan_id)
                        plan_category = plan.plan_category
                        plan_duation = plan.plan_duration
                        days = 0
                        if plan_duation == 'monthly':
                            days = 30
                        elif plan_duation == 'quarterly':
                            days = 90
                        elif plan_duation == 'semiannual':
                            days = 180
                        elif plan_duation == 'annual':
                            days = 360
                            
                        user_subscription_data = {
                            'plan_id' : plan_id ,
                            'user_id' : user_id , 
                            'is_expired' : False ,
                            'start_date' : created_at , 
                            'end_date' :  created_at + timedelta(days=days) , 
                            'created_at' : created_at , 
                            'updated_at' : datetime.now(),
                            'is_newly_registered' : False ,
                        }
                        
                        user_subscription_serializer = UserSubscriptionSerializer(data=user_subscription_data)
                        if user_subscription_serializer.is_valid():
                            user_subscription_serializer.save()
                            print("User Subscription Save")
                            request.session['msg'] = 'Your Payment is Successful'
                            return HttpResponseRedirect("http://127.0.0.1:8000/api/paymentstatus")
                    else:
                        return HttpResponseRedirect("http://127.0.0.1:8000/api/paymentstatus")
                    
                except:
                    return HttpResponseRedirect("http://127.0.0.1:8000/api/paymentstatus")
            else:
                return HttpResponseRedirect("http://127.0.0.1:8000/api/paymentstatus")
        except:
            return HttpResponseRedirect("http://127.0.0.1:8000/api/paymentstatus")


class IsUserSubscribed(APIView):
    def get(self ,request):
        try:
            current_date = datetime.now()
            current_date = utc.localize(current_date)
            user_profile = User.objects.get(user=request.user)
            user_subscriptions = UserSubscription.objects.filter(start_date__lte=current_date , end_date__gte=current_date , user_id=user_profile)
            
            if user_subscriptions:
                return Response({'is_user_subscribed':True} , status=HTTP_200_OK)
            return Response({'is_user_subscribed':False} , status=HTTP_200_OK)
        
        except Exception as error:
            return Response({'is_user_subscribed':False} , status=HTTP_200_OK)
