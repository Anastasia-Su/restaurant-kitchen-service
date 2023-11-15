  document.addEventListener('DOMContentLoaded', () => {
    const modal = document.querySelector('.modal');
    const openModalBtn = document.querySelector('.openModalBtn');

    openModalBtn.addEventListener('click', () => {
      modal.style.display = 'block';
      document.body.style.overflow = 'hidden';

      const backdrop = document.createElement('div');
      backdrop.classList.add('modal-backdrop', 'fade', 'show');
      document.body.appendChild(backdrop);
    });

    modal.addEventListener('click', (event) => {
      if (event.target === modal || event.target.classList.contains('close')) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';

        const backdrop = document.querySelector('.modal-backdrop');
        document.body.removeChild(backdrop);
      }
    });
  });