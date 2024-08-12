from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('manage-groups/', views.ManageGroups.as_view(), name='groups'),
    path('manage-groups/<int:pk>', views.RemoveManager.as_view(), name='groups'),
]