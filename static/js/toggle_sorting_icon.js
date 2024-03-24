const headerLinks = document.querySelectorAll('.header-link');
const iToggles = document.querySelectorAll('.i-toggle');

const urlParams = new URLSearchParams(window.location.search);
const sortParam = urlParams.get('sort_by');
if (sortParam) {
    headerLinks.forEach((headerLink, index) => {
        const currentIToggle = iToggles[index];
        const linkSortParam = headerLink.getAttribute('href').split('=')[1];
        currentIToggle.style.display = linkSortParam === sortParam ? 'inline' : 'none';
    });
}
