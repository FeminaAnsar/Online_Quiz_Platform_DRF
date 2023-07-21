from django.urls import path
from .views import (
    UserListCreateView, UserRetrieveUpdateDestroyView,RegisterView,UserProfileView,UserListView,UserLogoutView
)
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView
)
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/token/',TokenObtainPairView.as_view(),name='token'),
    path('login/refresh/',TokenRefreshView.as_view(),name='token-refresh'),
    path('logout/',UserLogoutView.as_view(),name='logout'),

    path('users/create/', UserListCreateView.as_view(), name='user-create'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('profile/',UserProfileView.as_view(),name='user-profile'),
]
