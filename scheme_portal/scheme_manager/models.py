from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Scheme(models.Model):
    scheme_name = models.CharField(max_length=255,db_index=True)
    scheme_link=models.URLField()
    tags=models.JSONField()
    details=models.TextField()
    benefits=models.TextField()
    eligibility_criteria=models.TextField()
    application_process=models.TextField()
    documents_required=models.TextField()
    scheme_short_title=models.CharField(max_length=100)
    scheme_category=models.JSONField()
    scheme_sub_category=models.JSONField()
    gender=models.JSONField()
    minority=models.BooleanField(default=False)
    beneficiary_state=models.JSONField(null=True,blank=True)
    residence=models.JSONField()
    caste=models.JSONField()
    disability=models.BooleanField(default=False)
    occupation=models.JSONField(null=True,blank=True)
    marital_status=models.JSONField()
    education=models.JSONField(null=True,blank=True)
    age=models.JSONField()
    is_bpl=models.BooleanField(default=False)
    is_student=models.BooleanField(default=False)
    original_eligibility=models.TextField(null=True,blank=True)
    summary=models.TextField(default="")

    def __str__(self):
        return self.scheme_name
    
class Feedback(models.Model):
       
    RATING_CHOICES=[
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5')
    ]
    rating=models.IntegerField(choices=RATING_CHOICES)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    scheme=models.ForeignKey(Scheme,on_delete=models.CASCADE,default=None)
    feedback=models.TextField()
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} -{self.scheme.scheme_name}-{self.rating} stars'
