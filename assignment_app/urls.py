from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'app'
urlpatterns = [
    path('courses/', views.CourseList.as_view(), name='courselist'),
    path('coursestudents/', views.CourseStudents.as_view(), name='coursestudents'),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='coursedetail'),
    path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
    path('pdf_list/', views.PDFList.as_view(), name='pdf_list'),
    path('inctag/',  views.inclusiontag),
    path('calendar/', views.CalendarView.as_view(), name='calendar'), # here
    url(r'^event/new/$', views.event, name='event_new'),
    url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    path('enroll_course/', views.enroll_course, name='enroll_course')
]