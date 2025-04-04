/**
 * Digital Agency Admin Panel - Dashboard JS
 * Dashboard specific javascript functionalities
 */

// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize statistics counters with animation
    initCounters();
    
    // Initialize dashboard charts if they exist
    initCharts();
    
    // Initialize datepickers
    initDatepickers();
    
    // Initialize sortable elements
    initSortables();
    
    // Setup dashboard quick actions
    setupQuickActions();
    
    // Animation for counters
    const counters = document.querySelectorAll('.counter');
    
    counters.forEach(counter => {
        const target = parseInt(counter.innerText);
        const count = 0;
        const increment = target / 20;
        
        function updateCount() {
            const currentCount = Math.ceil(parseInt(counter.innerText) || 0);
            
            if (currentCount < target) {
                counter.innerText = Math.ceil(currentCount + increment);
                setTimeout(updateCount, 50);
            } else {
                counter.innerText = target;
            }
        }
        
        updateCount();
    });
    
    // Initialize tooltips if Bootstrap JS is available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(tooltipTriggerEl => {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Current date and time in the footer
    const currentTimeElement = document.getElementById('current-time');
    if (currentTimeElement) {
        function updateTime() {
            const now = new Date();
            const options = { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            };
            currentTimeElement.textContent = now.toLocaleDateString('ru-RU', options);
        }
        
        updateTime();
        setInterval(updateTime, 1000);
    }
});

/**
 * Initialize statistics counters with animation
 */
function initCounters() {
    const counters = document.querySelectorAll('[data-counter]');
    
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-counter'), 10);
        const duration = parseInt(counter.getAttribute('data-duration') || '2000', 10);
        const decimal = counter.getAttribute('data-decimal') === 'true';
        const decimals = parseInt(counter.getAttribute('data-decimals') || '2', 10);
        const prefix = counter.getAttribute('data-prefix') || '';
        const suffix = counter.getAttribute('data-suffix') || '';
        
        let startTime;
        let currentValue = 0;
        
        function updateCounter(timestamp) {
            if (!startTime) startTime = timestamp;
            
            const progress = Math.min((timestamp - startTime) / duration, 1);
            currentValue = progress * target;
            
            if (decimal) {
                counter.textContent = prefix + currentValue.toFixed(decimals) + suffix;
            } else {
                counter.textContent = prefix + Math.floor(currentValue) + suffix;
            }
            
            if (progress < 1) {
                window.requestAnimationFrame(updateCounter);
            }
        }
        
        window.requestAnimationFrame(updateCounter);
    });
}

/**
 * Initialize dashboard charts
 */
