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
from django.urls import path,include
from myapp.views import *

from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'author_router', AuthorViewSet, basename='author_router')
router.register(r'book_router',BookViewset , basename='book_router')
router.register(r'mysqlstudent_router',MyStudentViewSet , basename='mysqlstudent_router')

urlpatterns = [
     # /////////// TEST /////////
    path('admin/', admin.site.urls),
    path('', index, name='hello_world'),  # เปลี่ยนเป็น path ว่าง
    path('sample-json/', sample_json, name='sample_json'),
    path('students/', display_students, name='display_students'),
    path('add_student/', add_student, name='add_student'),
    path('get_formapi/', get_formapi, name='get_formapi'),
    path('get_data_test/', get_data_test, name='get_data_test'),
    
    path('thaiconvert/', thaiconvert, name='thaiconvert'),
    
    # /////////// CRUD /////////
    path('get_api/', get_api, name='get_api'),
    path('create_api/', create_api, name='create_api'),  
    path('update_postapi/', update_postapi, name='update_postapi'), 
    path('update_api/<int:result_id>/', update_api, name='update_api'),
    path('delete_api/<int:result_id>/', delete_api, name='delete_api'),
    
    path('crud_student/', Crud_student.as_view(), name='crud_student_list'),
    path('crud_student/<int:id>/', Crud_student.as_view(), name='crud_student_detail'),
        # path('crud_student/<int:pk>/', Crud_student.as_view(), name='crud_student'),
    #/////////// REST FRAMEWORK /////////////
    path('mysqlstudent/', Mysql_StudentListCreate.as_view(), name='mysql_student-list-create'),
    path('mysqlstudent/<int:pk>/', Mysql_StudentDetailUpdateDelete.as_view(), name='mysql_student-detail-update-delete'),
    
    # //// DB SILTE
    path('student_restapi/', StudentListCreate.as_view(), name='data-list-create'),
    path('student_restapi/<int:pk>/', StudentDetailUpdateDelete.as_view(), name='data-detail-update-delete'),
    path('login/', LoginAPIView.as_view(), name='login'),
    
    path('my-view/', MyView.as_view(), name='my-view'),
    path('my-api-view/', MyAPIView.as_view(), name='my-api-view'),
    
    
    #  EX_1_Non_RestAPI
    path('author/', AuthorList.as_view()),
    path('author/<int:id>', AuthorDetail.as_view()),
    path('book/', BookList.as_view()),
    path('book/<int:id>', BookDetail.as_view()),
    
    
    #  EX_2_Serializer
    path('authorserializer/', AuthorList_Serializer.as_view()),
    path('authorserializer/<int:id>', AuthorDetail_Serializer.as_view()),
    path('bookserializer/', BookList_Serializer.as_view()),
    path('bookserializer/<int:id>', BookDetail_Serializer.as_view()),
    
    #  EX_3_RestAPI
    path('authorrestapi/', AuthorList_RestAPI.as_view()),
    path('authorrestapi/<int:id>', AuthorDetail_RestAPI.as_view()),
    path('bookrestapi/', BookList_RestAPI.as_view()),
    path('bookrestapi/<int:pk>', BookDetail_RestAPI.as_view()),
    
    #  EX_4_
    path('library/', include(router.urls)),
    # path('author_router/', AuthorViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    
    path('authormulti/', AuthorModelCreateAPIView.as_view()),
    # /////////////////// NEW ////////////////////
    # header-format
    path('post_formapi/', post_formapi, name='post_formapi'),
    path('apipost_jsonload/', apipost_jsonload, name='apipost_jsonload'),
    path('apipost_formdata/', apipost_formdata, name='apipost_formdata'),
    
    # Token
    path('format_token/', format_token, name='format_token'),   
    
    # Upload
    path('upload_chunks/', upload_chunks, name='upload_chunks'),
    path('upload_filebase64/', upload_filebase64, name='upload_filebase64'),
    path('upload_file_multiple/', upload_file_multiple, name='upload_file_multiple'),
    path('upload_file/', upload_file, name='upload_file'),
    
    path('restapiupload/', FileUploadView.as_view(), name='file-upload'),
    
    # /////////////////// END ////////////////////
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

