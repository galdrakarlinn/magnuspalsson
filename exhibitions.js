// exhibitions.js - Render exhibitions pages with i18n support

class ExhibitionsManager {
  constructor(type) {
    this.type = type; // 'solo' or 'group'
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
        console.log('Exhibitions: Language changed to', newLang);
        this.renderExhibitions();
      });
    }

    // Initial render
    this.renderExhibitions();
  }

  renderExhibitions() {
    const container = document.querySelector('main.archival');
    if (!container) return;

    // Get exhibitions data
    const exhibitions = i18n.getExhibitions(this.type);

    // Update page title
    const h1 = container.querySelector('h1');
    if (h1) {
      h1.textContent = this.type === 'solo' ? i18n.te('soloExhibitions') : i18n.te('groupExhibitions');
    }

    // Update "under construction" message if exists
    const underConstruction = container.querySelector('.under-construction');
    if (underConstruction) {
      underConstruction.textContent = i18n.te('underConstruction');
    }

    // Group exhibitions by year
    const exhibitionsByYear = {};
    exhibitions.forEach(exhibition => {
      const year = exhibition.year;
      if (!exhibitionsByYear[year]) {
        exhibitionsByYear[year] = [];
      }
      exhibitionsByYear[year].push(exhibition);
    });

    // Sort years in descending order
    const years = Object.keys(exhibitionsByYear).sort((a, b) => b - a);

    // Build HTML
    let html = '<h1>' + (this.type === 'solo' ? i18n.te('soloExhibitions') : i18n.te('groupExhibitions')) + '</h1>';

    if (underConstruction) {
      html += '<div class="under-construction">' + i18n.te('underConstruction') + '</div>';
    }

    years.forEach(year => {
      html += `<section>`;
      html += `<p class="year">${year}</p>`;
      html += `<ul>`;

      exhibitionsByYear[year].forEach(exhibition => {
        // Get localized values for bilingual fields
        const lang = i18n.getLang();
        const title = typeof exhibition.title === 'object' ? (exhibition.title[lang] || exhibition.title.en) : exhibition.title;
        const venue = typeof exhibition.venue === 'object' ? (exhibition.venue[lang] || exhibition.venue.en) : exhibition.venue;
        const notes = typeof exhibition.notes === 'object' ? (exhibition.notes[lang] || exhibition.notes.en) : exhibition.notes;

        html += `<li>`;
        html += `<span class="title">${title}</span> — `;
        html += `<span class="venue">${venue}</span>`;
        if (exhibition.location) {
          html += `, ${exhibition.location}`;
        }
        if (notes) {
          html += `. ${notes}`;
        }
        html += `</li>`;
      });

      html += `</ul>`;
      html += `</section>`;
    });

    container.innerHTML = html;
  }
}

// Auto-initialize based on page
document.addEventListener('DOMContentLoaded', () => {
  const path = window.location.pathname;

  if (path.includes('exhibitions-solo')) {
    new ExhibitionsManager('solo');
  } else if (path.includes('exhibitions-group')) {
    new ExhibitionsManager('group');
  }
});
