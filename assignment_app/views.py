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
from .forms import PDFForm, EnrollmentForm, StudentForm
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
from .utils import Calendar

# Create your views here.
@login_required
def index_view(request):
    student_name = Student.objects.filter(user = request.user)[0].first_name
    return render(request, 'appindex.html', {'student_name': student_name})




class CourseList(LoginRequiredMixin, generic.ListView):
    model = Course
    template_name = 'courselist.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        """
        Return all courses
        """
        return Course.objects.all()

@login_required
def get_courses(request):
    to_return = []
    query = request.GET.get('search')
    url = 'https://api.devhub.virginia.edu/v1/courses'
    data = requests.get(url).json()
    for course in data['class_schedules']['records']:
        # Make sure its the current semester
        if course[12] == '2021 Fall':
            if course[0] == query:
                # Change the days of the week to readable
                days = []
                for char in course[8]:
                    if char == 'M':
                        days.append("Monday")
                    elif char == 'T':
                        days.append("Tuesday")
                    elif char == 'W':
                        days.append("Wednesday")
                    elif char == "R":
                        days.append("Thursday")
                    elif char == 'F':
                        days.append("Friday")
                course[8] = ', '.join(days)
                to_return.append(course)
    return render(request, 'courselist.html', {'courses': to_return})

class CourseDetailView(LoginRequiredMixin, generic.DetailView):
    model = Course
    template_name = 'coursedetail.html'

    def get_queryset(self):
        return Course.objects.all()
'''
Declare function to render inclusiontag.html file
to load inclusion tag
'''
def inclusiontag(request):
    return render(request, "inclusiontag.html")

@login_required
def upload_pdf(request):
    if request.method == 'POST':
        form = PDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit=False)
            pdf.datetime = datetime.datetime.now()
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
        return PDF.objects.all()

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

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return date.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

@login_required
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        #return HttpResponseRedirect(reverse('CalendarView'))
    return render(request, 'event.html', {'form': form})

class EnrollList(LoginRequiredMixin, generic.ListView):
    model = Enrollment
    template_name = 'enroll_course.html'
    context_object_name = 'enroll_course'

    def get_queryset(self):
        """
        Return all enrollments
        """
        return Enrollment.objects.all()

@login_required
def enroll_course(request):
    student = Student.objects.filter(user = request.user)[0]
    enrollments = Enrollment.objects.filter(student = student)
    if request.method == 'POST':
        enrolled_form = EnrollmentForm(request.POST, student=student)
        if enrolled_form.is_valid():
            course = enrolled_form.save(commit=False)
            course.student = student
            course.save()
            return redirect('/app/enroll_course')
    else:
        enrolled_form = EnrollmentForm(student=student)
    return render(request, 'enroll_course.html', {'enrolled_form': enrolled_form, 'enrollments': enrollments})

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

class CourseStudents(LoginRequiredMixin, generic.ListView):
    model = Enrollment
    template_name = 'coursestudents.html'
    context_object_name = 'coursestudents'

    def get_queryset(self):
        """
        Return all students
        """
        return Enrollment.objects.all()
