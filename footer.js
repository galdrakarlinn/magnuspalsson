document.addEventListener("DOMContentLoaded", () => {
    fetch("footer.html")
      .then(response => {
        if (!response.ok) throw new Error("HTTP error " + response.status);
        return response.text();
      })
      .then(data => {
        document.getElementById("footer-placeholder").innerHTML = data;
        // Trigger i18n translation for the footer after it's loaded
        if (window.applyTranslations) {
          window.applyTranslations();
        }
      })
      .catch(error => console.error("Error loading footer:", error));
  });
  