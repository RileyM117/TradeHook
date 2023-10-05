import pytest
from rest_framework.test import APIClient
from tradehook.models import User

@pytest.fixture
def api_client():

    return APIClient()

@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_superuser=True):
        return api_client.force_authenticate(user=User(is_superuser=is_superuser))
    return do_authenticate


#api_client = APIClient()
#admin_user = User.objects.create_superuser('testadmin@example.com','testadmin', 'test','admin','password')
#api_client.force_authenticate(api_client, admin_user)