from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('send/', views.send_message, name='send'),
]
