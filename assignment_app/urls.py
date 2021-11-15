from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'app'
urlpatterns = [
    path('courses/', views.get_courses, name='courselist'),
    path('coursestudents/<int:course_id>', views.get_course_students, name='coursestudents'),
    path('', views.index_view, name='index'),
    path('courses/<int:course_id>/<view>/', views.get_course_detailed_view, name='coursedetail'),
    path('courses/unenroll/<int:course_id>/', views.unenroll_course, name='course_unenroll'),
    path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
    path('pdf_list/', views.PDFList.as_view(), name='pdf_list'),
    path('inctag/',  views.inclusiontag, name='online_now'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'), # here
    url(r'^event/new/$', views.event, name='event_new'),
    url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    path('enroll_course/<int:pk>/', views.enroll_course, name='enroll_course')
]