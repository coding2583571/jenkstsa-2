"""
python manage.py seed_data

Populates all default packet content, tiers, and site settings.
Safe to run multiple times — uses get_or_create, never overwrites existing data.
"""
from django.core.management.base import BaseCommand
from apps.packet.models import (
    SiteContent, CoverStat, PodiumFinish, BudgetItem,
    SponsorshipTier, TierBenefit, PartnerOption, ReachStat,
    TaxCard, ContactInfo
)


def sc(key, value, description=''):
    """Create SiteContent only if it doesn't already exist."""
    SiteContent.objects.get_or_create(
        key=key,
        defaults={'value': value, 'description': description}
    )


class Command(BaseCommand):
    help = 'Seed default packet content (safe to re-run)'

    def handle(self, *args, **options):
        self.stdout.write('Seeding site content...')

        # ── COVER PAGE ──────────────────────────────────
        sc('cover_eyebrow', 'TECHNOLOGY STUDENT ASSOCIATION')
        sc('cover_year', '2025–26')
        sc('cover_title', 'Invest in the next generation of tech leaders.')
        sc('cover_lede',
           'Jenks TSA is Oklahoma\'s fastest-rising technology student '
           'organization — one year old, state champions, and ready to grow.')
        sc('cover_deadline', 'ACCEPTING PARTNERS FOR 2025–26')

        # ── WHO WE ARE ──────────────────────────────────
        sc('who_eyebrow', 'ONE CHAPTER. ONE YEAR. A STATE SWEEP.')
        sc('who_title', 'A new chapter,<br/>already <em>winning</em>.')
        sc('who_lede',
           'Jenks TSA was founded in 2024 — one year ago. In that single year, '
           'we\'ve competed at Regional, State, and National conferences, and '
           'built a team that takes home hardware.')
        sc('who_body1',
           'The Technology Student Association is a national CareerTech Student '
           'Organization for middle and high schoolers in STEM, leadership, and '
           'applied technology. Our chapter is sponsored by Dr. David Lawrence '
           'and Cory Legrand — both CareerTech STEM instructors at Jenks High School.')
        sc('who_body2',
           'We compete in events spanning software development, engineering design, '
           'debate, video game design, and coding. Students don\'t just learn theory '
           '— they ship real projects, pitch to judges, and defend their work under pressure.')
        sc('callout_label', 'OUR ALUMNI')
        sc('callout_text',
           'TSA alumni have gone on to study at institutions including MIT, Stanford, '
           'and Northwestern. The students you\'re investing in today are the engineers, '
           'researchers, and founders of tomorrow.')
        sc('results_head', '2026 OKLAHOMA STATE CONFERENCE')
        sc('results_title', 'Nine podium finishes')

        # ── THE ASK ─────────────────────────────────────
        sc('ask_label', 'ANNUAL FUNDING GOAL')
        sc('ask_amount', '12,000')
        sc('ask_copy',
           'This year\'s goal funds national travel, competition fees, equipment, '
           'and student development programs that make our chapter competitive at '
           'the national level.')
        sc('why_bullets',
           'Real STEM impact for Jenks students\n'
           'Named visibility across the Jenks community\n'
           'Tax-deductible 501(c)(3) donation\n'
           'Recognized by students, parents, and faculty')

        # ── TIERS ───────────────────────────────────────
        sc('tiers_eyebrow', 'SPONSORSHIP TIERS')
        sc('tiers_title', 'Find your <em>level</em>.')
        sc('tiers_intro',
           'Every tier comes with meaningful recognition. Choose the level that '
           'fits your organization and we\'ll make sure your investment is visible.')

        # ── PARTNER OPTIONS ──────────────────────────────
        sc('partner_eyebrow', 'OTHER WAYS TO PARTNER')
        sc('partner_title', 'Beyond <em>cash</em>.')
        sc('partner_intro',
           'We welcome non-traditional partnerships. If you can offer expertise, '
           'access, or resources, we want to hear from you.')

        # ── PACKET FORM ─────────────────────────────────
        sc('form_year', '2025–26')
        sc('motto', '"Learning to lead in a technical world."')

        # ── HOMEPAGE ────────────────────────────────────
        sc('home_hero_title', 'Jenks <em>TSA</em>')
        sc('home_hero_body',
           'We compete. We build. We lead. Join the fastest-rising TSA chapter in Oklahoma.')

        # ── MISC ─────────────────────────────────────────
        sc('show_current_sponsors', 'false',
           'Set to "true" to show the current sponsors section on the packet page')
        sc('google_calendar_embed', '',
           'Paste the full Google Calendar iframe embed code here')

        self.stdout.write('  + SiteContent: OK')

        # ── COVER STATS ─────────────────────────────────
        stats = [
            ('25', '+', 'Active members\ncompeting this season', 0),
            ('9', '', 'State podium\nfinishes — year one', 1),
            ('1', '', 'Year old\nFounded 2024', 2),
        ]
        for num, unit, label, order in stats:
            CoverStat.objects.get_or_create(
                number=num, unit=unit,
                defaults={'label': label, 'order': order}
            )
        self.stdout.write('  + CoverStats: OK')

        # ── PODIUM FINISHES ──────────────────────────────
        finishes = [
            ('1st', 'Future Technology Teacher', 0),
            ('2nd', 'Future Technology Teacher', 1),
            ('1st', 'Debating Technological Issues', 2),
            ('1st', 'Coding', 3),
            ('3rd', 'Technology Bowl', 4),
            ('2nd', 'Video Game Design', 5),
            ('2nd', 'Webmaster', 6),
            ('3rd', 'Engineering Design', 7),
            ('3rd', 'Software Development', 8),
        ]
        for place, event, order in finishes:
            PodiumFinish.objects.get_or_create(
                place=place, event_name=event,
                defaults={'conference': '2026 Oklahoma State Conference', 'year': '2026', 'order': order}
            )
        self.stdout.write('  + PodiumFinishes: OK')

        # ── BUDGET ITEMS ─────────────────────────────────
        budget = [
            ('$4,200', 'National Conference Travel', 'Flights, hotel, and registration for qualifying members attending TSA Nationals.', 0),
            ('$2,800', 'State Conference Fees', 'Registration, event fees, and transportation for all competing members.', 1),
            ('$2,100', 'Equipment & Materials', 'CAD licenses, prototyping materials, and tech resources for event preparation.', 2),
            ('$1,400', 'Coaching & Development', 'Guest speakers, workshops, and curriculum for student growth.', 3),
            ('$900', 'Chapter Operations', 'Dues, chapter materials, and administrative costs.', 4),
            ('$600', 'Community Outreach', 'STEM events, mentorship programs, and school presentations.', 5),
        ]
        for amt, title, desc, order in budget:
            BudgetItem.objects.get_or_create(
                title=title,
                defaults={'amount': amt, 'description': desc, 'order': order}
            )
        self.stdout.write('  + BudgetItems: OK')

        # ── TAX CARDS ────────────────────────────────────
        tax = [
            ('501(c)(3)', 'Tax-Deductible Donation',
             'Donations are processed through Jenks Public Schools Foundation, '
             'a certified 501(c)(3) nonprofit. Your contribution is tax-deductible '
             'to the full extent permitted by law.', 0),
            ('SECTION 170', 'Corporate Deduction',
             'Corporate sponsors may deduct contributions as a business expense. '
             'Consult your tax advisor. We provide written acknowledgment of all '
             'donations upon receipt.', 1),
        ]
        for badge, title, content, order in tax:
            TaxCard.objects.get_or_create(
                title=title,
                defaults={'badge': badge, 'content': content, 'order': order}
            )
        self.stdout.write('  + TaxCards: OK')

        # ── SPONSORSHIP TIERS ────────────────────────────
        tiers_data = [
            {
                'name': 'Friend', 'slug': 'friend', 'amount': '$100+', 'amount_raw': 100,
                'color_class': 'friend', 'badge_text': '', 'badge_style': '', 'order': 0,
                'benefits': [
                    ('Name listed on chapter website', False),
                    ('Verbal recognition at chapter events', False),
                    ('Thank-you certificate', False),
                ],
            },
            {
                'name': 'Bronze', 'slug': 'bronze', 'amount': '$250+', 'amount_raw': 250,
                'color_class': 'bronze', 'badge_text': '', 'badge_style': '', 'order': 1,
                'benefits': [
                    ('All Friend benefits', False),
                    ('Logo on chapter website', True),
                    ('Social media shoutout', False),
                    ('Recognition in chapter newsletter', False),
                ],
            },
            {
                'name': 'Silver', 'slug': 'silver', 'amount': '$750+', 'amount_raw': 750,
                'color_class': 'silver', 'badge_text': 'Best Value', 'badge_style': 'value', 'order': 2,
                'benefits': [
                    ('All Bronze benefits', False),
                    ('Logo on competition banners', True),
                    ('Logo on student uniforms/apparel', True),
                    ('Featured in all press releases', False),
                    ('Dedicated social media post', False),
                ],
            },
            {
                'name': 'Gold', 'slug': 'gold', 'amount': '$2,000+', 'amount_raw': 2000,
                'color_class': 'gold', 'badge_text': '', 'badge_style': '', 'order': 3,
                'benefits': [
                    ('All Silver benefits', False),
                    ('Prime logo placement on all materials', True),
                    ('Speaking opportunity at chapter event', True),
                    ('Dedicated page on chapter website', False),
                    ('Student thank-you video', False),
                    ('Invitation to chapter banquet', False),
                ],
            },
            {
                'name': 'Presenting', 'slug': 'presenting', 'amount': '$5,000+', 'amount_raw': 5000,
                'color_class': 'platinum', 'badge_text': 'Flagship', 'badge_style': 'popular', 'order': 4,
                'benefits': [
                    ('All Gold benefits', False),
                    ('"Presented by" naming on all materials', True),
                    ('Custom partnership agreement', True),
                    ('Booth/table at chapter competitions', True),
                    ('Priority access to student talent pipeline', False),
                    ('Annual impact report', False),
                ],
            },
        ]
        for t in tiers_data:
            benefits = t.pop('benefits')
            tier, created = SponsorshipTier.objects.get_or_create(
                slug=t['slug'], defaults=t
            )
            if created:
                for i, (text, bold) in enumerate(benefits):
                    TierBenefit.objects.create(tier=tier, text=text, is_bold=bold, order=i)
        self.stdout.write('  + SponsorshipTiers: OK')

        # ── PARTNER OPTIONS ──────────────────────────────
        partners = [
            ('In-Kind Equipment',
             'Donate equipment, software licenses, or materials directly used in competitions.',
             'e.g. CAD software license, 3D printer filament, microcontrollers', 0),
            ('Mentorship & Expertise',
             'Send a professional to mentor students, judge events, or lead a workshop.',
             'e.g. Engineering firm sends a CAD specialist for a Saturday session', 1),
            ('Internship Pipeline',
             'Offer internship or job-shadow opportunities to TSA students and alumni.',
             'e.g. Summer internship for graduating TSA members entering STEM programs', 2),
            ('Venue or Facility Access',
             'Host a chapter event, mock competition, or professional development day.',
             'e.g. Corporate conference room for our annual design challenge', 3),
        ]
        for title, desc, example, order in partners:
            PartnerOption.objects.get_or_create(
                title=title,
                defaults={'description': desc, 'example': example, 'order': order}
            )
        self.stdout.write('  + PartnerOptions: OK')

        # ── REACH STATS ──────────────────────────────────
        reach = [
            ('25+', 'Active student members', 0),
            ('500+', 'Jenks community reach', 1),
            ('9', 'State podium finishes', 2),
            ('3', 'National events attended', 3),
        ]
        for num, label, order in reach:
            ReachStat.objects.get_or_create(
                label=label, defaults={'number': num, 'order': order}
            )
        self.stdout.write('  + ReachStats: OK')

        # ── CONTACT INFO ─────────────────────────────────
        contacts = [
            ('program', 'Faculty Sponsor',
             'Dr. David Lawrence\ndavid.lawrence@jenksps.org\n918-299-4415 x2312', 0),
            ('program', 'Chapter',
             'info@jenkstsa.org\nwww.jenkstsa.org\n@jenkstsa on Instagram', 1),
            ('payment', '501(c)(3) Partner',
             'Jenks Public Schools Foundation\njenksfoundation@jenksps.org\n918-299-4463', 0),
            ('payment', 'Mail Checks To',
             'P.O. Box 595, Jenks, OK 74037\nMemo: "Jenks TSA Sponsorship"', 1),
        ]
        for section, label, content, order in contacts:
            ContactInfo.objects.get_or_create(
                section=section, label=label,
                defaults={'content': content, 'order': order}
            )
        self.stdout.write('  + ContactInfo: OK')

        self.stdout.write(self.style.SUCCESS(
            '\nSeed complete. All default content is now in the database.\n'
            'Next: create a superuser with `python manage.py createsuperuser`'
        ))
