from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.db import models
from enum import Enum


User = get_user_model()


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.FileField(upload_to='media/', blank=True, null=True)
    selfdescription = models.CharField(max_length=500, blank=True, null=True)


class Tag(models.Model):
    name = models.CharField(max_length=30)


class Category(models.Model):
    title = models.CharField(max_length=30)
    image = models.FileField(upload_to='media/', blank=True, null=True)
    def __str__(self):
        return self.title


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='category', null=True, blank=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    time = models.CharField(max_length=30)
    difficulty = models.CharField(max_length=20)
    serves = models.IntegerField()
    ingredients = models.CharField(max_length=400)
    # de adaugat clasa Ingredients
    method = models.CharField(max_length=800)
    rating = models.IntegerField(default=0)
    image = models.FileField(upload_to='media/', blank=True, null=True)


class Comment(models.Model):
    content = models.CharField(max_length=200)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} created by {} at {}".format(self.content, self.created_by.username, self.created_at)
