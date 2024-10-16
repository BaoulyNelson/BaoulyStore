$(document).ready(function() {
    $('.add-to-cart-form').submit(function(e) {
        e.preventDefault(); // Empêche l'envoi du formulaire par défaut

        var form = $(this);
        var url = form.attr('action');
        var csrfToken = form.find('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            url: url,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                if (response.status === 'not_logged_in') {
                    // Affiche le modal si l'utilisateur n'est pas connecté
                    $('#customLoginModal').css('display', 'flex');
                } else if (response.status === 'success') {
                    // Redirige vers le panier si l'utilisateur est connecté et que le produit est ajouté
                    window.location.href = '/panier/';
                }
            }
        });
    });

    $('#okButton').click(function() {
        window.location.href = '/login/'; // Redirection vers la page de connexion
    });
});
