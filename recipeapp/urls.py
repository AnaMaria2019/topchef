from django.urls import path
from recipeapp.views import (
    index,
    RegisterView,
    LoginView,
    LogoutView,
    CommentCreateView,
    CommentEditView,
    CommentDeleteView,
    UserProfileView,
    UserProfileEditView,
)

urlpatterns = [
    path('', index, name='category_list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('recipe/<int:pk>/comment/create', CommentCreateView.as_view(), name='create_comment'),
    path('recipe/<int:pk>/comment/<int:pk_comment>/edit', CommentEditView.as_view(), name='edit_comment'),
    path('recipe/<int:pk>/comment/<int:pk_comment>/delete', CommentDeleteView.as_view(), name='delete_comment'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='user_profile'),
    path('profile/<int:pk>/edit', UserProfileEditView.as_view(), name='edit_user_profile'),
]
