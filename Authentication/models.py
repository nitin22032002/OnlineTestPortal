from django.db import models
from Institute.models import Institute,User
class User_website(models.Model):
    user_name=models.CharField(max_length=20)
    emailid=models.CharField(max_length=30,unique=True)
    password=models.CharField(max_length=24)
    institute_status=models.BooleanField(default=False)
    def delete(self, using=None, keep_parents=False):
        userid=self.id
        status=self.institute_status
        super().delete()
        if(status):
            institute=Institute.objects.get(admin_id=userid)
            institute.delete()
        users=User.objects.filter(admin_id=userid).all()
        for user in users:
            user.delete()

    def __str__(self):
        return f"Id {self.id}\nName {self.user_name}\nEmailid {self.emailid}\nPassword {self.password}\nStatus {self.institute_status}"
