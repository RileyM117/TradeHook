from rest_framework import serializers
from .models import *

# Defines user information to be shown in backend.
class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'user_id','email','first_name','last_name','username','password']
        
class CustomerBrokersSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = CustomerBrokers
        fields = ['id','user_id','broker_name','broker_api_key','broker_secret_key']
   
class APIKeysSerializer(serializers.ModelSerializer):
    # maintains tradehook_api_key being generated.
    tradehook_api_key = serializers.UUIDField(read_only=True)
    user_id = serializers.IntegerField()
    
    
    class Meta:
        model = APIKeys
        fields = ['id','user_id','tradehook_api_key']

class EventLogSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = EventLog
        fields = ['id','user_id','received_at','webhook_data','broker_response']

class BrokerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Broker
        fields = ['id','broker_name','description']

