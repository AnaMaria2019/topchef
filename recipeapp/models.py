from django.contrib.auth import get_user_model
from django.db import models
from enum import Enum

User = get_user_model()


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.FileField(upload_to='media/', blank=True, null=True)
    selfdescription = models.CharField(max_length=500)


class Tag(models.Model):
    name = models.CharField(max_length=30)


class Category(models.Model):
    title = models.CharField(max_length=30)

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='category')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    time = models.CharField(max_length=30)
    difficulty = models.CharField(max_length=20)
    serves = models.IntegerField()
    ingredients = models.CharField(max_length=400)
    # de adaugat clasa Ingredients
    method = models.CharField(max_length=800)
    rating = models.IntegerField(default=0)

