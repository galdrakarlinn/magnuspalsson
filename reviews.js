// reviews.js - Render reviews page with i18n support

class ReviewsManager {
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
        console.log('Reviews: Language changed to', newLang);
        this.renderReviews();
      });
    }

    // Initial render
    this.renderReviews();
  }

  async renderReviews() {
    const container = document.querySelector('main.container');
    if (!container) return;

    // Load reviews translations
    const lang = i18n.getLang();
    let reviewsData;

    try {
      const response = await fetch(`translations/reviews-${lang}.json`);
      reviewsData = await response.json();
    } catch (error) {
      console.error('Error loading reviews data:', error);
      return;
    }

    // Build HTML
    let html = '<h1>' + reviewsData.ui.reviewsTitle + '</h1>';

    // Introduction section
    if (reviewsData.introduction) {
      html += '<div class="introduction">';

      // Introduction paragraphs
      if (reviewsData.introduction.paragraphs) {
        reviewsData.introduction.paragraphs.forEach(paragraph => {
          if (paragraph) {
            html += `<p>${paragraph}</p>`;
          }
        });
      }

      // List
      if (reviewsData.introduction.list && reviewsData.introduction.list.length > 0) {
        html += '<ul>';
        reviewsData.introduction.list.forEach(item => {
          if (item) {
            html += `<li>${item}</li>`;
          }
        });
        html += '</ul>';
      }

      html += '</div>';
    }

    // Render each year group
    reviewsData.reviews.forEach(yearGroup => {
      html += '<section>';
      html += `<p class="year">${yearGroup.year}</p>`;

      if (yearGroup.items && yearGroup.items.length > 0) {
        html += '<ul>';
        yearGroup.items.forEach(item => {
          html += '<li>';

          // Title with optional link
          html += '<span class="title">';
          if (item.url) {
            html += `<a href="${item.url}" target="_blank" rel="noopener noreferrer">${item.title}</a>`;
          } else {
            html += item.title;
          }
          html += '</span>';

          // Description
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
  new ReviewsManager();
});
