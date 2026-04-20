import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import (
    SiteContent, CoverStat, PodiumFinish, BudgetItem,
    SponsorshipTier, PartnerOption, ReachStat, TaxCard,
    ContactInfo, CurrentSponsor, SponsorshipCommitment
)


def packet_view(request):
    """Main sponsorship packet — looks like a website now."""
    show_sponsors = SiteContent.get('show_current_sponsors', 'false').lower() == 'true'

    context = {
        'cover_title': SiteContent.get('cover_title', 'Invest in the next generation of tech leaders.'),
        'cover_lede': SiteContent.get('cover_lede', 'Jenks TSA is Oklahoma\'s fastest-rising technology student organization — one year old, state champions, and ready to grow.'),
        'cover_deadline': SiteContent.get('cover_deadline', 'ACCEPTING PARTNERS FOR 2025–26'),
        'cover_eyebrow': SiteContent.get('cover_eyebrow', 'TECHNOLOGY STUDENT ASSOCIATION'),
        'cover_year': SiteContent.get('cover_year', '2025–26'),
        'cover_stats': CoverStat.objects.all(),

        'who_title': SiteContent.get('who_title', 'A new chapter, already <em>winning</em>.'),
        'who_eyebrow': SiteContent.get('who_eyebrow', 'ONE CHAPTER. ONE YEAR. A STATE SWEEP.'),
        'who_lede': SiteContent.get('who_lede', 'Jenks TSA was founded in 2024 — one year ago. In that single year, we\'ve competed at Regional, State, and National conferences, and built a team that takes home hardware.'),
        'who_body1': SiteContent.get('who_body1', 'The Technology Student Association is a national CareerTech Student Organization for middle and high schoolers in STEM, leadership, and applied technology.'),
        'who_body2': SiteContent.get('who_body2', 'We compete in events spanning software development, engineering design, debate, video game design, and coding.'),
        'callout_label': SiteContent.get('callout_label', 'OUR ALUMNI'),
        'callout_text': SiteContent.get('callout_text', 'TSA alumni have gone on to study at institutions including MIT, Stanford, and Northwestern.'),
        'results_head': SiteContent.get('results_head', '— 2026 OKLAHOMA STATE CONFERENCE —'),
        'results_title': SiteContent.get('results_title', 'Nine podium finishes'),
        'podium_finishes': PodiumFinish.objects.all(),

        'ask_label': SiteContent.get('ask_label', 'ANNUAL FUNDING GOAL'),
        'ask_amount': SiteContent.get('ask_amount', '12,000'),
        'ask_copy': SiteContent.get('ask_copy', 'This year\'s goal funds national travel, competition fees, equipment, and student development programs.'),
        'budget_items': BudgetItem.objects.all(),
        'tax_cards': TaxCard.objects.all(),
        'why_bullets': [l.strip() for l in SiteContent.get('why_bullets', 'Real STEM impact\nNamed visibility across Jenks community\nTax-deductible donation').split('\n') if l.strip()],

        'tiers_eyebrow': SiteContent.get('tiers_eyebrow', 'SPONSORSHIP TIERS'),
        'tiers_title': SiteContent.get('tiers_title', 'Find your <em>level</em>.'),
        'tiers_intro': SiteContent.get('tiers_intro', 'Every tier comes with meaningful recognition. Choose the level that fits your organization.'),
        'tiers': SponsorshipTier.objects.prefetch_related('benefits').all(),

        'partner_eyebrow': SiteContent.get('partner_eyebrow', 'OTHER WAYS TO PARTNER'),
        'partner_title': SiteContent.get('partner_title', 'Beyond <em>cash</em>.'),
        'partner_intro': SiteContent.get('partner_intro', 'We welcome non-traditional partnerships. If you can offer expertise, access, or resources, we want to hear from you.'),
        'partner_options': PartnerOption.objects.all(),
        'reach_stats': ReachStat.objects.all(),

        'show_current_sponsors': show_sponsors,
        'current_sponsors': CurrentSponsor.objects.filter(is_active=True) if show_sponsors else [],

        'contact_program': ContactInfo.objects.filter(section='program').order_by('order'),
        'contact_payment': ContactInfo.objects.filter(section='payment').order_by('order'),
        'motto': SiteContent.get('motto', '"Learning to lead in a technical world."'),
        'form_year': SiteContent.get('form_year', '2025–26'),

        'page_title': 'Sponsorship Packet',
    }
    return render(request, 'packet/packet.html', context)


