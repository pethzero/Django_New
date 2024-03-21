# api/serializers.py
from rest_framework import serializers,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import *

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'name', 'score', 'grade')
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # บอกให้รหัสผ่านไม่ถูกส่งกลับไปใน response

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user
    
class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    
     
# //////////////////////////////////////////////////////// 
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'author']

class AuthorSerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField()
    def get_book_count(self, obj):
        return obj.book_set.count()
    class Meta:
        model = Author
        fields = ['id', 'name', 'book_count'] 