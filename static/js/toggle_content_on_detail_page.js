function toggleContent(targetId) {
    const targetElement = document.getElementById(targetId);
    targetElement.style.display = targetElement.style.display === 'none' || targetElement.style.display === ''
        ? 'block'
        : 'none';
    }


const toggleLink = document.querySelector('.toggle-link');
const targetId = toggleLink.getAttribute('data-target');
toggleLink.addEventListener('click', (event) => {
  event.preventDefault();
  event.stopPropagation();
  toggleContent(targetId);

});
