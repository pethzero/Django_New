# myapp/models.py
from django.db import models
from django.db.models.fields import BooleanField

class TbStudent(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    score = models.IntegerField()
    grade = models.CharField(max_length=1)
    filename = models.CharField(max_length=255)
    
    class Meta:
        managed = False
        db_table = 'students'

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
