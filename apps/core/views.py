from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from apps.packet.models import SiteContent, CurrentSponsor, SponsorshipTier
from apps.newsroom.models import BlogPost
from apps.events.models import Event
from apps.messaging.models import Message


def home(request):
    recent_posts = BlogPost.objects.filter(is_published=True).select_related('author')[:3]
    tiers = SponsorshipTier.objects.all()[:3]
    context = {
        'recent_posts': recent_posts,
        'tiers': tiers,
        'hero_title': SiteContent.get('home_hero_title', 'Jenks <em>TSA</em>'),
        'hero_subtitle': SiteContent.get('home_hero_subtitle', 'Technology Student Association — Jenks High School, Oklahoma'),
        'hero_body': SiteContent.get('home_hero_body', 'We compete. We build. We lead. Join the fastest-rising TSA chapter in the state.'),
        'page_title': 'Jenks TSA — Home',
    }
    return render(request, 'core/home.html', context)


def contact(request):
    return render(request, 'core/contact.html', {'page_title': 'Contact Us'})


def calendar_view(request):
    calendar_embed = SiteContent.get('google_calendar_embed', '')
    return render(request, 'core/calendar.html', {
        'calendar_embed': calendar_embed,
        'page_title': 'Calendar',
    })


@require_POST
def send_contact_message(request):
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    message_text = request.POST.get('message', '').strip()

    if not all([name, email, message_text]):
        return JsonResponse({'error': 'Name, email, and message are required.'}, status=400)

    sender_user = request.user if request.user.is_authenticated else None
    msg_type = 'student' if (sender_user and sender_user.role == 'student') else 'general'

    Message.objects.create(
        message_type=msg_type,
        sender_user=sender_user,
        sender_name=name,
        sender_email=email,
        sender_phone=phone,
        subject='Contact Form',
        content=message_text,
    )
    return JsonResponse({'success': True})
