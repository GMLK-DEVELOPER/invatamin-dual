/**
 * Digital Agency Admin Panel - Main JS
 * Core functionality for the admin panel
 */

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initTooltips();
    
    // Initialize popovers
    initPopovers();
    
    // Initialize custom dropdowns
    initCustomDropdowns();
    
    // Initialize sidebar toggle
    initSidebarToggle();
    
    // Initialize theme switcher
    initThemeSwitcher();
    
    // Initialize notification system
    initNotifications();
    
    // Handle form submissions
    handleForms();
    
    // Setup ajax functionality
    setupAjax();
});

/**
 * Initialize Bootstrap tooltips
 */
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => {
        new bootstrap.Tooltip(tooltip);
    });
}

/**
 * Initialize Bootstrap popovers
 */
function initPopovers() {
    const popovers = document.querySelectorAll('[data-bs-toggle="popover"]');
    popovers.forEach(popover => {
        new bootstrap.Popover(popover);
    });
}

/**
 * Initialize custom dropdowns
 */
function initCustomDropdowns() {
    const dropdowns = document.querySelectorAll('.custom-dropdown');
    
    dropdowns.forEach(dropdown => {
        const trigger = dropdown.querySelector('.dropdown-trigger');
        const menu = dropdown.querySelector('.dropdown-menu');
        
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const isActive = menu.classList.contains('show');
            
            // Close all open dropdowns
            document.querySelectorAll('.custom-dropdown .dropdown-menu.show').forEach(el => {
                if (el !== menu) {
                    el.classList.remove('show');
                }
            });
            
            // Toggle current dropdown
            menu.classList.toggle('show');
            
            // Add click outside listener only when opening
            if (!isActive) {
                setTimeout(() => {
                    document.addEventListener('click', closeDropdown);
                }, 10);
            } else {
                document.removeEventListener('click', closeDropdown);
            }
        });
        
        function closeDropdown(e) {
            if (!dropdown.contains(e.target)) {
                menu.classList.remove('show');
                document.removeEventListener('click', closeDropdown);
            }
        }
    });
}

/**
 * Initialize sidebar toggle functionality
 */
function initSidebarToggle() {
    const toggle = document.getElementById('sidebarToggle');
    const closeBtn = document.getElementById('sidebarClose');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    
    if (toggle && sidebar) {
        toggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
            document.body.classList.toggle('sidebar-collapsed');
            
            // Store user preference
            const isCollapsed = sidebar.classList.contains('collapsed');
            localStorage.setItem('sidebar-collapsed', isCollapsed);
        });
    }
    
    if (closeBtn && sidebar) {
        closeBtn.addEventListener('click', function() {
            sidebar.classList.add('collapsed');
            document.body.classList.add('sidebar-collapsed');
            localStorage.setItem('sidebar-collapsed', true);
        });
    }
    
    // Mobile sidebar
    const mobileToggle = document.getElementById('mobileSidebarToggle');
    
    if (mobileToggle && sidebar && overlay) {
        mobileToggle.addEventListener('click', function() {
            sidebar.classList.add('show');
            overlay.classList.add('show');
            document.body.classList.add('sidebar-mobile-open');
        });
        
        overlay.addEventListener('click', function() {
            sidebar.classList.remove('show');
            overlay.classList.remove('show');
            document.body.classList.remove('sidebar-mobile-open');
        });
    }
    
    // Restore user preference
    const savedState = localStorage.getItem('sidebar-collapsed');
    if (savedState === 'true' && sidebar) {
        sidebar.classList.add('collapsed');
        document.body.classList.add('sidebar-collapsed');
    }
}

/**
 * Initialize theme switcher (light/dark mode)
 */
function initThemeSwitcher() {
    const themeSwitch = document.getElementById('themeSwitch');
    const html = document.documentElement;
    
    if (themeSwitch) {
        themeSwitch.addEventListener('click', function() {
            const currentTheme = html.getAttribute('data-bs-theme') || 'light';
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            html.setAttribute('data-bs-theme', newTheme);
            document.body.classList.toggle('dark-mode');
            
            // Store user preference
            localStorage.setItem('theme', newTheme);
            
            // Update switch icon
            const icon = themeSwitch.querySelector('i');
            if (icon) {
                icon.className = newTheme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
            }
            
            // Show notification
            showNotification(`Theme changed to ${newTheme} mode`, 'info');
        });
        
        // Restore user preference
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            html.setAttribute('data-bs-theme', savedTheme);
            
            if (savedTheme === 'dark') {
                document.body.classList.add('dark-mode');
                
                // Update switch icon
                const icon = themeSwitch.querySelector('i');
                if (icon) {
                    icon.className = 'fas fa-sun';
                }
            }
        }
    }
}

/**
 * Initialize notification system
 */
