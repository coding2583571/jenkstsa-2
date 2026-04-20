import uuid
from django.db import models


class Event(models.Model):
    LEVEL_CHOICES = [
        ('ms', 'Middle School'),
        ('hs', 'High School'),
        ('both', 'Both'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='hs')
    category = models.CharField(max_length=100, blank=True, help_text='e.g. Engineering, Technology, Leadership')
    description = models.TextField()
    requirements = models.TextField(blank=True)
    eligibility = models.TextField(blank=True)
    pre_submission_info = models.TextField(blank=True)
    team_size = models.CharField(max_length=50, blank=True, help_text='e.g. 1-6 members')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'events_event'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Rubric(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rubrics')
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='rubrics/', blank=True, null=True)
    file_url = models.URLField(blank=True, help_text='External URL to rubric (e.g. TSA national site)')
    description = models.TextField(blank=True)
    year = models.CharField(max_length=10, default='2025-26')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'events_rubric'
        ordering = ['order']

    def __str__(self):
        return f"{self.event.name} — {self.name}"

    @property
    def url(self):
        if self.file:
            return self.file.url
        return self.file_url


class EventForm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='forms', null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='event_forms/', blank=True, null=True)
    file_url = models.URLField(blank=True)
    is_required = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'events_eventform'
        ordering = ['order']

    def __str__(self):
        return self.name

    @property
    def url(self):
        if self.file:
            return self.file.url
        return self.file_url


class Resource(models.Model):
    RESOURCE_TYPE_CHOICES = [
        ('portfolio_template', 'Documentation Portfolio Template'),
        ('worklog_template', 'Work Log Template'),
        ('guide', 'Guide / How-To'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=30, choices=RESOURCE_TYPE_CHOICES)
    description = models.TextField()
    how_to = models.TextField(blank=True, help_text='Instructions for using this resource')
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    file_url = models.URLField(blank=True)
    requires_login = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'events_resource'
        ordering = ['order']

    def __str__(self):
        return self.name

    @property
    def url(self):
        if self.file:
            return self.file.url
        return self.file_url
