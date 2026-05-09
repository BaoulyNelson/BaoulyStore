from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize default admin site header
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE

urlpatterns = [
    path('admin/', admin.site.urls),

    # Public catalogue (homepage + products)
    path('', include('apps.catalogue.urls', namespace='catalogue')),

    # Shopping cart
    path('panier/', include('apps.cart.urls', namespace='cart')),

    # Customer reviews / testimonials
    path('commentaires/', include('apps.reviews.urls', namespace='reviews')),

    # Authentication (login, signup, profile, password reset)
    path('', include('apps.accounts.urls', namespace='accounts')),

    # Static informational pages (FAQ, blog, contact, …)
    path('', include('apps.pages.urls', namespace='pages')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
