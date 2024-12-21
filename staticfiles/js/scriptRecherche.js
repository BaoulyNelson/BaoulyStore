function openSearch() {
    var searchForm = document.getElementById('searchForm');
    var searchInput = searchForm.querySelector('input[type="text"]');

    // Vérifiez si le formulaire est actuellement masqué
    if (searchForm.style.display === 'none') {
        searchForm.style.display = 'block'; // Affiche le formulaire
        searchInput.focus(); // Met le focus sur le champ de recherche
    } else {
        searchForm.style.display = 'none'; // Masque le formulaire
    }
}
