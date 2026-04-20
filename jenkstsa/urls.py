from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('events/', include('apps.events.urls')),
    path('newsroom/', include('apps.newsroom.urls')),
    path('packet/', include('apps.packet.urls')),
    path('messages/', include('apps.messaging.urls')),
    path('admin-ui/', include('apps.core.admin_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
