# myapp/views.py
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
from .forms import *
from .models import *
from .serializers import *

# Rest Framework
from rest_framework import generics,permissions,status,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
  
# Import
import json
import base64
import codecs
from .processdb import *



def index(request):
    # return HttpResponse("Hello, World!")
    # students = TbStudent.objects.using("mysqltest").all()
    

    # # แสดงผลลัพธ์
    # for name in thai_data:
    #     print(name.decode('utf-8'))
    # for index, student in enumerate(students):
    #     print(f"ID: {student.id}, Name: {student.name}, Address: {student.address}, Score: {student.score}, Grade: {student.grade}, Filename: {student.filename}")
    return render(request, 'index.html', {})


def thaiconvert(request):
    empl_thai = ThaiEmpl.objects.using("mysqlthai").all()
    # empl_thai_old = list(empl_thai.values())
    empl_thai_values = list(empl_thai.values())
    
    # empl_postgres = PostGresEmpl.objects.using("postgres-test").all()
    # empl_postgres_values = list(empl_postgres.values())
    empl_postgres_values = ''
    # print(empl_thai_values)
    # TextConverter.convert_text(empl_thai_values, 'latin-1', 'tis-620')
    
    # 
    # for employee in empl_thai_values:
    #      for key, value in employee.items():
    #         print(key,value)
    #         if isinstance(value, str):
    #             # แปลงเป็นภาษาไทยและ encode เป็น UTF-8
    #             thai_name = value.encode('latin1').decode('tis-620')
    #             thai_utf_8 = thai_name.encode('utf-8')
    #             employee[key] = thai_utf_8.decode('utf-8')
                
    #
    # for employee in empl_thai_values:
    #     if employee['empname']:
    #         # แปลง empname เป็นภาษาไทย (เป็น tis-620)
    #         thai_name = employee['empname'].encode('latin1').decode('tis-620')
    #         # encode เป็น UTF-8
    #         employee['empname'] = thai_name.encode('utf-8')    
            
                    
    # สร้างตัวแปรเพื่อเก็บข้อมูลที่แปลงและ encode เป็นภาษาไทย
    data = {'message': 'This is a sample JSON response.','data_mysql':empl_thai_values ,'data_postgres': empl_postgres_values}
    return JsonResponse(data)

