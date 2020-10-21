from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .. import users
from .. serializers import UserSerializer


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
        self.assertTrue( all(item in response.data.keys() for item in userprofile_resp.keys()))

        response = self.client.post("/search_userprofile", {"username": "user_num@gmail.com", "password": "TOPSECRET"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue( all(item in response.data.keys() for item in userprofile_resp.keys()))

        response = self.client.post("/search_userprofile", {"username": "User", "password": ""})
        self.assertEqual(response.status_code, 401)

        response = self.client.post("/search_userprofile", {"username": "User"})
        self.assertEqual(response.status_code, 401)

        response = self.client.post("/search_userprofile", {"username": "newUser", "password": "123"})
        self.assertEqual(response.status_code, 404)

        response = self.client.post("/search_userprofile")
        self.assertEqual(response.status_code, 400)


    def test_create(self):
        response = self.client.post("/users/", {"username":"newUser", "email":"newuser_num@gmail.com", "password":"TOPSECRET"}, format='json')
        self.assertEqual(response.status_code, 201)

        response = self.client.post("/users/", {"username":"User", "email":"user_num@gmail.com", "password":"TOPSECRET"}, format='json')
        self.assertEqual(response.status_code, 412)

        # если уже есть пользователь с таким же именем новый не сможет зарегаться
        response = self.client.post("/users/", {"username":"User", "email":"user_num2@gmail.com", "password":"TOPSECRET"}, format='json')
        self.assertEqual(response.status_code, 412)

        # но могут быть два разных пользователя с одной почтой
        response = self.client.post("/users/", {"username":"User2", "email":"newuser_num@gmail.com", "password":"TOPSECRET"}, format='json')
        self.assertEqual(response.status_code, 201)

        response = self.client.post("/users/", {"username":"", "email":"", "password":""}, format='json')
        self.assertEqual(response.status_code, 412)

        response = self.client.post("/users/", {"username":"dasdas", "email":"sdsdads", "password":"sadsad"}, format='json')
        self.assertEqual(response.status_code, 412)

        response = self.client.post("/users/", {"username":None, "email":None, "password":None}, format='json')
        self.assertEqual(response.status_code, 412)


    def test_serch_user_by_email(self):
        response = self.client.post("/search_user_by_email", {"email":"user_num@gmail.com"})
        self.assertEqual(response.status_code, 200)

        response = self.client.post("/search_user_by_email", {"email":"new_user_num@gmail.com"})
        self.assertEqual(response.status_code, 404)
