import json
import functools
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from apps.packet.models import (
    SiteContent, SponsorshipCommitment, SponsorshipTier,
    CoverStat, BudgetItem, PodiumFinish, PartnerOption, ReachStat, TaxCard
)
from apps.messaging.models import Message, MessageReply
from apps.newsroom.models import BlogPost


def admin_required(view_func):
    """Decorator: must be logged in as admin."""
    @functools.wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect('core:home')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def dashboard(request):
    ctx = {
        'page_title': 'Admin Dashboard',
        'total_commitments': SponsorshipCommitment.objects.count(),
        'pending': SponsorshipCommitment.objects.filter(status='pending').count(),
        'completed': SponsorshipCommitment.objects.filter(status='completed').count(),
        'unread_sponsor': Message.objects.filter(message_type='sponsor', is_read=False).count(),
        'unread_student': Message.objects.filter(message_type='student', is_read=False).count(),
        'unread_general': Message.objects.filter(message_type='general', is_read=False).count(),
        'recent_commitments': SponsorshipCommitment.objects.select_related('tier').order_by('-created_at')[:5],
        'recent_messages': Message.objects.order_by('-created_at')[:5],
        'published_posts': BlogPost.objects.filter(is_published=True).count(),
    }
    return render(request, 'admin_ui/dashboard.html', ctx)


@admin_required
def content_editor(request):
    """Dynamic content editor for all SiteContent keys."""
    content_items = SiteContent.objects.all().order_by('key')
    cover_stats = CoverStat.objects.all()
    budget_items = BudgetItem.objects.all()
    podium_finishes = PodiumFinish.objects.all()
    partner_options = PartnerOption.objects.all()
    reach_stats = ReachStat.objects.all()
    tax_cards = TaxCard.objects.all()
    tiers = SponsorshipTier.objects.prefetch_related('benefits').all()

    return render(request, 'admin_ui/content.html', {
        'page_title': 'Content Editor',
        'content_items': content_items,
        'cover_stats': cover_stats,
        'budget_items': budget_items,
        'podium_finishes': podium_finishes,
        'partner_options': partner_options,
        'reach_stats': reach_stats,
        'tax_cards': tax_cards,
        'tiers': tiers,
    })


@admin_required
@require_POST
def save_content(request):
    """Save a SiteContent key-value pair."""
    key = request.POST.get('key', '').strip()
    value = request.POST.get('value', '').strip()
    if not key:
        return JsonResponse({'error': 'Key is required.'}, status=400)
    obj, created = SiteContent.objects.update_or_create(
        key=key,
        defaults={'value': value}
    )
    return JsonResponse({'success': True, 'created': created})


@admin_required
def sponsorships_list(request):
    status_filter = request.GET.get('status', '')
    qs = SponsorshipCommitment.objects.select_related('tier', 'linked_user').order_by('-created_at')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'admin_ui/sponsorships.html', {
        'commitments': qs,
        'status_filter': status_filter,
        'statuses': SponsorshipCommitment.STATUS_CHOICES,
        'page_title': 'Sponsorship Commitments',
    })


@admin_required
def sponsorship_detail(request, pk):
    commitment = get_object_or_404(SponsorshipCommitment, pk=pk)
    messages = commitment.messages.order_by('created_at')
    info_rows = [
        ('Contact Name', commitment.contact_name),
        ('Email', commitment.email),
        ('Phone', commitment.phone or '—'),
        ('Tier', commitment.tier.name if commitment.tier else '—'),
        ('Contribution', f'${commitment.contribution_amount}' if commitment.contribution_amount else '—'),
        ('In-Kind Value', f'${commitment.in_kind_value}' if commitment.in_kind_value else '—'),
        ('Submitted', commitment.created_at.strftime('%B %d, %Y')),
        ('Linked Account', commitment.linked_user.email if commitment.linked_user else 'None'),
    ]
    return render(request, 'admin_ui/sponsorship_detail.html', {
        'commitment': commitment,
        'messages': messages,
        'info_rows': info_rows,
        'statuses': SponsorshipCommitment.STATUS_CHOICES,
        'page_title': f'{commitment.confirmation_number} — {commitment.company}',
    })


