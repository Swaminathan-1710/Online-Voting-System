/**
 * BallotHub - Interactive Effects & Animations
 * Adds dynamic interactions to enhance user experience
 */

// Initialize interactive effects when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  initRippleEffects();
  initParallaxEffects();
  initScrollAnimations();
  initButtonAnimations();
  initFormEnhancements();
});

/**
 * Ripple Effect for Buttons
 */
function initRippleEffects() {
  const buttons = document.querySelectorAll('.btn');
  
  buttons.forEach(button => {
    button.addEventListener('click', function(e) {
      const ripple = document.createElement('span');
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;
      
      ripple.style.width = ripple.style.height = size + 'px';
      ripple.style.left = x + 'px';
      ripple.style.top = y + 'px';
      ripple.classList.add('ripple');
      
      this.appendChild(ripple);
      
      setTimeout(() => {
        ripple.remove();
      }, 600);
    });
  });
}

/**
 * Parallax Effect for Background
 */
function initParallaxEffects() {
  let lastScrollTop = 0;
  
  window.addEventListener('scroll', function() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const parallaxElements = document.querySelectorAll('.parallax');
    
    parallaxElements.forEach(element => {
      const speed = element.dataset.speed || 0.5;
      const yPos = -(scrollTop * speed);
      element.style.transform = `translateY(${yPos}px)`;
    });
    
    lastScrollTop = scrollTop;
  });
}

/**
 * Scroll Animations
 */
function initScrollAnimations() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };
  
  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);
  
  const animatedElements = document.querySelectorAll('.card, .stat-card, .candidate-card');
  animatedElements.forEach(el => observer.observe(el));
}

/**
 * Button Hover Animations
 */
function initButtonAnimations() {
  const buttons = document.querySelectorAll('.btn');
  
  buttons.forEach(button => {
    button.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-3px) scale(1.02)';
    });
    
    button.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0) scale(1)';
    });
    
    button.addEventListener('mousedown', function() {
      this.style.transform = 'translateY(0) scale(0.98)';
    });
    
    button.addEventListener('mouseup', function() {
      this.style.transform = 'translateY(-3px) scale(1.02)';
    });
  });
}

/**
 * Form Input Enhancements
 */
function initFormEnhancements() {
  const inputs = document.querySelectorAll('.form-control, .form-select');
  
  inputs.forEach(input => {
    // Add floating label effect
    if (input.value) {
      input.classList.add('has-value');
    }
    
    input.addEventListener('focus', function() {
      this.parentElement?.classList.add('focused');
    });
    
    input.addEventListener('blur', function() {
      this.parentElement?.classList.remove('focused');
      if (this.value) {
        this.classList.add('has-value');
      } else {
        this.classList.remove('has-value');
      }
    });
    
    // Add input animation
    input.addEventListener('input', function() {
      if (this.value) {
        this.style.borderColor = 'var(--primary-color)';
      }
    });
  });
}


/**
 * Add Ripple CSS dynamically
 */
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
  .ripple {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.6);
    transform: scale(0);
    animation: ripple-animation 0.6s ease-out;
    pointer-events: none;
  }
  
  @keyframes ripple-animation {
    to {
      transform: scale(4);
      opacity: 0;
    }
  }
  
  .btn {
    position: relative;
    overflow: hidden;
  }
`;
document.head.appendChild(rippleStyle);

/**
 * Smooth Scroll for Anchor Links
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
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

/**
 * Add Loading States
 */
function showLoading(element) {
  if (element) {
    element.classList.add('loading-state');
    element.disabled = true;
    const originalText = element.textContent;
    element.dataset.originalText = originalText;
    element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
  }
}

function hideLoading(element) {
  if (element) {
    element.classList.remove('loading-state');
    element.disabled = false;
    element.textContent = element.dataset.originalText || 'Submit';
  }
}

/**
 * Toast Notification System
 */
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast-notification toast-${type}`;
  toast.textContent = message;
  
  const styles = {
    position: 'fixed',
    top: '20px',
    right: '20px',
    padding: '1rem 1.5rem',
    borderRadius: '12px',
    color: 'white',
    fontWeight: '600',
    zIndex: '10000',
    boxShadow: '0 10px 30px rgba(0,0,0,0.3)',
    animation: 'slideInRight 0.3s ease',
    maxWidth: '400px',
    wordWrap: 'break-word'
  };
  
  const typeColors = {
    success: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
    error: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
    info: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
    warning: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'
  };
  
  toast.style.background = typeColors[type] || typeColors.info;
  
  Object.assign(toast.style, styles);
  
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.style.animation = 'slideOutRight 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// Add toast animations
const toastAnimations = document.createElement('style');
toastAnimations.textContent = `
  @keyframes slideInRight {
    from {
      transform: translateX(100%);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }
  
  @keyframes slideOutRight {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(100%);
      opacity: 0;
    }
  }
`;
document.head.appendChild(toastAnimations);

// Export functions for global use
window.showToast = showToast;
window.showLoading = showLoading;
window.hideLoading = hideLoading;

