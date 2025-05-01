from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Event, Category
from .forms import EventForm, CategoryForm
import pandas as pd
import matplotlib.pyplot as plt
import os
from django.conf import settings
from django.db import IntegrityError

def event_list(request):
    query = request.GET.get('q')
    events = Event.objects.all().order_by('-date')
    if query:
        events = events.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(category__name__icontains=query)
        )
    return render(request, 'events/event_list.html', {'events': events, 'query': query})

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Add Event'})

def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Edit Event'})

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

def dashboard(request):
    events = Event.objects.all().values('category__name', 'date')
    df = pd.DataFrame(events)
    summary = {}
    plot_url = None
    if not df.empty:
        summary = {
            'total_events': len(df),
            'unique_categories': df['category__name'].nunique(),
            'upcoming_events': len(df[df['date'] > pd.Timestamp.now(tz='UTC')])
        }
        plt.figure(figsize=(8, 6))
        df['category__name'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Event Count by Category', fontsize=14, fontweight='bold', pad=20)
        plt.ylabel('')  # Remove the y-axis label ("count")
        plot_path = os.path.join(settings.MEDIA_ROOT, 'category_plot.png')
        plt.savefig(plot_path)
        plt.close()
        plot_url = '/media/category_plot.png'
    return render(request, 'events/dashboard.html', {'summary': summary, 'plot_url': plot_url})
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('event_list')
            except IntegrityError:
                form.add_error('name', 'Category with this name already exists.')
    else:
        form = CategoryForm()
    return render(request, 'events/category_form.html', {'form': form, 'title': 'Add Category'})