def sample_json(request):
    data = {'message': 'This is a sample JSON response.'}
    return JsonResponse(data)
    
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
# /////////////////////////////////////////////////////////////////////  CRUD   /////////////////////////////////////////////////////////////////////
# /////////////////// READ ///////////////////
def get_api(request):
    if request.method == 'GET':
        result = Student.objects.all().values()
        return JsonResponse(list(result), safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
# /////////////////// CREATE ///////////////////
@csrf_exempt
def create_api(request):
    if request.method == 'POST':
        try:
            # ดึงข้อมูล JSON ที่ถูกส่งมาจาก Vue.js
            data_from_api = json.loads(request.body.decode('utf-8'))
            # ใช้ transaction.atomic เพื่อรับประกันว่าการเพิ่มข้อมูลจะถูก commit ทั้งหมดหรือ rollback ทั้งหมด
            with transaction.atomic():
                result = Student.objects.create(
                    name=data_from_api['name'],
                    score=data_from_api['score'],
                    grade=data_from_api['grade']
                )
            response_data = {'message': 'Data added successfully'}
            return JsonResponse(response_data)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
# /////////////////// UPDATE ///////////////////
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
# /////////////////// TEST UPDATE BY METHOD POST ///////////////////
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
# /////////////////// DELETE ///////////////////  
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
# ///////////////////////////////////////// multipart/form-data /////////////////////////////////////////
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
        
# ////////////////////////////////////////////// application/json VS multipart/form-data  ////////////////////////////////////////////////////
# /////////// WHEN Fetch Header application/json
@csrf_exempt
def apipost_jsonload(request):
    if request.method == 'POST':
        try:
            data_from_api = json.loads(request.body) 
            # DB
            if data_from_api is None:
                data_from_api = None  # หรือให้เป็น None หรือค่าอื่นที่ต้องการเป็นค่าเริ่มต้น
            # print(data_from_api)
            # print(type(data_from_api))
            result = data_from_api
            if result is not None:
                response_data = {'result': data_from_api}
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': 'Invalid query ID'}, status=400)
        except Exception as e:
            print("An error occurred:", str(e))
            return JsonResponse({'error': 'An error occurred'}, status=500)
# /////////// WHEN Fetch Header Without application/json
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
            # print(ProcessDB_Queries.execute_query(dict_data))
            data_fetch = []
            # วนลูปผ่านทุก query ใน dict_data
            for query in dict_data:
                with transaction.atomic():
                    process = ProcessDB_Queries.execute_query(query)
                    data_fetch.append(ProcessDB_Queries.execute_query(query))
            # print(apidata)
            # print(type(apidata))
            # print(dict_data)
            # print(type(dict_data))
            result = data_fetch
            print(data_fetch)
            if result is not None:
                response_data = {'result': result}
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': 'Invalid query ID'}, status=400)
        except Exception as e:
            print("An error occurred:", str(e))
            return JsonResponse({'error': 'An error occurred'}, status=500)       


# ////////////////////////////////////////////// TEST Header //////////////////////////////////////////////
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
    
# ////////////////////////////////////////////// UPLOAD //////////////////////////////////////////////
# IF File_OverSize Increase DATA_UPLOAD_MAX_MEMORY_SIZE in setting.py
@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(image.name, image)  # (name.extension,file)
        return JsonResponse({'message': 'Image uploaded successfully', 'file_name': filename})
    return JsonResponse({'error': 'No image uploaded'}, status=400)

@csrf_exempt
def upload_file_multiple(request):
    if request.method == 'POST' and request.FILES.getlist('multiple_image'):
        images = request.FILES.getlist('multiple_image')
        filenames = []
        for image in images:
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(image.name, image)
            filenames.append(filename)
        return JsonResponse({'message': 'Images uploaded successfully', 'file_names': filenames})
    return JsonResponse({'error': 'No images uploaded'}, status=400)
@csrf_exempt
def upload_filebase64(request):
    if request.method == 'POST':
        try:
            # ดึงข้อมูล JSON ที่ถูกส่งมาจาก Vue.js
            memory_size = int(request.headers.get('Upload-Memory', ''))
            settings.DATA_UPLOAD_MAX_MEMORY_SIZE = memory_size + 1024
            
            data_from_api = json.loads(request.body.decode('utf-8'))
            destination_path = 'files/'
            file_name = data_from_api['name']  # ตั้งชื่อไฟล์ที่ต้องการให้เหมาะสม
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            # settings.DATA_UPLOAD_MAX_MEMORY_SIZE = data_from_api['size'] + 1024 # 50 MB หรือขนาดที่ต้องการ

            # # IF USE NOT OVERSIZE
            # # file_data  = data_from_api['file']
            # # file_binary_data = base64.b64decode(file_data)
            # # file_name = fs.save(destination_path + file_name, ContentFile(file_binary_data))
            # # file_url = fs.url(file_name)
            
            # ESLE
            # Chunk OVERSIZE
            file_data  = data_from_api['file']
              # แปลงข้อมูล Base64 กลับเป็น binary
            file_binary_data = b''.join(base64.b64decode(chunk) for chunk in file_data)
            # เขียนข้อมูล binary ลงในไฟล์
            with fs.open(fs.get_available_name(destination_path + file_name), 'wb+') as destination_file:
                destination_file.write(file_binary_data)
            # # สร้าง URL สำหรับเข้าถึงไฟล์
            
            file_url = fs.url(destination_path + file_name)
            # file_url = ''
            response_data = {'message': 'Data added successfully','upload':file_url}
            return JsonResponse(response_data)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@csrf_exempt
def upload_chunks(request):
    if request.method == 'POST':
        try:
            data_from_api = json.loads(request.body.decode('utf-8'))
            file_name = data_from_api['name']
            chunk_data = data_from_api['chunk']
            status_write = data_from_api['status_write']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            
            print(status_write)
            if status_write == 'F':
                with fs.open(file_name, 'wb+') as destination_file:
                    file_binary_data = base64.b64decode(chunk_data)
                    destination_file.write(file_binary_data)
                    status_write = 'W'
            else: 
                with fs.open(file_name, 'ab+') as destination_file:
                    file_binary_data = base64.b64decode(chunk_data)
                    destination_file.write(file_binary_data)
                    status_write = 'U'
            # ทำอะไรสักอย่างกับ chunk_data ที่ได้รับ เช่น เขียนลงไฟล์ชั่วคราว
            
            response_data = {'message': 'Chunk uploaded successfully','status_write':status_write}
            return JsonResponse(response_data)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    
class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']
            # print(uploaded_file)
            # ดำเนินการกับไฟล์ที่อัปโหลดต่อไปได้ตามต้องการ
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(uploaded_file.name, uploaded_file)
            return Response({'message': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
#  ////////////////////////////////  Django View VS RestFrameWork APIView  ////////////////////////////////
class MyView(View):
    def get(self, request):
        return HttpResponse('This is a Django View')
    
class MyAPIView(APIView):
    def get(self, request):
        return Response({'message': 'This is a Django Rest Framework APIView'}, status=status.HTTP_200_OK)    
# ////////////////////////////////////////////// RESET FRAMEWORK ////////////////////////////////////////////////////
#  ListAPIView       // แสดงผล Task ทั้งหมด
#  CreateAPIview     // สร้าง Task ใหม่
#  RetrievelAPIview  // แสดงผล Task นั้น ๆ
#  UpdateAPIview     // อัพเดต Task นั้น ๆ
#  DeleteAPIview     // ลบ Task นั้น ๆ

class StudentListCreate(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
        # Authenticate this view
    # permission_classes = [permissions.IsAuthenticated]
    
class StudentDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    
    


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)    
# ///////////////////////////////////////////////// EX_1_Non_RestAPI /////////////////////////////////////////////////
class AuthorList(View):
    def get(self, request):
        response = list()
        for author in Author.objects.all():
            response.append({
                'id': author.id,
                'name': author.name
            })
        return HttpResponse(json.dumps(response), content_type='application/json')

class AuthorDetail(View):
    def get(self, request, id):
        # if True:
        #     return self.http_method_not_allowed(request)
        try:
            author = get_object_or_404(Author, id=id)
            response = {
                'id' : author.id,
                'name': author.name
            }
            return HttpResponse(json.dumps(response), content_type='application/json')
        except Http404 as e:
            response = {'message': 'Data not found'}
            return HttpResponseNotFound(json.dumps(response), content_type='application/json')
        
    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['GET'], json.dumps({'message': 'Method Not Allowed'}), content_type='application/json')    

class BookList(View):
    def get(self, request):
        try:
            response = list()
            for book in Book.objects.all():
                response.append({
                    'id': book.id,
                    'name': book.name,
                    'author': {
                        'id': book.author.id,
                        'name': book.author.name
                    }
                })
            return HttpResponse(json.dumps(response), content_type='application/json')
        except Http404 as e:
            response = {'message': 'Data not found'}
            return HttpResponseNotFound(json.dumps(response), content_type='application/json')
        
class BookDetail(View):
    def get(self, request, id):
        try:
            book = get_object_or_404(Book, id=id)
            response = {
                'id': book.id,
                'name': book.name,
                'author': {
                    'id': book.author.id,
                    'name': book.author.name
                }
            }
            return HttpResponse(json.dumps(response), content_type='application/json')
        except Http404 as e:
            response = {'message': 'Data not found'}
            return HttpResponseNotFound(json.dumps(response), content_type='application/json')
# ///////////////////////////////////////////////// EX_2_Serializer  /////////////////////////////////////////////////
class AuthorList_Serializer(View):
    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Method Not Allowed'}, status=405)
    
    def dispatch(self, request, *args, **kwargs):
        try:
            #request.method.lower() # get
            #self.http_method_names # ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
            # ตรวจสอบเมธอดที่เรียกใช้งาน
            if request.method.lower() not in self.http_method_names:
            # if True:
                # ถ้าไม่มีเมธอดที่รองรับ
                # เรียกใช้ฟังก์ชัน http_method_not_allowed
                return self.http_method_not_allowed(request, *args, **kwargs)
            # ถ้ามีเมธอดที่รองรับ
            # เรียกใช้เมธอด dispatch ของคลาส View เพื่อทำการ dispatch ไปยังเมธอดที่ถูกเรียกใช้งาน
            return super().dispatch(request, *args, **kwargs)
        except Http404 as e:
            return JsonResponse({'message': 'Data not found'}, status=404)
    
class AuthorDetail_Serializer(View):
    def get(self, request, id):
        author = get_object_or_404(Author, id=id)
        serializer = AuthorSerializer(author)
        return JsonResponse(serializer.data)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Method Not Allowed'}, status=405)

    # วิ่งมาหา Dispatch ก่อน
    def dispatch(self, request, *args, **kwargs):
        try:
            if request.method.lower() not in self.http_method_names:
                return self.http_method_not_allowed(request, *args, **kwargs)
            return super().dispatch(request, *args, **kwargs)
        except Http404 as e:
            return JsonResponse({'message': 'Data not found'}, status=404)

class BookList_Serializer(View):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Method Not Allowed'}, status=405)

    # วิ่งมาหา Dispatch ก่อน
    def dispatch(self, request, *args, **kwargs):
        try:
            if request.method.lower() not in self.http_method_names:
                return self.http_method_not_allowed(request, *args, **kwargs)
            return super().dispatch(request, *args, **kwargs)
        except Http404 as e:
            return JsonResponse({'message': 'Data not found'}, status=404)

class BookDetail_Serializer(View):
    def get(self, request, id):
        book = get_object_or_404(Book, id=id)
        serializer = BookSerializer(book)
        return JsonResponse(serializer.data)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Method Not Allowed'}, status=405)

    # วิ่งมาหา Dispatch ก่อน
    def dispatch(self, request, *args, **kwargs):
        try:
            if request.method.lower() not in self.http_method_names:
                return self.http_method_not_allowed(request, *args, **kwargs)
            return super().dispatch(request, *args, **kwargs)
        except Http404 as e:
            return JsonResponse({'message': 'Data not found'}, status=404)
        except Exception as e:
            return JsonResponse({'message': 'Error'}, status=500)

# ///////////////////////////////////////////////// EX_3_RestAPI /////////////////////////////////////////////////    
class AuthorList_RestAPI(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorDetail_RestAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    lookup_field = 'id'
    serializer_class = AuthorSerializer

class BookList_RestAPI(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetail_RestAPI(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Book.objects.filter(id=self.kwargs.get('pk', None))
    serializer_class = BookSerializer
# ///////////////////////////////////////////////// EX_4_Router /////////////////////////////////////////////////    
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
        
# ///////////////////////////////////////////////// EX_4_Data /////////////////////////////////////////////////            
class AuthorModelCreateAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
# ////////////////////////////////////////////// RESET FRAMEWORK_MYSQL ////////////////////////////////////////////////////
#  ListAPIView       // แสดงผล Task ทั้งหมด
#  CreateAPIview     // สร้าง Task ใหม่
#  RetrievelAPIview  // แสดงผล Task นั้น ๆ
#  UpdateAPIview     // อัพเดต Task นั้น ๆ
#  DeleteAPIview     // ลบ Task นั้น ๆ
class Mysql_StudentListCreate(generics.ListCreateAPIView):
    queryset = TbStudent.objects.using("mysqltest").all()
    serializer_class = MYSQLStudentSerializer

class Mysql_StudentDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = TbStudent.objects.using("mysqltest").all()
    serializer_class = MYSQLStudentSerializer

class MyStudentViewSet(viewsets.ModelViewSet):
    queryset = TbStudent.objects.using("mysqltest").all()
    serializer_class = MYSQLStudentSerializer
    

# /////////////////////////////////////////////////////////////////////  CRUD   /////////////////////////////////////////////////////////////////////
# /////////////////// READ ///////////////////
@method_decorator(csrf_exempt, name='dispatch')
class Crud_student(View):
    def get(self, request):
        try:
            result = TbStudent.objects.using("mysqltest").values()
            return JsonResponse(list(result), safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request):
        try:
            data_from_api = json.loads(request.body.decode('utf-8'))
            with transaction.atomic():
                result =  TbStudent.objects.using("mysqltest").create(
                    name=data_from_api['name'],
                    detail=data_from_api['detail'],
                )
            return JsonResponse({ 'id': result.id, 'name': result.name,'detail':result.detail}, safe=False)  
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
    
