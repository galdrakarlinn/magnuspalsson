// publications.js - Render publications page with i18n support

class PublicationsManager {
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
        console.log('Publications: Language changed to', newLang);
        this.renderPublications();
      });
    }

    // Initial render
    this.renderPublications();
  }

  async renderPublications() {
    const container = document.querySelector('main.container');
    if (!container) return;

    // Load publications translations
    const lang = i18n.getLang();
    let publicationsData;

    try {
      const response = await fetch(`translations/publications-${lang}.json`);
      publicationsData = await response.json();
    } catch (error) {
      console.error('Error loading publications data:', error);
      return;
    }

    // Build HTML
    let html = '<h1>' + publicationsData.ui.publicationsTitle + '</h1>';

    // Under construction notice
    if (publicationsData.ui.underConstruction) {
      html += '<div class="under-construction">' + publicationsData.ui.underConstruction + '</div>';
    }

    // Render each year group
    publicationsData.publications.forEach(yearGroup => {
      html += '<section>';
      html += `<p class="year">${yearGroup.year}</p>`;

      if (yearGroup.items && yearGroup.items.length > 0) {
        html += '<ul>';
        yearGroup.items.forEach(item => {
          html += '<li>';
          html += `<span class="title">${item.title}</span>`;

          if (item.description) {
            html += ` — ${item.description}`;
          }

          html += '</li>';
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
  new PublicationsManager();
});
