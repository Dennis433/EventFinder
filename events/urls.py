from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('add/', views.event_create, name='event_create'),
    path('edit/<int:pk>/', views.event_edit, name='event_edit'),
    path('event_delete/<int:pk>/', views.event_delete, name='event_delete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('category/add/', views.category_create, name='category_create'),
]