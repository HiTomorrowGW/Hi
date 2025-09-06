// JavaScript for future interactive features

document.addEventListener('DOMContentLoaded', function() {
    let navbarPath = 'includes/navbar.html';
    let isRoomDetailPage = window.location.pathname.includes('/rooms/');

    if (isRoomDetailPage) {
        navbarPath = '../includes/navbar.html';
    }

    fetch(navbarPath)
        .then(response => response.text())
        .then(data => {
            const navbarPlaceholder = document.getElementById('navbar-placeholder');
            navbarPlaceholder.innerHTML = data;

            // Adjust hrefs if on a room detail page
            if (isRoomDetailPage) {
                const navLinks = navbarPlaceholder.querySelectorAll('a');
                navLinks.forEach(link => {
                    let href = link.getAttribute('href');
                    if (href && !href.startsWith('http') && !href.startsWith('#') && !href.startsWith('../')) {
                        // Prepend '../' to relative links that are not already adjusted
                        link.setAttribute('href', '../' + href);
                    }
                });
            }
        })
        .catch(error => console.error('Error loading navbar:', error));

    // Load footer
    fetch('includes/footer.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('footer-placeholder').innerHTML = data;
        })
        .catch(error => console.error('Error loading footer:', error));
});