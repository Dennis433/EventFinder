from django.contrib import admin
from .models import Category, Event

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_count']
    search_fields = ['name']
    ordering = ['name']

    def event_count(self, obj):
        return obj.event_set.count()
    event_count.short_description = 'Number of Events'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'category', 'created_at']
    list_filter = ['category', 'date']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'date'
    ordering = ['-date']