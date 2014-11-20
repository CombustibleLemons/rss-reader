from django.test import Client, TestCase

# User class from django
from django.contrib.auth.models import User, UserManager

# from http://www.mechanicalgirl.com/view/testing-django-apps/

class LoginTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a User
        cls.user = User.objects.create_user(username="test", password="test")
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_call_view_denies_anonymous(self):
        response = self.client.get('/', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/')

    def test_call_view_loads(self):
        self.client.login(username='test', password='test')  # defined in fixture or with factory in setUp()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.client.logout()

class RegisterTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/accounts/register/'
        self.user = User.objects.create_user("leGuin", "lefthand")

    def test_register_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')

    def test_valid_user(self):
        # This isn't right because the password will be hashed.
        response = self.client.post(self.url, {'username': 'Cherryh', 'password': 'downbelow'})
        self.assertEqual(response.status_code, 302) # 302 = URL redirection
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
