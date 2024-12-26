from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

# testeo de registro usuario

class TestRegistroView(TestCase):
    def setUp(self):
        # iniciarprueba
        self.client = Client()
        self.signup_url = reverse('signup')  

    def TesInicioExitoso(self):
        
        data = {
            'username': 'random123',
            'email': 'random@example.com',
            'password': '12345',
            'confirm_password': '12345',
        }
        response = self.client.post(self.signup_url, data)
        
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('login'))  

        self.assertTrue(User.objects.filter(username='random123').exists())

    def test_password_no_coinciden(self):
        data = {
            'username': 'random2',
            'email': 'random2@example.com',
            'password': '12345',
            'confirm_password': '123456',
        }
        response = self.client.post(self.signup_url, data)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Las contraseñas no coinciden.')

    def test_user_existe(self):
        User.objects.create_user(username='randomexistente', email='random44@example.com', password='12345')
        data = {
            'username': 'randomexistente',
            'email': 'random3@example.com',
            'password': '12345',
            'confirm_password': '12345',
        }
        response = self.client.post(self.signup_url, data)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'El nombre de usuario ya está en uso.')

    def test_email_xistente(self):
        User.objects.create_user(username='random42321', email='randomexistente@example.com', password='12345')
        data = {
            'username': 'random4',
            'email': 'randomexistente@example.com',
            'password': '12345',
            'confirm_password': '12345',
        }
        response = self.client.post(self.signup_url, data)
        
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'El correo electrónico ya está registrado.')