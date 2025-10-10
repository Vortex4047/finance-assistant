// Finance Mentor AI - Main JavaScript

// Global variables
let spendingChart = null;
let chatModal = null;

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    initializeScrollAnimations();
    initializeChatEnhancements();
});

function initializeApp() {
    // Initialize charts if on dashboard
    if (document.getElementById('spendingChart')) {
        initializeSpendingChart();
    }
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function initializeScrollAnimations() {
    // Create intersection observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                // Add staggered animation delay for multiple elements
                const delay = Array.from(entry.target.parentNode.children).indexOf(entry.target) * 100;
                entry.target.style.animationDelay = `${delay}ms`;
            }
        });
    }, observerOptions);
    
    // Observe all elements with animate-on-scroll class
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
    
    // Add animate-on-scroll class to cards and feature elements
    document.querySelectorAll('.card, .feature-card, .metric-card').forEach(el => {
        el.classList.add('animate-on-scroll');
    });
}

function initializeChatEnhancements() {
    // Initialize chat modal
    const chatModalElement = document.getElementById('chatModal');
    if (chatModalElement) {
        chatModal = new bootstrap.Modal(chatModalElement);
        
        // Focus on input when modal opens
        chatModalElement.addEventListener('shown.bs.modal', function () {
            const chatInput = document.getElementById('chatInput');
            if (chatInput) {
                chatInput.focus();
            }
        });
        
        // Add welcome message with delay
        setTimeout(() => {
            addWelcomeMessage();
        }, 500);
    }
}

function addWelcomeMessage() {
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages && chatMessages.children.length <= 1) {
        const welcomeMessages = [
            "👋 Hi there! I'm your Finance Mentor AI assistant.",
            "💰 I can help you with balance inquiries, spending analysis, forecasts, and savings advice.",
            "🚀 Try asking me: 'What's my balance?' or 'How can I save money?'"
        ];
        
        welcomeMessages.forEach((message, index) => {
            setTimeout(() => {
                addMessageToChat('bot', message);
            }, index * 1000);
        });
    }
}

function initializeSpendingChart() {
    const ctx = document.getElementById('spendingChart');
    if (!ctx) return;
    
    // Lazy load chart when visible
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const chartCtx = entry.target.getContext('2d');
                
                const spendingData = {
                    labels: ['Food & Drink', 'Transportation', 'Shopping', 'Bills', 'Entertainment'],
                    datasets: [{
                        data: [450, 200, 300, 800, 150],
                        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
                        borderWidth: 0
                    }]
                };
                
                spendingChart = new Chart(chartCtx, {
                    type: 'doughnut',
                    data: spendingData,
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        animation: { duration: 500 }, // Reduced animation time
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: { padding: 15, usePointStyle: true }
                            }
                        }
                    }
                });
                
                observer.unobserve(entry.target);
            }
        });
    });
    
    observer.observe(ctx);
}

// Chat functionality
function openChatModal() {
    const modal = new bootstrap.Modal(document.getElementById('chatModal'));
    modal.show();
    
    // Focus on input when modal opens
    document.getElementById('chatModal').addEventListener('shown.bs.modal', function () {
        document.getElementById('chatInput').focus();
    });
}

function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Disable input while processing
    input.disabled = true;
    const sendButton = input.nextElementSibling;
    sendButton.disabled = true;
    
    // Add user message to chat
    addMessageToChat('user', message);
    input.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    // Send to backend with realistic delay
    setTimeout(() => {
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            hideTypingIndicator();
            
            // Add slight delay for more natural feel
            setTimeout(() => {
                addMessageToChat('bot', data.response);
                
                // Re-enable input
                input.disabled = false;
                sendButton.disabled = false;
                input.focus();
            }, 500);
        })
        .catch(error => {
            hideTypingIndicator();
            addMessageToChat('bot', '❌ Sorry, I encountered an error. Please try again.');
            console.error('Chat error:', error);
            
            // Re-enable input
            input.disabled = false;
            sendButton.disabled = false;
            input.focus();
        });
    }, 800); // Simulate processing time
}

function addMessageToChat(sender, message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    if (sender === 'user') {
        content.innerHTML = message;
    } else {
        // Format bot messages with better styling
        const formattedMessage = formatBotMessage(message);
        content.innerHTML = formattedMessage;
    }
    
    messageDiv.appendChild(content);
    chatMessages.appendChild(messageDiv);
    
    // Smooth scroll to bottom
    chatMessages.scrollTo({
        top: chatMessages.scrollHeight,
        behavior: 'smooth'
    });
}

