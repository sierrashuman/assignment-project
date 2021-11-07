from django.contrib import admin

from .models import Course, PDF, Enrollment, Student

admin.site.register(Course)
admin.site.register(PDF)
admin.site.register(Enrollment)
admin.site.register(Student)


# Register your models here.