@admin_required
@require_POST
def update_sponsorship_status(request, pk):
    commitment = get_object_or_404(SponsorshipCommitment, pk=pk)
    new_status = request.POST.get('status', '')
    note = request.POST.get('note', '').strip()
    if new_status not in dict(SponsorshipCommitment.STATUS_CHOICES):
        return JsonResponse({'error': 'Invalid status.'}, status=400)
    commitment.status = new_status
    if note:
        commitment.status_note = note
    commitment.save()
    return JsonResponse({
        'success': True,
        'status': commitment.get_status_display(),
        'percent': commitment.status_percent,
    })


@admin_required
@require_POST
def send_sponsor_email(request, pk):
    commitment = get_object_or_404(SponsorshipCommitment, pk=pk)
    subject = request.POST.get('subject', '').strip()
    body = request.POST.get('body', '').strip()
    if not subject or not body:
        return JsonResponse({'error': 'Subject and body are required.'}, status=400)
    try:
        send_mail(
            subject=f'[Jenks TSA] {subject}',
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[commitment.email],
        )
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@admin_required
def messages_inbox(request):
    msg_type = request.GET.get('type', '')
    qs = Message.objects.select_related('sender_user').order_by('-created_at')
    if msg_type:
        qs = qs.filter(message_type=msg_type)
    return render(request, 'admin_ui/messages.html', {
        'messages': qs,
        'type_filter': msg_type,
        'page_title': 'Messages Inbox',
    })


@admin_required
def message_detail(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    if not msg.is_read:
        msg.is_read = True
        msg.save()
    replies = msg.replies.select_related('admin_user').all()
    return render(request, 'admin_ui/message_detail.html', {
        'msg': msg,
        'replies': replies,
        'page_title': f'Message from {msg.sender_name}',
    })


@admin_required
@require_POST
def reply_message(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    content = request.POST.get('content', '').strip()
    if not content:
        return JsonResponse({'error': 'Reply content required.'}, status=400)
    reply = MessageReply.objects.create(
        message=msg,
        admin_user=request.user,
        content=content,
    )
    # Optionally email the reply
    try:
        send_mail(
            subject=f'[Jenks TSA] Re: {msg.subject or "Your message"}',
            message=content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[msg.sender_email],
            fail_silently=True,
        )
    except Exception:
        pass
    return JsonResponse({'success': True, 'reply_id': str(reply.id)})


@admin_required
@require_POST
def mark_message_read(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    msg.is_read = True
    msg.save()
    return JsonResponse({'success': True})


@admin_required
def posts_list(request):
    posts = BlogPost.objects.select_related('author').order_by('-created_at')
    return render(request, 'admin_ui/posts.html', {
        'posts': posts,
        'page_title': 'Blog Posts',
    })


@admin_required
def post_edit(request, pk=None):
    post = get_object_or_404(BlogPost, pk=pk) if pk else None
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        is_published = request.POST.get('is_published') == 'on'
        if not title:
            return JsonResponse({'error': 'Title is required.'}, status=400)
        if post:
            post.title = title
            post.content = content
            post.is_published = is_published
            if is_published and not post.published_at:
                post.published_at = timezone.now()
            post.save()
        else:
            post = BlogPost.objects.create(
                title=title,
                content=content,
                author=request.user,
                is_published=is_published,
                published_at=timezone.now() if is_published else None,
            )
        return JsonResponse({'success': True, 'id': str(post.id)})

    return render(request, 'admin_ui/post_edit.html', {
        'post': post,
        'page_title': ('Edit Post' if post else 'New Post'),
    })


@admin_required
@require_POST
def post_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.delete()
    return JsonResponse({'success': True})
