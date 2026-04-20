# Jenks TSA — Setup & Deployment Guide

## What you need to provide before anything works

| Item | Where to put it |
|---|---|
| `jenkstsa_logo.png` (clear background) | `static/img/jenkstsa_logo.png` |
| `.env` file (copy from `.env.example`) | project root |
| AWS credentials (for S3 + SES) | `.env` |
| Google Calendar embed code | Admin UI → Packet Content → `google_calendar_embed` |

---

## Local development

```bash
# 1. Clone / enter the project
cd jenkstsa

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy and fill in env vars
cp .env.example .env
# Edit .env — at minimum set SECRET_KEY and DEBUG=True

# 4. Run migrations
python manage.py migrate

# 5. Populate default packet content
python manage.py seed_data

# 6. Create your admin account
python manage.py createsuperuser
# → role will default to 'student'; promote to admin via Django admin:
#   /django-admin/ → Users → select user → set role to 'admin'

# 7. Start the dev server
python manage.py runserver
```

Open http://127.0.0.1:8000 — the site should work with all default content loaded.

---

## User roles

| Role | Access |
|---|---|
| `admin` | Full admin UI at `/admin-ui/`, can manage all content, messages, sponsorships |
| `sponsor` | Dashboard showing linked sponsorship commitments |
| `student` | Dashboard with links to events, rubrics, resources, forms |

To set a user's role: Django Admin (`/django-admin/`) → Accounts → Users → change `role` field.

---

## Making someone an admin (after createsuperuser)

```
/django-admin/ → Accounts → Users → [your user] → Role: Web Admin → Save
```

They can then access `/admin-ui/` — the custom admin panel.

---

## Deploying to Vercel

### Prerequisites
- Vercel CLI: `npm i -g vercel`
- A Vercel account connected to your repo

### Steps

```bash
# Log in
vercel login

# First deploy (follow prompts)
vercel

# Set environment variables in Vercel dashboard:
# Project → Settings → Environment Variables
# Add every variable from .env (except DEBUG — set that to False)
```

Key Vercel environment variables to set:
```
SECRET_KEY          → your generated secret key
DEBUG               → False
DB_PASSWORD         → npg_zOaZG0ixpyl6
USE_S3              → True
AWS_ACCESS_KEY_ID   → your key
AWS_SECRET_ACCESS_KEY → your secret
AWS_STORAGE_BUCKET_NAME → jenkstsa-media
EMAIL_BACKEND       → django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER     → your SES SMTP user
EMAIL_HOST_PASSWORD → your SES SMTP password
CSRF_TRUSTED_ORIGINS → https://your-project.vercel.app,https://jenkstsa.org
SPONSORSHIP_NOTIFICATION_EMAILS → info@jenkstsa.org,...
```

### After first deploy — run migrations

Vercel doesn't run management commands automatically. Run them once via:

```bash
# Using Vercel CLI to exec on the deployed instance:
vercel run python manage.py migrate
vercel run python manage.py seed_data
```

Or connect to your Neon database directly and run commands locally pointing at the production DB.

---

## AWS S3 setup (for media files — logos, blog images, etc.)

1. Create an S3 bucket named `jenkstsa-media` in `us-east-1`
2. Set bucket policy to allow public read (for images)
3. Create an IAM user with `AmazonS3FullAccess` policy
4. Copy the access key and secret to `.env` / Vercel env vars
5. Set `USE_S3=True`

---

## AWS SES setup (for emails)

1. Verify your sending domain (`jenkstsa.org`) in SES
2. Request production access (out of sandbox) from AWS
3. Go to SES → SMTP Settings → Create SMTP credentials
4. Copy `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` to env vars
5. Set `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`

---

## Key URLs

| URL | What it is |
|---|---|
| `/` | Homepage |
| `/packet/` | Sponsorship packet |
| `/packet/commit/` | Commitment form (redirects to packet) |
| `/packet/status/` | Status lookup |
| `/packet/confirmation/<num>/` | Confirmation page |
| `/packet/progress/<num>/` | Progress page |
| `/events/rubrics/` | **Only page with no login required** |
| `/accounts/login/` | Sign in |
| `/accounts/signup/` | Create account |
| `/accounts/dashboard/` | User dashboard |
| `/admin-ui/` | Custom admin panel (admin role required) |
| `/django-admin/` | Django admin (superuser required) |

---

## Adding dynamic content

Everything on the packet page is editable through the admin UI without redeploying:

1. Sign in as an admin
2. Go to `/admin-ui/content/`
3. Edit any text field and click Save — changes are live instantly

For structured data (tiers, budget items, podium finishes), use the links to Django Admin from the content editor page.

---

## Turning on "Current Sponsors" section

In Admin UI → Packet Content → find key `show_current_sponsors` → set value to `true`

Then add sponsors via Django Admin → Packet → Current Sponsors.
