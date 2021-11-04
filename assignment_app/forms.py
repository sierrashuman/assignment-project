from django import forms
from .models import PDF

class PDFForm(forms.ModelForm):
    class Meta:
        model = PDF
        fields = ('title', 'course', 'pdf_file')