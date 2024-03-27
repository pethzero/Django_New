from django.contrib import admin
from .models import *


class user_id(admin.ModelAdmin):
	list_display = ('id','name','score','grade')
	search_fields = ('id','name','score','grade')
 
 
class TbStudentAdmin(admin.ModelAdmin):
    # Define which fields you want to display in the admin list view
    list_display = ('id', 'name', 'detail', 'score', 'tier', 'filename')
    
    # Optionally, you can add search functionality based on specific fields
    search_fields = ['name', 'detail']
    
    # Optionally, you can add filters based on specific fields
    list_filter = ['tier']

# Register the TbStudent model with the custom admin options
admin.site.register(TbStudent, TbStudentAdmin)
admin.site.register(Student,user_id)




