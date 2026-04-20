from django.urls import path
from . import views

app_name = 'packet'

urlpatterns = [
    path('', views.packet_view, name='packet'),
    path('commit/', views.commit_view, name='commit'),
    path('status/', views.status_check_view, name='status'),
    path('link/', views.link_commitment_view, name='link'),
    path('confirmation/<str:confirmation_number>/', views.confirmation_view, name='confirmation'),
    path('progress/<str:confirmation_number>/', views.progress_view, name='progress'),
]
