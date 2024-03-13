# myapp/views.py
from django.http import HttpResponse,JsonResponse, HttpResponseNotFound, HttpResponseRedirect,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
# from .models import *
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from .serializers import *
from rest_framework import generics,permissions  
import json
from .processdb import ProcessDB

from django.conf import settings
from django.core.files.storage import FileSystemStorage

def index(request):
    return HttpResponse("Hello, World!")

def sample_json(request):
    data = {'message': 'This is a sample JSON response.'}
    return JsonResponse(data)

# @csrf_exempt
# def handle_data_from_api(request):
#     if request.method == 'POST':
#         try:
#             data_from_api = json.loads(request.body.decode('utf-8'))
#             response_data = {'message': 'Data received successfully'}
#             return JsonResponse(response_data)
#         except json.JSONDecodeError as e:
#             return JsonResponse({'error': 'Invalid JSON format'}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)
    
def display_students(request):
    students = Student.objects.all()
    return render(request, 'students.html', {'students': students})


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            print('Data Add SuccessFully')
            return redirect('display_students')  # ไปที่หน้าแสดงข้อมูลนักเรียนหลังจากเพิ่มข้อมูลเสร็จ
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})

def get_data_test(request):
    if request.method == 'GET':
        # Replace this with your actual data or database query
        data_from_django = {
            'message': 'Hello from Django!',
            'example_data': [1, 2, 3, 4, 5],
        }
        return JsonResponse(data_from_django)
    return JsonResponse({'error': 'Invalid request method'}, status=405)




# ////////////////////////////////////////////////  CRUD   /////////////////////////////////////////////////////////////////////
def get_api(request):
    if request.method == 'GET':
        result = Student.objects.all().values()
        return JsonResponse(list(result), safe=False)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

from django.db import transaction

@csrf_exempt
def create_api(request):
    if request.method == 'POST':
        try:
            # ดึงข้อมูล JSON ที่ถูกส่งมาจาก Vue.js
            data_from_api = json.loads(request.body.decode('utf-8'))
            print(data_from_api)
            # ใช้ transaction.atomic เพื่อรับประกันว่าการเพิ่มข้อมูลจะถูก commit ทั้งหมดหรือ rollback ทั้งหมด
            with transaction.atomic():
                # สร้าง student ใหม่จากข้อมูลที่ได้รับ
                result = Student.objects.create(
                    name=data_from_api['name'],
                    score=data_from_api['score'],
                    grade=data_from_api['grade']
                )
                # (Optional) ทำการประมวลผลเพิ่มเติมหรือทำอย่างอื่น ๆ ที่คุณต้องการ
            # ส่ง JSON response กลับไปยัง Vue.js
            response_data = {'message': 'Data added successfully'}
            return JsonResponse(response_data)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def update_api(request, result_id):
    if request.method == 'PUT':    
        try:
            # ดึงข้อมูล JSON ที่ถูกส่งมาจาก Vue.js
            data_from_api = json.loads(request.body)
            
            # ใช้ transaction.atomic เพื่อรับประกันว่าการเพิ่มข้อมูลจะถูก commit ทั้งหมดหรือ rollback ทั้งหมด
            with transaction.atomic():
                # ดึงข้อมูลนักเรียนที่ต้องการอัปเดต
                result = Student.objects.get(pk=result_id)

                # อัปเดตข้อมูลนักเรียน
                result.name = data_from_api['name']
                result.score = data_from_api['score']
                result.grade = data_from_api['grade']
                result.save()

            # ส่ง JSON response กลับไปยัง Vue.js
            response_data = {'message': 'Data updated successfully'}
            return JsonResponse(response_data)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Data not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def update_postapi(request):
    if request.method == 'POST':
    # if request.method == 'PUT':    
        try:
            # ดึงข้อมูล JSON ที่ถูกส่งมาจาก Vue.js
            data_from_api = json.loads(request.body)
            
            # ใช้ transaction.atomic เพื่อรับประกันว่าการเพิ่มข้อมูลจะถูก commit ทั้งหมดหรือ rollback ทั้งหมด
            with transaction.atomic():
                # ดึงข้อมูลนักเรียนที่ต้องการอัปเดต
                result = Student.objects.get(pk=data_from_api['id'])

                # อัปเดตข้อมูลนักเรียน
                result.name = data_from_api['name']
                result.score = data_from_api['score']
                result.grade = data_from_api['grade']
                result.save()

            # ส่ง JSON response กลับไปยัง Vue.js
            response_data = {'message': 'Data updated successfully'}
            return JsonResponse(response_data)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Data not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@csrf_exempt
def delete_api(request, result_id):
    if request.method == 'DELETE':
        try:
            result = Student.objects.get(pk=result_id)
            result.delete()
            response_data = {'message': 'Data deleted successfully'}
            return JsonResponse(response_data)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Data not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@csrf_exempt
def get_formapi(request):
 if request.method == 'GET':
        # ดึงข้อมูลจาก request.GET
        foo_value = request.GET.get('foo', '')

        # ทำสิ่งที่คุณต้องการกับข้อมูลที่ดึงมา เช่น สร้าง response
        response_data = {'result': f'Value of foo is {foo_value}'}

        # ส่ง response กลับไป
        return JsonResponse(response_data)
    
