from django import forms
from .models import PDF, Enrollment

class PDFForm(forms.ModelForm):
    class Meta:
        model = PDF
        fields = ('title', 'course', 'pdf_file')

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ('user', 'course')