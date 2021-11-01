from django.test import TestCase, Client, Course
from django.contrib.auth import get_user_model
from django.contrib import auth

# NOTE: All tests must start with the word 'test'

class LoginTest(TestCase):
      #Reference CS 3240 Recorded Lectures - 11:00 Lecture (10/7/21)
      def setUp(self):
            User = get_user_model()
            user = User.objects.create(username='bob')
            user.set_password('Bob!14')
            user.save()
      
      def test_correct(self):
            c = Client()
            logged_in = c.login(username='bob', password='Bob!14')
            self.assertTrue(logged_in)
      
      #Reference: https://stackoverflow.com/questions/5660952/test-that-user-was-logged-in-successfully/35871564#35871564
      def test_logout(self):
            c = Client()
            c.login(username='bob', password='Bob!14')
            user = auth.get_user(c)
            self.assertTrue(user.is_authenticated) 
            c.logout()
            user = auth.get_user(c)
            self.assertFalse(user.is_authenticated) 
      
class UnusablePasswordTest(TestCase):
      def setUp(self):
            User = get_user_model()
            user = User.objects.create(username='bob')
            user.set_unusable_password()
            user.save()

      def test_unusable_password(self):
            c = Client()
            User = get_user_model()
            user = User.objects.get(username='bob')
            self.assertFalse(user.has_usable_password())

class CourseListCountTest(TestCase):
      def test_number_of_objects(self):
            course1 = Course.objects.create(name="class1")
            course2 = Course.objects.create(name="class2")
            course3 = Course.objects.create(name="class3")
            c = Course.objects.all().count()
            self.assertEqual(c, 3)

