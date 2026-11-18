from urllib.parse import parse_qs, urlsplit

from django.core import mail
from django.test import TestCase
from rest_framework.test import APIClient

from config.test_helpers import client_for, make_adopter


class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_adopter(self):
        response = self.client.post('/api/auth/register/', {
            'email': 'anna@mail.com', 'password': 'password123', 'account_type': 'adopter'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['account_type_label'], 'Adopter')
        self.assertIn('token', response.data)

    def test_register_wrong_data(self):
        make_adopter('anna@mail.com')
        response = self.client.post('/api/auth/register/', {
            'email': 'anna@mail.com', 'password': '123456', 'account_type': 'adopter'}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['email'], ['Email is already registered'])
        self.assertEqual(response.data['password'], ['Password must have at least 8 characters'])

    def test_login_wrong_password(self):
        make_adopter('anna@mail.com')
        response = self.client.post('/api/auth/login/', {'email': 'anna@mail.com', 'password': 'wrong'}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], 'Wrong email or password')

    def test_login_ok(self):
        make_adopter('anna@mail.com')
        response = self.client.post('/api/auth/login/', {'email': 'anna@mail.com', 'password': 'password123'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_logout(self):
        user = make_adopter()
        client = client_for(user)
        self.assertEqual(client.get('/api/auth/me/').status_code, 200)
        self.assertEqual(client.post('/api/auth/logout/').status_code, 200)
        self.assertEqual(client.get('/api/auth/me/').status_code, 401)

    def test_register_shelter_staff(self):
        response = self.client.post('/api/auth/register/', {
            'email': 'staff@mail.com', 'password': 'password123', 'account_type': 'shelter_staff',
            'shelter_name': 'Happy Paws', 'shelter_city': 'Almaty'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['account_type'], 'shelter_staff')
        self.assertEqual(response.data['user']['shelter']['name'], 'Happy Paws')

    def test_register_shelter_staff_needs_shelter(self):
        response = self.client.post('/api/auth/register/', {
            'email': 'staff@mail.com', 'password': 'password123', 'account_type': 'shelter_staff'}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('shelter_name', response.data)

    def test_registration_cannot_join_existing_shelter(self):
        data = {'email': 'staff@mail.com', 'password': 'password123', 'account_type': 'shelter_staff',
                'shelter_name': 'Happy Paws', 'shelter_city': 'Almaty'}
        self.assertEqual(self.client.post('/api/auth/register/', data, format='json').status_code, 201)
        data['email'] = 'other@mail.com'
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('shelter_name', response.data)

    def test_password_reset_link_is_single_use_and_revokes_session(self):
        user = make_adopter('anna@mail.com')
        authenticated = client_for(user)
        reset_url = '/api/auth/reset-password/'
        response = self.client.post('/api/auth/forgot-password/', {'email': user.email}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        fragment = urlsplit(mail.outbox[0].body.splitlines()[-1]).fragment
        params = parse_qs(fragment.partition('?')[2])

        data = {'uid': params['uid'][0], 'token': params['token'][0], 'password': 'new-password123'}
        self.assertEqual(self.client.post(reset_url, data, format='json').status_code, 200)
        self.assertEqual(self.client.post(reset_url, data, format='json').status_code, 400)
        self.assertEqual(authenticated.get('/api/auth/me/').status_code, 401)
        response = self.client.post('/api/auth/login/', {
            'email': user.email, 'password': data['password'],
        }, format='json')
        self.assertEqual(response.status_code, 200)
