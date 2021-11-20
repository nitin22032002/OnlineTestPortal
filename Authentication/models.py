from django.db import models

class User_website(models.Model):
    user_name=models.CharField(max_length=20)
    emailid=models.CharField(max_length=30,unique=True)
    password=models.CharField(max_length=24)
    institute_status=models.BooleanField(default=False)
    def __str__(self):
        return f"Id {self.id}\nName {self.user_name}\nEmailid {self.emailid}\nPassword {self.password}\nStatus {self.institute_status}"
