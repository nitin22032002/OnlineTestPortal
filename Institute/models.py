from django.db import models
class Institute(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=1000)
    contact_number=models.CharField(max_length=10)
    admin_id=models.IntegerField()
    institute_code=models.CharField(max_length=7)

class Batches(models.Model):
    institute_id=models.IntegerField()
    batch_code=models.CharField(max_length=10,primary_key=True)
    batch_name=models.CharField(max_length=20)

class User(models.Model):
    institute_id=models.IntegerField()
    contact_number = models.CharField(max_length=10)
    batch_code=models.CharField(max_length=5)
    admin_id = models.IntegerField()
    status=models.BooleanField(default=False)

