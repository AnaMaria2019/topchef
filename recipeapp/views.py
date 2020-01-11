from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    TemplateView, ListView,
    CreateView, UpdateView, DeleteView, DetailView
)
from recipeapp.models import User, UserProfile, Tag, Category, Recipe, Comment
from recipeapp.forms import UserProfileForm


def index(request):
    category_list = Category.objects.all()
    return render(request, 'index.html', {'category_list': category_list})


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    model = User

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(username=data['username'],
                                        password=data['password1'])
        UserProfile.objects.create(user=user)
        return redirect(reverse_lazy('category_list'))


class LoginView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self):
        form = AuthenticationForm()
        return {'form': form}

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'],
                                password=data['password'])
            login(request, user)
            return redirect(reverse_lazy('category_list'))
        else:
            return render(request, "login.html", {"form": form})


class LogoutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('category_list'))


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        recipe = Recipe.objects.get(id=self.kwargs['pk'])
        Comment.objects.create(
            created_by=self.request.user,
            recipe=recipe,
            **form.cleaned_data
        )
        return redirect(reverse_lazy('show_recipe'))


def recipe_list(request):
    recipe_list = Recipe.objects.all()
    return render(request, 'recipe_list.html', {'recipe_list': recipe_list})


def recipe_detail(request, pk):
    recipe = Recipe.objects.get(id=pk)
    return render(request, "recipe_detail.html", {"recipe": recipe})


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    #category_list = Category.objects.all()
    fields = ['category', 'title', 'description', 'time', 'difficulty', 'serves', 'ingredients', 'method']
    template_name = 'recipe_create.html'
    #context = {'category_list': category_list}

    def form_valid(self, form):
        recipe = Recipe.objects.create(
            user=self.request.user,
            **form.cleaned_data
        )
        return redirect(reverse_lazy("recipe_detail", kwargs={"pk": recipe.id}))

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['title', 'image']
    template_name = 'category_create.html'

    def form_valid(self, form):
        category = Category.objects.create(
            **form.cleaned_data
        )
        return redirect(reverse_lazy("category_list"))

def category_detail(request, pk):
    category = Category.objects.get(id=pk)
    recipe_list = Recipe.objects.filter(category=category);
    return render(request, "category_detail.html", {"category": category, "recipe_list": recipe_list})
