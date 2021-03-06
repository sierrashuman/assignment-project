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
    url(r'^pdf_list/(?P<subset>\d+)/$', views.PDFList.as_view(), name='pdf_list_subset'),
    path('inctag/',  views.inclusiontag, name='online_now'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    url(r'^calendar/(?P<month>[\w\-]+)/$', views.CalendarView.as_view(), name='calendar_month_specified'), # here
    url(r'^event/new/$', views.event, name='event_new'),
    url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    url(r'^event/edit/(?P<event_id>\d+)/CalendarView/$', views.CalendarView.as_view(), name='calendar'),
    path('enroll_course/<int:pk>/', views.enroll_course, name='enroll_course'),
    path('event/new/CalendarView/', views.CalendarView.as_view(), name='calendar2')
]