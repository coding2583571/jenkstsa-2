from django.contrib import admin
from .models import Message, MessageReply

class ReplyInline(admin.TabularInline):
    model = MessageReply
    extra = 0
    readonly_fields = ('admin_user', 'created_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'sender_email', 'message_type', 'is_read', 'created_at')
    list_filter = ('message_type', 'is_read')
    inlines = [ReplyInline]
