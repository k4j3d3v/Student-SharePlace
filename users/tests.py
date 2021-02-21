from content.models import Degree
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, Client
# Create your tests here.
from django.urls import reverse
from users.models import CustomUser


class UsersManagerTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIs(user.username, '')
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='foo')

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)


class UserViewTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.registration_url = reverse("register")
        self.login_url = reverse("login")
        self.degree = Degree.objects.create(name="Biotech", type_of='LT')

    def test_user_registration_GET(self):
        # Issue a GET request.
        response = self.client.get(self.registration_url)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'users/register.html')  # so will be displayed registration page

    def Test_user_registration_view_POST_success_redirect(self):
        """
        Test che si occupa di verificare che dato l'url della registrazione utente, effettuata una richiesta POST con
        i dati dell'utente si venga rediretti (registrazione avvenuta correttamente)

        :return: None
        """

        response = self.client.post(self.registration_url, {
            'email': 'myemail@email.it',
            'username': 'user_test',
            'degree': self.degree.id,
            'password1': 'pwtest12',
            'password2': 'pwtest12'
        }, follow=True)

        self.assertRedirects(response, reverse('content:course-list'), status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'course_tables.html')  # so will be displayed registration page
        self.assertEquals(CustomUser.objects.get(email='myemail@email.it').username, 'user_test')

    def test_user_registration_view_POST_error_not_redirect(self):
        """
        Test che si occupa di verificare che dato l'url della registrazione utente, effettuata una richiesta POST con
        i dati dell'utente (errati, campo DEGREE mancante) non si venga rediretti (errore nella registrazione)
        ma si visualizzi la stessa pagina con gli errori trovati

        :return: None
        """

        response = self.client.post(self.registration_url, {
            'email': 'myemail@email.it',
            'username': 'user_test',
            'password1': 'pwtest12',
            'password2': 'pwtest12'
        }, follow=True)

        self.assertEquals(response.status_code, 200)  # there is no redirect
        self.assertTemplateUsed(response, 'users/register.html')  # so will be displayed registration page

    def Test_user_login_view_POST_success(self):
        """
        Test che si occupa di verificare che dato l'url del login utente, effettuata una richiesta POST con
        i dati dell'utente si venga rediretti alla homepage (login effettuato correttamente)

        :return: None
        """
        response = self.client.post(self.login_url, {
            'username': 'myemail@email.it',
            'password': 'pwtest12'
        }, follow=True)

        # get user registered with previous successful test
        user_in_db = CustomUser.objects.get(email='myemail@email.it')

        self.assertRedirects(response, reverse('content:course-list'), status_code=302,
                             target_status_code=200)  # redirection to homepage
        self.assertTemplateUsed(response, 'course_tables.html')  # so will be displayed another time login page
        self.assertEquals(response.context['user'], user_in_db)  # so correct user is logged

    def test_user_login_view_POST_error(self):
        """
        Test che si occupa di verificare che dato l'url del login utente, effettuata una richiesta POST con
        i dati dell'utente (errati) non si venga rediretti alla homepage ma si visualizzi la schermata di login
        con gli errori specificati (login fallito)

        :return: None
        """

        response = self.client.post(self.login_url, {
            'email': 'notregistered@email.it',
            'password': 'unusefulpwd'
        })
        self.assertEqual(response.status_code, 200)  # no redirect to homepage
        self.assertTemplateUsed(response, 'registration/login.html')  # so will be displayed another time login page
        self.assertEquals(response.context['user'].pk, AnonymousUser.pk)  # and user is Anonymous

    def test_user_registration_and_login_no_session(self):
        """
        Test generale che concatena una registrazione avvenuta correttamente, non mantenendo l'utente loggato,
        con un login successivo dell'utente appena registrato
        :return: None
        """
        self.Test_user_registration_view_POST_success_redirect()
        self.client.logout()  # delete session created with registration
        self.Test_user_login_view_POST_success()
