from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from users.views import CustomPasswordChangeView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/password/change/', CustomPasswordChangeView.as_view()),
    path('accounts/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('groups/', include('groups.urls')),
    path('subjects/', include('subjects.urls')),
    path('calendar/', include('calendars.urls')),

    path('', include('pages.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
