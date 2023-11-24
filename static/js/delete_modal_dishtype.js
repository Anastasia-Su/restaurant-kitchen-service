const openModalBtns = document.querySelectorAll('.openModalBtn');

openModalBtns.forEach(openModalBtn => {
    openModalBtn.addEventListener('click', (event) => {
        const dishtypeId = event.currentTarget.getAttribute('data-dishtype-id');
        const modal = document.getElementById(`deleteModal${dishtypeId}`);

        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';

        const backdrop = document.createElement('div');
        backdrop.classList.add('modal-backdrop', 'fade', 'show');
        document.body.appendChild(backdrop);

        modal.addEventListener('click', (event) => {
          if (event.target === modal || event.target.classList.contains('close')) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';

            const backdrop = document.querySelector('.modal-backdrop');
            document.body.removeChild(backdrop);
          }
        });
    });
});