function initCharts() {
    // Area Chart - Website Traffic
    const trafficCanvas = document.getElementById('websiteTrafficChart');
    if (trafficCanvas) {
        const trafficCtx = trafficCanvas.getContext('2d');
        
        // Get color theme
        const isDarkMode = document.body.classList.contains('dark-mode');
        const gridColor = isDarkMode ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)';
        const textColor = isDarkMode ? 'rgba(255, 255, 255, 0.7)' : 'rgba(0, 0, 0, 0.7)';
        
        // Sample data for last 30 days
        const labels = Array.from({length: 30}, (_, i) => i + 1);
        const visitorsData = [
            1500, 1600, 1550, 1800, 1950, 2000, 1900, 
            2100, 2200, 2150, 2300, 2400, 2300, 2400, 
            2550, 2500, 2700, 2750, 2800, 2700, 2900, 
            3000, 2950, 3100, 3200, 3150, 3300, 3350, 3400, 3450
        ];
        const pageviewsData = [
            3800, 4000, 3900, 4200, 4500, 4600, 4400, 
            4700, 4900, 4800, 5100, 5400, 5200, 5500, 
            5700, 5600, 6000, 6100, 6200, 6000, 6300, 
            6500, 6400, 6700, 6900, 6800, 7100, 7200, 7300, 7500
        ];
        
        new Chart(trafficCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Visitors',
                        data: visitorsData,
                        borderColor: '#0d6efd',
                        backgroundColor: 'rgba(13, 110, 253, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4,
                        pointBackgroundColor: '#0d6efd',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 0,
                        pointHoverRadius: 6
                    },
                    {
                        label: 'Page Views',
                        data: pageviewsData,
                        borderColor: '#198754',
                        backgroundColor: 'rgba(25, 135, 84, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4,
                        pointBackgroundColor: '#198754',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 0,
                        pointHoverRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            boxWidth: 8,
                            color: textColor
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: isDarkMode ? 'rgba(0, 0, 0, 0.8)' : 'rgba(255, 255, 255, 0.8)',
                        titleColor: isDarkMode ? '#fff' : '#000',
                        bodyColor: isDarkMode ? '#fff' : '#000',
                        titleFont: {
                            size: 14,
                            weight: 'bold'
                        },
                        bodyFont: {
                            size: 13
                        },
                        padding: 12,
                        boxWidth: 10,
                        usePointStyle: true,
                        caretSize: 6,
                        cornerRadius: 6
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: textColor,
                            maxRotation: 0,
                            autoSkip: true,
                            maxTicksLimit: 10
                        }
                    },
                    y: {
                        grid: {
                            color: gridColor,
                            borderDash: [5, 5]
                        },
                        ticks: {
                            color: textColor
                        }
                    }
                },
                interaction: {
                    mode: 'nearest',
                    axis: 'x',
                    intersect: false
                },
                elements: {
                    line: {
                        borderJoinStyle: 'round'
                    }
                }
            }
        });
    }
    
    // Pie Chart - Traffic Sources
    const sourcesCanvas = document.getElementById('trafficSourcesChart');
    if (sourcesCanvas) {
        const sourcesCtx = sourcesCanvas.getContext('2d');
        
        // Get color theme
        const isDarkMode = document.body.classList.contains('dark-mode');
        const textColor = isDarkMode ? 'rgba(255, 255, 255, 0.7)' : 'rgba(0, 0, 0, 0.7)';
        
        new Chart(sourcesCtx, {
            type: 'doughnut',
            data: {
                labels: ['Organic Search', 'Direct', 'Social Media', 'Referrals', 'Email'],
                datasets: [{
                    data: [45, 25, 15, 10, 5],
                    backgroundColor: [
                        '#0d6efd',
                        '#198754',
                        '#ffc107',
                        '#0dcaf0',
                        '#dc3545'
                    ],
                    borderWidth: 0,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            boxWidth: 8,
                            color: textColor,
                            padding: 20,
                            font: {
                                size: 12
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: isDarkMode ? 'rgba(0, 0, 0, 0.8)' : 'rgba(255, 255, 255, 0.8)',
                        titleColor: isDarkMode ? '#fff' : '#000',
                        bodyColor: isDarkMode ? '#fff' : '#000',
                        padding: 12,
                        cornerRadius: 6,
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                return `${label}: ${value}%`;
                            }
                        }
                    }
                },
                cutout: '70%'
            }
        });
    }
    
    // Bar Chart - Top Pages
    const pagesCanvas = document.getElementById('topPagesChart');
    if (pagesCanvas) {
        const pagesCtx = pagesCanvas.getContext('2d');
        
        // Get color theme
        const isDarkMode = document.body.classList.contains('dark-mode');
        const gridColor = isDarkMode ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)';
        const textColor = isDarkMode ? 'rgba(255, 255, 255, 0.7)' : 'rgba(0, 0, 0, 0.7)';
        
        new Chart(pagesCtx, {
            type: 'bar',
            data: {
                labels: ['Home', 'About', 'Services', 'Portfolio', 'Blog', 'Contact'],
                datasets: [{
                    label: 'Page Views',
                    data: [12500, 7800, 6500, 5400, 4200, 3800],
                    backgroundColor: [
                        'rgba(13, 110, 253, 0.8)',
                        'rgba(13, 110, 253, 0.7)',
                        'rgba(13, 110, 253, 0.6)',
                        'rgba(13, 110, 253, 0.5)',
                        'rgba(13, 110, 253, 0.4)',
                        'rgba(13, 110, 253, 0.3)'
                    ],
                    borderWidth: 0,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: isDarkMode ? 'rgba(0, 0, 0, 0.8)' : 'rgba(255, 255, 255, 0.8)',
                        titleColor: isDarkMode ? '#fff' : '#000',
                        bodyColor: isDarkMode ? '#fff' : '#000',
                        padding: 12,
                        cornerRadius: 6
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: gridColor,
                            borderDash: [5, 5]
                        },
                        ticks: {
                            color: textColor
                        }
                    },
                    y: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: textColor
                        }
                    }
                }
            }
        });
    }
    
    // Line Chart - Conversion Rates
    const conversionCanvas = document.getElementById('conversionRateChart');
    if (conversionCanvas) {
        const conversionCtx = conversionCanvas.getContext('2d');
        
        // Get color theme
        const isDarkMode = document.body.classList.contains('dark-mode');
        const gridColor = isDarkMode ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)';
        const textColor = isDarkMode ? 'rgba(255, 255, 255, 0.7)' : 'rgba(0, 0, 0, 0.7)';
        
        // Sample data for last 12 months
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        const conversionData = [2.4, 2.2, 2.8, 2.6, 3.0, 3.2, 3.1, 3.5, 3.8, 3.6, 4.0, 3.8];
        
        new Chart(conversionCtx, {
            type: 'line',
            data: {
                labels: months,
                datasets: [{
                    label: 'Conversion Rate (%)',
                    data: conversionData,
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#dc3545',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: isDarkMode ? 'rgba(0, 0, 0, 0.8)' : 'rgba(255, 255, 255, 0.8)',
                        titleColor: isDarkMode ? '#fff' : '#000',
                        bodyColor: isDarkMode ? '#fff' : '#000',
                        padding: 12,
                        cornerRadius: 6,
                        callbacks: {
                            label: function(context) {
                                const label = context.dataset.label || '';
                                const value = context.parsed.y || 0;
                                return `${label}: ${value}%`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: textColor
                        }
                    },
                    y: {
                        grid: {
                            color: gridColor,
                            borderDash: [5, 5]
                        },
                        ticks: {
                            color: textColor,
                            callback: function(value) {
                                return value + '%';
                            }
                        },
                        beginAtZero: true,
                        suggestedMax: 5
                    }
                }
            }
        });
    }
}

