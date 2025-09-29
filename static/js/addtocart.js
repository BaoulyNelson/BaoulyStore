document.addEventListener("DOMContentLoaded", () => {
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Animation
            button.textContent = 'Ajouté !';
            button.style.backgroundColor = '#4CAF50';

            setTimeout(() => {
                button.textContent = 'Ajouter au panier';
                button.style.backgroundColor = '';
            }, 1500);

            // Update cart count
            const cartCount = document.querySelector('.cart-count');
            if (cartCount) {
                cartCount.textContent = parseInt(cartCount.textContent) + 1;
            }
        });
    });
});
