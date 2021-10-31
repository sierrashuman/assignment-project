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
