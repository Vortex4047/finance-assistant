// Performance optimization utilities

// Debounce function for scroll events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function for frequent events
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Lazy load images
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Optimize chart rendering
function optimizeCharts() {
    if (typeof Chart !== 'undefined') {
        // Global Chart.js optimizations
        Chart.defaults.animation.duration = 600;
        Chart.defaults.animation.easing = 'easeOutQuart';
        Chart.defaults.responsive = true;
        Chart.defaults.maintainAspectRatio = false;
        
        // Optimize interactions
        Chart.defaults.interaction.intersect = false;
        Chart.defaults.interaction.mode = 'index';
        
        // Optimize tooltips
        Chart.defaults.plugins.tooltip.animation.duration = 200;
        Chart.defaults.plugins.tooltip.cornerRadius = 8;
        Chart.defaults.plugins.tooltip.displayColors = false;
        
        // Optimize rendering
        Chart.defaults.elements.point.radius = 3;
        Chart.defaults.elements.point.hoverRadius = 5;
        Chart.defaults.elements.line.tension = 0.3;
        
        // Disable unnecessary features for performance
        Chart.defaults.plugins.legend.display = false;
        
        console.log('Chart.js optimizations applied');
    }
}

// Preload critical resources
function preloadCriticalResources() {
    const criticalResources = [
        '/static/css/style.css',
        '/static/js/app.js'
    ];
    
    criticalResources.forEach(resource => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.href = resource;
        link.as = resource.endsWith('.css') ? 'style' : 'script';
        document.head.appendChild(link);
    });
}

// Initialize performance optimizations
document.addEventListener('DOMContentLoaded', function() {
    lazyLoadImages();
    
    // Only initialize charts if Chart.js is loaded
    if (typeof Chart !== 'undefined') {
        optimizeCharts();
    }
    
    // Optimize scroll performance
    const optimizedScrollHandler = throttle(() => {
        // Handle scroll events here
    }, 16); // ~60fps
    
    window.addEventListener('scroll', optimizedScrollHandler, { passive: true });
});

// Memory cleanup
window.addEventListener('beforeunload', function() {
    // Clean up any intervals or timeouts
    // Remove event listeners if needed
});

// Reduce motion for users who prefer it
if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    // Disable animations
    const style = document.createElement('style');
    style.textContent = `
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    `;
    document.head.appendChild(style);
}/
/ Performance mode CSS for heavy pages
const performanceCSS = `
.performance-mode .card {
    transition: none !important;
    transform: none !important;
    will-change: auto !important;
}

.performance-mode .card:hover {
    transform: none !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1) !important;
}

.performance-mode * {
    animation-duration: 0.1s !important;
    transition-duration: 0.1s !important;
}

.performance-mode .btn {
    transition: background-color 0.1s ease !important;
}
`;

// Add performance CSS to document
const performanceStyle = document.createElement('style');
performanceStyle.textContent = performanceCSS;
document.head.appendChild(performanceStyle);