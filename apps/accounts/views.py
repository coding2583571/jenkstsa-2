from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import User
from apps.packet.models import SponsorshipCommitment


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    error = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        error = 'Invalid email or password.'
    return render(request, 'accounts/login.html', {'error': error, 'page_title': 'Sign In'})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    error = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        role = request.POST.get('role', 'student')
        company = request.POST.get('company', '').strip()

        if role not in ('student', 'sponsor'):
            role = 'student'
        if password != password2:
            error = 'Passwords do not match.'
        elif User.objects.filter(email=email).exists():
            error = 'An account with that email already exists.'
        else:
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=role,
                company=company,
            )
            login(request, user)
            return redirect('accounts:dashboard')
    return render(request, 'accounts/signup.html', {'error': error, 'page_title': 'Create Account'})


def logout_view(request):
    logout(request)
    return redirect('core:home')


@login_required
def dashboard(request):
    ctx = {'page_title': 'My Dashboard'}
    if request.user.is_sponsor:
        ctx['commitments'] = SponsorshipCommitment.objects.filter(
            linked_user=request.user
        ).order_by('-created_at')
    return render(request, 'accounts/dashboard.html', ctx)


@login_required
@require_POST
def link_commitment(request):
    """Link a sponsorship commitment to the logged-in sponsor's account."""
    if not request.user.is_sponsor:
        return JsonResponse({'error': 'Only sponsor accounts can link commitments.'}, status=403)

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
        return JsonResponse({'success': True})
    except SponsorshipCommitment.DoesNotExist:
        return JsonResponse({'error': 'Confirmation number and email do not match our records.'}, status=404)


@login_required
@require_POST
def update_profile(request):
    user = request.user
    user.first_name = request.POST.get('first_name', user.first_name).strip()
    user.last_name = request.POST.get('last_name', user.last_name).strip()
    user.phone = request.POST.get('phone', user.phone).strip()
    if request.user.is_sponsor:
        user.company = request.POST.get('company', user.company).strip()
    user.save()
    return JsonResponse({'success': True})
