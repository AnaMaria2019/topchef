from django import forms
from recipeapp import models


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    e_mail = forms.CharField(max_length=100)
    class Meta:
        model = models.UserProfile
        exclude = ['user']


class RecipeForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=models.Category.objects.all().order_by('title'), empty_label="Category")

    class Meta:
        model = models.Recipe
        fields = ['title', 'description', 'time', 'difficulty', 'serves', 'ingredients', 'method','image']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['title','image']