function initNotifications() {
    // Create notification container if not exists
    let container = document.getElementById('notificationContainer');
    
    if (!container) {
        container = document.createElement('div');
        container.id = 'notificationContainer';
        container.className = 'notification-container';
        document.body.appendChild(container);
    }
    
    // Check for notifications in flash messages
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(flash => {
        const message = flash.textContent.trim();
        const type = flash.getAttribute('data-type') || 'info';
        
        if (message) {
            showNotification(message, type);
        }
        
        flash.remove();
    });
}

/**
 * Handle form submissions
 */
function handleForms() {
    const forms = document.querySelectorAll('form:not([data-no-ajax])');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const isAjax = form.getAttribute('data-ajax') === 'true';
            
            if (!isAjax) return;
            
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(form);
            const submitBtn = form.querySelector('[type="submit"]');
            
            // Disable submit button
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.classList.add('loading');
                
                // Store original text
                submitBtn.dataset.originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            }
            
            // Send form data via AJAX
            fetch(form.action, {
                method: form.method,
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                // Show notification
                if (data.message) {
                    showNotification(data.message, data.status || 'success');
                }
                
                // Handle redirect
                if (data.redirect) {
                    setTimeout(() => {
                        window.location.href = data.redirect;
                    }, 1000);
                }
                
                // Reset form on success
                if (data.status === 'success' && !data.redirect) {
                    form.reset();
                }
            })
            .catch(error => {
                showNotification('An error occurred. Please try again.', 'error');
                console.error('Form submission error:', error);
            })
            .finally(() => {
                // Re-enable submit button
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.classList.remove('loading');
                    submitBtn.innerHTML = submitBtn.dataset.originalText;
                }
            });
        });
    });
}

/**
 * Setup AJAX functionality
 */
function setupAjax() {
    // Handle data-ajax-url elements
    document.addEventListener('click', function(e) {
        const element = e.target.closest('[data-ajax-url]');
        
        if (!element) return;
        
        e.preventDefault();
        
        const url = element.getAttribute('data-ajax-url');
        const method = element.getAttribute('data-method') || 'GET';
        const confirm = element.getAttribute('data-confirm');
        
        // Handle confirmation if required
        if (confirm && !window.confirm(confirm)) {
            return;
        }
        
        // Show loading state
        element.classList.add('loading');
        const originalHtml = element.innerHTML;
        element.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        
        // Make AJAX request
        fetch(url, {
            method: method,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            // Show notification
            if (data.message) {
                showNotification(data.message, data.status || 'success');
            }
            
            // Handle redirect
            if (data.redirect) {
                window.location.href = data.redirect;
            }
            
            // Handle element update
            if (data.update) {
                Object.keys(data.update).forEach(selector => {
                    const target = document.querySelector(selector);
                    if (target) {
                        target.innerHTML = data.update[selector];
                    }
                });
            }
            
            // Handle callback
            if (element.hasAttribute('data-callback')) {
                const callback = element.getAttribute('data-callback');
                if (typeof window[callback] === 'function') {
                    window[callback](data, element);
                }
            }
        })
        .catch(error => {
            showNotification('An error occurred. Please try again.', 'error');
            console.error('AJAX request error:', error);
        })
        .finally(() => {
            // Restore element
            element.classList.remove('loading');
            element.innerHTML = originalHtml;
        });
    });
}

/**
 * Show a notification message
 * @param {string} message - The notification message
 * @param {string} type - The notification type (success, error, warning, info)
 * @param {number} duration - Duration in milliseconds to show the notification
 */
function showNotification(message, type = 'info', duration = 5000) {
    const container = document.getElementById('notificationContainer');
    
    if (!container) return;
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    
    // Create icon based on type
    let icon = 'info-circle';
    if (type === 'success') icon = 'check-circle';
    if (type === 'error') icon = 'times-circle';
    if (type === 'warning') icon = 'exclamation-triangle';
    
    // Build notification content
    notification.innerHTML = `
        <div class="notification-icon">
            <i class="fas fa-${icon}"></i>
        </div>
        <div class="notification-content">
            <div class="notification-message">${message}</div>
        </div>
        <div class="notification-close">
            <i class="fas fa-times"></i>
        </div>
    `;
    
    // Add to container
    container.appendChild(notification);
    
    // Add shown class after a small delay (for animation)
    setTimeout(() => {
        notification.classList.add('shown');
    }, 10);
    
    // Setup close button
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        closeNotification(notification);
    });
    
    // Auto remove after duration
    if (duration > 0) {
        setTimeout(() => {
            closeNotification(notification);
        }, duration);
    }
}

/**
 * Close a notification with animation
 * @param {Element} notification - The notification element to close
 */
function closeNotification(notification) {
    notification.classList.remove('shown');
    
    // Remove from DOM after animation completes
    notification.addEventListener('transitionend', function() {
        notification.remove();
    }, { once: true });
} 