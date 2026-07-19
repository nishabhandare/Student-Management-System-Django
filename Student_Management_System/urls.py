from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from Students import views   # if your app name is Students

urlpatterns = [
    path('admin/', admin.site.urls),

    # login / logout
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # students app
    path('Students/', include('Students.urls')),

    # home page
    path('', views.dashboard, name='home'),
]