def commit_view(request):
    """Sponsorship commitment form submission."""
    if request.method == 'POST':
        company = request.POST.get('company', '').strip()
        contact_name = request.POST.get('contact_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        tier_id = request.POST.get('tier_id', '').strip()
        contribution_amount = request.POST.get('contribution_amount', '').strip()
        in_kind_value = request.POST.get('in_kind_value', '').strip()

        if not all([company, contact_name, email]):
            return JsonResponse({'error': 'Company, contact name, and email are required.'}, status=400)

        tier = None
        if tier_id:
            try:
                tier = SponsorshipTier.objects.get(id=tier_id)
            except SponsorshipTier.DoesNotExist:
                pass

        commitment = SponsorshipCommitment.objects.create(
            company=company,
            contact_name=contact_name,
            email=email,
            phone=phone,
            tier=tier,
            contribution_amount=contribution_amount if contribution_amount else None,
            in_kind_value=in_kind_value if in_kind_value else None,
        )

        # Link to user account if sponsor is logged in
        if request.user.is_authenticated and request.user.role == 'sponsor':
            commitment.linked_user = request.user
            commitment.save()

        # Send confirmation email
        _send_sponsorship_emails(commitment)

        return JsonResponse({
            'success': True,
            'confirmation_number': commitment.confirmation_number,
            'redirect': f'/packet/confirmation/{commitment.confirmation_number}/'
        })

    # Form lives in the packet page — redirect there on GET
    return redirect('packet:packet')


def confirmation_view(request, confirmation_number):
    """Show confirmation page after submitting sponsorship."""
    commitment = get_object_or_404(SponsorshipCommitment, confirmation_number=confirmation_number)
    return render(request, 'packet/confirmation.html', {
        'commitment': commitment,
        'page_title': f'Confirmation — {commitment.confirmation_number}',
    })


def progress_view(request, confirmation_number):
    """Show sponsorship progress/status page."""
    commitment = get_object_or_404(SponsorshipCommitment, confirmation_number=confirmation_number)
    return render(request, 'packet/progress.html', {
        'commitment': commitment,
        'statuses': [s for s in SponsorshipCommitment.STATUS_CHOICES if s[0] != 'declined'],
        'page_title': f'Sponsorship Status — {commitment.confirmation_number}',
    })


def status_check_view(request):
    """Let users look up their sponsorship status."""
    commitment = None
    error = None
    query = request.GET.get('query', '').strip()
    query_type = request.GET.get('type', 'confirmation')

    if query:
        try:
            if query_type == 'confirmation':
                commitment = SponsorshipCommitment.objects.get(confirmation_number=query.upper())
            elif query_type == 'email':
                commitment = SponsorshipCommitment.objects.filter(email=query).order_by('-created_at').first()
                if not commitment:
                    error = 'No sponsorship found with that email.'
            elif query_type == 'company':
                commitment = SponsorshipCommitment.objects.filter(company__icontains=query).order_by('-created_at').first()
                if not commitment:
                    error = 'No sponsorship found for that company.'
        except SponsorshipCommitment.DoesNotExist:
            error = 'No sponsorship found with that confirmation number.'

    return render(request, 'packet/status.html', {
        'commitment': commitment,
        'error': error,
        'query': query,
        'query_type': query_type,
        'page_title': 'Check Sponsorship Status',
    })


@login_required
def link_commitment_view(request):
    """Let a logged-in sponsor link a commitment to their account."""
    if request.method == 'POST':
        confirmation_number = request.POST.get('confirmation_number', '').strip().upper()
        email = request.POST.get('email', '').strip()

        try:
            commitment = SponsorshipCommitment.objects.get(
                confirmation_number=confirmation_number,
                email=email
            )
            if commitment.linked_user and commitment.linked_user != request.user:
                return JsonResponse({'error': 'This commitment is already linked to another account.'}, status=400)
            commitment.linked_user = request.user
            commitment.save()
            return JsonResponse({'success': True, 'message': 'Commitment linked to your account.'})
        except SponsorshipCommitment.DoesNotExist:
            return JsonResponse({'error': 'Confirmation number and email do not match our records.'}, status=400)

    return render(request, 'packet/link_commitment.html')


def _send_sponsorship_emails(commitment):
    """Send notification emails when a new sponsorship is submitted."""
    try:
        # Confirmation to sponsor
        send_mail(
            subject=f'[Jenks TSA] Sponsorship Inquiry Received — {commitment.confirmation_number}',
            message=f"""Dear {commitment.contact_name},

Thank you for your interest in sponsoring Jenks TSA!

Your confirmation number is: {commitment.confirmation_number}

You can check the status of your sponsorship at any time:
https://jenkstsa.org/packet/status/?type=confirmation&query={commitment.confirmation_number}

We will be in touch soon.

— Jenks TSA Team""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[commitment.email],
            fail_silently=True,
        )

        # Internal notification
        notification_emails = getattr(settings, 'SPONSORSHIP_NOTIFICATION_EMAILS', [])
        if notification_emails:
            send_mail(
                subject=f'[Jenks TSA] New Sponsorship Inquiry — {commitment.company}',
                message=f"""New sponsorship inquiry received.

Confirmation: {commitment.confirmation_number}
Company: {commitment.company}
Contact: {commitment.contact_name}
Email: {commitment.email}
Phone: {commitment.phone}
Tier: {commitment.tier_name_snapshot or 'Not selected'}
Amount: ${commitment.contribution_amount or 'Not specified'}

View in admin: https://jenkstsa.org/admin-ui/sponsorships/{commitment.id}/""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=list(notification_emails),
                fail_silently=True,
            )
    except Exception:
        pass
