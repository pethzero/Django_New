# myapp/views.py
from datetime import datetime
import os
import sys
from myapp.controllers.lib import zxlib
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
            with transaction.atomic():
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
@csrf_exempt
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
            data_head = json_data[0].get('data_head', {})
            data_user = json_data[0].get('data_user', [])

            # Extract log_mode from data_head
            log_mode = int(data_head.get('log_mode', 1))  # Default to 1 (Enable logging)

            # Example logic for handling file uploads
            upload_file_current = request.FILES.get('file1', None)
            upload_file_temp = data_head.get('file_temp', None)
            
            list_path = ['uploads', 'user_files']  # Path to store files
            # DEV
            upload_file_temp = request.POST.get('mode', '')
            upload_mode =   int(request.POST.get('mode', ''))  # Mode: 1 (SAVE), 2 (EDIT), 3 (DELETE)
            current_time = datetime.now()  # Get the current date and time
            name_custom = zxlib.generate_datetime_string(current_time, 'upload')

            file_manager = zxlib.FileUploadManager(
                file_name_custom=name_custom,
                log_mode=log_mode  # ส่ง log_mode เข้าไป
            )
            upload_data = file_manager.handle_upload(
                upload_file_current, upload_file_temp, list_path, upload_mode
            )
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
            result['status'] = 'err'
            result['message'] = 'Invalid request method. Only POST is allowed.'

    except json.JSONDecodeError as json_err:
        result['status'] = 'err'
        result['message'] = f"Invalid JSON format: {json_err}"

    except Exception as e:
        print(f"{sys.exc_info()[-1].tb_lineno} : {str(e)}")
        # Rollback on error (delete the uploaded file if any)
        if uploaded_file_path and os.path.exists(uploaded_file_path):
            file_manager.roll_delete_file(uploaded_file_path)

        result['status'] = 'err'
        result['message'] = str(e)

    return JsonResponse(result, safe=False)


@csrf_exempt
def upload_multiple(request):
    result = {}
    uploaded_file_paths = []  # List to track uploaded file paths
    try:
        if request.method == 'POST':
            # Parse 'data' from the POST request
            form_data = request.POST.get('data', '')
            if not form_data:
                raise ValueError("No 'data' key found in the request.")
            
            json_data = json.loads(form_data)  # Convert JSON string to Python dict
            data_head = json_data[0].get('data_head', {})
            data_user = json_data[0].get('data_user', [])

            # Extract log_mode from data_head
            log_mode = int(data_head.get('log_mode', 1))  # Default to 1 (Enable logging)

            # Example logic for handling multiple file uploads
            upload_files_current = request.FILES.getlist('files')  # Get multiple files as a list
            upload_file_temp = data_head.get('file_temp', None)
            
            list_path = ['uploads', 'user_files']  # Path to store files
            upload_mode = int(request.POST.get('mode', 1))  # Mode: 1 (SAVE), 2 (EDIT), 3 (DELETE)
            current_time = datetime.now()  # Get the current date and time
            name_custom = zxlib.generate_datetime_string(current_time, 'upload')

            file_manager = zxlib.FileUploadManager(
                file_name_custom=name_custom,
                log_mode=log_mode  # ส่ง log_mode เข้าไป
            )
            for upload_file in upload_files_current:
                # Handle each file upload
                print('a')
                upload_data = file_manager.handle_upload(
                    upload_file, upload_file_temp, list_path, upload_mode
                )
                if upload_data['status']:
                    uploaded_file_paths.append(upload_data['uploaded_file_path'])  # Track uploaded file path
                else:
                    # Handle error for individual file upload failure
                    result['status'] = 'err'
                    result['message'] = f"Error uploading file: {upload_data['message']}"
                    return JsonResponse(result, safe=False)

            # Define result data
            result['status'] = 'ok'
            result['message'] = 'Complete'
            result['data'] = {
                'data_head': data_head,
                'data_user': data_user,
                'uploaded_file_paths': uploaded_file_paths,  # List of uploaded file paths
            }
        else:
            result['status'] = 'err'
            result['message'] = 'Invalid request method. Only POST is allowed.'

    except json.JSONDecodeError as json_err:
        result['status'] = 'err'
        result['message'] = f"Invalid JSON format: {json_err}"

    except Exception as e:
        print(f"{sys.exc_info()[-1].tb_lineno} : {str(e)}")
        result['status'] = 'err'
        result['message'] = str(e)

    return JsonResponse(result, safe=False)



@csrf_exempt
def example_error(request):
    if request.method == 'POST':
        try:
            # Simulating an error during file processing or request handling
            data = request.POST.get('data')
            if not data:
                raise ValueError("Data is missing from the request.")

            # If data exists, proceed with your normal logic (this is just a placeholder)
            return JsonResponse({"message": "Data processed successfully!"})

        except Exception as e:
            # Log the error
            error_logger = zxlib.ErrorLogger()
            error_logger.log_error(f"Error occurred: {str(e)}")
            
            # Return an error response
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid method. Use POST."}, status=405)
    
    
    
@csrf_exempt
def api_test(request):
    if request.method == 'POST':
        try:
            # แปลง JSON payload
            data = json.loads(request.body.decode('utf-8'))
            # TEST FUCTION
            
            list_path = ['uploads', 'user_files']
            manager = zxlib.FileDirectoryManager()
            # 1. List files in directory
            print(manager.list_files_in_directory(list_path))

            # # 2. Check missing files
            # print(manager.missing_files(list_path, ['file1.txt', 'file2.txt']))

            # # 3. Check if all files exist
            # print(manager.all_files_exist(list_path, ['file1.txt', 'file2.txt']))

            # # 4. Add a new file
            # print(manager.add_file(list_path, 'test_file.txt', 'Hello World'))

            # # 5. Delete a file
            # print(manager.delete_file(list_path, 'test_file.txt'))
            # print(result)
            
            
            # ประมวลผลข้อมูล
            processed_data = {"processed": True, "original_data": data}
            return JsonResponse({ "status": True, "message": "Data processed successfully.", "data": processed_data }, status=200)
        except json.JSONDecodeError:
            return JsonResponse({ "status": False, "message": "Invalid JSON format." }, status=400)
        except Exception as e:
            return JsonResponse({ "status": False, "message": str(e) }, status=500)
    else:
        return JsonResponse({ "status": False, "message": "Only POST requests are allowed." }, status=405)
