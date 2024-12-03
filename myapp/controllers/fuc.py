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