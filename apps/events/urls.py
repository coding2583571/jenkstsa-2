from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.events_index, name='index'),
    path('rubrics/', views.rubrics, name='rubrics'),
    path('forms/', views.forms, name='forms'),
    path('resources/', views.resources, name='resources'),
    path('<slug:slug>/', views.event_detail, name='detail'),
]
