import datetime
from decimal import Decimal
import hashlib
import os
import os.path
import shutil
import sys
import threading
import uuid


# เนื่องจาก Exception ก็ยังเข้าเงื่อนไขได้ แม้จะ ERROR ก็ตาม
class Process:
    def __init__(self, conn):
        self.conn = conn

    def data_result(self, log, status, message, data=None):
        result = {
            'log': log,
            'status': status,
            'message': message
        }
        if data:
            result['data'] = data
        return result
    # มีปรับเล็กน้อย
    def handle_error(self, exception, log=None,result=None):
        return {
            'log': log,
            'status': 'err',
            'message': f"An error occurred: {str(exception)}",
            'result':result
        }
            
    ############################################################### VERSION NEW ###############################################################
    def handle_result(self,result=None):
        return {
            'status': 'ok',
            'message': 'process successfully',
            'result':result
        }
    def bapi_process(self,fuction_name,param):
        result = None
        try:
            result = self.conn.call(fuction_name, **param)
        except Exception as e:
            return self.handle_error(e,'0000EX')
        return self.handle_result(result)