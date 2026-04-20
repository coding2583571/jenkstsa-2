from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Message


@require_POST
def send_message(request):
    """Public endpoint — anyone can send a message."""
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    subject = request.POST.get('subject', '').strip()
    content = request.POST.get('content', '').strip()
    commitment_id = request.POST.get('commitment_id', '').strip()

    if not all([name, email, content]):
        return JsonResponse({'error': 'Name, email, and message are required.'}, status=400)

    sender_user = request.user if request.user.is_authenticated else None
    if sender_user:
        msg_type = 'sponsor' if sender_user.is_sponsor else 'student'
    else:
        msg_type = 'general'

    related = None
    if commitment_id:
        from apps.packet.models import SponsorshipCommitment
        try:
            related = SponsorshipCommitment.objects.get(id=commitment_id)
            msg_type = 'sponsor'
        except SponsorshipCommitment.DoesNotExist:
            pass

    Message.objects.create(
        message_type=msg_type,
        sender_user=sender_user,
        sender_name=name,
        sender_email=email,
        sender_phone=phone,
        subject=subject,
        content=content,
        related_commitment=related,
    )
    return JsonResponse({'success': True})
