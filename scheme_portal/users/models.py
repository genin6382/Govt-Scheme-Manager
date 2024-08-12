from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from .choices import STATES
# Create your models here.

class UserProfile(models.Model):

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('transgender', 'Transgender'),
    ]

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    gender=models.CharField(choices=GENDER_CHOICES,max_length=20)
    recidence_state=models.CharField(max_length=50,choices=STATES)
    recidence_district=models.CharField(max_length=50)
    caste=models.CharField(max_length=20)
    education=models.CharField(max_length=100,null=True,blank=True)
    occupation=models.CharField(max_length=70,null=True,blank=True)
    age=models.IntegerField()                         
    is_bpl=models.BooleanField(default=False)
    is_student=models.BooleanField(default=False)
    marital_status=models.CharField(max_length=30,default="single")
    is_disabled=models.BooleanField(default=False)
    phone_number=models.CharField(max_length=10)    

    REQUIRED_FIELDS=['recidence_state','recidence_district','caste','education','occupation','age','marital_status','is_disabled','is_bpl','is_student','phone_number']

    def __str__(self):
        return self.user.username
