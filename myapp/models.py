# myapp/models.py
from django.db import models
from django.db.models.fields import BooleanField

class TbStudent(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    detail = models.CharField(max_length=255, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    tier = models.CharField(max_length=1, blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'students'  # ตารางที่จะใช้ในฐานข้อมูล MySQL

    # objects = models.Manager.using('mysqltest')  # ระบุให้ใช้ฐานข้อมูล mysqltest

class Student(models.Model):
    name = models.CharField(max_length=255)
    score = models.FloatField()
    grade = models.CharField(max_length=1)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=255)


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class Task(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    class Meta:
        db_table = 'task'
        ordering = ['-date_created']

    def __str__(self):
        return self.title
    
    
class ThaiEmpl(models.Model):
    # recno = models.IntegerField(db_column='RECNO')  # Field name made lowercase.
    recno = models.AutoField(primary_key=True)
    empno = models.CharField(db_column='EMPNO', max_length=16, blank=True, null=True)  # Field name made lowercase.
    empname = models.CharField(db_column='EMPNAME', max_length=80, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'empl'


class PostGresEmpl(models.Model):
    recno = models.AutoField(primary_key=True)
    empno = models.CharField(max_length=16, blank=True, null=True)
    empname = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'empl'
