from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.FileField(upload_to='media/', blank=True, null=True)
    selfdescription = models.CharField(max_length=500)


class Tag(models.Model):
    name = models.CharField(max_length=30)


class Category(models.Model):
    title = models.CharField(max_length=30)
