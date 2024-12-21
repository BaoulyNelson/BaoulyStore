function openPanel() {
    // Ouvre le panneau
    document.getElementById("sidePanel").style.width = "100%";

    // Sélectionne les liens de la navigation principale
    const navLinks = document.querySelectorAll('.nav-links a');

    // Sélectionne le panneau latéral
    const sidePanel = document.getElementById("sidePanel");

    // Supprime tous les anciens liens (pour éviter la duplication)
    const oldLinks = sidePanel.querySelectorAll('a:not(.close-btn)');
    oldLinks.forEach(link => link.remove());

    // Copie chaque lien dans le panneau latéral
    navLinks.forEach(link => {
        const newLink = link.cloneNode(true); // Clone le lien
        sidePanel.appendChild(newLink); // Ajoute le lien cloné dans le panneau
    });
}



function closePanel() {
    document.getElementById("sidePanel").style.width = "0";
}





