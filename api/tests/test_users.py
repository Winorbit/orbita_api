from django.test import TestCase
from rest_framework.test import APIClient
from .. import users 
from django.contrib.auth.models import User

class UsersTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        test_user = User.objects.create(username= "User", password = 'TOPSECRET', email="user_num@gmail.com")
        test_user_profile = users.UserProfile.objects.create(user=test_user, id=test_user.id, user_courses=[])

    def test_search_userprofile(self):
        userprofile_resp = {'email': 'user_num@gmail.com',
                            'id': 1,
                            'password': 'TOPSECRET',
                            'profile_image': None,
                            'user': 1,
                            'is_superuser': False,
                            'user_courses': [],
                            'username': 'User'}
       
        response = self.client.post("/search_userprofile", {"username": "User", "password": "TOPSECRET"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue( all(item in response.data.items() for item in userprofile_resp.items()))

        response = self.client.post("/search_userprofile", {"username": "user_num@gmail.com", "password": "TOPSECRET"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue( all(item in response.data.items() for item in userprofile_resp.items()))

        response = self.client.post("/search_userprofile", {"username": "User", "password": ""})
        self.assertEqual(response.status_code, 401)
        
        response = self.client.post("/search_userprofile", {"username": "User"})
        self.assertEqual(response.status_code, 401)
        
        response = self.client.post("/search_userprofile")
        self.assertEqual(response.status_code, 400)
