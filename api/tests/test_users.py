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