function formatBotMessage(message) {
    // Convert markdown-like formatting to HTML
    let formatted = message
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
        .replace(/\*(.*?)\*/g, '<em>$1</em>') // Italic
        .replace(/^(#{1,6})\s+(.+)$/gm, '<h$1>$2</h$1>') // Headers
        .replace(/^• (.+)$/gm, '<li>$1</li>') // List items
        .replace(/^(\d+)\. (.+)$/gm, '<li>$2</li>'); // Numbered lists
    
    // Wrap consecutive list items in ul tags
    formatted = formatted.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>');
    
    // Add emoji spacing
    formatted = formatted.replace(/([\u{1F600}-\u{1F64F}]|[\u{1F300}-\u{1F5FF}]|[\u{1F680}-\u{1F6FF}]|[\u{1F1E0}-\u{1F1FF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}])/gu, '$1 ');
    
    return formatted;
}

function showTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing-indicator';
    typingDiv.className = 'message bot-message';
    
    const typingContent = document.createElement('div');
    typingContent.className = 'typing-indicator';
    typingContent.innerHTML = `
        <div class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
        <span style="margin-left: 10px; color: #6c757d;">Finance AI is typing...</span>
    `;
    
    typingDiv.appendChild(typingContent);
    chatMessages.appendChild(typingDiv);
    
    // Smooth scroll to bottom
    chatMessages.scrollTo({
        top: chatMessages.scrollHeight,
        behavior: 'smooth'
    });
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.style.opacity = '0';
        setTimeout(() => {
            if (typingIndicator.parentNode) {
                typingIndicator.remove();
            }
        }, 300);
    }
}

function handleChatKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function sendQuickMessage(message) {
    const input = document.getElementById('chatInput');
    input.value = message;
    sendMessage();
}

// Account connection functionality
function connectAccount() {
    // Check if user already has accounts
    const accountsSection = document.querySelector('.card-body');
    const hasAccounts = !accountsSection.textContent.includes('No accounts connected yet');
    
    if (hasAccounts) {
        showPlaidLinkDemo();
        return;
    }
    
    // Create demo data for first-time users
    if (confirm('Would you like to create demo financial data to explore the features?')) {
        createDemoData();
    } else {
        showPlaidLinkDemo();
    }
}

function createDemoData() {
    // Show loading state
    const button = event.target;
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Creating Demo Data...';
    button.disabled = true;
    
    fetch('/create_demo_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show success message
            showSuccessMessage('Demo data created! Refreshing page...');
            
            // Refresh page after short delay
            setTimeout(() => {
                window.location.reload();
            }, 2000);
        } else {
            showErrorMessage(data.error || 'Failed to create demo data');
            button.innerHTML = originalText;
            button.disabled = false;
        }
    })
    .catch(error => {
        console.error('Error creating demo data:', error);
        showErrorMessage('Failed to create demo data');
        button.innerHTML = originalText;
        button.disabled = false;
    });
}

function showSuccessMessage(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-success alert-dismissible fade show position-fixed';
    alert.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alert);
    
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

function showErrorMessage(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show position-fixed';
    alert.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alert);
    
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

