from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView
from django.utils import timezone
from django.shortcuts import get_object_or_404, render

from .models import Course

# Create your views here.

class ViewCourse(CreateView):
    model = Course
    template_name = 'templates/courses.html'
    fields = ['name', 'courseID', 'professor', 
    'course_descrip', 'lecture_times', 'prereqs', 'enrolled']

    
