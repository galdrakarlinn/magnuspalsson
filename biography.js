// biography.js - Render biography page with i18n support

class BiographyManager {
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

      // Load biography translations
      await this.loadBiographyTranslations(i18n.getLang());

      // Listen for language changes and re-render
      i18n.onChange(async (newLang) => {
        await this.loadBiographyTranslations(newLang);
        this.renderBiography();
      });
    }

    // Initial render
    this.renderBiography();
  }

  async loadBiographyTranslations(lang) {
    try {
      const response = await fetch(`translations/biography-${lang}.json`);
      this.biographyData = await response.json();
    } catch (error) {
      console.error(`Error loading biography-${lang}.json:`, error);
      this.biographyData = { ui: {}, sections: [] };
    }
  }

  renderBiography() {
    const container = document.querySelector('main.container');
    if (!container) return;

    // Build HTML
    let html = `<h1>${this.biographyData.ui?.biography || 'Biography'}</h1>`;
    html += `<div class="under-construction">${this.biographyData.ui?.underConstruction || 'This page is under construction'}</div>`;
    html += `<section class="biography-content">`;

    // Render each section
    this.biographyData.sections.forEach(section => {
      if (section.title) {
        html += `<h2>${section.title}</h2>`;
      }
      section.paragraphs.forEach(paragraph => {
        if (paragraph) {
          html += `<p>${paragraph}</p>`;
        }
      });
    });

    html += `</section>`;

    container.innerHTML = html;

    // Update page title
    document.title = `${this.biographyData.ui?.biography || 'Biography'} – Magnús Pálsson`;
  }
}

// Auto-initialize
document.addEventListener('DOMContentLoaded', () => {
  new BiographyManager();
});
