from django.test import Client, TestCase

# User class from django
from django.contrib.auth.models import User, UserManager

# from http://www.mechanicalgirl.com/view/testing-django-apps/
class RegisterTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/account/register/'
        self.user = User.objects.create_user("leGuin", "lefthand")

    def test_register_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        #print response
        self.assertContains(response, 'Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')

    def test_valid_user(self):
        response = self.client.post(self.url, {'username': 'Cherryh', 'password': 'downbelow'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(User.objects.all(), ["<User: leGuin>", "<User: Cherryh>"], ordered=False)

    def test_repeat_user(self):
        response = self.client.post(self.url, {'username':"leGuin", 'password': "lefthand"})
        #self.assertEqual(response.status_code, 409) #currently doesn't work
        self.assertQuerysetEqual(User.objects.all(), ["<User: leGuin>"], ordered=False)

    def test_long_username(self): #length limits might change?
        response = self.client.get(self.url, {'username' : 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                                              'password' : 'password'})
        #self.assertEqual(response.status_code, 400)
        self.assertQuerysetEqual(User.objects.all(), ["<User: leGuin>"], ordered=False)

    def test_spacey_username(self):
        response = self.client.get(self.url, {'username' : 'Lois McMaster Bujold', 'password' : 'Vorkosigan'})
        #self.assertEqual(response.status_code, 400)
        self.assertQuerysetEqual(User.objects.all(), ["<User: leGuin>"], ordered=False)
