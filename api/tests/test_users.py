from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
import logging
import json

from .. import users, courses
from .. serializers import UserSerializer


class UsersTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        test_user = User.objects.create(username= "User", password = 'TOPSECRET', email="user_num@gmail.com")
        test_user_profile = users.UserProfile.objects.create(user=test_user, id=test_user.id)

        self.userprofile_resp = {'email': 'user_num@gmail.com',
                                 'password': 'TOPSECRET',
                                 'profile_image': None,
                                 'is_superuser': False,
                                 'username': 'User'}

        """
        login
        logout
        if authorized - show courses list, if not - show author.page
        """

    """
    def test_search_userprofile_by_username(self):
        request_body = {"username": "User", "password": "TOPSECRET"}
        response = self.client.post("/search_userprofile", json.dumps(request_body), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue( all(item in response.data.items() for item in self.userprofile_resp.items()))
    
    def test_search_userprofile_by_email (self):
        request_body = {"username": "user_num@gmail.com", "password": "TOPSECRET"}

        response = self.client.post("/search_userprofile", json.dumps(request_body), content_type="application/json")
        self.assertEqual(response.status_code, 200)
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
        request_body = {"username":"newUser", "email":"newuser_num@gmail.com", "password":"TOPSECRET"}

        response = self.client.post("/users/", json.dumps(request_body), content_type="application/json")
       
        self.assertEqual(response.status_code, 201)
     
    def test_create_with_existing_fields(self):
        request_body = {"username":"User", "email":"user_num@gmail.com", "password":"TOPSECRET"}

        response = self.client.post("/users/", json.dumps(request_body), content_type="application/json")

        self.assertEqual(response.status_code, 409)

    def test_create_with_existing_username(self):
        request_body = {"username":"User", "email":"user_num2@gmail.com", "password":"TOPSECRET"}
        response = self.client.post("/users/", json.dumps(request_body), content_type="application/json")
        self.assertEqual(response.status_code, 409)

    def test_create_with_existing_email(self):
        request_body = {"username":"User2", "email":"user_num@gmail.com", "password":"TOPSECRET"}

        response = self.client.post("/users/", json.dumps(request_body), content_type="application/json")

        self.assertEqual(response.status_code, 409)

    def test_create_with_invalid_email(self):
        request_body = {"username":"dasdas", "email":"sdsdads", "password":"sadsad"}
        response = self.client.post("/users/", json.dumps(request_body), content_type="application/json")
        self.assertEqual(response.status_code, 412)
    
    def test_create_with_blank_fields(self):
        request_body = {"username":"", "email":"", "password":""}
        response = self.client.post("/users/", json.dumps(request_body), content_type="application/json")
        self.assertEqual(response.status_code, 412)

    def test_create_with_empty_fields(self):
        request_body = {"username":None, "email":None, "password":None}
        response = self.client.post("/users/", json.dumps(request_body), content_type="application/json")
        self.assertEqual(response.status_code, 412)

    def test_create_without_arguments (self):
        response = self.client.post("/users/")
        self.assertEqual(response.status_code, 412)

    
    def test_serch_user_by_email(self):
        response = self.client.post("/search_user_by_email", {"email":"user_num@gmail.com"})
        self.assertEqual(response.status_code, 200)

    def test_serch_user_by_email_uncreated_email(self):
        response = self.client.post("/search_user_by_email", {"email":"new_user_num@gmail.com"})
        self.assertEqual(response.status_code, 404)

    def test_serch_user_by_email_with_invalid_email(self):
        response = self.client.post("/usesearch_user_by_email", {"email":"sdsdads"})
        self.assertEqual(response.status_code, 404)

    def test_serch_user_by_email_with_blank_field(self):
        response = self.client.post("/usesearch_user_by_email", {"email":""})
        self.assertEqual(response.status_code, 404)

    def test_serch_user_by_email_with_empty_field(self):
        response = self.client.post("/usesearch_user_by_email", {"email":None}, format='json')
        self.assertEqual(response.status_code, 404)
    """


class UsersTestAddToGroup(TestCase):

    def setUp(self):
        self.client = APIClient()

        test_user = User.objects.create(username= "Username", password = 'TOPSECRET', email="testuser@gmail.com")
        test_user_profile = users.UserProfile.objects.create(user=test_user, id=test_user.id)
        test_group_one = courses.Group.objects.create(title="title", discord_chat_link="link")

    def test_add_user_to_group_empty_request(self):
        response = self.client.put("/add_user_to_group")
        self.assertEqual(response.status_code, 400)
    
    def test_add_user_to_group_unexisted_user_id(self):
        group = courses.Group.objects.get(title="title")
        response = self.client.put("/add_user_to_group", {"user_id": 9999, "group_id":group.id} )
        self.assertEqual(response.status_code, 404)
        pass

    def test_add_user_to_group_unexisted_group_id(self):
        user = users.User.objects.get(username="Username")
        response = self.client.put("/add_user_to_group", {"user_id": user.id, "group_id":99999} )
        self.assertEqual(response.status_code, 404)
        pass

    def test_add_user_to_group_twice(self):
        user = users.User.objects.get(username="Username")
        user_profile = users.UserProfile.objects.get(user=user)
        group = courses.Group.objects.get(title="title")
        user_profile.groups.append(group.id)
        user_profile.save()
        response = self.client.put("/add_user_to_group", {"user_id": user.id, "group_id":group.id} )
        self.assertEqual(response.status_code, 409)
        pass

    
    def test_add_user_to_group(self):
        user = users.User.objects.get(username="Username")
        user_profile = users.UserProfile.objects.get(user=user)
        group = courses.Group.objects.get(title="title")
        response = self.client.put("/add_user_to_group", {"user_id": user.id, "group_id":group.id} )
        self.assertEqual(response.status_code, 200)
        pass
