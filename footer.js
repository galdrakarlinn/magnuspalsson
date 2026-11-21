document.addEventListener("DOMContentLoaded", () => {
    fetch("footer.html")
      .then(response => {
        if (!response.ok) throw new Error("HTTP error " + response.status);
        return response.text();
      })
      .then(data => {
        document.getElementById("footer-placeholder").innerHTML = data;

        // Apply translations to footer after it's loaded
        if (typeof i18n !== 'undefined' && i18n.isReady()) {
          // Update all elements with data-i18n attribute in the footer
          document.querySelectorAll('#footer-placeholder [data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = i18n.t(key);
            element.textContent = translation;
          });
        }
      })
      .catch(error => console.error("Error loading footer:", error));
  });
  