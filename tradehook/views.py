import json
from .broker_apis import alpaca_orders
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import ListModelMixin,CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import action
from django.contrib.auth import login, authenticate
from django.urls import reverse, reverse_lazy
from django.conf import settings
from rest_framework import permissions
from rest_framework import status
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.filters import SearchFilter, OrderingFilter
from django.views.decorators.csrf import csrf_exempt
import alpaca_trade_api as alpaca
import jwt, datetime
from .models import *
from .permissions import *
from .forms import *
from .serializers import *
from.pagination import *
ALPACA_API_BASE_URL = "https://paper-api.alpaca.markets"

#___________________________________________________________________________________________________________________________________________#
# Backend ViewSets

class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination

class CustomerBrokersViewSet(ModelViewSet):
    
    serializer_class = CustomerBrokersSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    queryset = CustomerBrokers.objects.all()

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        broker_name = request.data.get('broker_name')

        # Check if the user already has a CustomerBroker object with the same broker_name
        if CustomerBrokers.objects.filter(user_id=user_id, broker_name=broker_name).exists():
            return Response({'error': f'A CustomerBrokers object with the broker_name "{broker_name}" already exists for this customer.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomerBrokersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class APIKeysViewSet(ModelViewSet):
    
    serializer_class = APIKeysSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    queryset = APIKeys.objects.all()


    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')

        # Check if the user already has a CustomerBroker object with the same broker_name
        if APIKeys.objects.filter(user_id=user_id).exists():
            return Response({'error': f'A Tradehook API key already exists for this user.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = APIKeysSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventLogViewSet(DestroyModelMixin,ListModelMixin,RetrieveModelMixin,GenericViewSet):

    serializer_class = EventLogSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    queryset = EventLog.objects.all()
    

class BrokerViewSet(ListModelMixin,DestroyModelMixin,RetrieveModelMixin,GenericViewSet):

    serializer_class = BrokerSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    queryset = Broker.objects.all()
    

    def create(self, request, *args, **kwargs):

        serializer = BrokerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#___________________________________________________________________________________________________________________________________________#
# Frontend Views


def register(request):
    if request.method == 'POST':
        # If the form has been submitted, create a UserCreationForm instance with the POST data
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # If the form is valid, save the user and log them in
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)  # Replace 'home' with the URL name of your home page
    else:
        # If it's a GET request, display an empty registration form
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def home_page(request):
    return render(request,'home.html')


def brokers_list(request):
    brokers = Broker.objects.all()
    return render(request, 'brokers_list.html', {'brokers': brokers})


class MeView(View):
    permission_classes = [IsAuthenticated]

    
    def get(self,request,*args,**kwargs):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return render(request, 'customer_profile.html', {'customer': serializer.data})
        elif request.method == 'PUT':
            serializer = UserSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        

class EventLogView(View):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        # Query the APIKeys model to get the user's tradehook_api_key
        try:
            event_logs = EventLog.objects.filter(user=user)
        except EventLog.DoesNotExist:
            event_logs = None

        context = {
            'event_logs': event_logs,
        }

        return render(request, 'event_logs.html', context)

        #return render(request,'event_logs.html', {'event_logs': event_logs})


class APIKeyView(View):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        # Query the APIKeys model to get the user's tradehook_api_key
        try:
            api_key = APIKeys.objects.get(user=user)
        except APIKeys.DoesNotExist:
            api_key = None

        # Query the CustomerBrokers model to get the user's brokers
        user_brokers = CustomerBrokers.objects.filter(user=user)

        # Pass the API key and user brokers to the template
        context = {
            'api_key': api_key,
            'user_brokers': user_brokers,
        }

        return render(request, 'api_keys.html', context)

    def post(self, request, *args, **kwargs):
        user = request.user

        if request.POST.get('action') == 'generate':
            api_key, created = APIKeys.objects.get_or_create(user=user)
            if not created:
                return JsonResponse({'error': 'API key already exists.'}, status=400)
            #return redirect('http://127.0.0.1:8000/tradehook/manage/my_api_keys/')
            return redirect('https://tradehook-prod-fbb7997de66a.herokuapp.com/tradehook/manage/my_api_keys/')

        elif request.POST.get('action') == 'delete':
            try:
                api_key = APIKeys.objects.get(user=user)
                api_key.delete()
                #return redirect('http://127.0.0.1:8000/tradehook/manage/my_api_keys/')
                return redirect('https://tradehook-prod-fbb7997de66a.herokuapp.com/tradehook/manage/my_api_keys/')
            except APIKeys.DoesNotExist:
                return JsonResponse({'error': 'API key not found.'}, status=404)

        elif request.POST.get('action') == 'add_broker':
        # Handle the form submission to add a new broker
            broker_form = CustomerBrokerForm(request.POST)
            try:
                if broker_form.is_valid():
                    broker = broker_form.save(commit=False)
                    broker.user = user
                    broker.save()
                    #return redirect('http://127.0.0.1:8000/tradehook/manage/my_api_keys/')
                    return redirect('https://tradehook-prod-fbb7997de66a.herokuapp.com/tradehook/manage/my_api_keys/')
            except:
                #return redirect('http://127.0.0.1:8000/tradehook/manage/my_api_keys/')
                return redirect('https://tradehook-prod-fbb7997de66a.herokuapp.com/tradehook/manage/my_api_keys/')
          
            
        elif request.POST.get('action') == 'delete_broker':
            broker_id = request.POST.get('broker_id')
            try:
                broker = CustomerBrokers.objects.get(id=broker_id, user=user)
                broker.delete()
                #return redirect('http://127.0.0.1:8000/tradehook/manage/my_api_keys/')
                return redirect('https://tradehook-prod-fbb7997de66a.herokuapp.com/tradehook/manage/my_api_keys/')
            except CustomerBrokers.DoesNotExist:
                return JsonResponse({'error': 'Broker not found.'}, status=404)

    # Query the CustomerBrokers model to get the user's brokers
        user_brokers = CustomerBrokers.objects.filter(user=user)

        # Pass the API key and user brokers to the template
        context = {

            'user_brokers': user_brokers,
            'broker_form': broker_form,  # Include the broker form in the context
        }

        return render(request, 'api_keys.html', context)

#___________________________________________________________________________________________________________________________________________#
# Webhook Receiver

@csrf_exempt
def webhook_receiver(request):
    if request.method == 'POST':
        data = json.loads(request.body)
            
            # Extract the tradehook_api_key from the webhook data
        tradehook_api_key = data.get('tradehook_api_key')
        broker_name = data.get('broker_name')
        if not tradehook_api_key:
            return JsonResponse({'message': 'tradehook_api_key is missing in the webhook data'}, status=400)

            # Find the customer associated with the tradehook_api_key
        try:
            user = User.objects.get(apikeys__tradehook_api_key=tradehook_api_key)
        except User.DoesNotExist:
            return Response({'message': 'No customer found with this tradehook_api_key'}, status.HTTP_400_BAD_REQUEST)

            # Fetch the customer's broker_api_key and broker_secret_key
        try:
            customer_broker = CustomerBrokers.objects.get(user=user,broker_name=broker_name)
        except CustomerBrokers.DoesNotExist:
            return Response({'message': 'No broker information found for this customer'}, status.HTTP_400_BAD_REQUEST)

        #broker = customer_broker.broker_name
        broker_api_key = customer_broker.broker_api_key
        broker_secret_key = customer_broker.broker_secret_key
        api = alpaca.REST(broker_api_key, broker_secret_key, ALPACA_API_BASE_URL, api_version='v2')
          
        #order = api.submit_order(
        #symbol=data['ticker'],
        #qty=data['qty'],
        #side='buy',
        #type='market',
        #time_in_force='gtc'  # Good 'til Cancelled
        #)
        order = alpaca_orders.place_order(data,api)
        

                
    # Get the full JSON response for the order
        broker_response = order#json.dumps(order._raw)
        EventLog.objects.create(
        user=user,
        webhook_data=data,
        broker_response=broker_response,
        )
        
        return JsonResponse({'message': 'Webhook data processed and saved successfully'}, status=status.HTTP_201_CREATED)




