from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
import logging

from .. import users
from .. serializers import UserSerializer


class UsersTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        test_user = User.objects.create(username= "User", password = 'TOPSECRET', email="user_num@gmail.com")
        test_user_profile = users.UserProfile.objects.create(user=test_user, id=test_user.id, user_courses=[])

        logging.disable(logging.CRITICAL)

        self.userprofile_resp = {'email': 'user_num@gmail.com',
                            'password': 'TOPSECRET',
                            'profile_image': None,
                            'is_superuser': False,
                            'user_courses': [],
                            'username': 'User'}


    def tearDown(self):
        logging.disable(logging.NOTSET)


    def test_search_userprofile_by_username(self):
        response = self.client.post("/search_userprofile", {"username": "User", "password": "TOPSECRET"})
        self.assertEqual(response.status_code, 200)

    def test_search_userprofile_on_valid_response_by_username(self):
        response = self.client.post("/search_userprofile", {"username": "User", "password": "TOPSECRET"})
        self.assertTrue( all(item in response.data.items() for item in self.userprofile_resp.items()))

    def test_search_userprofile_by_email (self):
        response = self.client.post("/search_userprofile", {"username": "user_num@gmail.com", "password": "TOPSECRET"})
        self.assertEqual(response.status_code, 200)

    def test_search_userprofile_on_valid_response_by_email (self):
        response = self.client.post("/search_userprofile", {"username": "user_num@gmail.com", "password": "TOPSECRET"})
        self.assertTrue( all(item in response.data.items() for item in self.userprofile_resp.items()))

    def test_search_userprofile_with_blank_password (self):
        response = self.client.post("/search_userprofile", {"username": "User", "password": ""})
        self.assertEqual(response.status_code, 401)

    def test_search_userprofile_only_username (self):
        response = self.client.post("/search_userprofile", {"username": "User"})
        self.assertEqual(response.status_code, 401)

    def test_search_userprofile_nonexistent_username (self):
        response = self.client.post("/search_userprofile", {"username": "newUser", "password": "123"})
        self.assertEqual(response.status_code, 404)

    def test_search_userprofile_without_arguments (self):
        response = self.client.post("/search_userprofile")
        self.assertEqual(response.status_code, 400)


    def test_create_new_user(self):
        response = self.client.post("/users", {"username":"newUser", "email":"newuser_num@gmail.com", "password":"TOPSECRET"})
        self.assertEqual(response.status_code, 201)

    def test_create_with_existing_fields(self):
        response = self.client.post("/users", {"username":"User", "email":"user_num@gmail.com", "password":"TOPSECRET"})
        self.assertEqual(response.status_code, 409)

    def test_create_with_existing_username(self):
        response = self.client.post("/users", {"username":"User", "email":"user_num2@gmail.com", "password":"TOPSECRET"})
        self.assertEqual(response.status_code, 409)

    def test_create_with_existing_email(self):
        response = self.client.post("/users", {"username":"User2", "email":"user_num@gmail.com", "password":"TOPSECRET"})
        self.assertEqual(response.status_code, 409)

    def test_create_with_invalid_email(self):
        response = self.client.post("/users", {"username":"dasdas", "email":"sdsdads", "password":"sadsad"})
        self.assertEqual(response.status_code, 400)

    def test_create_with_blank_fields(self):
        response = self.client.post("/users", {"username":"", "email":"", "password":""})
        self.assertEqual(response.status_code, 400)

    def test_create_with_empty_fields(self):
        response = self.client.post("/users", {"username":None, "email":None, "password":None}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_create_without_arguments (self):
        response = self.client.post("/users")
        self.assertEqual(response.status_code, 400)


    def test_serch_user_by_email(self):
        response = self.client.post("/search_user_by_email", {"email":"user_num@gmail.com"})
        self.assertEqual(response.status_code, 200)

    def test_serch_user_by_email_uncreated_email(self):
        response = self.client.post("/search_user_by_email", {"email":"new_user_num@gmail.com"})
        self.assertEqual(response.status_code, 404)

    def test_serch_user_by_email_with_invalid_email(self):
        response = self.client.post("/usesearch_user_by_email", {"email":"sdsdads"})
        self.assertEqual(response.status_code, 400)

    def test_serch_user_by_email_with_blank_field(self):
        response = self.client.post("/usesearch_user_by_email", {"email":""})
        self.assertEqual(response.status_code, 400)

    def test_serch_user_by_email_with_empty_field(self):
        response = self.client.post("/usesearch_user_by_email", {"email":None}, format='json')
        self.assertEqual(response.status_code, 400)