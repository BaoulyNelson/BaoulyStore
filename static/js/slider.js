document.addEventListener("DOMContentLoaded", () => {
  const dots = document.querySelectorAll('.dot');
  const slides = document.querySelectorAll('.testimonial-slide');

  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      dots.forEach(d => d.classList.remove('active'));
      slides.forEach(s => s.classList.remove('active'));

      dot.classList.add('active');
      slides[index].classList.add('active');
    });
  });
});
