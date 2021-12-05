from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.core.files.storage import FileSystemStorage
from .models import Course, PDF, Enrollment
from .forms import PDFForm, StudentForm, PDFCourseForm
import datetime
from datetime import date, timedelta
import calendar
from django.db import models
from django.db import IntegrityError
from django.utils.safestring import mark_safe
from assignment_app.forms import EventForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import requests
import json

from .models import *
from .utils import Calendar, translate_days, get_date, next_month, prev_month

# Core views (index, others online, student creation)
# index_view: direct view to the appindex html file
# inclusiontag: Declare function to render inclusiontag.html file to load inclusion tag
# student_intialization: Create a new student when they first log into the application
@login_required
def index_view(request):
    student = Student.objects.get(user = request.user)
    return render(request, 'appindex.html', {'student_name': student.first_name, 'student_id': student.id})

@login_required
def inclusiontag(request):
    return render(request, "inclusiontag.html")

@login_required
def student_initialization(request):
    student_created = Student.objects.filter(user = request.user).exists()
    # Redirect to the main page if already have a student
    if student_created:
        return redirect('/app')
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            student = student_form.save(commit=False)
            student.user = request.user
            student.save()
            return redirect('/app')
    else:
        student_form = StudentForm()
    return render(request, 'index.html', {'student_form': student_form})



# Views for courses (course list and course detail)
# get_courses: Hits UVA API to get a list of all classes matching user input query
# get_course_detailed_view: Hits UVA API and redirects to a page for the course selected
# If the course is not already in our database, add it
# enroll_course: Create a new enrollment for a student in a specific course
# unenroll_course: Delete the associated enrollment for a student in a course
# get_course_students: Get a list of students currently enrolled in a course
@login_required
def get_courses(request):
    to_return = []
    query = request.GET.get('search')
    url = 'https://api.devhub.virginia.edu/v1/courses'
    data = requests.get(url).json()
    for course in data['class_schedules']['records']:
        if query:
            query_elements = query.split(' ')
            # Make sure its the current semester
            if course[12] == '2021 Fall':
                if len(query_elements) == 2:
                    if course[0].lower() == query_elements[0].lower() and course[1] == query_elements[1]:
                        course[8] = translate_days(course[8])
                        to_return.append(course)
                else:
                    if course[0].lower() == query_elements[0].lower() or query_elements[0].lower() == course[6].lower():
                        course[8] = translate_days(course[8])
                        to_return.append(course)
    return render(request, 'courselist.html', {'courses': to_return})

@login_required
def get_course_detailed_view(request, course_id, view):
    if Course.objects.filter(course_id=course_id).exists():
        course = Course.objects.get(course_id=course_id)
    else:
        url = 'https://api.devhub.virginia.edu/v1/courses'
        data = requests.get(url).json()
        for course in data['class_schedules']['records']:
            if course[3] == course_id and course[12] == '2021 Fall':
                course_info = course
        course = Course(
            name=course_info[4],
            course_mnemonic = f"{course_info[0]} {course_info[1]}",
            professor=' '.join(reversed(course_info[6].split(','))),
            course_description=course_info[5],
            start_time=course_info[9],
            end_time=course_info[10],
            monday = 'M' in course_info[8],
            tuesday = 'T' in course_info[8],
            wednesday = 'W' in course_info[8],
            thursday = 'R' in course_info[8],
            friday = 'F' in course_info[8],
            course_id = int(course_id)
        )
        course.save()
    student = Student.objects.get(user = request.user)
    enrollment = Enrollment(
        course=course,
        student=student
    )

    is_enrolled = Enrollment.objects.filter(course=course, student=student).exists()
    if not is_enrolled and view != 'view':
        enrollment.save()
        is_enrolled = True

    return render(request, 'coursedetail.html', {'course': course, 'is_enrolled': is_enrolled})

@login_required
def enroll_course(request, pk):
    student = Student.objects.get(id=pk)
    enrollments = Enrollment.objects.filter(student=student)
    return render(request, 'enroll_course.html', {'enrollments': enrollments, 'student_name': student.first_name})

@login_required
def unenroll_course(request, course_id):
    student = Student.objects.get(user=request.user)
    course = Course.objects.get(course_id=course_id)
    Enrollment.objects.filter(student=student, course=course).delete()
    return redirect(f'/app/courses/{course_id}/view')

@login_required
def get_course_students(request, course_id):
    course = Course.objects.get(course_id=course_id)
    enrollments = Enrollment.objects.filter(course=course)
    students = []
    for enrollment in enrollments:
        students.append(enrollment.student)
    return render(request, 'coursestudents.html', {'students': students, 'course': course})



# Views for PDF related operations (upload PDF, PDF list)
# upload_pdf: Works with form to upload a inputted PDF to our database
# PDFList: A view to support a list of PDFs, also can be restricted to PDFs for a specific class
@login_required
def upload_pdf(request):
    if request.method == 'POST':
        form = PDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit=False)
            # Adjust for heroku servers time
            incorrect_datetime = datetime.datetime.now()
            correct_datetime = incorrect_datetime - datetime.timedelta(hours=5)
            pdf.datetime = correct_datetime
            pdf.uploader = request.user
            pdf.save()
            return redirect('/app/pdf_list')
    else:
        form = PDFForm()
    return render(request, 'upload_pdf.html', {'form': form})

class PDFList(LoginRequiredMixin, generic.ListView):
    model = PDF
    template_name = 'pdf_list.html'
    context_object_name = 'pdf_list'

    def get_queryset(self):
        """
        Return all courses
        """
        subset = self.kwargs.get('subset')
        if subset is not None:
            course = Course.objects.get(course_id=int(subset))
            pdfs_unsorted = PDF.objects.filter(course=course)
        else:
            pdfs_unsorted = PDF.objects.all()
        pdfs_sorted = sorted(pdfs_unsorted, key = lambda i: i.datetime, reverse=True)

        return pdfs_sorted



# Views to support calendar related functionality (Calendar view, event creation)
# CalendarView: View to support the display of the calendar
# event: Create or delete a new calendar event
class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Event
    template_name = 'assignment_app/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

@login_required
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    
    form = EventForm(request.POST or None, instance=instance)
    if 'submit' in request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect('CalendarView')

    elif 'delete' in request.POST:
        instance.delete()
        return HttpResponseRedirect('CalendarView')

    return render(request, 'event.html', {'form': form})
