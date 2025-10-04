// theater.js - Render theater page with i18n support

class TheaterManager {
  constructor() {
    this.init();
  }

  async init() {
    // Wait for i18n to be ready
    if (typeof i18n !== 'undefined') {
      if (!i18n.isReady()) {
        await i18n.init();
      }

      // Load theater translations
      await this.loadTheaterTranslations(i18n.getLang());

      // Listen for language changes
      i18n.onChange(async (newLang) => {
        await this.loadTheaterTranslations(newLang);
        this.renderTheater();
      });
    }

    this.renderTheater();
  }

  async loadTheaterTranslations(lang) {
    try {
      const response = await fetch(`translations/theater-${lang}.json`);
      this.theaterData = await response.json();
    } catch (error) {
      console.error(`Error loading theater-${lang}.json:`, error);
      this.theaterData = { ui: {}, productions: [] };
    }
  }

  renderTheater() {
    const container = document.querySelector('main.archival');
    if (!container) return;

    // Group productions by year
    const productionsByYear = {};
    this.theaterData.productions.forEach(prod => {
      if (!productionsByYear[prod.year]) {
        productionsByYear[prod.year] = [];
      }
      productionsByYear[prod.year].push(prod);
    });

    // Sort years descending
    const years = Object.keys(productionsByYear).sort((a, b) => b - a);

    // Build HTML
    let html = `<h1>${this.theaterData.ui?.theater || 'Theater'}</h1>`;
    html += `<div class="under-construction">${this.theaterData.ui?.underConstruction || 'This page is under construction'}</div>`;

    years.forEach(year => {
      html += `<section>`;
      html += `<p class="year">${year}</p>`;
      html += `<ul>`;

      productionsByYear[year].forEach(prod => {
        html += `<li>`;
        html += `<span class="title">${prod.title}</span>`;
        if (prod.author) {
          html += ` — ${prod.author}`;
        }
        if (prod.director) {
          html += `, director: ${prod.director}`;
        }
        if (prod.venue) {
          html += `, <span class="venue">${prod.venue}</span>`;
        }
        html += `</li>`;
      });

      html += `</ul>`;
      html += `</section>`;
    });

    container.innerHTML = html;

    // Update page title
    document.title = `${this.theaterData.ui?.theater || 'Theater'} – Magnús Pálsson`;
  }
}

// Auto-initialize
document.addEventListener('DOMContentLoaded', () => {
  new TheaterManager();
});
