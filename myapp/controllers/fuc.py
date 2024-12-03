# myapp/views.py
from datetime import datetime
import os
import sys
from django.http import HttpResponse,JsonResponse, HttpResponseNotFound, HttpResponseRedirect,HttpResponseBadRequest, Http404,HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect ,get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate
from django.core.files.base import ContentFile
from django.views import View
from django.db import transaction
from django.utils.decorators import method_decorator

# Format
from ..forms import *
from ..models import *
from ..serializers import *

# Rest Framework
from rest_framework import generics,permissions,status,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
  
# Import
import json
import base64
import codecs
from ..processdb import *
from django.core.files.storage import FileSystemStorage

def index(request):
    print('55')
    return render(request, 'index.html', {})


@method_decorator(csrf_exempt, name='dispatch')
class Crud_student(View):
    def get(self, request):
        try:
            result = TbStudent.objects.using("mysqltest").values()
            print('www')
            return JsonResponse(list(result), safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request):
        try:
            data_from_api = json.loads(request.body.decode('utf-8'))
            message = ''
            status = False
            # with transaction.atomic():
            #     result =  TbStudent.objects.using("mysqltest").create(
            #         name=data_from_api['name'],
            #         detail=data_from_api['detail'],
            #     )
            result, created =   TbStudent.objects.using("mysqltest").get_or_create(
                    name=data_from_api['name'],
                    defaults={'detail': data_from_api['detail']}
                )
            if created:
                message = "New data created"
                status = True
            else:
                message = "มีข้อมูลของ " + data_from_api['name'] + " ในฐานละ"
                
                
            return JsonResponse({ 'id': result.id, 'name': result.name,'detail':result.detail,'message':message,'status':status}, safe=False)  
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
          
    def put(self, request,id):
        try:
            data_from_api = json.loads(request.body)
            with transaction.atomic():
                result = TbStudent.objects.using("mysqltest").get(pk=id)
                result.name = data_from_api['name']
                result.detail = data_from_api['detail']
                result.save()
            return JsonResponse({ 'id': result.id, 'name': result.name,'detail':result.detail}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def delete(self, request,id):
        try:
            with transaction.atomic():
                result = TbStudent.objects.using("mysqltest").get(pk=id)
                result.delete()
            return JsonResponse({'message': 'This is a Django DELETE View for student with ID {}'.format(id)}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        
# POSTMAN ตัวอย่าง
# curl --location 'http://127.0.0.1:8000/myapp/upload' \
# --form 'data="[
#     {
#         \"data_head\": [{\"key\": \"value\"}],
#         \"data_user\": [{\"name\": \"John Doe\"}]
#     }
# ]"' \
# --form 'file1=@"/C:/Users/PethZero/Downloads/59834.jpg"'
@csrf_exempt  # Disable CSRF for testing; remove this in production.
def example_upload(request):
    result = {}
    uploaded_file_path = None  # Variable to track uploaded file paths
    try:
        if request.method == 'POST':
            # Parse 'data' from the POST request
            form_data = request.POST.get('data', '')
            if not form_data:
                raise ValueError("No 'data' key found in the request.")

            json_data = json.loads(form_data)  # Convert JSON string to Python dict
            data_head = json_data[0].get('data_head', [])
            data_user = json_data[0].get('data_user', [])

            # Print statements for debugging
            print(f"data_head: {data_head}")
            print(f"data_user: {data_user}")

            # Example logic (replace with your actual logic)
            upload_file_current = request.FILES.get('file1', None)
            upload_file_temp = None    
            # upload_file_temp  = data_head.get('file_temp', None)
            list_path = ['uploads', 'user_files']  # Path to store files
            # MODE 2 ทำการปรับปรุงใหม่สามารถ SAVE EDIT ได้โดยไม่จำเป็นต้อง (1) SAVE ก็ได้
            upload_mode = 2  # Mode: 1 (SAVE), 2 (EDIT), 3 (DELETE)
            current_time = datetime.now()  # Get the current date and time
            name_custom = generate_datetime_string(current_time,'upload')
            
            # file_name_custom มีไว้ทำไม เนื่องจาก Database id 1 คือมีคน upload a.txt id 2 ก็ a.txt 
            # ลบ id 1 ไปแล้วทำให้ id 2 โดนลบไปด้วย วิธี ดักอาจจะเป็นการเช็ค id ที่ 
            # เหลือจำนวนในชื่อเดียวกัน เราเลยทำการ เปลี่ยนชื่อให้มีความต่างกัน
            # ข้อเสีย มี 2 ไฟล์ อาจจะไฟล์เดียวกัน
            # ไม่จำเป็นต้องใช้ time อาจจะ id แล้วก็ได้แล้วแต่การออกแบบ
            file_name_custom = name_custom
            file_manager = FileUploadManager(file_name_custom=file_name_custom)
            upload_data = file_manager.handle_upload(upload_file_current, upload_file_temp, list_path, upload_mode)
            print(upload_data)

            uploaded_file_path = upload_data['uploaded_file_path']  # Track uploaded file path

            # Define result data
            result['status'] = 'ok'
            result['message'] = 'complete'
            result['data'] = {
                'data_head': data_head,
                'data_user': data_user,
                'upload_data': upload_data,
            }
        else:
            # Handle invalid request methods
            result['status'] = 'err'
            result['message'] = 'Invalid request method. Only POST is allowed.'
            
        # TEST ROLL BACK
        # raise ValueError("Upload_ERROR")
        
    except json.JSONDecodeError as json_err:
        result['status'] = 'err'
        result['message'] = f"Invalid JSON format: {json_err}"

    except Exception as e:
        print("{0} : {1}".format(sys.exc_info()[-1].tb_lineno, str(e)))

        # Rollback on error (delete the uploaded file if any)
        if uploaded_file_path and os.path.exists(uploaded_file_path):
            file_manager.roll_delete_file(uploaded_file_path)

        result['status'] = 'err'
        result['message'] = str(e)

    return JsonResponse(result, safe=False)


class OverwriteStorage(FileSystemStorage):
    # ใช้ในการทับไฟล์ เช่น a.txt  ล่าสุด ทับ a.txt อันเก่า
    def get_available_name(self, name, max_length = None):
        if self.exists(name):
            self.delete(name)
        return name

class FileUploadManager:
    """Class สำหรับจัดการการอัปโหลด แก้ไข ลบ และบันทึกการกระทำ"""

    def __init__(self, file_name_custom, allowed_extensions=None, max_file_size=None):
        self.file_name_custom = file_name_custom
        self.allowed_extensions = allowed_extensions or ['.png', '.jpg', '.jpeg', '.pdf']  # Default extensions
        self.max_file_size = max_file_size or 5 * 1024 * 1024  # Default to 5 MB
        self.file_storage = OverwriteStorage()
        self.log_file = os.path.join(settings.MEDIA_ROOT, 'upload_logs.txt')  # Log file path

    def _generate_file_path(self, directory, file_name, extension, use_suffix=True):
        """สร้างเส้นทางไฟล์ที่ต้องการ"""
        suffix = f"{self.file_name_custom}" if use_suffix else ""
        return os.path.join(directory, f"{file_name.strip()}{suffix}{extension}")

    def _validate_file(self, file):
        """ตรวจสอบความถูกต้องของไฟล์ (นามสกุลและขนาด)"""
        file_name, extension = os.path.splitext(file.name)
        if extension.lower() not in self.allowed_extensions:
            raise ValueError(f"File extension '{extension}' is not allowed.")
        if file.size > self.max_file_size:
            raise ValueError(f"File size exceeds the allowed limit of {self.max_file_size / (1024 * 1024)} MB.")

    def log_action(self, action_type, file_name=None, status='success', message=''):
        """บันทึก log การดำเนินการ"""
        with open(self.log_file, 'a') as log:
            log.write(f"{datetime.now()} | {action_type} | File: {file_name or 'N/A'} | Status: {status} | Message: {message}\n")

    def roll_delete_file(self, uploaded_file_path):
        """Delete the uploaded file in case of rollback"""
        try:
            if uploaded_file_path and os.path.exists(uploaded_file_path):
                os.remove(uploaded_file_path)
                print(f"Rollback: Deleted uploaded file {uploaded_file_path}")
            else:
                print(f"Rollback: File {uploaded_file_path} not found")
        except Exception as file_error:
            print(f"Error deleting file during rollback: {file_error}")

    def handle_upload(self, upload_file_current, upload_file_temp, list_path, mode):
        """Handle file upload for different modes (SAVE, EDIT, DELETE)"""
        result = {
            'status': False,
            'filename': '',
            'message': 'Unknown error',
            'uploaded_file_path': None  # To track the uploaded file path for rollback
        }
        try:
            # Prepare the path to store the file
            upload_directory = os.path.join(settings.MEDIA_ROOT, *list_path)
            os.makedirs(upload_directory, exist_ok=True)

            file_name = None
            uploaded_file_path = None

            if mode == 1:  # SAVE
                self._validate_file(upload_file_current)
                file_name, extension = os.path.splitext(upload_file_current.name)
                uploaded_file_path = self._generate_file_path(upload_directory, file_name, extension)
                self.file_storage.save(uploaded_file_path, upload_file_current)
                result['filename'] = f"{file_name.strip()}{self.file_name_custom}{extension}"
                result['uploaded_file_path'] = uploaded_file_path  # Track file path for rollback

            elif mode == 2:  # EDIT
                self._validate_file(upload_file_current)
                # Delete old file if it exists
                if upload_file_temp:
                    file_name_temp, extension_temp = os.path.splitext(upload_file_temp.name)
                    file_path_temp = self._generate_file_path(upload_directory, file_name_temp, extension_temp, use_suffix=False)
                    if os.path.exists(file_path_temp):
                        os.unlink(file_path_temp)

                # Save new file
                file_name, extension = os.path.splitext(upload_file_current.name)
                uploaded_file_path = self._generate_file_path(upload_directory, file_name, extension)
                self.file_storage.save(uploaded_file_path, upload_file_current)
                result['filename'] = f"{file_name.strip()}{self.file_name_custom}{extension}"
                result['uploaded_file_path'] = uploaded_file_path  # Track file path for rollback

            elif mode == 3:  # DELETE
                if upload_file_temp:
                    file_name_temp, extension_temp = os.path.splitext(upload_file_temp.name)
                    file_path_temp = self._generate_file_path(upload_directory, file_name_temp, extension_temp, use_suffix=False)
                    if os.path.exists(file_path_temp):
                        os.unlink(file_path_temp)

            else:
                result['message'] = 'Invalid mode specified'
                return result

            # Return success status and the uploaded file path for rollback
            result['status'] = True
            result['message'] = 'Operation completed successfully'

        except Exception as e:
            print(f"{sys.exc_info()[-1].tb_lineno} : {str(e)}")
            result['message'] = str(e)
        return result
    
def generate_datetime_string(time,mode='upload'):
    formatted_time = time.strftime('_%Y%m%d_%H%M%S')  # Format as yMd_hhmmss
    
    return formatted_time