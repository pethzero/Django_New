"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# myproject/urls.py
from django.contrib import admin
from django.urls import path
from myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='hello_world'),  # เปลี่ยนเป็น path ว่าง
    path('sample-json/', sample_json, name='sample_json'),
    # path('api/handle-data-from-vue/', handle_data_from_vue, name='handle_data_from_vue'),
    path('students/', display_students, name='display_students'),
    path('add_student/', add_student, name='add_student'),
    path('get_formapi/', get_formapi, name='get_formapi'),
    path('get_data_test/', get_data_test, name='get_data_test'),
    # /////////// CRUD /////////
    path('get_api/', get_api, name='get_api'),
    path('create_api/', create_api, name='create_api'),  # เปลี่ยนที่นี่
    path('update_postapi/', update_postapi, name='update_postapi'), 
    path('update_api/<int:result_id>/', update_api, name='update_api'),
    path('delete_api/<int:result_id>/', delete_api, name='delete_api'),
    # ////////////////////////
    
    #/////////// REST FRAMEWORK /////////////
    path('data/', DataListCreate.as_view(), name='data-list-create'),
    path('data/<int:pk>/', DataDetailUpdateDelete.as_view(), name='data-detail-update-delete'),
    # ////////////////////////
    
    # /////////////////// NEW ////////////////////
    path('post_formapi/', post_formapi, name='post_formapi'),
    # ///////////////////////////////////////
]

