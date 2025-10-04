// films.js - Render films page with i18n support

class FilmsManager {
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
        console.log('Films: Language changed to', newLang);
        this.renderFilms();
      });
    }

    // Initial render
    this.renderFilms();
  }

  async renderFilms() {
    const container = document.querySelector('main.container');
    if (!container) return;

    // Load films translations
    const lang = i18n.getLang();
    let filmsData;

    try {
      const response = await fetch(`translations/films-${lang}.json`);
      filmsData = await response.json();
    } catch (error) {
      console.error('Error loading films data:', error);
      return;
    }

    // Build HTML
    let html = '<h1>' + filmsData.ui.filmsTitle + '</h1>';

    // Under construction notice
    if (filmsData.ui.underConstruction) {
      html += '<div class="under-construction">' + filmsData.ui.underConstruction + '</div>';
    }

    // Render each year group
    filmsData.films.forEach(yearGroup => {
      html += '<section>';
      html += `<p class="year">${yearGroup.year}</p>`;

      if (yearGroup.items && yearGroup.items.length > 0) {
        html += '<ul>';
        yearGroup.items.forEach(item => {
          html += '<li>';
          if (item.title) {
            html += `<em>${item.title}</em>`;
            if (item.description) {
              html += `, ${item.description}`;
            }
          } else {
            html += item.description;
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
  new FilmsManager();
});
