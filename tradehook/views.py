import json
from .broker_apis import alpaca_orders
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.mixins import ListModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django.contrib.auth import login
from django.conf import settings
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import alpaca_trade_api as alpaca
from .models import *
from .permissions import *
from .forms import *
from .serializers import *
from.pagination import *

ALPACA_API_BASE_URL = "https://paper-api.alpaca.markets"
ALPACA_LIVE_URL = "https://api.alpaca.markets"

#___________________________________________________________________________________________________________________________________________#
# Backend ViewSets

class UserViewSet(ModelViewSet):

    # loads all users to be viewed if authenticated user is an admin. ModelViewSet also allows for modifying, creating, and deleting model objects.
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination

class CustomerBrokersViewSet(ModelViewSet):
    
   
    serializer_class = CustomerBrokersSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    queryset = CustomerBrokers.objects.all()

    # Custom CustomerBroker creation method
    def create(self, request, *args, **kwargs):
        # gets the user id
        user_id = request.data.get('user_id')
        # gets the broker name
        broker_name = request.data.get('broker_name')
        # Check if the user already has a CustomerBroker object with the same broker_name
        if CustomerBrokers.objects.filter(user_id=user_id, broker_name=broker_name).exists():
            return Response({'error': f'A CustomerBrokers object with the broker_name "{broker_name}" already exists for this customer.'}, status=status.HTTP_400_BAD_REQUEST)

        # If user does not have duplicate object, check if information is valid and create.
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

    # Custom APIKey creation method
    def create(self, request, *args, **kwargs):
        # same as before, get user id
        user_id = request.data.get('user_id')

        # Check if the user already has a TradeHook api key already
        if APIKeys.objects.filter(user_id=user_id).exists():
            return Response({'error': f'A Tradehook API key already exists for this user.'}, status=status.HTTP_400_BAD_REQUEST)

        # if not then create.
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

# Custom registration view.
def register(request):
    if request.method == 'POST':
        # Check if user information is valid
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
            
    else:
        form = UserRegistrationForm()

    # Customize the labels
    form.fields['first_name'].label = "First Name"
    form.fields['last_name'].label = "Last Name"
    form.fields['username'].label = "Username"
    form.fields['email'].label = "Email"
    form.fields['password1'].label = "Password"
    form.fields['password2'].label = "Password Confirmation"

    # render custom registration page.
    return render(request, 'registration/register.html', {'form': form})

# render home page with total webhook count. for fun
def home_page(request):
    webhook_count = EventLog.objects.all().count()
    return render(request,'home.html', {'webhook_count': webhook_count})

# render current broker list
def brokers_list(request):
    brokers = Broker.objects.all()
    return render(request, 'brokers_list.html', {'brokers': brokers})

def account(request):
    return render(request,'setup_guide.html')

def alert_guide(request):
    return render(request,'alert_guide.html')

# Custom View to see user profile
class MeView(View):

    # custom get method.
    def get(self,request,*args,**kwargs):
        # get the current user
        user = request.user
        # serializer current users data to be rendered in html.
        serializer = UserSerializer(user)
        return render(request, 'customer_profile.html', {'customer': serializer.data})
    
class EventLogView(View):
    
    # Custom get method for users Event Log
    def get(self, request, *args, **kwargs):
        user = request.user

        # if user has event log, retrieve it, else render nothing.
        try:
            event_logs = EventLog.objects.filter(user=user)
        except EventLog.DoesNotExist:
            event_logs = None

        context = {
            'event_logs': event_logs,
        }

        return render(request, 'event_logs.html', context)

