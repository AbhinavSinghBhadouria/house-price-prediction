/**
 * Landing Page JavaScript
 * Handles animations and navigation to prediction page
 */

// Smooth page load animation
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 1s ease-in';
        document.body.style.opacity = '1';
    }, 100);
});

// Enter System Button Handler
function enterSystem() {
    
    const button = document.querySelector('.enter-button');
    const container = document.querySelector('.container');
    
    if (!button || !container) {
        window.location.href = '/predict';
        return;
    }
    
    // Add click animation
    button.style.transform = 'scale(0.95)';
    
    // Create transition effect
    container.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
    container.style.opacity = '0';
    container.style.transform = 'scale(0.95)';
    
    // Navigate to prediction page after animation
    setTimeout(() => {
        window.location.href = '/predict';
    }, 500);
}

// Make function globally accessible
window.enterSystem = enterSystem;

// Add particle animation
function createParticles() {
    const particlesContainer = document.querySelector('.particles');
    if (!particlesContainer) return;
    
    for (let i = 0; i < 10; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 15 + 's';
        particle.style.animationDuration = (10 + Math.random() * 10) + 's';
        particlesContainer.appendChild(particle);
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    
    createParticles();
    
    // Add click event listener to button (more reliable than onclick)
    const enterButton = document.querySelector('.enter-button');
    if (enterButton) {
        
        enterButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            enterSystem();
        });
    } else {
    }
    
    // Add hover effects to feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Add keyboard support for enter button
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            const button = document.querySelector('.enter-button');
            if (button && document.activeElement !== button) {
                enterSystem();
            }
        }
    });
});

// Add parallax effect on mouse move
document.addEventListener('mousemove', (e) => {
    const holographicScreen = document.querySelector('.holographic-screen');
    if (!holographicScreen) return;
    
    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;
    
    holographicScreen.style.transform = `perspective(1000px) rotateY(${(x - 0.5) * 5}deg) rotateX(${(y - 0.5) * -5}deg)`;
});

