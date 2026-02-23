class GlobalSearch {
  constructor() {
    this.searchIndex = [];
    this.searchInput = null;
    this.searchResults = null;
    this.searchFilters = null;
    this.currentResults = [];
    this.currentFilters = {
      type: 'all',
      year: 2024,
      medium: 'all',
      institution: 'all'
    };

    this.init();
  }

  // Get current language from localStorage
  getCurrentLang() {
    return localStorage.getItem('language') || 'en';
  }

  // Get localized value from bilingual object or string
  getLocalizedValue(field, fallback) {
    if (!field) return fallback || '';
    if (typeof field === 'string') return field;
    const lang = this.getCurrentLang();
    return field[lang] || field.en || field.is || fallback || '';
  }

  // Get localized title from bilingual title object or string
  getLocalizedTitle(title) {
    return this.getLocalizedValue(title, 'Untitled');
  }

  init() {
    // Load search index - setupEventListeners and restoreSearchState are called from loadSearchIndex callback
    this.loadSearchIndex();
  }

  loadSearchIndex() {
    // Edge-compatible version using XMLHttpRequest instead of fetch
    const xhr = new XMLHttpRequest();
    xhr.open('GET', 'search-index.json', true);
    const self = this; // Edge compatibility: store 'this' reference
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          try {
            const data = JSON.parse(xhr.responseText);
            self.searchIndex = data.searchableContent;
            self.setupEventListeners();
            self.restoreSearchState();
          } catch (error) {
            console.error('Error parsing search index:', error);
            self.showSearchError('Unable to load search data. Please refresh the page.');
            self.searchIndex = [];
          }
        } else {
          console.error('Error loading search index:', xhr.status, xhr.statusText);
          self.showSearchError('Search is temporarily unavailable. Please try again later.');
          self.searchIndex = [];
        }
      }
    };
    xhr.onerror = function() {
      console.error('Network error loading search index');
      self.showSearchError('Network error. Please check your connection and try again.');
      self.searchIndex = [];
    };
    xhr.send();
  }

  showSearchError(message) {
    // Show error in search inputs placeholder
    if (this.searchInputMobile) {
      this.searchInputMobile.placeholder = message;
      this.searchInputMobile.disabled = true;
    }
    if (this.searchInputDesktop) {
      this.searchInputDesktop.placeholder = message;
      this.searchInputDesktop.disabled = true;
    }
  }

  setupEventListeners() {
    // Support both mobile and desktop search inputs
    this.searchInputMobile = document.getElementById('global-search-mobile');
    this.searchInputDesktop = document.getElementById('global-search-desktop');
    this.searchResultsMobile = document.getElementById('search-results-mobile');
    this.searchResultsDesktop = document.getElementById('search-results-desktop');
    this.searchFilters = document.getElementById('search-filters');

    // Set primary search input based on what's available
    this.searchInput = this.searchInputDesktop || this.searchInputMobile;
    this.searchResults = this.searchResultsDesktop || this.searchResultsMobile;

    if (!this.searchInput || !this.searchResults) {
      return;
    }

    // Set up event listeners for both inputs
    this.setupSearchInput(this.searchInputMobile, this.searchResultsMobile);
    this.setupSearchInput(this.searchInputDesktop, this.searchResultsDesktop);

    // Handle search result navigation - use mousedown to catch it earlier
    document.addEventListener('mousedown', (e) => {
      const searchResultLink = e.target.closest('a.search-result');
      if (searchResultLink) {
        // Prevent any other handlers from interfering
        e.stopPropagation();
        e.stopImmediatePropagation();
      }
    }, true);

    // Handle search result navigation
    document.addEventListener('click', (e) => {
      // Handle search result link clicks
      const searchResultLink = e.target.closest('a.search-result');
      if (searchResultLink) {
        // Let the link work naturally - don't prevent default
        return;
      }

      // Don't hide if clicking within search results container
      if (e.target.closest('#search-results-mobile') || e.target.closest('#search-results-desktop')) {
        return;
      }

      // Only hide if clicking on main content area, not navigation or search
      if (!e.target.closest('.nav-search') &&
          !e.target.closest('.navbar') &&
          e.target.closest('main')) {
        this.hideResults();
        this.hideFilters();
      }
    });

    // Global keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.hideResults();
        this.hideFilters();
        if (this.searchInputMobile) this.searchInputMobile.blur();
        if (this.searchInputDesktop) this.searchInputDesktop.blur();
      } else if (e.key === 'Enter' && this.currentResults.length > 0) {
        const activeElement = document.activeElement;
        if (activeElement === this.searchInputMobile || activeElement === this.searchInputDesktop) {
          e.preventDefault();
          window.location.href = this.currentResults[0].url;
        }
      }
    });

    // Setup filter event listeners
    this.setupFilterEventListeners();
  }

  getCurrentQuery() {
    const mobileValue = this.searchInputMobile ? this.searchInputMobile.value.trim() : '';
    const desktopValue = this.searchInputDesktop ? this.searchInputDesktop.value.trim() : '';
    return mobileValue || desktopValue || '';
  }

  setupSearchInput(searchInput, searchResults) {
    if (!searchInput || !searchResults) return;

    // Create a debounced search function to improve iOS performance
    let searchTimeout;
    const debouncedSearch = (query) => {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(() => {
        // Sync with other search input
        if (searchInput === this.searchInputMobile && this.searchInputDesktop) {
          this.searchInputDesktop.value = query;
        } else if (searchInput === this.searchInputDesktop && this.searchInputMobile) {
          this.searchInputMobile.value = query;
        }

        // Set active search results container
        this.searchResults = searchResults;

        if (query.length >= 2) {
          this.showFilters();
          this.performSearch(query);
        } else {
          this.hideFilters();
          this.hideResults();
        }
      }, 150); // 150ms debounce for better iOS performance
    };

    // Primary input event (works on most browsers)
    searchInput.addEventListener('input', (e) => {
      const query = e.target.value.trim();
      debouncedSearch(query);
    });

    // iOS Safari fallback events
    searchInput.addEventListener('keyup', (e) => {
      const query = e.target.value.trim();
      debouncedSearch(query);
    });

    // Additional iOS Safari fallback
    searchInput.addEventListener('change', (e) => {
      const query = e.target.value.trim();
      debouncedSearch(query);
    });

    // iOS-specific touch events
    searchInput.addEventListener('touchend', (e) => {
      // Small delay to let iOS Safari process the touch
      setTimeout(() => {
        const query = e.target.value.trim();
        if (query !== searchInput.dataset.lastQuery) {
          searchInput.dataset.lastQuery = query;
          debouncedSearch(query);
        }
      }, 50);
    });

    searchInput.addEventListener('focus', () => {
      // Set active search results container
      this.searchResults = searchResults;

      // iOS Safari focus handling
      setTimeout(() => {
        if (this.currentResults.length > 0) {
          this.showResults();
          if (searchInput.value.trim().length >= 2) {
            this.showFilters();
          }
        }
      }, 100);
    });

    // Prevent iOS zoom on focus
    searchInput.addEventListener('touchstart', (e) => {
      if (parseFloat(searchInput.style.fontSize) < 16) {
        searchInput.style.fontSize = '16px';
      }
    });
  }

  setupFilterEventListeners() {
    // Filter buttons
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('filter-btn')) {
        const filterType = e.target.dataset.filter;
        const filterValue = e.target.dataset.value;

        // Update active state
        document.querySelectorAll(`[data-filter="${filterType}"]`).forEach(btn => {
          btn.classList.remove('active');
        });
        e.target.classList.add('active');

        // Update filter state
        this.currentFilters[filterType] = filterValue;

        // Re-run search if there's a query
        const query = this.getCurrentQuery();
        if (query.length >= 2) {
          this.performSearch(query);
        }
        this.saveSearchState();
      }
    });

    // Year range slider
    const yearFilter = document.getElementById('year-filter');
    const yearDisplay = document.getElementById('year-display');
    
    if (yearFilter && yearDisplay) {
      yearFilter.addEventListener('input', (e) => {
        const year = parseInt(e.target.value);
        this.currentFilters.year = year;
        yearDisplay.textContent = `1960-${year}`;
        
        // Re-run search if there's a query
        const query = this.getCurrentQuery();
        if (query.length >= 2) {
          this.performSearch(query);
        }
        this.saveSearchState();
      });
    }

    // Clear filters button
    const clearFilters = document.getElementById('clear-filters');
    if (clearFilters) {
      clearFilters.addEventListener('click', () => {
        this.clearAllFilters();
      });
    }

    // Toggle filters button
    const toggleFilters = document.getElementById('toggle-filters');
    if (toggleFilters) {
      toggleFilters.addEventListener('click', () => {
        if (this.searchFilters.style.display === 'none') {
          this.showFilters();
          toggleFilters.textContent = 'Hide Filters';
        } else {
          this.hideFilters();
          toggleFilters.textContent = 'Show Filters';
        }
      });
    }
  }

  // Normalize Icelandic characters for better searching
  normalizeIcelandic(text) {
    const charMap = {
      'á': 'a', 'à': 'a', 'ä': 'a', 'â': 'a',
      'é': 'e', 'è': 'e', 'ë': 'e', 'ê': 'e',
      'í': 'i', 'ì': 'i', 'ï': 'i', 'î': 'i',
      'ó': 'o', 'ò': 'o', 'ö': 'o', 'ô': 'o',
      'ú': 'u', 'ù': 'u', 'ü': 'u', 'û': 'u',
      'ý': 'y', 'ÿ': 'y',
      'þ': 'th', 'ð': 'd',
      'æ': 'ae'
    };
    
    return text.toLowerCase().replace(/[áàäâéèëêíìïîóòöôúùüûýÿþðæ]/g, char => charMap[char] || char);
  }

  // Calculate similarity between two strings (for fuzzy matching)
  calculateSimilarity(str1, str2) {
    const longer = str1.length > str2.length ? str1 : str2;
    const shorter = str1.length > str2.length ? str2 : str1;
    
    if (longer.length === 0) return 1.0;
    
    const levenshteinDistance = this.levenshteinDistance(longer, shorter);
    return (longer.length - levenshteinDistance) / longer.length;
  }

  // Levenshtein distance algorithm for fuzzy matching
  levenshteinDistance(str1, str2) {
    const matrix = [];
    for (let i = 0; i <= str2.length; i++) {
      matrix[i] = [i];
    }
    for (let j = 0; j <= str1.length; j++) {
      matrix[0][j] = j;
    }
    for (let i = 1; i <= str2.length; i++) {
      for (let j = 1; j <= str1.length; j++) {
        if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
          matrix[i][j] = matrix[i - 1][j - 1];
        } else {
          matrix[i][j] = Math.min(
            matrix[i - 1][j - 1] + 1,
            matrix[i][j - 1] + 1,
            matrix[i - 1][j] + 1
          );
        }
      }
    }
    return matrix[str2.length][str1.length];
  }

  performSearch(query) {
    const queryLower = query.toLowerCase();
    const queryNormalized = this.normalizeIcelandic(queryLower);
    const queryWords = queryLower.split(' ').filter(word => word.length > 2);

    const results = this.searchIndex
      .filter(item => this.passesFilters(item))
      .map(item => {
        let score = 0;

        // Get BOTH language titles for searching (bilingual search)
        const titleEn = (typeof item.title === 'object' ? (item.title.en || '') : (item.title || '')).toLowerCase();
        const titleIs = (typeof item.title === 'object' ? (item.title.is || '') : '').toLowerCase();
        const titleEnNorm = this.normalizeIcelandic(titleEn);
        const titleIsNorm = this.normalizeIcelandic(titleIs);

        const contentLower = item.content.toLowerCase();
        const contentNormalized = this.normalizeIcelandic(contentLower);

        // Exact title match gets highest score - check BOTH languages
        if (titleEn === queryLower || titleIs === queryLower ||
            titleEnNorm === queryNormalized || titleIsNorm === queryNormalized) {
          score += 1000;
        } else if (titleEn.includes(queryLower) || titleIs.includes(queryLower) ||
                   titleEnNorm.includes(queryNormalized) || titleIsNorm.includes(queryNormalized)) {
          score += 500;
        }

        // Fuzzy title matching for typos - check both languages, use best score
        const titleEnSimilarity = this.calculateSimilarity(titleEnNorm, queryNormalized);
        const titleIsSimilarity = this.calculateSimilarity(titleIsNorm, queryNormalized);
        const bestTitleSimilarity = Math.max(titleEnSimilarity, titleIsSimilarity);
        if (bestTitleSimilarity > 0.7 && bestTitleSimilarity < 1) {
          score += Math.floor(bestTitleSimilarity * 300);
        }

        // Exact content phrase match
        if (contentLower.includes(queryLower) || contentNormalized.includes(queryNormalized)) {
          score += 200;
        }

        // Significant word matches in title (avoid common words)
        const significantWords = queryWords.filter(word =>
          !['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'have', 'it', 'my', 'i'].includes(word)
        );

        significantWords.forEach(word => {
          if (word.length > 3) { // Only meaningful words
            const wordNormalized = this.normalizeIcelandic(word);

            // Regular matches - check both language titles
            if (titleEn.includes(word) || titleIs.includes(word) ||
                titleEnNorm.includes(wordNormalized) || titleIsNorm.includes(wordNormalized)) {
              score += 50;
            }
            if (contentLower.includes(word) || contentNormalized.includes(wordNormalized)) {
              score += 20;
            }

            // Fuzzy word matching against both language titles
            const allTitleWords = (titleEnNorm + ' ' + titleIsNorm).split(' ');
            const contentWords = contentNormalized.split(' ');

            allTitleWords.forEach(titleWord => {
              if (!titleWord) return;
              const similarity = this.calculateSimilarity(titleWord, wordNormalized);
              if (similarity > 0.75 && similarity < 1) {
                score += Math.floor(similarity * 30);
              }
            });

            contentWords.forEach(contentWord => {
              const similarity = this.calculateSimilarity(contentWord, wordNormalized);
              if (similarity > 0.75 && similarity < 1) {
                score += Math.floor(similarity * 15);
              }
            });
          }
        });

        // Year matches
        if (query.match(/^\d{4}$/) && item.year.toString() === query) {
          score += 100;
        }

        return { ...item, score };
      })
      .filter(item => item.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 8); // Limit to 8 results

    this.currentResults = results;
    this.displayResults(results, query);
    this.saveSearchState();
  }

  displayResults(results, query) {
    // Prevent re-rendering if already showing the same results
    if (this.lastDisplayedQuery === query && this.lastDisplayedResults === results.length) {
      return;
    }
    this.lastDisplayedQuery = query;
    this.lastDisplayedResults = results.length;

    const isIcelandic = this.getCurrentLang() === 'is';

    if (results.length === 0) {
      this.hideFilters(); // Hide filters when no results
      this.searchResults.innerHTML = `
        <div class="search-no-results">
          <div class="search-result-title">${isIcelandic ? `Ekkert fannst fyrir "${query}"` : `No results found for "${query}"`}</div>
          <div class="search-result-snippet">${isIcelandic ? 'Prófaðu að leita að:' : 'Try searching for:'}</div>
          <div class="search-suggestions">
            <span class="suggestion-item">${isIcelandic ? 'nöfn verka' : 'work titles'}</span>
            <span class="suggestion-item">${isIcelandic ? 'tækni listamanns' : 'artist techniques'}</span>
            <span class="suggestion-item">${isIcelandic ? 'ár (1960-2020)' : 'years (1960-2020)'}</span>
            <span class="suggestion-item">${isIcelandic ? 'sýningarnöfn' : 'exhibition names'}</span>
          </div>
        </div>
      `;
    } else {
      const activeFilters = this.getActiveFiltersText();
      const resultsText = isIcelandic
        ? `${results.length} ${results.length === 1 ? 'niðurstaða' : 'niðurstöður'} fyrir "${query}"`
        : `${results.length} result${results.length === 1 ? '' : 's'} for "${query}"`;
      this.searchResults.innerHTML = `
        <div class="search-results-header">
          <span>${resultsText}${activeFilters ? ` (${activeFilters})` : ''}</span>
          <button class="search-close-btn" onclick="window.globalSearchInstance.clearSearch(); event.stopPropagation();">×</button>
        </div>
        ${results.map(result => `
          <a href="${result.url}" class="search-result" style="text-decoration: none; color: inherit; display: block; pointer-events: auto; position: relative; z-index: 5000;">
            <div class="search-result-header" style="pointer-events: none;">
              <div class="search-result-badge search-badge-${result.type}">${this.getTypeBadge(result.type)}</div>
              ${result.year ? `<div class="search-result-year">${result.year}</div>` : ''}
            </div>
            <div class="search-result-title" style="pointer-events: none;">${this.highlightQueryAdvanced(this.getLocalizedTitle(result.title), query)}</div>
            <div class="search-result-snippet" style="pointer-events: none;">${this.highlightQueryAdvanced(this.getLocalizedValue(result.snippet, ''), query)}</div>
            <div class="search-result-meta" style="pointer-events: none;">
              <span class="search-result-page">${this.getPageLabel(result.type, result.page)}</span>
              ${result.score ? `<span class="search-result-relevance">${isIcelandic ? 'Samsvörun' : 'Relevance'}: ${Math.round(result.score/10)}/100</span>` : ''}
            </div>
          </a>
        `).join('')}
      `;
    }
    
    this.showResults();
  }

  highlightQuery(text, query) {
    const queryWords = query.toLowerCase().split(' ').filter(word => word.length > 1);
    let highlightedText = text;
    
    queryWords.forEach(word => {
      const regex = new RegExp(`(${word})`, 'gi');
      highlightedText = highlightedText.replace(regex, '<strong>$1</strong>');
    });
    
    return highlightedText;
  }

  getTypeBadge(type) {
    const isIcelandic = this.getCurrentLang() === 'is';
    const badges = isIcelandic ? {
      'work': '🎨 Verk',
      'group-exhibition': '🏛️ Samsýning',
      'solo-exhibition': '🎭 Einkasýning',
      'review': '📝 Umfjöllun',
      'publication': '📚 Útgáfa',
      'biography': '👤 Æviágrip',
      'theater': '🎭 Leikhús',
      'collections': '🗃️ Safn',
      'collection-work': '🏛️ Safn'
    } : {
      'work': '🎨 Work',
      'group-exhibition': '🏛️ Group Show',
      'solo-exhibition': '🎭 Solo Show',
      'review': '📝 Review',
      'publication': '📚 Publication',
      'biography': '👤 Biography',
      'theater': '🎭 Theater',
      'collections': '🗃️ Collection',
      'collection-work': '🏛️ Museum'
    };

    return badges[type] || (isIcelandic ? '📄 Síða' : '📄 Page');
  }

  getPageLabel(type, page) {
    const isIcelandic = this.getCurrentLang() === 'is';
    const labels = isIcelandic ? {
      'work': 'Verk',
      'group-exhibition': 'Samsýningar',
      'solo-exhibition': 'Einkasýningar',
      'review': 'Umfjöllun',
      'publication': 'Útgáfur',
      'biography': 'Æviágrip',
      'theater': 'Leikhús',
      'collections': 'Söfn',
      'collection-work': 'Safneign'
    } : {
      'work': 'Works',
      'group-exhibition': 'Group Exhibitions',
      'solo-exhibition': 'Solo Exhibitions',
      'review': 'Reviews',
      'publication': 'Publications',
      'biography': 'Biography',
      'theater': 'Theater',
      'collections': 'Collections',
      'collection-work': 'Museum Collection'
    };

    return labels[type] || page.charAt(0).toUpperCase() + page.slice(1);
  }

  highlightQueryAdvanced(text, query) {
    const queryLower = query.toLowerCase();
    const queryNormalized = this.normalizeIcelandic(queryLower);
    const queryWords = queryLower.split(' ').filter(word => word.length > 1);
    let highlightedText = text;
    
    // Highlight exact query first
    const exactRegex = new RegExp(`(${this.escapeRegex(query)})`, 'gi');
    highlightedText = highlightedText.replace(exactRegex, '<mark class="search-highlight-exact">$1</mark>');
    
    // Then highlight individual words
    queryWords.forEach(word => {
      const wordNormalized = this.normalizeIcelandic(word);
      const wordRegex = new RegExp(`(${this.escapeRegex(word)})`, 'gi');
      highlightedText = highlightedText.replace(wordRegex, '<mark class="search-highlight-word">$1</mark>');
    });
    
    return highlightedText;
  }

  escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  showResults() {
    this.searchResults.style.display = 'block';
  }

  hideResults() {
    this.searchResults.style.display = 'none';
  }

  showFilters() {
    if (this.searchFilters) {
      this.searchFilters.style.display = 'block';
    }
  }

  hideFilters() {
    if (this.searchFilters) {
      this.searchFilters.style.display = 'none';
    }
  }

  clearSearch() {
    // Clear both search inputs
    if (this.searchInputMobile) this.searchInputMobile.value = '';
    if (this.searchInputDesktop) this.searchInputDesktop.value = '';

    // Clear results
    this.currentResults = [];
    this.hideResults();
    this.hideFilters();

    // Clear session storage
    sessionStorage.removeItem('globalSearchState');
  }

  passesFilters(item) {
    // Type filter
    if (this.currentFilters.type !== 'all') {
      if (this.currentFilters.type === 'exhibition') {
        if (!item.type.includes('exhibition')) return false;
      } else if (this.currentFilters.type === 'collection') {
        if (item.type !== 'collections' && item.type !== 'collection-work') return false;
      } else if (this.currentFilters.type === 'work') {
        if (item.type !== 'work') return false;
      }
    }

    // Year filter
    if (item.year && item.year > this.currentFilters.year) return false;

    // Medium filter (based on content keywords)
    if (this.currentFilters.medium !== 'all') {
      const contentLower = item.content.toLowerCase();
      const mediumMap = {
        'sculpture': ['sculpture', 'sculptural'],
        'sound': ['sound', 'audio', 'voice', 'poetry'],
        'installation': ['installation', 'mixed media'],
        'performance': ['performance', 'body']
      };
      
      const mediumKeywords = mediumMap[this.currentFilters.medium];
      if (mediumKeywords && !mediumKeywords.some(keyword => contentLower.includes(keyword))) {
        return false;
      }
    }

    // Institution filter (based on content keywords)
    if (this.currentFilters.institution !== 'all') {
      const contentLower = item.content.toLowerCase();
      const institutionMap = {
        'living-art': ['living art museum', 'nýlistasafnið'],
        'national-gallery': ['national gallery', 'listasafn íslands'],
        'reykjavik-art': ['reykjavik art museum', 'reykjavík art museum', 'hafnarhús', 'kjarvalstaðir']
      };
      
      const institutionKeywords = institutionMap[this.currentFilters.institution];
      if (institutionKeywords && !institutionKeywords.some(keyword => contentLower.includes(keyword))) {
        return false;
      }
    }

    return true;
  }

  clearAllFilters() {
    // Reset filter state
    this.currentFilters = {
      type: 'all',
      year: 2024,
      medium: 'all',
      institution: 'all'
    };

    // Reset UI
    document.querySelectorAll('.filter-btn').forEach(btn => {
      btn.classList.remove('active');
      if (btn.dataset.value === 'all') {
        btn.classList.add('active');
      }
    });

    const yearFilter = document.getElementById('year-filter');
    const yearDisplay = document.getElementById('year-display');
    if (yearFilter && yearDisplay) {
      yearFilter.value = 2024;
      yearDisplay.textContent = '1960-2024';
    }

    // Re-run search if there's a query
    const query = this.searchInput.value.trim();
    if (query.length >= 2) {
      this.performSearch(query);
    }
  }

  getActiveFiltersText() {
    const activeFilters = [];
    
    if (this.currentFilters.type !== 'all') {
      activeFilters.push(this.currentFilters.type);
    }
    
    if (this.currentFilters.year < 2024) {
      activeFilters.push(`before ${this.currentFilters.year}`);
    }
    
    if (this.currentFilters.medium !== 'all') {
      activeFilters.push(this.currentFilters.medium);
    }
    
    if (this.currentFilters.institution !== 'all') {
      const institutionNames = {
        'living-art': 'Living Art Museum',
        'national-gallery': 'National Gallery',
        'reykjavik-art': 'Reykjavík Art Museum'
      };
      activeFilters.push(institutionNames[this.currentFilters.institution] || this.currentFilters.institution);
    }
    
    return activeFilters.join(', ');
  }

  saveSearchState() {
    const state = {
      query: this.getCurrentQuery(),
      filters: this.currentFilters,
      results: this.currentResults,
      timestamp: Date.now(),
      page: window.location.pathname
    };
    sessionStorage.setItem('globalSearchState', JSON.stringify(state));
  }

  restoreSearchState() {
    try {
      const saved = sessionStorage.getItem('globalSearchState');
      if (saved) {
        const state = JSON.parse(saved);
        // Only restore if saved within last 10 minutes AND we're on the same page
        if (Date.now() - state.timestamp < 10 * 60 * 1000 && state.page === window.location.pathname) {
          if (this.searchInputMobile) this.searchInputMobile.value = state.query;
          if (this.searchInputDesktop) this.searchInputDesktop.value = state.query;
          this.currentFilters = state.filters;
          this.currentResults = state.results;

          if (state.query.length >= 2) {
            this.displayResults(state.results, state.query);
            this.showResults();
            this.showFilters();
            this.updateFilterUI();
          }
        } else {
          // Clear outdated or different page search
          sessionStorage.removeItem('globalSearchState');
          if (this.searchInputMobile) this.searchInputMobile.value = '';
          if (this.searchInputDesktop) this.searchInputDesktop.value = '';
        }
      }
    } catch (error) {
      // Could not restore search state
    }
  }

  updateFilterUI() {
    // Update filter button states
    document.querySelectorAll('.filter-btn').forEach(btn => {
      btn.classList.remove('active');
      const filterType = btn.dataset.filter;
      const filterValue = btn.dataset.value;
      if (this.currentFilters[filterType] === filterValue) {
        btn.classList.add('active');
      }
    });

    // Update year slider
    const yearFilter = document.getElementById('year-filter');
    const yearDisplay = document.getElementById('year-display');
    if (yearFilter && yearDisplay) {
      yearFilter.value = this.currentFilters.year;
      yearDisplay.textContent = `1960-${this.currentFilters.year}`;
    }
  }
}

// Initialize global search when DOM is loaded
// Edge-compatible initialization with error handling
function initializeGlobalSearch() {
  try {
    if (typeof GlobalSearch !== 'undefined') {
      window.globalSearchInstance = new GlobalSearch();
    } else {
      console.error('GlobalSearch class not defined');
    }
  } catch (error) {
    console.error('Error initializing GlobalSearch:', error);
    // Fallback: show a message to use a modern browser
    const searchInputs = document.querySelectorAll('#global-search-desktop, #global-search-mobile');
    searchInputs.forEach(input => {
      if (input) {
        input.placeholder = 'Search requires a modern browser';
        input.disabled = true;
      }
    });
  }
}

// Check if DOM is already loaded (for dynamically loaded scripts)
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeGlobalSearch);
} else {
  // DOMContentLoaded has already fired - use timeout for Edge compatibility
  setTimeout(initializeGlobalSearch, 100);
}

