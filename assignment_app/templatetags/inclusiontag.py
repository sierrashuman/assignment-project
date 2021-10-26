from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from django import template

register = template.Library()
# Define the template file for the inclusion tag
@register.inclusion_tag('listusers.html')

def render_logged_in_user_list():
    return { 'users': get_all_logged_in_users() }

def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    return User.objects.filter(id__in=uid_list)


# def display_even_numbers(a, b):
#     # Declare a empty list
#     number = []
#     # Iterate the loop to find out the even number between a and b
#     for i in range(a, b):
#         # Check the number is even or not
#         if i % 2 == 0:
#             # Add the number in the list if it is even
#             number.append(i)
#     # Return the list to the display.html file
#     return {"output": number}

