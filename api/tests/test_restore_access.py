from django.contrib.auth.models import User
from freezegun import freeze_time

from django.test import TestCase
from rest_framework.test import APIClient
from unittest import mock

import logging

from .. import users


class AccessRestoreTest(TestCase):

    test_email = "testuser@gmail.com" 
    test_cypher_key = "my_simple_key_42"

    test_datetime_now = "2020.12.12.18.15"
    hashed_test_datetime_now = "X0ltQ0dcQkJUbUVUQXEFBw=="

    test_datetime_23_hours_ago = "2020.12.11.19.15"
    hashed_test_datetime_23_hours_ago = "X0ltQ0dcQkJUbkVUQHEFBw=="

    test_datetime_25_hours_ago = "2020.12.11.17.15"
    hashed_test_datetime_25_hours_ago = "X0ltQ0dcQkJUbkVUTnEFBw=="

    def setUp(self):
        User.objects.create(username="SayMyName", password="IDDQD", email="gibson@gmail.com")
        User.objects.create(username="MyName", password="IDDQD", email=self.test_email)
        pass

    def test_encrypt_decrypt(self):
        test_str = "my_test@string.com"
        encrypted_test_str = users.encrypt(self.test_cypher_key, test_str)

        expected_hash = b'AAAABwweBCwWKxkMFzgaUQIU'

        unhashed_to_str = users.decrypt(self.test_cypher_key, encrypted_test_str)

        self.assertEqual(encrypted_test_str, expected_hash)
        self.assertEqual(unhashed_to_str, test_str)
        pass

    def test_create_restore_access_url(self):
        test_cypher_key = "my_simple_key_42"

        # откуда его брать?
        test_root_url = "localhost:8000"
        hashed_email_in_utf_8 = "GRwsBxweFR4lOAYEEDMaUQIU"
        expected_restore_access_url = f"{test_root_url}/{hashed_email_in_utf_8}||{self.hashed_test_datetime_now}"

        restore_access_url = users.create_restore_access_url(test_root_url, self.test_email, self.test_datetime_now, test_cypher_key) 
        self.assertEqual(expected_restore_access_url, restore_access_url)


    def test_restore_access_url_validation(self):
        valid_url = ""
        invalid_url = ""
        # checked_valid_url = check_restore_access_url(valid_url)
        # checked_invalid_url = check_restore_access_url(valid_url)
        #self.assertTrue(checked_valid_url)
        #self.assertTrue(checked_invalid_url)


    def test_send_restore_access_email(self):
        user_email = "gibson@gmail.com" 

        resp = self.client.post("/request_restore_access", {"email": user_email})
        self.assertEqual(resp.status_code, 200)
        pass

    def test_reset_password(self):

        # check if user with this email exist
        # check if new_password != old_password
        # check if user password was changed
        # DON'T give access if password not changed!
        # check_Status_code
        # check f email was sended
        pass


    def test_send_restore_access_email_fail_email(self):
        unexisted_user_email = "not_user@gmail.com" 
        resp = self.client.post("/request_restore_access", {"email": unexisted_user_email})
        self.assertEqual(resp.status_code, 404)
        pass

    def test_send_restore_access_email_empty_request(self):
        resp = self.client.post("/request_restore_access", {})
        self.assertEqual(resp.status_code, 400)
        pass


    @freeze_time("2020-12-12-18-15")
    def test_reset_user_password_unhappy_path(self):
        hashed_info_23_hours_ago = f"GRwsBxweFR4lOAYEEDMaUQIU||{self.hashed_test_datetime_23_hours_ago}"
        hashed_info_25_hours_ago = f"GRwsBxweFR4lOAYEEDMaUQIU||{self.hashed_test_datetime_25_hours_ago}"

        invalid_hashed_user_info = "GR2323llxweFR4lOAYEEDMaUQIU||X0ltQ0dcQkJUbUVUQXEFBw=="

        current_user_password = "IDDQD"
        new_user_password = "NewSecret"

        resp = self.client.post("/reset_user_password", {"hashed_user_info":""})
        self.assertEqual(resp.status_code, 404)

        resp = self.client.post("/reset_user_password", {"hashed_user_info": hashed_info_23_hours_ago, "password": new_user_password})
        self.assertEqual(resp.status_code, 408)

        
        resp = self.client.post("/reset_user_password", {"hashed_user_info": hashed_info_23_hours_ago, "password": current_user_password})
        self.assertEqual(resp.status_code, 400)

 
        resp = self.client.post("/reset_user_password", {"hashed_user_info": invalid_hashed_user_info, "password": current_user_password})
        self.assertEqual(resp.status_code, 400)

        resp = self.client.post("/reset_user_password", {"hashed_user_info": hashed_info_23_hours_ago, "password":new_pass})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(User.objects.get(email="testuser@gmail.com").password, new_pass)


        # if time expired
        # if not data
        # if not valid email - PRE-CHECK
