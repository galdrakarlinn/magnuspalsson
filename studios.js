// studios.js - Render studios page with i18n support

class StudiosManager {
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
        console.log('Studios: Language changed to', newLang);
        this.renderStudios();
      });
    }

    // Initial render
    this.renderStudios();
  }

  async renderStudios() {
    const container = document.querySelector('main.container');
    if (!container) return;

    // Load studios translations
    const lang = i18n.getLang();
    let studiosData;

    try {
      const response = await fetch(`translations/studios-${lang}.json`);
      studiosData = await response.json();
    } catch (error) {
      console.error('Error loading studios data:', error);
      return;
    }

    // Build HTML
    let html = '<h1>' + studiosData.ui.studiosTitle + '</h1>';

    // Introduction
    if (studiosData.introduction && studiosData.introduction.length > 0) {
      html += '<div class="introduction">';
      studiosData.introduction.forEach(paragraph => {
        html += `<p>${paragraph}</p>`;
      });
      html += '</div>';
    }

    html += '<section class="studio-grid">';

    // Render studio entries
    // Track section headers
    let lastSectionType = null;
    studiosData.studios.forEach((studio, index) => {
      // Add section headers at appropriate points
      if (index === 13) {  // Additional workspaces section
        html += '<h2 style="margin-top: 3rem; margin-bottom: 2rem; border-top: 2px solid #ccc; padding-top: 2rem; color: #666;">';
        html += studiosData.ui.additionalWorkspacesTitle;
        html += '</h2>';
      } else if (index === 19) {  // Institutional workspaces section
        html += '<h2 style="margin-top: 3rem; margin-bottom: 2rem; border-top: 2px solid #ccc; padding-top: 2rem; color: #666;">';
        html += studiosData.ui.institutionalWorkspacesTitle;
        html += '</h2>';
      }

      html += `<div class="studio-entry" id="${studio.id}">`;
      html += `<h2>${studio.title}</h2>`;

      // Images
      if (studio.images && studio.images.length > 0) {
        html += '<div class="studio-images">';
        studio.images.forEach(img => {
          if (img.placeholder) {
            html += `<div class="placeholder-image">${studiosData.ui.placeholderText}</div>`;
          } else {
            html += `<img src="${img.src}" alt="${img.alt}">`;
          }
        });
        html += '</div>';
      }

      // Description
      html += '<div class="studio-description">';
      studio.paragraphs.forEach(paragraph => {
        html += `<p>${paragraph}</p>`;
      });

      // Tags
      if (studio.tags && studio.tags.length > 0) {
        html += '<p class="studio-tags">Tags: ';
        studio.tags.forEach(tag => {
          html += `<span class="tag">${tag}</span> `;
        });
        html += '</p>';
      }

      // Period
      if (studio.period) {
        html += `<p class="studio-period">Period: ${studio.period}</p>`;
      }

      html += '</div>'; // studio-description
      html += '</div>'; // studio-entry
    });

    html += '</section>'; // studio-grid

    // Context section
    if (studiosData.context) {
      html += '<section class="studio-context">';
      if (studiosData.context.title) {
        html += `<h2>${studiosData.context.title}</h2>`;
      }

      studiosData.context.paragraphs.forEach((p, index) => {
        html += `<p>${p}</p>`;

        // Insert list after first paragraph
        if (index === 0 && studiosData.context.list && studiosData.context.list.length > 0) {
          html += '<ul>';
          studiosData.context.list.forEach(item => {
            html += `<li>${item}</li>`;
          });
          html += '</ul>';
        }
      });

      html += '</section>';
    }

    container.innerHTML = html;
  }
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new StudiosManager();
});
