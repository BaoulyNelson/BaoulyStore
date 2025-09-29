document.addEventListener("DOMContentLoaded", () => {
    const testimonialSlides = document.getElementById('testimonialSlides');
    const testimonialDots = document.querySelectorAll('.testimonial-dot');
    let currentSlide = 0;

    function showSlide(index) {
        if (testimonialSlides) {
            testimonialSlides.style.transform = `translateX(-${index * 100}%)`;
        }
        testimonialDots.forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
        });
        currentSlide = index;
    }

    testimonialDots.forEach((dot, index) => {
        dot.addEventListener('click', () => showSlide(index));
    });

    setInterval(() => {
        if (testimonialDots.length > 0) {
            currentSlide = (currentSlide + 1) % testimonialDots.length;
            showSlide(currentSlide);
        }
    }, 5000);
});
