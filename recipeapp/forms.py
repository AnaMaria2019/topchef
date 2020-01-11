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
    #category = forms.ChoiceField(choices=[(c.id, c.title) for c in models.Category.objects.all()])

    class Meta:
        model = models.Recipe
        fields = ['title', 'description', 'time', 'difficulty', 'serves', 'ingredients', 'method']
