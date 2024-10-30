// Add this script to handle horizontal scrolling
document.addEventListener('DOMContentLoaded', function () {
  const container = document.querySelector('.posts-scroll-container');
  const scrollLeftBtn = document.querySelector('.scroll-left');
  const scrollRightBtn = document.querySelector('.scroll-right');

  if (container && scrollLeftBtn && scrollRightBtn) {
    const scrollAmount = 300; // Adjust based on card width

    scrollLeftBtn.addEventListener('click', () => {
      container.scrollBy({
        left: -scrollAmount,
        behavior: 'smooth'
      });
    });

    scrollRightBtn.addEventListener('click', () => {
      container.scrollBy({
        left: scrollAmount,
        behavior: 'smooth'
      });
    });
  }
});