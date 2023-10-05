from rest_framework.test import APIClient
from rest_framework import status
from tradehook.models import CustomerBrokers, User
import pytest
from model_bakery import baker

@pytest.fixture
def create_customer_brokers(api_client):
    def do_create_customer_brokers(customer_broker):
        return api_client.post('/tradehook/customer_brokers/', customer_broker)
    return do_create_customer_brokers

@pytest.mark.django_db
class TestCreateCustomerBroker:

    def test_if_customer_broker_data_is_invalid_returns_400(self):#,authenticate,create_customer_brokers):

        customer_broker = baker.make(CustomerBrokers)
        user = baker.make(User)
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/tradehook/customer_brokers/',{"user_id": user.id,"broker_name": customer_broker.broker_name,
                                                               "broker_api_key": "",
                                                               "broker_secret_key": ""})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['broker_api_key'] is not None
        assert response.data['broker_secret_key'] is not None

    def test_if_customer_broker_data_is_valid_returns_201(self):

        customer_broker = baker.make(CustomerBrokers)
        user = baker.make(User)
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/tradehook/customer_brokers/',{"user_id": user.id,"broker_name": customer_broker.broker_name,
                                                               "broker_api_key": customer_broker.broker_api_key,
                                                               "broker_secret_key": customer_broker.broker_secret_key})
        assert response.status_code == status.HTTP_201_CREATED
