from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('contact/send/', views.send_contact_message, name='send_contact'),
]
