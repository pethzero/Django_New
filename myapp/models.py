# myapp/models.py
from django.db import models
from django.db.models.fields import BooleanField

class Student(models.Model):
    name = models.CharField(max_length=255)
    score = models.FloatField()
    grade = models.CharField(max_length=1)

    def __str__(self):
        return self.name

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