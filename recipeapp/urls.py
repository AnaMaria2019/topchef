from django.urls import path
from recipeapp.views import (
    index,
    RegisterView,
    LoginView,
    LogoutView,
    CommentCreateView,
    recipe_list,
    recipe_detail,
    RecipeCreateView,
    category_detail,
    CategoryCreateView,
)

urlpatterns = [
    path('', index, name='category_list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('recipe/<int:pk>/comment/create', CommentCreateView.as_view(), name='create_comment'),
    path('recipe/recipe_list', recipe_list, name='recipe_list'),
    path('recipe/<int:pk>', recipe_detail, name='recipe_detail'),
    path('recipe/create', RecipeCreateView.as_view(), name='recipe_create'),
    path('category/create', CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>', category_detail, name='category_detail'),
]
