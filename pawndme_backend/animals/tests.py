from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from animals.models import Animal
from config.test_helpers import animal_form, client_for, make_adopter, make_staff


class AnimalTests(TestCase):
    def setUp(self):
        self.guest = APIClient()
        self.staff = make_staff()
        self.staff_client = client_for(self.staff)
        self.adopter_client = client_for(make_adopter())

    def create_animal(self, **changes):
        response = self.staff_client.post('/api/animals/', animal_form(**changes), format='multipart')
        self.assertEqual(response.status_code, 201, response.data)
        return response.data

    def test_create_profile(self):
        data = self.create_animal()
        self.assertEqual(data['status'], 'available')
        self.assertEqual(len(data['photos']), 1)
        self.assertEqual(Animal.objects.count(), 1)

    def test_create_profile_empty_field(self):
        response = self.staff_client.post('/api/animals/', animal_form(name='', location=''), format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.data)
        self.assertIn('location', response.data)
        self.assertEqual(Animal.objects.count(), 0)

    def test_create_profile_wrong_photo(self):
        text_file = SimpleUploadedFile('notes.txt', b'hello', content_type='text/plain')
        response = self.staff_client.post('/api/animals/', animal_form(photos=text_file), format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertIn('photos', response.data)

        big_file = SimpleUploadedFile('big.png', b'0' * (5 * 1024 * 1024 + 1), content_type='image/png')
        response = self.staff_client.post('/api/animals/', animal_form(photos=big_file), format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertIn('photos', response.data)
        self.assertEqual(Animal.objects.count(), 0)

    def test_create_profile_without_photo(self):
        data = animal_form()
        del data['photos']
        response = self.staff_client.post('/api/animals/', data, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['photos'], ['Add at least 1 photo'])

    def test_create_profile_wrong_role(self):
        response = self.adopter_client.post('/api/animals/', animal_form(), format='multipart')
        self.assertEqual(response.status_code, 403)
        response = self.guest.post('/api/animals/', animal_form(), format='multipart')
        self.assertEqual(response.status_code, 401)

    def test_edit_and_delete(self):
        first = self.create_animal(name='Bella')
        second = self.create_animal(name='Rex')
        response = self.staff_client.patch('/api/animals/%d/' % first['id'], {'description': 'New text'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['description'], 'New text')

        response = self.staff_client.delete('/api/animals/%d/' % second['id'])
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Animal.objects.count(), 1)

    def test_other_shelter_cannot_edit(self):
        animal = self.create_animal()
        other_client = client_for(make_staff('other@mail.com', 'Other Shelter', 'Astana'))
        response = other_client.patch('/api/animals/%d/' % animal['id'], {'name': 'Hacked'}, format='json')
        self.assertEqual(response.status_code, 403)
        response = other_client.delete('/api/animals/%d/' % animal['id'])
        self.assertEqual(response.status_code, 403)

    def test_catalog_for_guest(self):
        self.create_animal(name='Bella')
        self.create_animal(name='Rex')
        self.create_animal(name='Milo')
        response = self.guest.get('/api/animals/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 3)
        card = response.data['results'][0]
        for field in ['name', 'type', 'age', 'status', 'photos']:
            self.assertIn(field, card)

    def test_detailed_profile(self):
        animal = self.create_animal()
        response = self.guest.get('/api/animals/%d/' % animal['id'])
        self.assertEqual(response.status_code, 200)
        for field in ['photos', 'description', 'age', 'size', 'personality', 'health_info', 'status']:
            self.assertIn(field, response.data)
        self.assertEqual(self.guest.get('/api/animals/9999/').status_code, 404)

    def fill_catalog(self):
        self.create_animal(name='Bella', type='dog', size='small', age=3, location='Almaty', personality='calm')
        self.create_animal(name='Rex', type='dog', size='large', age=9, location='Almaty', personality='active')
        self.create_animal(name='Milo', type='cat', size='small', age=1, location='Astana', personality='shy')
        self.create_animal(name='Luna', type='cat', size='medium', age=5, location='Almaty', personality='friendly')

    def test_filter_one(self):
        self.fill_catalog()
        response = self.guest.get('/api/animals/?type=dog')
        self.assertEqual(response.data['count'], 2)

    def test_filter_many(self):
        self.fill_catalog()
        response = self.guest.get('/api/animals/?type=dog&size=small&location=Almaty')
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Bella')

    def test_filter_age_group_and_personality(self):
        self.fill_catalog()
        self.assertEqual(self.guest.get('/api/animals/?age_group=up_to_1').data['count'], 1)
        self.assertEqual(self.guest.get('/api/animals/?age_group=1_3').data['count'], 1)
        self.assertEqual(self.guest.get('/api/animals/?age_group=4_7').data['count'], 1)
        self.assertEqual(self.guest.get('/api/animals/?age_group=8_plus').data['count'], 1)
        self.assertEqual(self.guest.get('/api/animals/?personality=shy').data['count'], 1)

    def test_search_by_name(self):
        self.fill_catalog()
        response = self.guest.get('/api/animals/?search=bell')
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Bella')

    def test_no_result(self):
        self.fill_catalog()
        response = self.guest.get('/api/animals/?type=cat&size=large&location=Almaty')
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])

    def test_locations(self):
        self.fill_catalog()
        self.assertEqual(self.guest.get('/api/animals/locations/').data, ['Almaty', 'Astana'])

    def test_change_status(self):
        animal = self.create_animal()
        url = '/api/animals/%d/status/' % animal['id']
        response = self.staff_client.patch(url, {'status': 'reserved'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'reserved')
        self.assertEqual(self.guest.get('/api/animals/%d/' % animal['id']).data['status'], 'reserved')

    def test_change_status_wrong_role_and_value(self):
        animal = self.create_animal()
        url = '/api/animals/%d/status/' % animal['id']
        self.assertEqual(self.adopter_client.patch(url, {'status': 'reserved'}, format='json').status_code, 403)
        self.assertEqual(self.staff_client.patch(url, {'status': 'sold'}, format='json').status_code, 400)

    def test_my_animals(self):
        self.create_animal(name='Bella')
        self.create_animal(name='Rex')
        self.create_animal(name='Milo')
        other_client = client_for(make_staff('other@mail.com', 'Other Shelter', 'Astana'))
        other_client.post('/api/animals/', animal_form(name='Luna'), format='multipart')
        response = self.staff_client.get('/api/my-animals/')
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(self.guest.get('/api/animals/').data['count'], 4)
        self.assertEqual(self.adopter_client.get('/api/my-animals/').status_code, 403)

    def test_favorites(self):
        animal = self.create_animal()
        url = '/api/favorites/%d/' % animal['id']
        self.assertEqual(self.adopter_client.post(url).status_code, 201)
        self.assertEqual(self.adopter_client.post(url).status_code, 200)
        response = self.adopter_client.get('/api/favorites/')
        self.assertEqual(response.data['count'], 1)
        self.assertTrue(response.data['results'][0]['is_favorite'])
        self.assertEqual(self.adopter_client.delete(url).status_code, 204)
        self.assertEqual(self.adopter_client.get('/api/favorites/').data['count'], 0)

    def test_favorites_wrong_role(self):
        animal = self.create_animal()
        url = '/api/favorites/%d/' % animal['id']
        self.assertEqual(self.guest.post(url).status_code, 401)
        self.assertEqual(self.staff_client.post(url).status_code, 403)