from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models

class post(models.Model):
    title = models.CharField(max_length=150)
    desc = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Connect with the User model
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the field to now when the object is created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set the field to now every time the object is saved

    
# model for feedback as named Contact
class Contact(models.Model):
     sno=models.AutoField(primary_key=True) 
     name=models.CharField(max_length=200)  
     email=models.EmailField(max_length = 254)
     phone=models.CharField(max_length=12)
     desc=models.TextField()
     time=models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return self.name
