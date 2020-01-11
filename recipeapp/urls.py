from django.urls import path
from recipeapp.views import (
    RegisterView,
    LoginView,
    LogoutView,
    CommentCreateView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('recipe/<int:pk>/comment/create', CommentCreateView.as_view(), name='create_comment'),
]
