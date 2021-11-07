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
from .forms import PDFForm, EnrollmentForm
import datetime

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

class EnrollList(generic.ListView):
    model = Enrollment
    template_name = 'enroll_list.html'
    context_object_name = 'enroll_list'

    def get_queryset(self):
        """
        Return all enrollments
        """
        return Enrollment.objects.all()

def enroll_course(request):
    if request.method == 'POST':
        enrolled = EnrollmentForm(request.POST, request.FILES)
        if enrolled.is_valid():
            course = enrolled.save(commit=False)
            course.save()
            return redirect('/app/enroll_list')
    else:
        form = EnrollmentForm()
    return render(request, 'enroll_course.html', {'form': form})