from django import template
from ..models import Student

register = template.Library()

@register.simple_tag
def get_student(request):
    student = Student.objects.get(user=request.user)
    return student.id