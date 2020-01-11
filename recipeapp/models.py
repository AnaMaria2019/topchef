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


class Comment(models.Model):
    content = models.CharField(max_length=200)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} created by {} at {}".format(self.content, self.created_by.username, self.created_at)
