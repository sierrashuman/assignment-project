from django.contrib import admin

from .models import Course, PDF, Enrollment

admin.site.register(Course)
admin.site.register(PDF)
admin.site.register(Enrollment)


# Register your models here.
