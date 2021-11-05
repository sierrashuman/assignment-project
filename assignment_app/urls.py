from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    path('courses/', views.CourseList.as_view(), name='courselist'),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='coursedetail'),
    path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
    path('pdf_list/', views.PDFList.as_view(), name='pdf_list'),
    path('inctag/',  views.inclusiontag),
]