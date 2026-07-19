from django.urls import path
from . import views

urlpatterns = [
   
     path('', views.dashboard, name='dashboard'),  
    path('students/', views.view_students, name='view_students'),
    path('add/', views.add_student, name='add_student'),
    path('update/<int:id>/', views.update_student, name='update_student'),
    path('delete/<int:id>/', views.delete_student, name='delete_student'),
    path('student/<int:id>/', views.view_student, name='view_student'),
    path('search/', views.search_student, name='search_student'),
    path('register/', views.register, name='register'),
   
]  
