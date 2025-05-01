from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('store.urls')),
]

# Ces lignes doivent être dé-indentées
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.BASE_DIR / 'media')
