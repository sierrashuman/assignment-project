from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    path('courses/', views.CourseList.as_view(), name='courselist'),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='coursedetail'),
]
