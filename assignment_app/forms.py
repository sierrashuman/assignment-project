from django import forms
from django.forms import ModelForm, DateInput
from assignment_app.models import Event
from .models import PDF, Enrollment, Student

class PDFForm(forms.ModelForm):
    class Meta:
        model = PDF
        fields = ('title', 'course', 'pdf_file')

class EventForm(ModelForm):
      class Meta:
        model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
         'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super(EventForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
            self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
            self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
            
class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ('student','course')

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('major', 'grad_year')
