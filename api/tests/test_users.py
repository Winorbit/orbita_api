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

        self.userprofile_resp = {'email': 'user_num@gmail.com',
                                 'password': 'TOPSECRET',
                                 'profile_image': None,
                                 'is_superuser': False,
                                 'user_courses': [],
                                 'username': 'User'}


    """
    def test_search_userprofile_by_username(self):
        response = self.client.post("/search_userprofile", {"username": "User", "password": "TOPSECRET"})
        self.assertEqual(response.status_code, 200)
  
    def test_search_userprofile_on_valid_response_by_username(self):
        response = self.client.post("/search_userprofile", {"username": "User", "password": "TOPSECRET"})
        print(response.data)
        #self.assertTrue( all(item in response.data.items() for item in self.userprofile_resp.items()))
    
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
        self.assertEqual(response.status_code, 401)

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
    
    """

    def test_update_user_fields(self):
        User.objects.create(username= "Testname", password = 'TOPSECRET', email="test@gmail.com", id=19)
        user = User.objects.get(id=42)

        new_username = "NewUsername"
        request_body = {"username":new_username}
        response = self.client.put(f"/update_user_info/{user.id}", request_body)
        current_username = User.objects.get(id=42).username

        self.assertEqual(response.status_code, 202)
        self.assertEqual(current_username,  new_username)

       
        new_email = "new@gmail.com"
        request_body = {"email": new_email}
        response = self.client.put(f"/update_user_info/{user.id}", request_body)
        current_email = User.objects.get(id=42).email

        self.assertEqual(response.status_code, 202)
        self.assertEqual(current_email,  new_email)
        
        # check 404-resp if empty body
        response = self.client.put(f"/update_user_info/{user.id}", {})
        self.assertEqual(response.status_code, 404)

    
    def test_not_update_user_if_value_exist(self):
        User.objects.create(username= "first_user", password = 'TOPSECRET', email="first@gmail.com", id=98)
        User.objects.create(username= "second_user", password = 'TOPSECRET', email="second@gmail.com", id=99)
        user = User.objects.get(id=98)

        # check fail if use existing email
        request_body = {"username":"my_new_username", "email":"second@gmail.com"}
        response = self.client.put(f"/update_user_info/{user.id}", request_body)
        self.assertEqual(response.status_code, 409)

        # check fail if use existing username
        request_body = {"username":"second_user", "email":"new@gmail.com"}
        response = self.client.put(f"/update_user_info/{user.id}", request_body)
        self.assertEqual(response.status_code, 409)
        # проверить что с пустыышой не сработает и с не существующим юзером тоже
