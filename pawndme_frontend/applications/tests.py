from django.test import TestCase
from rest_framework.test import APIClient

from config.test_helpers import animal_form, client_for, make_adopter, make_staff

APPLICATION = {
    'full_name': 'Anna Ivanova',
    'phone': '+77001234567',
    'email': 'anna@mail.com',
    'message': 'I live in a house with a garden and I had a dog before.',
}


class ApplicationTests(TestCase):
    def setUp(self):
        self.guest = APIClient()
        self.staff = make_staff()
        self.staff_client = client_for(self.staff)
        self.adopter_client = client_for(make_adopter())

        response = self.staff_client.post('/api/animals/', animal_form(), format='multipart')
        self.animal_id = response.data['id']
        self.url = '/api/animals/%d/apply/' % self.animal_id

    def test_send_application(self):
        response = self.adopter_client.post(self.url, APPLICATION, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['detail'], 'Application sent')

    def test_empty_field(self):
        data = dict(APPLICATION)
        data['phone'] = ''
        response = self.adopter_client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('phone', response.data)

    def test_animal_not_available(self):
        self.staff_client.patch('/api/animals/%d/status/' % self.animal_id, {'status': 'reserved'}, format='json')
        response = self.adopter_client.post(self.url, APPLICATION, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], 'This animal is not available for adoption')

    def test_guest_must_log_in(self):
        response = self.guest.post(self.url, APPLICATION, format='json')
        self.assertEqual(response.status_code, 401)

    def test_second_application(self):
        self.adopter_client.post(self.url, APPLICATION, format='json')
        response = self.adopter_client.post(self.url, APPLICATION, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], 'You already applied')
        detail = self.adopter_client.get('/api/animals/%d/' % self.animal_id)
        self.assertTrue(detail.data['has_applied'])

    def test_shelter_staff_cannot_apply(self):
        response = self.staff_client.post(self.url, APPLICATION, format='json')
        self.assertEqual(response.status_code, 403)

    def test_shelter_sees_applications(self):
        self.adopter_client.post(self.url, APPLICATION, format='json')
        other_adopter = client_for(make_adopter('petr@mail.com'))
        other_adopter.post(self.url, dict(APPLICATION, full_name='Petr Petrov'), format='json')
        response = self.staff_client.get('/api/applications/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        item = response.data['results'][0]
        for field in ['full_name', 'phone', 'email', 'message', 'animal']:
            self.assertIn(field, item)

        other_staff = client_for(make_staff('other@mail.com', 'Other Shelter', 'Astana'))
        self.assertEqual(other_staff.get('/api/applications/').data['count'], 0)
        self.assertEqual(self.adopter_client.get('/api/applications/').status_code, 403)