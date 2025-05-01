from django.db import migrations

def create_default_categories_and_events(apps, schema_editor):
    Category = apps.get_model('events', 'Category')
    Event = apps.get_model('events', 'Event')
    default_categories = ['Sport', 'Entertainment', 'Educative', 'Religious']
    for name in default_categories:
        category, created = Category.objects.get_or_create(name=name)
        Event.objects.get_or_create(
            title=f"Sample {name} Event",
            description=f"A sample {name} event for testing.",
            date="2025-06-01T10:00:00Z",
            location="Sample Venue",
            category=category,
        )

class Migration(migrations.Migration):
    dependencies = [
        ('events', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_default_categories_and_events),
    ]