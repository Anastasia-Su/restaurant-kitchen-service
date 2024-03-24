const menu = document.querySelector('.nav-pills'),
  menuItem = document.querySelectorAll('.nav-item'),
  hamburger = document.querySelector('.hamburger');

  hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('hamburger_active');
      menu.classList.toggle('nav-pills_active');
  });

  menuItem.forEach(item => {
    item.addEventListener('click', () => {
        hamburger.classList.toggle('hamburger_active');
        menu.classList.toggle('nav-pills_active');
    });
});
