from rest_framework.test import APIClient
from rest_framework import status
from tradehook.models import User, APIKeys
import pytest
from model_bakery import baker

@pytest.fixture
def create_api_key(api_client):
    def do_create_api_key(api_key):
        return api_client.post('/tradehook/users/', api_key)
    return do_create_api_key

@pytest.mark.django_db
class TestCreateAPIKey:

    def test_if_data_is_invalid_returns_400(self):
        
        
        # Act
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/tradehook/api_keys/',{})
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['user_id'] is not None

    def test_if_data_is_valid_returns_201(self):
       # AAA = Arrange, Act, Assert

       # Arrange
       user = baker.make(User)
       # Act
       client = APIClient()
       client.force_authenticate(user=User(is_staff=True))
       response = client.post('/tradehook/api_keys/',{"user_id": user.id})
       # Assert
       assert response.status_code == status.HTTP_201_CREATED
       assert response.data['id'] > 0

    
