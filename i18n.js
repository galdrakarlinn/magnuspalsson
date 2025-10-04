// i18n.js - Translation utility for Magnus Palsson website

class I18n {
  constructor() {
    this.currentLang = localStorage.getItem('language') || 'en';
    this.translations = {};
    this.listeners = [];
  }

  async init() {
    await this.loadTranslations(this.currentLang);
    this.updateHtmlLang();
  }

  async loadTranslations(lang) {
    try {
      const response = await fetch(`translations/${lang}.json`);
      this.translations = await response.json();
      this.currentLang = lang;
      localStorage.setItem('language', lang);
      this.updateHtmlLang();
      this.notifyListeners();
      return true;
    } catch (error) {
      console.error(`Error loading ${lang} translations:`, error);
      // Fallback to English if translation fails
      if (lang !== 'en') {
        return await this.loadTranslations('en');
      }
      return false;
    }
  }

  updateHtmlLang() {
    document.documentElement.lang = this.currentLang;
  }

  // Get translation for a work
  getWork(workId) {
    return this.translations.works?.[workId] || {};
  }

  // Get UI translation
  t(key) {
    return this.translations.ui?.[key] || key;
  }

  // Get current language
  getLang() {
    return this.currentLang;
  }

  // Set language and reload translations
  async setLang(lang) {
    if (lang !== this.currentLang) {
      return await this.loadTranslations(lang);
    }
    return true;
  }

  // Subscribe to language changes
  onChange(callback) {
    this.listeners.push(callback);
  }

  // Notify all listeners of language change
  notifyListeners() {
    this.listeners.forEach(callback => callback(this.currentLang));
  }
}

// Create global i18n instance
const i18n = new I18n();
