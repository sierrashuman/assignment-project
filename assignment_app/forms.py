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
    def __init__(self, *args, **kwargs):
        self.student = kwargs.pop('student', None)
        super(EnrollmentForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(EnrollmentForm, self).clean()
        course = cleaned_data.get('course')
        if Enrollment.objects.filter(student=self.student, course=course).exists():
            raise forms.ValidationError('You are already enrolled in this course')
    class Meta:
        model = Enrollment
        fields = ('course',)

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'grad_year', 'major')
