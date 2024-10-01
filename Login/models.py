from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="users")
    pro_pic = models.ImageField(upload_to='profile_pics')
    