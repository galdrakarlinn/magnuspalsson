// nav.js
document.addEventListener("DOMContentLoaded", () => {
    fetch("nav.html")
      .then(response => response.text())
      .then(data => {
        document.getElementById("nav-placeholder").innerHTML = data;
        
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
  