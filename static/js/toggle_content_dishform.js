function toggleContent(targetId) {
    const targetElement = document.getElementById(targetId);
    targetElement.style.display = targetElement.style.display === 'none' || targetElement.style.display === ''
        ? 'block'
        : 'none';
    const labelIngred = document.querySelector('.field-lbl');
    labelIngred.style.display = targetElement.style.display === 'block' ? 'none' : 'block';
  }

    const toggleLink = document.querySelector('.toggle-link');
    const fieldLink = document.querySelector('.field-link');
    const targetId = toggleLink.getAttribute('data-target');

    toggleLink.addEventListener('click', (event) => {
      event.preventDefault();
      toggleContent(targetId);
    });
    fieldLink.addEventListener('click', (event) => {
      event.preventDefault();
      toggleContent(targetId);
    });
