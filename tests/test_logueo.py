from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class TestLogueoView(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')  
        self.username = 'testuser'
        self.password = 'testpassword'
        
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_logueo_exitoso(self):
        
        data = {
            'username': self.username,
            'password': self.password,
        }
        response = self.client.post(self.login_url, data)
        
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, reverse('dashboard'))
        
        user = self.client.get(reverse('dashboard'))
        self.assertContains(user, self.username)



    def test_logueo_incorrecto(self):
        data = {
            'username': 'usuario_random',
            'password': 'passworddebil',
        }
        response = self.client.post(self.login_url, data)
        
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, 'Credenciales Incorrectas')