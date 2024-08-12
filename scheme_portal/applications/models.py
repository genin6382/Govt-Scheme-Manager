from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Application(models.Model):
    STATUS_CHOICES=[
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected')
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    scheme=models.ForeignKey('scheme_manager.Scheme',on_delete=models.CASCADE)
    status=models.CharField(choices=STATUS_CHOICES,max_length=20,default='pending')
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.scheme.scheme_name} - {self.status}'
    
class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    application = models.ForeignKey('Application', related_name='documents', on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name

    