function showPlaidLinkDemo() {
    // Demo modal for Plaid Link
    const modalHtml = `
        <div class="modal fade" id="plaidDemo" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Connect Your Bank Account</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body text-center">
                        <i class="fas fa-university fa-3x text-primary mb-3"></i>
                        <h6>Plaid Link Integration</h6>
                        <p class="text-muted">
                            To connect real bank accounts, you'll need to:
                        </p>
                        <ol class="text-start">
                            <li>Sign up for a Plaid developer account</li>
                            <li>Get your Client ID and Secret Key</li>
                            <li>Add them to your .env file</li>
                            <li>Install the Plaid Link SDK</li>
                        </ol>
                        <div class="alert alert-info">
                            <small>This is a demo version. Real integration requires Plaid credentials.</small>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <a href="https://plaid.com/docs/" target="_blank" class="btn btn-primary">
                            View Plaid Docs
                        </a>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Add modal to page if it doesn't exist
    if (!document.getElementById('plaidDemo')) {
        document.body.insertAdjacentHTML('beforeend', modalHtml);
    }
    
    const modal = new bootstrap.Modal(document.getElementById('plaidDemo'));
    modal.show();
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric'
    });
}

// Load forecast data
function loadForecast() {
    fetch('/api/forecast')
        .then(response => response.json())
        .then(data => {
            if (data.predicted_balance) {
                document.getElementById('forecast-amount').textContent = 
                    formatCurrency(data.predicted_balance);
                
                // Add confidence indicator
                const confidenceClass = data.confidence > 0.8 ? 'confidence-high' : 
                                      data.confidence > 0.6 ? 'confidence-medium' : 'confidence-low';
                
                const forecastElement = document.getElementById('forecast-amount');
                forecastElement.className = confidenceClass;
                forecastElement.title = `Confidence: ${Math.round(data.confidence * 100)}%`;
            }
        })
        .catch(error => {
            console.error('Forecast error:', error);
            document.getElementById('forecast-amount').textContent = 'N/A';
        });
}

// Spending insights
function loadSpendingInsights() {
    fetch('/api/insights')
        .then(response => response.json())
        .then(data => {
            updateSpendingChart(data.category_spending);
            displayInsights(data.insights);
        })
        .catch(error => {
            console.error('Insights error:', error);
        });
}

function updateSpendingChart(categoryData) {
    if (spendingChart && categoryData) {
        const labels = Object.keys(categoryData);
        const amounts = Object.values(categoryData);
        
        spendingChart.data.labels = labels;
        spendingChart.data.datasets[0].data = amounts;
        spendingChart.update();
    }
}

function displayInsights(insights) {
    const insightsContainer = document.getElementById('insights-container');
    if (insightsContainer && insights) {
        insightsContainer.innerHTML = '';
        
        insights.forEach(insight => {
            const insightDiv = document.createElement('div');
            insightDiv.className = 'alert alert-info insight-card';
            insightDiv.innerHTML = `
                <i class="fas fa-lightbulb me-2"></i>
                ${insight.message}
            `;
            insightsContainer.appendChild(insightDiv);
        });
    }
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
});

// Service worker registration (for PWA capabilities)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/static/sw.js')
            .then(function(registration) {
                console.log('SW registered: ', registration);
            })
            .catch(function(registrationError) {
                console.log('SW registration failed: ', registrationError);
            });
    });
}
// Forec
ast loading function
function loadForecast() {
    const forecastElement = document.getElementById('forecast-amount');
    if (!forecastElement) return;
    
    // Show loading state
    forecastElement.innerHTML = `
        <div class="spinner-border spinner-border-sm" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    `;
    
    // Fetch forecast from API
    fetch('/api/forecast')
        .then(response => response.json())
        .then(data => {
            if (data.predicted_balance) {
                forecastElement.textContent = formatCurrency(data.predicted_balance);
                
                // Add confidence indicator
                const confidence = data.confidence || 0;
                const confidenceClass = confidence > 0.8 ? 'text-success' : 
                                      confidence > 0.6 ? 'text-warning' : 'text-danger';
                
                forecastElement.className = `metric-value ${confidenceClass}`;
                forecastElement.title = `Confidence: ${Math.round(confidence * 100)}%`;
            } else {
                forecastElement.textContent = 'N/A';
                forecastElement.title = 'Insufficient data for forecast';
            }
        })
        .catch(error => {
            console.error('Forecast error:', error);
            forecastElement.textContent = '$2,450.00'; // Fallback demo value
            forecastElement.title = 'Demo forecast - connect accounts for real predictions';
        });
}

// Optimized animations with throttling
function initializeOptimizedAnimations() {
    // Throttled scroll handler
    let scrollTimeout;
    const navbar = document.getElementById('mainNavbar');
    
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (scrollTimeout) return;
            
            scrollTimeout = setTimeout(() => {
                if (window.scrollY > 50) {
                    navbar.classList.add('scrolled');
                } else {
                    navbar.classList.remove('scrolled');
                }
                scrollTimeout = null;
            }, 16); // ~60fps
        }, { passive: true });
    }
    
    // Simplified counter animation
    animateCountersOptimized();
    
    // Reduced animations
    initializeBasicAnimations();
}

function animateCountersOptimized() {
    const counters = document.querySelectorAll('.metric-value, .stat-value, .portfolio-value');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseFloat(counter.textContent.replace(/[$,]/g, ''));
                
                if (!isNaN(target) && target > 0) {
                    // Simplified animation - just fade in
                    counter.style.opacity = '0';
                    counter.style.transition = 'opacity 0.5s ease';
                    setTimeout(() => {
                        counter.style.opacity = '1';
                    }, 100);
                }
                observer.unobserve(counter);
            }
        });
    }, { threshold: 0.1 });
    
    counters.forEach(counter => observer.observe(counter));
}

function initializeBasicAnimations() {
    // Simple fade-in for cards
    const cards = document.querySelectorAll('.card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        observer.observe(card);
    });
}

// Simplified hover effects
function initializeSimpleHoverEffects() {
    // Simple card hover effect
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-2px)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });
}

// Initialize optimized features
document.addEventListener('DOMContentLoaded', function() {
    initializeOptimizedAnimations();
    initializeSimpleHoverEffects();
});

// Removed heavy ripple effect for better performance

// Load forecast on page load with delay for better UX
setTimeout(() => {
    if (document.getElementById('forecast-amount')) {
        loadForecast();
    }
}, 1500);