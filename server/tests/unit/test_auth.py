# server/tests/unit/test_auth.py

import json
import time
import unittest
from app.models import User
from tests.base import BaseTestClass
from tests.sample_data import data1, data2


class AuthLoginTest(BaseTestClass):

    def test_login_user_does_not_exist(self):
        response = self.send_POST('/auth/login', {
            'email': 'staff@brandery.org',
            'password': 'staff'
        })
        self.assert404(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn(
            'wrong password or user does not exist', response_['message'])

    def test_login_invalid_email(self):
        response = self.send_POST('/auth/login', {
            'email': '',
            'password': 'staff'
        })
        self.assert400(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('invalid login request', response_['message'])

    def test_login_no_password(self):
        response = self.send_POST('/auth/login', {
            'email': 'staff@brandery.org'
        })
        self.assert400(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('invalid login request', response_['message'])

    def test_empty_request(self):
        response = self.send_POST('/auth/login', {})
        self.assert400(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('invalid login request', response_['message'])

    def test_login_staff_member(self):
        User(
            name="Staff",
            email="staff@brandery.org",
            password="staff",
        ).save()
        response = self.send_POST('/auth/login', {
            'email': 'staff@brandery.org',
            'password': 'staff'
        })
        self.assert200(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('auth_token', response_)
        self.assertIn('registered_on', response_)
        self.assertIn('company', response_)
        self.assertIn('company_id', response_)
        self.assertIn('staff', response_)
        self.assertIn('success', response_['status'])
        self.assertIn('successfully logged in', response_['message'])

    def test_login_founder(self):
        self.get_id_from_POST(data1)
        response = self.send_POST('/auth/login', {
            'email': 'john@demo.com',
            'password': 'founder'
        })
        self.assert200(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('auth_token', response_)
        self.assertIn('success', response_['status'])
        self.assertIn('successfully logged in', response_['message'])

    def test_login_wrong_password(self):
        User(
            name="Staff",
            email="staff@brandery.org",
            password="staff",
        ).save()
        response = self.send_POST('/auth/login', {
            'email': 'staff@brandery.org',
            'password': 'staffff'
        })
        self.assert404(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn(
            'wrong password or user does not exist', response_['message'])


class AuthLogoutTest(BaseTestClass):

    @unittest.skip
    def test_valid_logout(self):
        auth_token = self.get_auth_token(staff=True)
        # user log out
        response = self.send_POST(
            '/auth/logout',
            data=None,
            headers=self.get_authorized_header(auth_token)
        )
        self.assert200(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('success', response_['status'])
        self.assertIn('successfully logged out', response_['message'])

        status_response = self.client.get(
            '/auth/status', headers=self.get_authorized_header(auth_token))
        self.assert401(status_response)
        status_response_ = json.loads(status_response.data.decode())
        self.assertIn('failure', status_response_['status'])

    def test_never_logged_in(self):
        response = self.send_POST(
            '/auth/logout',
            data=None,
        )
        self.assert401(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('unauthorized', response_['message'])

    def test_expired_token(self):
        auth_token = self.get_auth_token(staff=True)
        time.sleep(3)
        response = self.send_POST(
            '/auth/logout',
            data=None,
            headers=self.get_authorized_header(auth_token)
        )
        response_ = json.loads(response.data.decode())
        self.assert500(response)
        self.assertIn('failure', response_['status'])


class AuthRegisterTest(BaseTestClass):

    def test_register_empty_request(self):
        response = self.send_POST('/auth/register', {})
        self.assert400(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('invalid register request', response_['message'])

    def test_register_lacking_field(self):
        response = self.send_POST('/auth/register', {
            'email': 'staff@brandery.org'
        })
        self.assert400(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('invalid register request', response_['message'])

    def test_register_email_exists(self):
        self.send_POST('/auth/register', {
            'email': 'tu@demo.com',
            'password': 'test123'
        })
        response = self.send_POST('/auth/register', {
            'email': 'tu@demo.com',
            'password': 'test123'
        })
        self.assertEqual(response.status_code, 202)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('user exists. log in instead', response_['message'])

    def test_register_successfully(self):
        response = self.send_POST('/auth/register', {
            'email': 'staff@brandery.org',
            'password': 'staff'
        })
        self.assertEqual(response.status_code, 201)
        response_ = json.loads(response.data.decode())
        self.assertIn('success', response_['status'])
        self.assertIn('successfully registered', response_['message'])
        self.assertIn('auth_token', response_)


class AuthUserTest(BaseTestClass):

    def test_not_logged_in(self):
        response = self.client.get('auth/status')
        self.assert401(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('unauthorized', response_['message'])

    def test_logged_in(self):
        auth_token = self.get_auth_token(staff=True)
        response = self.client.get(
            '/auth/status',
            headers=self.get_authorized_header(auth_token))
        self.assert200(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('success', response_['status'])
        self.assertIn('data', response_)
        self.assertIn('user_id', response_['data'])
        self.assertIn('email', response_['data'])
        self.assertIn('company', response_['data'])
        self.assertIn('registered_on', response_['data'])
        self.assertIn('staff', response_['data'])


class AuthCompanyApiTest(BaseTestClass):

    def test_non_staff_not_allowed_to_get_all_companies(self):
        company_id = self.get_id_from_POST(data1)
        auth_token = self.get_auth_token(staff=False, company_id=company_id)
        response = self.client.get(
            '/companies', headers=self.get_authorized_header(auth_token))
        self.assert401(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('non-staff members not allowed', response_['message'])

    def test_not_logged_in_get_all_companies(self):
        response = self.client.get(
            '/companies')
        self.assert401(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('unauthorized', response_['message'])

    def test_non_staff_not_allowed_to_create_company(self):
        self.get_id_from_POST(data1)
        auth_token = self.get_auth_token(staff=False, company_id=1)
        response = self.send_POST(
            '/companies', data=data2,
            headers=self.get_authorized_header(auth_token))
        self.assert401(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('non-staff members not allowed', response_['message'])

    def test_not_logged_in_create_company(self):
        response = self.send_POST(
            '/companies', data=data2)
        self.assert401(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('unauthorized', response_['message'])

    def test_different_employee_get_a_company(self):
        company_id1 = self.get_id_from_POST(data1)
        auth_token1 = self.get_auth_token(staff=False, company_id=company_id1)
        company_id2 = self.get_id_from_POST(data2)
        response = self.client.get(
            f'/companies/{company_id2}',
            headers=self.get_authorized_header(auth_token1)
        )
        self.assert401(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('user not authorized to this view', response_['message'])

    def test_respective_employee_allowed_to_one_company(self):
        company_id = self.get_id_from_POST(data1)
        auth_token = self.get_auth_token(staff=False, company_id=company_id)
        response = self.client.get(
            f'/companies/{company_id}',
            headers=self.get_authorized_header(auth_token)
        )
        self.assert200(response)
