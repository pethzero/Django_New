from django.contrib import admin
from .models import *


class user_id(admin.ModelAdmin):
	list_display = ('id','name','score','grade')
	search_fields = ('id','name','score','grade')
 
 
admin.site.register(Student,user_id)