/**
 * Initialize datepickers
 */
function initDatepickers() {
    const datepickers = document.querySelectorAll('.datepicker');
    if (datepickers.length && typeof flatpickr !== 'undefined') {
        datepickers.forEach(function(el) {
            flatpickr(el, {
                dateFormat: 'Y-m-d',
                disableMobile: true
            });
        });
    }
    
    const daterangepickers = document.querySelectorAll('.daterangepicker');
    if (daterangepickers.length && typeof flatpickr !== 'undefined') {
        daterangepickers.forEach(function(el) {
            flatpickr(el, {
                mode: 'range',
                dateFormat: 'Y-m-d',
                disableMobile: true
            });
        });
    }
}

/**
 * Initialize sortable elements
 */
function initSortables() {
    const sortables = document.querySelectorAll('.sortable');
    if (sortables.length && typeof Sortable !== 'undefined') {
        sortables.forEach(function(el) {
            Sortable.create(el, {
                animation: 150,
                ghostClass: 'sortable-ghost',
                chosenClass: 'sortable-chosen',
                dragClass: 'sortable-drag'
            });
        });
    }
}

/**
 * Setup dashboard quick actions
 */
function setupQuickActions() {
    // Refresh dashboard stats
    const refreshBtn = document.getElementById('refreshStats');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            refreshBtn.classList.add('fa-spin');
            
            // Simulate refreshing data
            setTimeout(function() {
                refreshBtn.classList.remove('fa-spin');
                showNotification('Dashboard statistics refreshed!', 'success');
                
                // Re-initialize counters with new random values
                const counters = document.querySelectorAll('[data-counter]');
                counters.forEach(counter => {
                    const oldValue = parseInt(counter.getAttribute('data-counter'), 10);
                    const newValue = Math.floor(oldValue * (0.9 + Math.random() * 0.2));
                    counter.setAttribute('data-counter', newValue);
                });
                
                initCounters();
            }, 1500);
        });
    }
    
    // Toggle chart view
    const chartViewBtns = document.querySelectorAll('.chart-view-btn');
    chartViewBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const chartId = btn.getAttribute('data-chart');
            const viewType = btn.getAttribute('data-view');
            const chartContainer = document.getElementById(chartId);
            
            if (chartContainer) {
                // Update active button
                btn.closest('.btn-group').querySelectorAll('.btn').forEach(function(b) {
                    b.classList.remove('active');
                });
                btn.classList.add('active');
                
                // Update chart view (in a real app, this would reconstruct the chart)
                showNotification(`Chart view changed to ${viewType}`, 'info');
            }
        });
    });
    
    // Date range filter
    const dateRangeSelect = document.getElementById('dateRangeSelect');
    if (dateRangeSelect) {
        dateRangeSelect.addEventListener('change', function() {
            const range = this.value;
            showNotification(`Dashboard filtered by: ${range}`, 'info');
            
            // In a real app, this would reload the charts with new data
        });
    }
}

/**
 * Show a notification message (defined in main.js)
 * This is a fallback in case main.js is not loaded
 */
if (typeof showNotification !== 'function') {
    function showNotification(message, type = 'info') {
        alert(message);
    }
} 