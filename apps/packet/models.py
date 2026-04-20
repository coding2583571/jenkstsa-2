import uuid
import secrets
from django.db import models


def gen_confirmation():
    """Generate a unique TSA-XXXXXXXX confirmation number."""
    return f"TSA-{secrets.token_hex(4).upper()}"


class SiteContent(models.Model):
    """Generic key-value store for dynamic site content."""
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True)
    content_type = models.CharField(
        max_length=20,
        choices=[('text', 'Text'), ('html', 'HTML'), ('number', 'Number')],
        default='text'
    )
    description = models.CharField(max_length=200, blank=True, help_text='Admin notes')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'packet_sitecontent'
        ordering = ['key']

    def __str__(self):
        return self.key

    @classmethod
    def get(cls, key, default=''):
        try:
            return cls.objects.get(key=key).value
        except cls.DoesNotExist:
            return default


class CoverStat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=20)
    unit = models.CharField(max_length=10, blank=True)
    label = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'packet_coverstat'
        ordering = ['order']

    def __str__(self):
        return f"{self.number}{self.unit} — {self.label}"


class PodiumFinish(models.Model):
    PLACE_CHOICES = [('1st', '1st'), ('2nd', '2nd'), ('3rd', '3rd'), ('4th', '4th'), ('5th', '5th')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    place = models.CharField(max_length=5, choices=PLACE_CHOICES)
    event_name = models.CharField(max_length=200)
    conference = models.CharField(max_length=200, default='Oklahoma State Conference')
    year = models.CharField(max_length=10, default='2026')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'packet_podiumfinish'
        ordering = ['order']

    def __str__(self):
        return f"{self.place} — {self.event_name}"


class BudgetItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'packet_budgetitem'
        ordering = ['order']

    def __str__(self):
        return f"{self.amount} — {self.title}"


class SponsorshipTier(models.Model):
    BADGE_STYLE_CHOICES = [
        ('', 'None'),
        ('popular', 'Popular (Red)'),
        ('value', 'Best Value (Gold)'),
        ('default', 'Default (Blue)'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    amount = models.CharField(max_length=30, help_text='e.g. $250+')
    amount_raw = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Numeric amount for sorting/filtering')
    color_class = models.CharField(max_length=30, blank=True, help_text='CSS class: friend, bronze, silver, gold, platinum')
    badge_text = models.CharField(max_length=50, blank=True)
    badge_style = models.CharField(max_length=20, choices=BADGE_STYLE_CHOICES, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'packet_sponsorshiptier'
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.amount})"


class TierBenefit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tier = models.ForeignKey(SponsorshipTier, on_delete=models.CASCADE, related_name='benefits')
    text = models.TextField()
    is_bold = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'packet_tierbenefit'
        ordering = ['order']

    def __str__(self):
        return f"{self.tier.name}: {self.text[:60]}"


class PartnerOption(models.Model):
    """Other ways to partner section."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    example = models.TextField(blank=True, help_text='Italicized example text')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'packet_partneroption'
        ordering = ['order']

    def __str__(self):
        return self.title


class ReachStat(models.Model):
    """Stats shown in the reach strip."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=20)
    label = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'packet_reachstat'
        ordering = ['order']

    def __str__(self):
        return f"{self.number} {self.label}"


class TaxCard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    badge = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'packet_taxcard'
        ordering = ['order']

    def __str__(self):
        return self.title


class ContactInfo(models.Model):
    SECTION_CHOICES = [
        ('program', 'Program Contact'),
        ('payment', 'Payment Processing'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    label = models.CharField(max_length=100)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'packet_contactinfo'
        ordering = ['section', 'order']

    def __str__(self):
        return f"{self.section}: {self.label}"


class CurrentSponsor(models.Model):
    TIER_CHOICES = [
        ('presenting', 'Presenting'),
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
        ('friend', 'Friend'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    tier = models.CharField(max_length=20, choices=TIER_CHOICES)
    logo = models.ImageField(upload_to='sponsor_logos/', blank=True, null=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'packet_currentsponsor'
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.tier})"


class SponsorshipCommitment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('contacted', 'Contacted'),
        ('committed', 'Committed'),
        ('payment_pending', 'Payment Pending'),
        ('completed', 'Completed'),
        ('declined', 'Declined'),
    ]

    # UUID PK — NEVER conflicts with sequential IDs
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    confirmation_number = models.CharField(max_length=20, unique=True, editable=False, db_index=True)

    # Contact info
    company = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)

    # Sponsorship details
    tier = models.ForeignKey(SponsorshipTier, on_delete=models.SET_NULL, null=True, blank=True)
    tier_name_snapshot = models.CharField(max_length=50, blank=True, help_text='Snapshot of tier name at time of submission')
    contribution_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    in_kind_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    status_note = models.TextField(blank=True, help_text='Internal notes about status')

    # Account link (optional — sponsor can later link to an account)
    linked_user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='sponsorship_commitments'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'packet_sponsorshipcommitment'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.confirmation_number:
            # Generate unique confirmation number, retry if collision
            for _ in range(10):
                candidate = gen_confirmation()
                if not SponsorshipCommitment.objects.filter(confirmation_number=candidate).exists():
                    self.confirmation_number = candidate
                    break
        if self.tier and not self.tier_name_snapshot:
            self.tier_name_snapshot = self.tier.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.confirmation_number} — {self.company}"

    @property
    def status_percent(self):
        map_ = {
            'pending': 10,
            'contacted': 30,
            'committed': 50,
            'payment_pending': 70,
            'completed': 100,
            'declined': 0,
        }
        return map_.get(self.status, 10)

    @property
    def status_display_color(self):
        map_ = {
            'pending': '#6C7A89',
            'contacted': '#0047AB',
            'committed': '#B8862E',
            'payment_pending': '#D93832',
            'completed': '#22863A',
            'declined': '#999',
        }
        return map_.get(self.status, '#6C7A89')