@csrf_exempt
def post_formapi(request):
    if request.method == 'POST':
        queryID = request.POST.get('queryID', '')
        # DB
        result = ProcessDB.execute_query(queryID)
        
        if result is not None:
            response_data = {'result': list(result)}
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'Invalid query ID'}, status=400)
        
# ////////////////////////////////////////////// Modify ////////////////////////////////////////////////////
@csrf_exempt
def apipost_jsonload(request):
    if request.method == 'POST':
        try:
            data_from_api = json.loads(request.body) 
            
            # DB
            if data_from_api is None:
                data_from_api = None  # หรือให้เป็น None หรือค่าอื่นที่ต้องการเป็นค่าเริ่มต้น
            print(data_from_api)
            print(type(data_from_api))
            result = data_from_api
            
            
            if result is not None:
                response_data = {'result': data_from_api}
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': 'Invalid query ID'}, status=400)
        except Exception as e:
            print("An error occurred:", str(e))
            return JsonResponse({'error': 'An error occurred'}, status=500)

@csrf_exempt
def apipost_formdata(request):
    if request.method == 'POST':
        try:
            # django_key = request.META.get('HTTP_GENARATE_DJANGO_KEY', '')
            # auth_header = request.headers.get('Authorization', None)
            # django_key = request.headers.get('Genarate-Django-KEY', '')
            
            apidata = request.POST.get('apidata', '')
            if apidata is None:
                apidata = None  # หรือให้เป็น None หรือค่าอื่นที่ต้องการเป็นค่าเริ่มต้น
            dict_data = json.loads(apidata)
                
            # print(apidata)
            # print(type(apidata))
            # print(dict_data)
            # print(type(dict_data))
            
            result = dict_data
            if result is not None:
                response_data = {'result': result}
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': 'Invalid query ID'}, status=400)
        except Exception as e:
            print("An error occurred:", str(e))
            return JsonResponse({'error': 'An error occurred'}, status=500)       

def format_token(request):
    try:
        # ดึงค่าของหัวข้อ Authorization จาก request headers
        auth_header = request.headers.get('Authorization', None)
        django_key = request.headers.get('Genarate-Django-KEY', '')
        print('data',auth_header)
        print('data',django_key)
        
        if django_key != '052571QADWFER':
            return JsonResponse({'result': 'You Not Permission'})
        # ตรวจสอบว่ามีหัวข้อ Authorization หรือไม่
        if auth_header is not None:
            # แยกค่าของหัวข้อ Authorization เพื่อให้ได้ Access Token
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                access_token = parts[1]

                # ทำสิ่งที่คุณต้องการกับ Access Token ที่ได้รับ
                # เช่น การตรวจสอบความถูกต้องของ Access Token, การดึงข้อมูลผู้ใช้, ฯลฯ

                # สร้าง dictionary ที่มี key เป็น 'message' และ value เป็นข้อความ Access Token
                response_data = {'message': 'Access Token: ' + access_token}
                return JsonResponse(response_data)
        # หากไม่มีหัวข้อ Authorization หรือหากมีรูปแบบไม่ถูกต้อง
        # คุณสามารถตอบกลับด้วยข้อความข้อผิดพลาดหรือทำการรับทราบได้
    except Exception as e:
        print("An error occurred:", str(e))
        return JsonResponse({'error': 'An error occurred'}, status=500)
  
@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        
        # บันทึกไฟล์ภาพที่อัปโหลดลงในโฟลเดอร์ media
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(image.name, image)
        
        # ทำอะไรต่อกับไฟล์ที่อัปโหลด เช่น บันทึกลงฐานข้อมูล หรือเป็นการประมวลผลรูปภาพ
        # ส่งข้อความยืนยันการอัปโหลดสำเร็จกลับไปยังผู้ใช้
        return JsonResponse({'message': 'Image uploaded successfully', 'file_name': filename})
    
    # หากไม่มีไฟล์ภาพถูกอัปโหลด ส่งข้อความแจ้งเตือนกลับไปยังผู้ใช้
    return JsonResponse({'error': 'No image uploaded'}, status=400)

@csrf_exempt
def upload_image_multiple(request):
    if request.method == 'POST' and request.FILES.getlist('multiple_image'):
        images = request.FILES.getlist('multiple_image')
        filenames = []
        for image in images:
            # บันทึกไฟล์ภาพที่อัปโหลดลงในโฟลเดอร์ media
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(image.name, image)
            filenames.append(filename)
        
        # ส่งข้อความยืนยันการอัปโหลดสำเร็จกลับไปยังผู้ใช้
        return JsonResponse({'message': 'Images uploaded successfully', 'file_names': filenames})
    
    # หากไม่มีไฟล์ภาพถูกอัปโหลด ส่งข้อความแจ้งเตือนกลับไปยังผู้ใช้
    return JsonResponse({'error': 'No images uploaded'}, status=400)
# ////////////////////////////////////////////// RESET FRAMEWORK ////////////////////////////////////////////////////
class DataListCreate(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = DataSerializer
        # Authenticate this view
    permission_classes = [permissions.IsAuthenticated]
    
class DataDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = DataSerializer