import uuid
from django.db import models


class Message(models.Model):
    TYPE_CHOICES = [
        ('sponsor', 'Sponsor Inquiry'),
        ('student', 'Student Message'),
        ('general', 'General Contact'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='general')

    # Sender - can be anonymous or linked to a user
    sender_user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='sent_messages'
    )
    sender_name = models.CharField(max_length=200)
    sender_email = models.EmailField()
    sender_phone = models.CharField(max_length=30, blank=True)

    # Content
    subject = models.CharField(max_length=300, blank=True)
    content = models.TextField()

    # Related sponsorship (if applicable)
    related_commitment = models.ForeignKey(
        'packet.SponsorshipCommitment',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='messages'
    )

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messaging_message'
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.message_type}] {self.sender_name}: {self.subject or self.content[:50]}"


class MessageReply(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='replies')
    admin_user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='message_replies'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messaging_messagereply'
        ordering = ['created_at']

    def __str__(self):
        return f"Reply to {self.message}"
