from django.db import models
from datetime import datetime

class Paper(models.Model):
    institute_id=models.IntegerField()
    test_start=models.CharField(max_length=100,default=str(datetime.now()))
    test_end=models.CharField(max_length=100,default=str(datetime.now()))
    number_question=models.IntegerField()
    name=models.CharField(max_length=30)
    total_marks=models.IntegerField()
    batch_code=models.CharField(max_length=30)

    def delete(self, using=None, keep_parents=False):
        id=self.id
        super().delete()
        questions=Question.objects.filter(paper_id=id).all()
        for que in questions:
            que.delete()

class Question(models.Model):
    paper_id=models.IntegerField()
    question_type=models.IntegerField()
    marks=models.IntegerField()
    time=models.TimeField()
    question=models.TextField(max_length=10000)
    answere=models.CharField(default="",max_length=100)
    option_a=models.CharField(max_length=100)
    option_b=models.CharField(max_length=100)
    option_c=models.CharField(max_length=100)
    option_d=models.CharField(max_length=100)

class Result(models.Model):
    paper_id=models.IntegerField()
    user_id=models.IntegerField()
    marks_obtain=models.IntegerField()
    question_left = models.IntegerField(default=0)
    question_attempt = models.IntegerField(default=0)
    question_wrong = models.IntegerField(default=0)



