// nav.js
document.addEventListener("DOMContentLoaded", () => {
    fetch("nav.html")
      .then(response => response.text())
      .then(data => {
        document.getElementById("nav-placeholder").innerHTML = data;

        // Initialize hamburger menu functionality
        initializeHamburgerMenu();

        // Load global search functionality after nav is loaded
        if (!document.getElementById('global-search-script')) {
          const script = document.createElement('script');
          script.id = 'global-search-script';
          script.src = 'global-search.js';
          document.head.appendChild(script);
        }
      })
      .catch(error => console.error("Error loading navigation:", error));
  });

  function initializeHamburgerMenu() {
    const hamburgerBtn = document.getElementById('hamburger-btn');
    const navMenu = document.getElementById('nav-menu');
    const searchToggleBtn = document.getElementById('mobile-search-toggle');
    const mobileSearch = document.getElementById('mobile-search');

    // Hamburger menu toggle
    if (hamburgerBtn && navMenu) {
      hamburgerBtn.addEventListener('click', () => {
        const isOpen = navMenu.classList.contains('mobile-open');

        if (isOpen) {
          // Close menu
          navMenu.classList.remove('mobile-open');
          hamburgerBtn.classList.remove('open');
        } else {
          // Open menu
          navMenu.classList.add('mobile-open');
          hamburgerBtn.classList.add('open');

          // Close search if open
          if (mobileSearch) {
            mobileSearch.classList.remove('search-open');
          }
        }
      });
    }

    // Mobile search toggle
    if (searchToggleBtn && mobileSearch) {
      searchToggleBtn.addEventListener('click', () => {
        const isOpen = mobileSearch.classList.contains('search-open');

        if (isOpen) {
          // Close search
          mobileSearch.classList.remove('search-open');
        } else {
          // Open search
          mobileSearch.classList.add('search-open');

          // Close menu if open
          if (navMenu) {
            navMenu.classList.remove('mobile-open');
            hamburgerBtn.classList.remove('open');
          }

          // Focus on search input
          const searchInput = mobileSearch.querySelector('#global-search');
          if (searchInput) {
            searchInput.focus();
          }
        }
      });
    }

    // Close menu when clicking menu items (mobile)
    const menuLinks = navMenu ? navMenu.querySelectorAll('a') : [];
    menuLinks.forEach(link => {
      link.addEventListener('click', () => {
        if (window.innerWidth <= 768) {
          navMenu.classList.remove('mobile-open');
          hamburgerBtn.classList.remove('open');
          if (mobileSearch) {
            mobileSearch.classList.remove('search-open');
          }
        }
      });
    });

    // Close menu when clicking outside (mobile)
    document.addEventListener('click', (e) => {
      if (window.innerWidth <= 768) {
        const navbar = document.querySelector('.navbar');

        if (navbar && !navbar.contains(e.target)) {
          if (navMenu) {
            navMenu.classList.remove('mobile-open');
          }
          if (hamburgerBtn) {
            hamburgerBtn.classList.remove('open');
          }
          if (mobileSearch) {
            mobileSearch.classList.remove('search-open');
          }
        }
      }
    });

    // Handle window resize
    window.addEventListener('resize', () => {
      if (window.innerWidth > 768) {
        // Reset mobile states on desktop
        if (navMenu) {
          navMenu.classList.remove('mobile-open');
        }
        if (hamburgerBtn) {
          hamburgerBtn.classList.remove('open');
        }
        if (mobileSearch) {
          mobileSearch.classList.remove('search-open');
        }
      }
    });
  }
  