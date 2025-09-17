// JavaScript for future interactive features

document.addEventListener('DOMContentLoaded', function() {
    // Handle image modal
    const imageModal = document.getElementById('imageModal');
    if (imageModal) {
        imageModal.addEventListener('show.bs.modal', function (event) {
            // Button that triggered the modal
            const openerLink = event.relatedTarget;
            // Extract info from data-bs-whatever attributes
            const largeSrc = openerLink.getAttribute('data-large-src');
            const altText = openerLink.querySelector('img').alt;

            // Update the modal's content.
            const modalImage = imageModal.querySelector('#modalImage');
            const modalTitle = imageModal.querySelector('.modal-title');

            modalImage.src = largeSrc;
            modalImage.alt = altText;
            modalTitle.textContent = altText; // Set modal title to alt text of the image
        });
    }
});