// Obtenir l'année actuelle
const currentYear = new Date().getFullYear();

// Insérer l'année dans l'élément avec l'ID "currentYear"
document.getElementById('currentYear').textContent = currentYear;


// Fonction pour afficher ou masquer la flèche selon le défilement
window.onscroll = function() {
    var backToTopButton = document.querySelector('.back-to-top');
    
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        backToTopButton.classList.add('show');
    } else {
        backToTopButton.classList.remove('show');
    }
};

// Fonction pour faire défiler la page vers le haut
document.querySelector('.back-to-top').addEventListener('click', function(e) {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
});
