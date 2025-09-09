// JavaScript for future interactive features

document.addEventListener('DOMContentLoaded', function() {
    let headerPath = 'includes/header.html';
    let footerPath = 'includes/footer.html';

    const currentPath = window.location.pathname;
    if (currentPath.includes('/rooms/') || currentPath.endsWith('/rooms.html') || currentPath.endsWith('/room.html') || currentPath.endsWith('/contact.html')) {
        headerPath = '../includes/header.html';
        footerPath = '../includes/footer.html';
    }

    fetch(headerPath)
        .then(response => response.text())
        .then(data => {
            const headerPlaceholder = document.getElementById('header-placeholder');
            headerPlaceholder.innerHTML = data;
        })
        .catch(error => console.error('Error loading header:', error));

    // Load footer
    fetch(footerPath)
        .then(response => response.text())
        .then(data => {
            document.getElementById('footer-placeholder').innerHTML = data;
        })
        .catch(error => console.error('Error loading footer:', error));

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