from django import forms
from .models import PDF, Enrollment, Student

class PDFForm(forms.ModelForm):
    class Meta:
        model = PDF
        fields = ('title', 'course', 'pdf_file')

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ('student','course')

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('major', 'grad_year')