from django.db import models


class Commentaire(models.Model):
    """Customer testimonial / review displayed on the homepage."""

    nom = models.CharField(max_length=100, verbose_name='Nom')
    photo = models.ImageField(
        upload_to='commentaires_photos/',
        blank=True,
        null=True,
        verbose_name='Photo',
    )
    texte = models.TextField(verbose_name='Commentaire')
    role = models.CharField(max_length=100, default='Client', verbose_name='Rôle')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date')

    class Meta:
        verbose_name = 'Commentaire'
        verbose_name_plural = 'Commentaires'
        ordering = ['-date']

    def __str__(self) -> str:
        return f"{self.nom} — {self.texte[:40]}…"
