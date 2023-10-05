from locust import HttpUser, task, between
from random import randint
#user_id=7
class APIKeyTester(HttpUser):
    wait_time=between(1,3)
    @task
    def create_api_key(self):
        self.client.post('/tradehook/api_keys/',name='tradehook/api_keys',json={"user_id":7})
    @task
    def delete_api_key(self):
        self.client.delete('/tradehook/api_keys/12',name='tradehook/api_keys/delete')