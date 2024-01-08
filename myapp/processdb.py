# processdb.py
from myapp.models import *

class ProcessDB:
    @staticmethod
    def execute_query(query_id):
        if query_id == 'SQL0000':
            # ดึงข้อมูลทั้งหมดจาก Student model
            data = Student.objects.all().values()
            return data
        else:
            return None
