// awards.js - Render awards page with i18n support

class AwardsManager {
  constructor() {
    this.init();
  }

  async init() {
    // Wait for i18n to be ready
    if (typeof i18n !== 'undefined') {
      if (!i18n.isReady()) {
        await i18n.init();
      }

      // Listen for language changes and re-render
      i18n.onChange((newLang) => {
        console.log('Awards: Language changed to', newLang);
        this.renderAwards();
      });
    }

    // Initial render
    this.renderAwards();
  }

  async renderAwards() {
    const container = document.querySelector('main.container');
    if (!container) return;

    // Load awards translations
    const lang = i18n.getLang();
    let awardsData;

    try {
      const response = await fetch(`translations/awards-${lang}.json`);
      awardsData = await response.json();
    } catch (error) {
      console.error('Error loading awards data:', error);
      return;
    }

    // Build HTML
    let html = '<h1>' + awardsData.ui.awardsTitle + '</h1>';

    // Under construction notice
    if (awardsData.ui.underConstruction) {
      html += '<div class="under-construction">' + awardsData.ui.underConstruction + '</div>';
    }

    // Render each year group
    awardsData.awards.forEach(yearGroup => {
      html += '<section>';
      html += `<p class="year">${yearGroup.year}</p>`;

      if (yearGroup.items && yearGroup.items.length > 0) {
        html += '<ul>';
        yearGroup.items.forEach(item => {
          html += `<li>${item}</li>`;
        });
        html += '</ul>';
      }

      html += '</section>';
    });

    container.innerHTML = html;
  }
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new AwardsManager();
});
