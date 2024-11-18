const slides = document.querySelectorAll('.slide');
const controls = document.querySelectorAll('.control');
let currentSlide = 0;
let interval = setInterval(() => {
  slides[currentSlide].classList.remove('active');
  controls[currentSlide].classList.remove('active');
  currentSlide = (currentSlide + 1) % slides.length;
  slides[currentSlide].classList.add('active');
  controls[currentSlide].classList.add('active');
}, 3000);
