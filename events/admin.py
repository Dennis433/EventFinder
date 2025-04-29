from django.contrib import admin
from .models import Category, Event

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'category', 'created_at']
    list_filter = ['category', 'date']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'date'