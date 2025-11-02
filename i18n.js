// i18n.js - Translation utility for Magnus Palsson website

class I18n {
  constructor() {
    this.currentLang = localStorage.getItem('language') || 'en';
    this.translations = {};
    this.listeners = [];
    this.initialized = false;
  }

  async init() {
    if (this.initialized) return; // Already initialized
    await this.loadTranslations(this.currentLang);
    await this.loadExhibitionsTranslations(this.currentLang);
    this.updateHtmlLang();
    this.initialized = true;
  }

  async loadTranslations(lang) {
    try {
      const response = await fetch(`translations/${lang}.json`);
      this.translations = await response.json();
      this.currentLang = lang;
      localStorage.setItem('language', lang);
      this.updateHtmlLang();
      // Don't notify listeners yet - wait for exhibitions translations too
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

  async loadExhibitionsTranslations(lang) {
    try {
      // Load single bilingual exhibitions.json file if not already loaded
      if (!this.exhibitionsData) {
        const response = await fetch(`exhibitions.json`);
        this.exhibitionsData = await response.json();
      }

      // Extract data for current language
      this.exhibitionsTranslations = {
        ui: this.exhibitionsData.ui?.[lang] || {},
        solo: this.exhibitionsData.solo || [],
        group: this.exhibitionsData.group || []
      };

      return true;
    } catch (error) {
      console.error(`Error loading exhibitions translations:`, error);
      this.exhibitionsTranslations = { ui: {}, solo: [], group: [] };
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
      await this.loadTranslations(lang);
      await this.loadExhibitionsTranslations(lang);
      // Now notify listeners after BOTH files are loaded
      this.notifyListeners();
      return true;
    }
    return true;
  }

  // Get exhibitions data
  getExhibitions(type) {
    if (!this.exhibitionsTranslations) {
      return [];
    }
    return this.exhibitionsTranslations[type] || [];
  }

  // Get exhibition UI translation
  te(key) {
    if (!this.exhibitionsTranslations || !this.exhibitionsTranslations.ui) {
      return key;
    }
    return this.exhibitionsTranslations.ui[key] || key;
  }

  // Check if i18n is ready
  isReady() {
    return this.initialized;
  }

  // Wait for i18n to be ready
  async waitForReady() {
    if (this.initialized) return;
    // Wait for initialization to complete
    return new Promise((resolve) => {
      const checkReady = setInterval(() => {
        if (this.initialized) {
          clearInterval(checkReady);
          resolve();
        }
      }, 50);
    });
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
