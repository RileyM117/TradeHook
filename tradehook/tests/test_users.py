from rest_framework.test import APIClient
from rest_framework import status
from tradehook.models import User
import pytest
from model_bakery import baker

@pytest.fixture
def create_user(api_client):
    def do_create_user(user):
        return api_client.post('/tradehook/users/', user)
    return do_create_user

@pytest.mark.django_db
class TestCreateUser:

    def test_if_user_is_not_admin_returns_403(self,authenticate,create_user):

        # Arrange
        authenticate()
        # Act
        response = create_user({"email": "testuser@test.com","first_name": "test","last_name": "user","password": "TestPassword123"})
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self):
        # AAA = Arrange, Act, Assert

        # Arrange

        # Act
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/tradehook/users/',{"email": "","first_name": "test","last_name": "user","password": "TestPassword123"})

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['email'] is not None

    def test_if_data_is_valid_returns_201(self):
        # AAA = Arrange, Act, Assert

        # Arrange

        # Act
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/tradehook/users/',{"email": "testuser@test.com","first_name": "test","last_name": "user","password": "TestPassword123"})

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

    
