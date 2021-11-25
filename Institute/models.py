from django.db import models
from Test.models import Paper,Result

class Institute(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=1000)
    contact_number=models.CharField(max_length=10)
    admin_id=models.IntegerField()
    institute_code=models.CharField(max_length=7)

    def delete(self, using=None, keep_parents=False):
        id=self.id
        batches=Batches.objects.filter(institute_id=id).all()
        for batch in batches:
            batch.delete()
        super().delete()

class Batches(models.Model):
    institute_id=models.IntegerField()
    batch_code=models.CharField(max_length=10,primary_key=True)
    batch_name=models.CharField(max_length=20)

    def delete(self, using=None, keep_parents=False):
        id=self.institute_id
        batch=self.batch_code
        users=User.objects.filter(institute_id=id,batch_code=batch).all()
        paper=Paper.objects.filter(institute_id=id,batch_code=batch).all()
        for pap in paper:
            pap.delete()
        for user in users:
            user.delete()
        super().delete()
class User(models.Model):
    institute_id=models.IntegerField()
    contact_number = models.CharField(max_length=10)
    batch_code=models.CharField(max_length=5)
    admin_id = models.IntegerField()
    status=models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        id=self.id
        result=Result.objects.filter(user_id=id).all()
        for res in result:
            res.delete()
        super().delete()