# Custom View to render all API keys on one page. (Broker API Keys and TradeHook API key)
class APIKeyView(View):

        #
        # INSTEAD OF ERROR JSON RESPONSES, IMPLEMENT IN FRONTEND, JUST HIDE BUTTONS 
        #

    def get(self, request, *args, **kwargs):
        user = request.user

        # Query the APIKeys model to get the user's tradehook_api_key if it exists
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

    # custom post method for creating and deleting various API keys and brokers
    def post(self, request, *args, **kwargs):
        user = request.user

        # differentiate between generating and deleting for TradeHook API Key
        if request.POST.get('action') == 'generate':
            form = APIKeyForm(request.POST)


            # violates rule
            api_key, created = APIKeys.objects.get_or_create(user=user)

            # JUST HIDE THE GENERATE BUTTON INSTEAD OF STATUS ERROR AND JSONRESPONSE
            #if not created:
            #    return JsonResponse({'error': 'API key already exists.'}, status=400)
            
            # reload the page. 

            #return render(request, "api_keys.html", {'api_key': api_key})


            return redirect('https://tradehook-prod-fbb7997de66a.herokuapp.com/tradehook/api-keys/')
        
            
        elif request.POST.get('action') == 'delete':
            try:
                api_key = APIKeys.objects.get(user=user)
                api_key.delete()
                
                return redirect('https://tradehook-prod-fbb7997de66a.herokuapp.com/tradehook/api-keys/')
            # JUST HIDE THE DELETE BUTTON INSTEAD OF STATUS ERROR AND JSONRESPONSE
            except APIKeys.DoesNotExist:
                return redirect('https://tradehook-prod-fbb7997de66a.herokuapp.com/tradehook/api-keys/')
                #return JsonResponse({'error': 'API key not found.'}, status=404)
            
        # Handle the form submission to add a new broker
        elif request.POST.get('action') == 'add_broker':
        
            broker_form = CustomerBrokerForm(request.POST)
            try:
                if broker_form.is_valid():
                    broker = broker_form.save(commit=False)
                    broker.user = user
                    broker.save()
                    
                    return redirect('https://tradehook-prod-fbb7997de66a.herokuapp.com/tradehook/api-keys/')
                # JUST HIDE THE GENERATE BUTTON INSTEAD OF REDIRECT
            except:
                
                return redirect('https://tradehook-prod-fbb7997de66a.herokuapp.com/tradehook/api-keys/')
          
            
        elif request.POST.get('action') == 'delete_broker':
            broker_id = request.POST.get('broker_id')
            try:
                broker = CustomerBrokers.objects.get(id=broker_id, user=user)
                broker.delete()
                
                return redirect('https://tradehook-prod-fbb7997de66a.herokuapp.com/tradehook/api-keys/')
            # JUST HIDE THE DELETE BUTTON INSTEAD OF STATUS ERROR AND JSONRESPONSE
            except CustomerBrokers.DoesNotExist:
                return JsonResponse({'error': 'Broker not found.'}, status=404)

        # Query the CustomerBrokers model to get the user's brokers
        user_brokers = CustomerBrokers.objects.filter(user=user)

        # Pass the API keys and user brokers to the template
        context = {

            'user_brokers': user_brokers,
            'broker_form': broker_form,  # Include the broker form in the context
        }

        return render(request, 'api_keys.html', context)

#___________________________________________________________________________________________________________________________________________#
# Webhook Receiver

# This logic is in a view so that it can be easily applied to an endpoint. 
# it is csrf exempt since it does not have direct server-client interactions.
@csrf_exempt
#@api_view(['POST'])
def webhook_receiver(request):
    # Check for post request
    if request.method == 'POST':
        # load received webhook
        data = json.loads(request.body)
            
        # Extract the tradehook_api_key and broker name from the webhook data
        tradehook_api_key = data.get('tradehook_api_key')
        broker_name = data.get('broker_name')
        if not tradehook_api_key:
            return JsonResponse({'message': 'tradehook_api_key is missing in the webhook data'}, status=400)

        # Find the user associated with the tradehook_api_key
        try:
            user = User.objects.get(apikeys__tradehook_api_key=tradehook_api_key)
        except User.DoesNotExist:
            return Response({'message': 'No customer found with this tradehook_api_key'}, status.HTTP_400_BAD_REQUEST)

        # Fetch the customer's broker_api_key and broker_secret_key
        try:
            customer_broker = CustomerBrokers.objects.get(user=user,broker_name=broker_name)
        except CustomerBrokers.DoesNotExist:
            return Response({'message': 'No broker information found for this customer'}, status.HTTP_400_BAD_REQUEST)

        broker_api_key = customer_broker.broker_api_key
        broker_secret_key = customer_broker.broker_secret_key
        # differentiate between live and paper trading brokerage endpoints
        # When adding more brokers will have to add conditions for different brokers.
        if 'Paper' in broker_name:
            api = alpaca.REST(broker_api_key, broker_secret_key, ALPACA_API_BASE_URL, api_version='v2')
        else:
            api = alpaca.REST(broker_api_key, broker_secret_key, ALPACA_LIVE_URL, api_version='v2')
          
        order = alpaca_orders.place_order(data,api)
        

                
    # Get the JSON response for the order
        broker_response = order
        EventLog.objects.create(
        user=user,
        webhook_data=data,
        broker_response=broker_response,
        )
        
        return JsonResponse({'message': 'Webhook data processed and saved successfully'}, status=status.HTTP_201_CREATED)
    # if non post request is made to this endpoint, throw error.
    return HttpResponseBadRequest('Only POST requests are supported for this endpoint')


