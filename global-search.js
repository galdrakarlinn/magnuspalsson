class GlobalSearch {
  constructor() {
    this.searchIndex = [];
    this.searchInput = null;
    this.searchResults = null;
    this.currentResults = [];
    
    this.init();
  }

  async init() {
    console.log('GlobalSearch: Initializing...');
    await this.loadSearchIndex();
    this.setupEventListeners();
    console.log('GlobalSearch: Ready!');
  }

  async loadSearchIndex() {
    try {
      const response = await fetch('search-index.json');
      const data = await response.json();
      this.searchIndex = data.searchableContent;
    } catch (error) {
      console.error('Error loading search index:', error);
      this.searchIndex = [];
    }
  }

  setupEventListeners() {
    this.searchInput = document.getElementById('global-search');
    this.searchResults = document.getElementById('search-results');
    
    if (!this.searchInput || !this.searchResults) {
      console.log('GlobalSearch: Elements not found', {
        searchInput: !!this.searchInput,
        searchResults: !!this.searchResults
      });
      return;
    }
    
    console.log('GlobalSearch: Event listeners attached');

    this.searchInput.addEventListener('input', (e) => {
      const query = e.target.value.trim();
      if (query.length >= 2) {
        this.performSearch(query);
      } else {
        this.hideResults();
      }
    });

    this.searchInput.addEventListener('focus', () => {
      if (this.currentResults.length > 0) {
        this.showResults();
      }
    });

    // Hide results when clicking outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.nav-search')) {
        this.hideResults();
      }
    });

    // Handle keyboard navigation
    this.searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.hideResults();
        this.searchInput.blur();
      } else if (e.key === 'Enter' && this.currentResults.length > 0) {
        // Go to first result on Enter
        e.preventDefault();
        window.location.href = this.currentResults[0].url;
      }
    });
  }

  performSearch(query) {
    const queryLower = query.toLowerCase();
    const queryWords = queryLower.split(' ').filter(word => word.length > 2); // Ignore very short words
    
    const results = this.searchIndex
      .map(item => {
        let score = 0;
        const titleLower = item.title.toLowerCase();
        const contentLower = item.content.toLowerCase();
        
        // Exact title match gets highest score
        if (titleLower === queryLower) {
          score += 1000;
        } else if (titleLower.includes(queryLower)) {
          score += 500;
        }
        
        // Exact content phrase match
        if (contentLower.includes(queryLower)) {
          score += 200;
        }
        
        // Significant word matches in title (avoid common words)
        const significantWords = queryWords.filter(word => 
          !['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'have', 'it', 'my', 'i'].includes(word)
        );
        
        significantWords.forEach(word => {
          if (word.length > 3) { // Only meaningful words
            if (titleLower.includes(word)) {
              score += 50;
            }
            if (contentLower.includes(word)) {
              score += 20;
            }
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
  }

  displayResults(results, query) {
    if (results.length === 0) {
      this.searchResults.innerHTML = `
        <div class="search-result">
          <div class="search-result-title">No results found</div>
          <div class="search-result-snippet">Try searching for works, exhibitions, years, or keywords</div>
        </div>
      `;
    } else {
      this.searchResults.innerHTML = results.map(result => `
        <div class="search-result" onclick="window.location.href='${result.url}'">
          <div class="search-result-title">${this.highlightQuery(result.title, query)}</div>
          <div class="search-result-snippet">${this.highlightQuery(result.snippet, query)}</div>
          <div class="search-result-page">${this.getPageLabel(result.type, result.page)} • ${result.year}</div>
        </div>
      `).join('');
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

  getPageLabel(type, page) {
    const labels = {
      'work': 'Works',
      'group-exhibition': 'Group Exhibitions', 
      'solo-exhibition': 'Solo Exhibitions',
      'review': 'Reviews',
      'publication': 'Publications',
      'biography': 'Biography',
      'theater': 'Theater'
    };
    
    return labels[type] || page.charAt(0).toUpperCase() + page.slice(1);
  }

  showResults() {
    this.searchResults.style.display = 'block';
  }

  hideResults() {
    this.searchResults.style.display = 'none';
  }
}

// Initialize global search when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.globalSearchInstance = new GlobalSearch();
});

// Global function to search for a specific work from modal
window.searchForWork = function(searchData) {
  const globalSearchInput = document.getElementById('global-search');
  if (globalSearchInput) {
    // Handle both string (legacy) and object (new) formats
    let searchTerm;
    if (typeof searchData === 'string') {
      searchTerm = searchData;
    } else {
      // Use just the primary title without parenthetical additions
      searchTerm = searchData.primary;
      
      // Special handling for specific works
      if (searchData.workId === 'thyrlulending') {
        // Just search for the simple Icelandic name
        searchTerm = 'Þyrlulending';
      }
    }
    
    globalSearchInput.value = searchTerm;
    globalSearchInput.focus();
    
    // Close the modal first
    const modal = document.getElementById('work-modal');
    if (modal) {
      modal.style.display = 'none';
    }
    
    // Small delay then trigger search and show results
    setTimeout(() => {
      // Find the GlobalSearch instance and trigger search manually
      const searchInstance = window.globalSearchInstance;
      if (searchInstance) {
        searchInstance.performSearch(searchTerm);
      } else {
        // Fallback - trigger input event
        const event = new Event('input', { bubbles: true });
        globalSearchInput.dispatchEvent(event);
      }
    }, 100);
  }
};