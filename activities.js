// activities.js - Render activities page with i18n support

class ActivitiesManager {
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
        console.log('Activities: Language changed to', newLang);
        this.renderActivities();
      });
    }

    // Initial render
    this.renderActivities();
  }

  async renderActivities() {
    const container = document.querySelector('main.container');
    if (!container) return;

    // Load activities translations
    const lang = i18n.getLang();
    let activitiesData;

    try {
      const response = await fetch(`translations/activities-${lang}.json`);
      activitiesData = await response.json();
    } catch (error) {
      console.error('Error loading activities data:', error);
      return;
    }

    // Build HTML
    let html = '<h1>' + activitiesData.ui.activitiesTitle + '</h1>';

    // Under construction notice
    if (activitiesData.ui.underConstruction) {
      html += '<div class="under-construction">' + activitiesData.ui.underConstruction + '</div>';
    }

    // Render each year group
    activitiesData.activities.forEach(yearGroup => {
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
  new ActivitiesManager();
});
