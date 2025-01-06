"""
URL configuration for joblisting_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/jobs/<int:id>', Job.as_view(), name='jobs'),
    path('api/v1/token' , TokenObtainPairView.as_view(), name='token'),
    path('api/v1/jobs', Jobs.as_view(), name='jobs'),
    path('api/v1/register', Register.as_view(), name='register'),
    path('api/v1/login', Login.as_view(), name='login'),
]
