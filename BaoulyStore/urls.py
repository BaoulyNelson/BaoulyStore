from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),  # Utilise ton site d'administration personnalisé
    path('', include('store.urls')),  # Inclut les URLs de l'application store
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
