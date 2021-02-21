# Create your tests here.
from content.models import ExchangeRequest, Degree, Note, Course, Notification
from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomUser


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.url_action = reverse('content:request-action')
        self.login_url = reverse('login')
        self.d = Degree.objects.create(name="Biotech", type_of='LT')
        self.c = Course.objects.create(name="Bioinformatics", credits=3, lecturer='Bicciato')
        self.c.degree.add(self.d)
        self.user_1 = CustomUser.objects.create_user(email="leopoldo@unimore.it", username="leopoldo", password="pass")
        self.user_1.degree.add(self.d)
        self.user_2 = CustomUser.objects.create_user(email="gianbattista@unimore.it", username="gianbattista",
                                                     password="pass")
        self.user_2.degree.add(self.d)
        self.n1 = Note.objects.create(title='Note 1', owner=self.user_1, course=self.c, price=12)
        self.n2 = Note.objects.create(title='Note 2', owner=self.user_2, course=self.c, price=10)
        self.er = ExchangeRequest.objects.create(requested_note=self.n2, proposed_note=self.n1,
                                                 user_requester=self.n1.owner,
                                                 user_receiver=self.n2.owner)

    def test_manage_exchange_view_REJECT(self):
        self.assertFalse(self.er.seen)
        self.assertFalse(self.er.accepted)
        self.assertTrue(self.client.login(username="leopoldo@unimore.it", password="pass"))
        response = self.client.post(self.url_action, {
            'req': self.er.id,
            'action': 'reject',
        }, follow=True)
        refreshed_er = ExchangeRequest.objects.get(id=self.er.id)
        self.assertEqual(response.status_code, 200)  # no redirect to homepage
        self.assertFalse(refreshed_er.accepted)
        self.assertTrue(refreshed_er.seen)
        self.assertGreaterEqual(Notification.objects.filter(request__id=self.er.id).count(), 1)

    def test_manage_exchange_view_ACCEPT(self):
        self.assertFalse(self.er.seen)
        self.assertFalse(self.er.accepted)
        self.assertTrue(self.client.login(username="leopoldo@unimore.it", password="pass"))
        response = self.client.post(self.url_action, {
            'req': self.er.id,
            'action': 'accept',
        }, follow=True)
        refreshed_er = ExchangeRequest.objects.get(id=self.er.id)
        self.assertEqual(response.status_code, 200)  # no redirect to homepage
        self.assertTrue(refreshed_er.accepted)
        self.assertTrue(refreshed_er.seen)
        self.assertGreaterEqual(Notification.objects.filter(request__id=self.er.id).count(), 1)
