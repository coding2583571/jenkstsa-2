from apps.messaging.models import Message


def site_globals(request):
    """Inject global context into all templates."""
    unread_counts = {}
    if request.user.is_authenticated and request.user.role == 'admin':
        unread_counts = {
            'sponsor_msgs': Message.objects.filter(message_type='sponsor', is_read=False).count(),
            'student_msgs': Message.objects.filter(message_type='student', is_read=False).count(),
            'general_msgs': Message.objects.filter(message_type='general', is_read=False).count(),
        }

    return {
        'site_name': 'Jenks TSA',
        'unread_counts': unread_counts,
    }
