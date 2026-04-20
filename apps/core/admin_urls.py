from django.urls import path
from . import admin_views

urlpatterns = [
    path('', admin_views.dashboard, name='admin_dashboard'),
    path('content/', admin_views.content_editor, name='admin_content'),
    path('content/save/', admin_views.save_content, name='admin_save_content'),
    path('sponsorships/', admin_views.sponsorships_list, name='admin_sponsorships'),
    path('sponsorships/<uuid:pk>/', admin_views.sponsorship_detail, name='admin_sponsorship_detail'),
    path('sponsorships/<uuid:pk>/update-status/', admin_views.update_sponsorship_status, name='admin_update_status'),
    path('sponsorships/<uuid:pk>/send-email/', admin_views.send_sponsor_email, name='admin_send_email'),
    path('messages/', admin_views.messages_inbox, name='admin_messages'),
    path('messages/<uuid:pk>/', admin_views.message_detail, name='admin_message_detail'),
    path('messages/<uuid:pk>/reply/', admin_views.reply_message, name='admin_reply_message'),
    path('messages/<uuid:pk>/mark-read/', admin_views.mark_message_read, name='admin_mark_read'),
    path('posts/', admin_views.posts_list, name='admin_posts'),
    path('posts/new/', admin_views.post_edit, name='admin_post_new'),
    path('posts/<uuid:pk>/', admin_views.post_edit, name='admin_post_edit'),
    path('posts/<uuid:pk>/delete/', admin_views.post_delete, name='admin_post_delete'),
]
