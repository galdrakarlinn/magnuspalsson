// collections.js - Render collections page with i18n support

class CollectionsManager {
  constructor() {
    this.init();
  }

  async init() {
    // Wait for i18n to be ready
    if (typeof i18n !== 'undefined') {
      // Make sure i18n is initialized
      if (!i18n.isReady()) {
        await i18n.init();
      }

      // Listen for language changes and re-render
      i18n.onChange((newLang) => {
        console.log('Collections: Language changed to', newLang);
        this.renderCollections();
      });
    }

    // Initial render
    this.renderCollections();
  }

  async renderCollections() {
    const container = document.querySelector('main.container');
    if (!container) return;

    // Load collections translations
    const lang = i18n.getLang();
    let collectionsData;

    try {
      const response = await fetch(`translations/collections-${lang}.json`);
      collectionsData = await response.json();
    } catch (error) {
      console.error('Error loading collections data:', error);
      return;
    }

    // Build HTML
    let html = '<h1>' + collectionsData.ui.collectionsTitle + '</h1>';

    // Introduction section
    if (collectionsData.introduction) {
      html += '<div class="introduction">';

      // Introduction paragraphs
      collectionsData.introduction.paragraphs.forEach(paragraph => {
        if (paragraph) {
          html += `<p>${paragraph}</p>`;
        }
      });

      // Holdings list
      if (collectionsData.introduction.holdings && collectionsData.introduction.holdings.length > 0) {
        html += `<p>${collectionsData.ui.holdings}</p>`;
        html += '<ul>';
        collectionsData.introduction.holdings.forEach(item => {
          if (item) {
            html += `<li>${item}</li>`;
          }
        });
        html += '</ul>';
      }

      html += '</div>';
    }

    // Institutions sections
    collectionsData.institutions.forEach(institution => {
      html += '<section>';

      // Institution name with or without link
      if (institution.url) {
        html += `<h2><a href="${institution.url}" target="_blank" rel="noopener noreferrer">${institution.name}</a></h2>`;
      } else {
        html += `<h2>${institution.name}</h2>`;
      }

      // Works list
      if (institution.works && institution.works.length > 0) {
        html += '<ul>';
        institution.works.forEach(work => {
          html += '<li>';

          if (work.url) {
            html += `<a href="${work.url}" target="_blank" rel="noopener noreferrer">`;
          }

          html += `<span class="title">${work.title}</span>`;

          if (work.url) {
            html += '</a>';
          }

          if (work.type) {
            html += ` <span class="type">(${work.type})</span>`;
          }

          if (work.note) {
            html += ` <span class="note">${work.note}</span>`;
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
  new CollectionsManager();
});
