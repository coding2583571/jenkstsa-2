from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event, Rubric, EventForm, Resource


def events_index(request):
    events = Event.objects.filter(is_active=True)
    return render(request, 'events/index.html', {
        'events': events,
        'page_title': 'Event Information',
    })


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug, is_active=True)
    return render(request, 'events/detail.html', {
        'event': event,
        'page_title': event.name,
    })


# Rubrics page is the ONE page that does NOT require login
def rubrics(request):
    events_with_rubrics = Event.objects.filter(
        is_active=True, rubrics__isnull=False
    ).prefetch_related('rubrics').distinct()
    return render(request, 'events/rubrics.html', {
        'events': events_with_rubrics,
        'page_title': 'Rubrics',
    })


@login_required
def forms(request):
    events_with_forms = Event.objects.filter(
        is_active=True
    ).prefetch_related('forms').distinct()
    standalone_forms = EventForm.objects.filter(event__isnull=True).order_by('order')
    return render(request, 'events/forms.html', {
        'events': events_with_forms,
        'standalone_forms': standalone_forms,
        'page_title': 'Forms',
    })


@login_required
def resources(request):
    portfolio_resources = Resource.objects.filter(resource_type='portfolio_template')
    worklog_resources = Resource.objects.filter(resource_type='worklog_template')
    guides = Resource.objects.filter(resource_type='guide')
    other = Resource.objects.filter(resource_type='other')
    return render(request, 'events/resources.html', {
        'portfolio_resources': portfolio_resources,
        'worklog_resources': worklog_resources,
        'guides': guides,
        'other': other,
        'page_title': 'Templates & Resources',
    })
