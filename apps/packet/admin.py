from django.contrib import admin
from .models import (
    SiteContent, CoverStat, PodiumFinish, BudgetItem,
    SponsorshipTier, TierBenefit, PartnerOption, ReachStat,
    TaxCard, ContactInfo, CurrentSponsor, SponsorshipCommitment
)

@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'updated_at')
    search_fields = ('key', 'value')

class TierBenefitInline(admin.TabularInline):
    model = TierBenefit
    extra = 1

@admin.register(SponsorshipTier)
class SponsorshipTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'order')
    inlines = [TierBenefitInline]
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SponsorshipCommitment)
class SponsorshipCommitmentAdmin(admin.ModelAdmin):
    list_display = ('confirmation_number', 'company', 'contact_name', 'status', 'created_at')
    list_filter = ('status', 'tier')
    search_fields = ('company', 'contact_name', 'email', 'confirmation_number')
    readonly_fields = ('id', 'confirmation_number', 'created_at', 'updated_at')

admin.site.register(CoverStat)
admin.site.register(PodiumFinish)
admin.site.register(BudgetItem)
admin.site.register(PartnerOption)
admin.site.register(ReachStat)
admin.site.register(TaxCard)
admin.site.register(ContactInfo)
admin.site.register(CurrentSponsor)
