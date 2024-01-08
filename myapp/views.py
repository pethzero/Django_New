# myapp/views.py
from django.http import HttpResponse,JsonResponse, HttpResponseNotFound, HttpResponseRedirect
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
    # if request.method == 'POST':
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
        result = ProcessDB.execute_query(queryID)
        if result is not None:
            response_data = {'result': list(result)}
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'Invalid query ID'}, status=400)
# ////////////////////////////////////////////// RESET FRAMEWORK ////////////////////////////////////////////////////
class DataListCreate(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = DataSerializer
        # Authenticate this view
    permission_classes = [permissions.IsAuthenticated]
    
class DataDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = DataSerializer