from django.contrib import admin
from .models import Event, Rubric, EventForm, Resource

class RubricInline(admin.TabularInline):
    model = Rubric
    extra = 0

class EventFormInline(admin.TabularInline):
    model = EventForm
    extra = 0

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'category', 'is_active', 'order')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [RubricInline, EventFormInline]

admin.site.register(Resource)
