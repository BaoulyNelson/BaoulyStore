"""
Static informational page views — contact, FAQ, blog, policies, etc.
"""
import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import ContactForm

logger = logging.getLogger(__name__)


def contact_view(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        body = form.cleaned_data['message']
        try:
            send_mail(
                subject=f"[BaoulyStore] Nouveau message de {name}",
                message=f"De : {name} <{email}>\n\n{body}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            messages.success(request, "Votre message a bien été envoyé. Nous vous répondrons rapidement !")
            return redirect('pages:contact_success')
        except Exception as exc:
            logger.error("Failed to send contact email: %s", exc, exc_info=True)
            messages.error(request, "Une erreur est survenue lors de l'envoi. Veuillez réessayer.")

    return render(request, 'pages/contact.html', {'form': form})


def contact_success_view(request):
    return render(request, 'pages/contact_success.html')


def promotions(request):
    return render(request, 'pages/promotions.html')


def blog(request):
    return render(request, 'pages/blog.html')


def faq(request):
    return render(request, 'pages/faq.html')


def return_policy(request):
    return render(request, 'pages/return_policy.html')


def order_tracking(request):
    return render(request, 'pages/order_tracking.html')


def about(request):
    return render(request, 'pages/about.html')
