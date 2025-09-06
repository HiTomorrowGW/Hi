// JavaScript for future interactive features

document.addEventListener('DOMContentLoaded', function() {
    let headerPath = 'includes/header.html';
    let footerPath = 'includes/footer.html';

    const currentPath = window.location.pathname;
    if (currentPath.includes('/rooms/') || currentPath.endsWith('/rooms.html') || currentPath.endsWith('/room.html')) {
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
});