"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path run_query
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp.controllers import fuc

urlpatterns = [
    path('hello_world', fuc.index),
    path('crud_student/', fuc.Crud_student.as_view()),    
    path('crud_student/<int:id>/', fuc.Crud_student.as_view()), 
    path('upload', fuc.example_upload),         
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)