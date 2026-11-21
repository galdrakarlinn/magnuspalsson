document.addEventListener("DOMContentLoaded", () => {
    fetch("footer.html")
      .then(response => {
        if (!response.ok) throw new Error("HTTP error " + response.status);
        return response.text();
      })
      .then(data => {
        document.getElementById("footer-placeholder").innerHTML = data;

        // Apply translations to footer after it's loaded
        const applyFooterTranslations = () => {
          if (typeof i18n !== 'undefined' && i18n.isReady()) {
            // Update all elements with data-i18n attribute in the footer
            document.querySelectorAll('#footer-placeholder [data-i18n]').forEach(element => {
              const key = element.getAttribute('data-i18n');
              const translation = i18n.t(key);
              element.textContent = translation;
            });
          } else {
            // If i18n is not ready yet, wait a bit and try again
            setTimeout(applyFooterTranslations, 100);
          }
        };

        applyFooterTranslations();
      })
      .catch(error => console.error("Error loading footer:", error));
  });
  