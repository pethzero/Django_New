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


class ProcessDB_Queries:
    @staticmethod
    def execute_query(query):
        print(query)
        if query['queryID'] == 'SQL0000':
            data = list(Student.objects.all().values())
            return data
        else:
            return None


class TextConverter:
    @staticmethod
    def convert_text(data_list, source_encoding, target_encoding):
        for data in data_list:
            for key, value in data.items():
                if isinstance(value, str):
                    encoded_text = value.encode(source_encoding).decode(target_encoding)
                    # utf8_encoded_text = encoded_text.encode('utf-8')
                    # data[key] = utf8_encoded_text.decode('utf-8')
                    # data[key] = encoded_text.encode('utf-8').decode('utf-8')
                    # data[key] = value.encode('tis-620').decode('utf-8')
                    data[key] = encoded_text
                    
