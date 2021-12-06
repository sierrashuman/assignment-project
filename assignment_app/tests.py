from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib import auth
from .models import Course, PDF, Enrollment
from .utils import translate_days, get_date, next_month, prev_month
from django.urls import reverse
import datetime

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
      def setUp(self):
            course1 = Course.objects.create(
                  name="course1",
                  course_mnemonic = "CR 1000",
                  professor="professor",
                  course_description="simple",
                  start_time='12:00',
                  end_time='1:00',
                  monday = True,
                  tuesday = False,
                  wednesday = True,
                  thursday = False,
                  friday = True,
                  course_id = '2222'
            )
            course2 = Course.objects.create(
                  name="course2",
                  course_mnemonic = "CR 2000",
                  professor="professor",
                  course_description="simple",
                  start_time='12:00',
                  end_time='1:00',
                  monday = True,
                  tuesday = False,
                  wednesday = True,
                  thursday = False,
                  friday = True,
                  course_id = '11111'
            )
            course3 = Course.objects.create(
                  name="course3",
                  course_mnemonic = "CR 3000",
                  professor="professor",
                  course_description="simple",
                  start_time='12:00',
                  end_time='1:00',
                  monday = True,
                  tuesday = False,
                  wednesday = True,
                  thursday = False,
                  friday = True,
                  course_id = '33333'
            )

      def test_number_of_objects(self):
            c = Course.objects.get_queryset().count()
            self.assertEqual(c, 3)

class UploadPDFTest(TestCase):
      def setUp(self):
            User = get_user_model()
            user = User.objects.create(username='bob')
            user.set_unusable_password()
            user.save()

            course = Course.objects.create(
                  name="test_course",
                  course_mnemonic = "TS 1000",
                  professor="professor",
                  course_description="simple",
                  start_time='12:00',
                  end_time='1:00',
                  monday = True,
                  tuesday = False,
                  wednesday = True,
                  thursday = False,
                  friday = True,
                  course_id = '11111'
            )

            PDF.objects.create(
                  title="test_pdf",
                  course=course,
                  uploader=user,
                  datetime=datetime.datetime.strptime('2021-11-01, 12:12:12', '%Y-%m-%d, %H:%M:%S'),
                  pdf_file="fake/pdf/url"
            )

      def test_pdf_in_database(self):
            pdf = PDF.objects.get(title="test_pdf")
            self.assertEquals(pdf.course.name, 'test_course')
            self.assertEquals(pdf.uploader.username, 'bob')

class CalendarViewTestCase(TestCase):      
      def setUp(self):
            User = get_user_model()
            user = User.objects.create(username='bob')
            user.set_password('Bob!14')
            user.save()
            c = Client()
            c.login(username='bob', password='Bob!14')

      def test_view_uses_correct_template(self):
            url = reverse('app:calendar')
            response = self.client.get(url, follow=True)
            self.assertTemplateUsed(response, 'bootstrap5/messages.html') 

class TranslateDaysTest(TestCase):
      def setUp(self):
            pass # no setup to do

      def test_MWF(self):
            test_string = 'MWF'
            expected_string = "Monday, Wednesday, Friday"
            returned_string = translate_days(test_string)
            self.assertEquals(expected_string, returned_string)
      
      def test_TTh(self):
            test_string = 'TR'
            expected_string = "Tuesday, Thursday"
            returned_string = translate_days(test_string)
            self.assertEquals(expected_string, returned_string)
      
      def test_out_of_order(self):
            test_string = 'FRWTM'
            expected_string = "Monday, Tuesday, Wednesday, Thursday, Friday"
            returned_string = translate_days(test_string)
            self.assertEquals(expected_string, returned_string)
      
      def test_empty(self):
            test_string = ''
            expected_string = ""
            returned_string = translate_days(test_string)
            self.assertEquals(expected_string, returned_string)

class MonthUtilsTest(TestCase):
      def setUp(self):
            pass # no setup to do

      def test_get_date_none_param(self):
            expected_date = datetime.date.today()
            returned_date = get_date(None)
            self.assertEquals(expected_date, returned_date)
      
      def test_get_date_with_param(self):
            expected_date = datetime.date(2021, 8, 1)
            returned_date = get_date('2021-08')
            self.assertEquals(expected_date, returned_date)
      
      def test_prev_month_none_param(self):
            expected_string = '2021-7'
            returned_string = prev_month(datetime.date(2021, 8, 17))
            self.assertEquals(expected_string, returned_string)
      
      def test_next_month_with_param(self):
            expected_string =  '2021-9'
            returned_string = next_month(datetime.date(2021, 8, 17))
            self.assertEquals(expected_string, returned_string)
