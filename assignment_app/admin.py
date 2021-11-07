from django.contrib import admin

from .models import Course, PDF, Enrollment, Event

admin.site.register(Course)
admin.site.register(PDF)
admin.site.register(Enrollment)
admin.site.register(Event)

# Register your models here.
