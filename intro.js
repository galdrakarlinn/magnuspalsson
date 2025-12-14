// Intro page i18n support
class IntroPage {
  constructor() {
    this.init();
  }

  async init() {
    // Initialize i18n if available
    if (typeof i18n !== 'undefined') {
      await i18n.init();
      // Listen for language changes and re-render
      i18n.onChange(() => this.updateContent());
      // Initial content update
      this.updateContent();
    }
  }

  updateContent() {
    if (typeof i18n === 'undefined') return;

    const lang = i18n.getLang();

    // Update page title
    document.title = lang === 'is'
      ? 'Magnús Pálsson – Listamaður'
      : 'Magnús Pálsson – Artist';

    // Update quotes
    const quoteText = document.querySelector('.intro-quote p[data-i18n="home.quote"]');
    if (quoteText) {
      quoteText.textContent = i18n.t('home.quote');
    }
    const quote2Text = document.querySelector('.intro-quote p[data-i18n="home.quote2"]');
    if (quote2Text) {
      quote2Text.textContent = i18n.t('home.quote2');
    }
    const quote2Source = document.querySelector('.intro-quote p[data-i18n="home.quote2source"]');
    if (quote2Source) {
      quote2Source.textContent = i18n.t('home.quote2source');
    }

    // Update button links
    const links = document.querySelectorAll('.intro-links a');
    if (links.length >= 3) {
      links[0].textContent = lang === 'is' ? 'Skoða verk' : 'View Works';
      links[1].textContent = lang === 'is' ? 'Æviágrip' : 'Biography';
      links[2].textContent = lang === 'is' ? 'Sýningar' : 'Exhibitions';
    }
  }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new IntroPage();
});
