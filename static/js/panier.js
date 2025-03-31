  // Fonction pour envoyer une requête AJAX lorsque le bouton "Ajouter au panier" est cliqué
  document.querySelectorAll('.add-to-cart-form').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault(); // Empêcher le formulaire de se soumettre normalement

        let url = form.action; // L'URL de la vue d'ajout au panier

        fetch(url, {
            method: 'POST',
            body: new FormData(form),
            headers: {
                'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            // Mettre à jour le compteur du panier en temps réel pour l'OffCanvas
            document.getElementById('panier-count').textContent = `(${data.panier_count})`;

            // Mettre à jour le compteur du panier dans la barre de navigation
            const navPanierCount = document.querySelector('a[href="{% url "afficher_panier" %}"]');
            if (data.panier_count > 0) {
                // Si panier_count est positif, on affiche le nombre d'articles
                navPanierCount.innerHTML = `🛒Panier (${data.panier_count})`;
            } else {
                // Sinon, on garde l'affichage standard
                navPanierCount.innerHTML = `🛒Panier`;
            }
        })
        .catch(error => console.error('Erreur lors de l\'ajout au panier:', error));
    });
});