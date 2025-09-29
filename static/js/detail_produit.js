// Animation d'entrée
    document.addEventListener('DOMContentLoaded', function() {
        const elements = document.querySelectorAll('.product-info > *');
        elements.forEach((el, index) => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            setTimeout(() => {
                el.style.transition = 'all 0.6s ease';
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }, index * 100);
        });
    });

    // Gestion du zoom sur l'image
    const productImage = document.querySelector('.product-image');
    if (productImage) {
        productImage.addEventListener('click', function() {
            if (this.style.transform === 'scale(1.5)') {
                this.style.transform = 'scale(1)';
                this.style.cursor = 'zoom-in';
            } else {
                this.style.transform = 'scale(1.5)';
                this.style.cursor = 'zoom-out';
            }
        });
    }

    // Gestion des boutons
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            // Animation de clic
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });