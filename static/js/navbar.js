// Navbar functionality
document.addEventListener('DOMContentLoaded', function() {
    // Toggle mobile menu
    const navbarToggle = document.getElementById('navbar-toggle');
    const navbarMenu = document.getElementById('navbar-menu');
    
    if (navbarToggle && navbarMenu) {
        navbarToggle.addEventListener('click', () => {
            navbarMenu.classList.toggle('active');
            navbarToggle.classList.toggle('active');
        });
    }
    
    // Shrink navbar on scroll
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
        if (navbarMenu && navbarMenu.classList.contains('active')) {
            if (!navbarMenu.contains(e.target) && !navbarToggle.contains(e.target)) {
                navbarMenu.classList.remove('active');
                navbarToggle.classList.remove('active');
            }
        }
    });
    
    // Highlight active menu item
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        
        if (linkPath === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Smooth scroll for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                // Close mobile menu if open
                if (navbarMenu && navbarMenu.classList.contains('active')) {
                    navbarMenu.classList.remove('active');
                    navbarToggle.classList.remove('active');
                }
                
                // Smooth scroll to target
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });
}); 