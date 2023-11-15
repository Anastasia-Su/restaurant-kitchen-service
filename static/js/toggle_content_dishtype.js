function toggleContent(targetId) {
    const targetElement = document.getElementById(targetId);
    const allElems = document.querySelectorAll('.dishtypes-content');
    allElems.forEach(elem => {
        if (elem.id !== targetId) {
            elem.style.display = 'none';
        }
    });
    targetElement.style.display = targetElement.style.display === 'none' || targetElement.style.display === ''
        ? 'block'
        : 'none';
}

const toggleLinks = document.querySelectorAll('.toggle-link');
toggleLinks.forEach(toggleLink => {
    toggleLink.addEventListener('click', (event) => {
        event.preventDefault();
        const targetId = toggleLink.getAttribute('data-target');
        toggleContent(targetId);
    });
});
