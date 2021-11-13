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
from django.utils.safestring import mark_safe
from assignment_app.forms import EventForm

from .models import *
from .utils import Calendar

# Create your views here.

class IndexView(generic.ListView):
    model = Course
    template_name = 'appindex.html'


class CourseList(generic.ListView):
    model = Course
    template_name = 'courselist.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        """
        Return all courses
        """
        return Course.objects.all()

class CourseDetailView(generic.DetailView):
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

class PDFList(generic.ListView):
    model = PDF
    template_name = 'pdf_list.html'
    context_object_name = 'pdf_list'

    def get_queryset(self):
        """
        Return all courses
        """
        return PDF.objects.all()


class CalendarView(generic.ListView):
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
    
class EnrollList(generic.ListView):
    model = Enrollment
    template_name = 'enroll_course.html'
    context_object_name = 'enroll_course'

    def get_queryset(self):
        """
        Return all enrollments
        """
        return Enrollment.objects.all()

def enroll_course(request):
    if request.method == 'POST':
        enrolled_form = EnrollmentForm(request.POST)
        student_form = StudentForm(request.POST)
        if enrolled_form.is_valid():
            course = enrolled_form.save(commit=False)
            course.save()
            return
        if student_form.is_valid():
            student = student_form.save(commit=False)
            student.user = request.user
            student.save()
            return redirect('/app/enroll_course')
    else:
        enrolled_form = EnrollmentForm()
        student_form = StudentForm()
    return render(request, 'enroll_course.html', {'enrolled_form': enrolled_form, 'student_form': student_form})

class CourseStudents(generic.ListView):
    model = Enrollment
    template_name = 'coursestudents.html'
    context_object_name = 'coursestudents'

    def get_queryset(self):
        """
        Return all students
        """
        return Enrollment.objects.all()