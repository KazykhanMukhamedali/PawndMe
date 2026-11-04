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