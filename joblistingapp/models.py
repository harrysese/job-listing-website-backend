from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    title=models.CharField(max_length=50)
    type=models.CharField(max_length=50)
    location=models.CharField(max_length=50)
    description=models.TextField(max_length=1000)
    salary=models.CharField(max_length=50)
    companyname=models.CharField(max_length=50)
    companydescription=models.TextField(max_length=1000)
    company_contactemail=models.EmailField()
    company_contactphone=models.CharField(max_length=20)
    user=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.title
    