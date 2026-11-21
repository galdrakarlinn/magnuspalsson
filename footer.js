document.addEventListener("DOMContentLoaded", async () => {
    try {
      const response = await fetch("footer.html");
      if (!response.ok) throw new Error("HTTP error " + response.status);
      const data = await response.text();
      document.getElementById("footer-placeholder").innerHTML = data;

      // Apply footer translations - this will be called on initial load and language changes
      function applyFooterTranslations() {
        if (typeof i18n !== 'undefined' && i18n.isReady()) {
          document.querySelectorAll('#footer-placeholder [data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = i18n.t(key);
            element.textContent = translation;
          });
        }
      }

      // Subscribe to i18n language changes
      if (typeof i18n !== 'undefined') {
        // Wait for i18n to initialize (nav.js will call init())
        await i18n.waitForReady();

        // Apply initial translations
        applyFooterTranslations();

        // Subscribe to future language changes
        i18n.onChange(() => {
          applyFooterTranslations();
        });
      }
    } catch (error) {
      console.error("Error loading footer:", error);
    }
  });
  