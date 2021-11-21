from django.db import models
from datetime import datetime

class Paper(models.Model):
    institute_id=models.IntegerField()
    test_start=models.DateField(default=datetime.now())
    number_question=models.IntegerField()
    name=models.CharField(max_length=30)
    total_marks=models.IntegerField()
    batch_code=models.CharField(max_length=30)

class Question(models.Model):
    paper_id=models.IntegerField()
    question_type=models.IntegerField()
    marks=models.IntegerField()
    time=models.TimeField()
    question=models.TextField(max_length=10000)
    option_a=models.CharField(max_length=100)
    option_b=models.CharField(max_length=100)
    option_c=models.CharField(max_length=100)
    option_d=models.CharField(max_length=100)

class Result(models.Model):
    paper_id=models.IntegerField()
    user_id=models.IntegerField()
    marks_obtain=models.IntegerField()

class AnswereKey(models.Model):
    paper_id=models.IntegerField()
    file_id=models.CharField(max_length=1000)

