from django.contrib import admin
from .models import Commentaire

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('nom', 'role', 'date', 'apercu_texte')
    search_fields = ('nom', 'texte', 'role')
    list_filter = ('role', 'date')
    ordering = ('-date',)

    @admin.display(description='Aperçu')
    def apercu_texte(self, obj):
        return obj.texte[:60] + ('…' if len(obj.texte) > 60 else '')
