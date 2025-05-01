 // Mobile Menu Toggle
 const mobileToggle = document.getElementById('mobileToggle');
 const navLinks = document.getElementById('navLinks');
 const closeMenu = document.getElementById('closeMenu');

 mobileToggle.addEventListener('click', () => {
     navLinks.classList.add('show');
 });

 closeMenu.addEventListener('click', () => {
     navLinks.classList.remove('show');
 });

 // Back to Top Button
 const backToTopBtn = document.getElementById('backToTop');

 window.addEventListener('scroll', () => {
     if (window.pageYOffset > 300) {
         backToTopBtn.classList.add('show');
     } else {
         backToTopBtn.classList.remove('show');
     }
 });

 backToTopBtn.addEventListener('click', (e) => {
     e.preventDefault();
     window.scrollTo({ top: 0, behavior: 'smooth' });
 });

 // Product Filter
 const filterBtns = document.querySelectorAll('.filter-btn');

 filterBtns.forEach(btn => {
     btn.addEventListener('click', () => {
         filterBtns.forEach(b => b.classList.remove('active'));
         btn.classList.add('active');
         // Here you would add logic to filter products
     });
 });

 const dots = document.querySelectorAll('.dot');
const slides = document.querySelectorAll('.testimonial-slide');

dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
        // Retirer la classe active de tous les dots et slides
        dots.forEach(d => d.classList.remove('active'));
        slides.forEach(s => s.classList.remove('active'));

        // Ajouter la classe active au dot et à la slide cliquée
        dot.classList.add('active');
        slides[index].classList.add('active');
    });
});
