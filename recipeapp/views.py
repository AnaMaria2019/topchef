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


class UserProfileView(DetailView):
    template_name = 'user_profile.html'
    context_object_name = 'userprofile'

    def get_object(self):
        user = User.objects.get(id=self.kwargs['pk'])
        return user


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'edit_profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileEditView, self).get_context_data(**kwargs)
        user = self.object.user
        context['form'].fields['first_name'].initial = user.first_name
        context['form'].fields['last_name'].initial = user.last_name
        context['form'].fields['e_mail'].initial = user.email
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        self.object.selfdescription = data['selfdescription']
        self.object.avatar = data['avatar']
        self.request.user.first_name = data['first_name']
        self.request.user.last_name = data['last_name']
        self.request.user.email = data['e_mail']
        self.object.save()
        self.request.user.save()
        return redirect(reverse_lazy('user_profile',
                                     kwargs={'pk': self.request.user.id}))


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
        return redirect(reverse_lazy('recipe_detail', kwargs={'pk': self.kwargs['pk']}))


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


@login_required
def recipe_delete(request, pk):
    if request.method == "POST":
        recipe = Recipe.objects.get(pk=pk)
        recipe.delete()
        return redirect(reverse_lazy("recipe_list"))
    elif request.method == "GET":
        recipe = Recipe.objects.get(pk=pk)
        return render(request, "recipe_delete.html",
                      {"recipe": recipe})


class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    fields = ['name']
    template_name = 'tag_create.html'

    def form_valid(self, form):
        tag = Tag.objects.create(
            **form.cleaned_data
        )
        return redirect(reverse_lazy("category_list"))


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
    recipe_list = Recipe.objects.filter(category=category)
    return render(request, "category_detail.html", {"category": category, "recipe_list": recipe_list})


class CommentEditView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['content']
    pk_url_kwarg = 'pk_comment'
    template_name = 'edit_comment.html'

    def form_valid(self, form):
        comment = Comment.objects.get(pk=self.kwargs['pk_comment'])
        comment.content = form.cleaned_data['content']
        comment.save()
        return redirect(reverse_lazy('recipe_detail', kwargs={'pk': self.kwargs['pk']}))


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'recipe_detail.html'
    pk_url_kwarg = 'pk_comment'

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.kwargs['pk']})
