class WorksManager {
  constructor() {
    this.allWorks = [];
    this.filteredWorks = [];
    this.currentFilters = {
      categories: [],
      mediums: [],
      tags: [],
      decades: []
    };
    this.filterPanelOpen = false;
    this.tagCategories = null;
    this.categories = ['sculpture', 'sound', 'painting', 'print', 'book', 'performance', 'video', 'installation', 'stage'];
    this.tagTranslations = {
      animals: 'dýr', camouflage: 'dulbúningur', childhood: 'æska', collaboration: 'samstarf',
      death: 'dauði', dreams: 'draumar', fluxus: 'fluxus', folklore: 'þjóðsögur',
      humor: 'húmor', identity: 'sjálfsmynd', language: 'tungumál', letters: 'bréf',
      love: 'ást', mythology: 'goðafræði', nature: 'náttúra',
      'positive/negative space': 'jákvætt/neikvætt rými', sagas: 'sögur', social: 'samfélag',
      space: 'rými', teaching: 'kennsla', time: 'tími'
    };
    this.mediumTranslations = {
      'book art': 'bóklist', 'ceramic': 'keramík', 'choral work': 'kórverk',
      'collage': 'klippimynd', 'drawing': 'teikning', 'installation': 'innsetning',
      'painting': 'málverk', 'performance': 'gjörningur', 'photography': 'ljósmyndun',
      'play': 'leikrit', 'print': 'prentmynd', 'public art': 'almenningsverk',
      'sculpture': 'skúlptúr', 'sound art': 'hljóðlist', 'sound clearing': 'hljóðrjóður',
      'sound poetry': 'hljóðljóð', 'sound sculpture': 'hljóðskúlptúr',
      'stage design': 'leikmyndahönnun', 'text art': 'textalist',
      'video': 'vídeó', 'voice sculpture': 'raddskúlptúr', 'watercolor': 'vatnslitamynd'
    };
    this.exhibitionsData = null; // Will hold all exhibitions from exhibitions.json

    this.init();
  }

  async init() {
    // Initialize i18n if available
    if (typeof i18n !== 'undefined') {
      await i18n.init();
      // Listen for language changes and re-render
      i18n.onChange(() => this.refreshAll());
    }

    await this.loadConfig();
    await this.loadExhibitions();
    await this.loadWorks();
    this.setupEventListeners();

    // Set initial page title
    this.updatePageTitle();

    this.injectNavFilterToggle();
    this.renderFilterPanel();
    this.setupFilterToggle();
    this.renderWorks();
    this.checkForDirectWorkLink();
  }

  async loadConfig() {
    try {
      const response = await fetch('config.json');
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const config = await response.json();
      this.tagCategories = config.tagCategories;
    } catch (error) {
      console.error('Error loading config:', error);
      // Fallback to hardcoded categories if config fails to load
      this.tagCategories = {
        medium: ['sculpture', 'sound poetry', 'video', 'installation', 'audio art', 'book', 'headphones'],
        concepts: ['negative space', 'positive space', 'materializing immaterial', 'void', 'absence', 'memory', 'perception', 'vulnerability', 'shadow', 'presence', 'death', 'mortality', 'dreams', 'authenticity', 'reproduction', 'revelation', 'irony', 'time', 'place', 'nature', 'landscape', 'mountain', 'technology', 'aviation'],
        historical: ['1960s', '1970s', 'debut exhibition', 'anti-art', 'provocation', 'public reaction', 'destruction', 'dieter roth', 'frúöld', 'ásmundarsalur', 'SÚM', 'vatnsstígur', 'living art museum', 'sikorski', 'helicopter', 'collaboration', 'documentation', 'conversations', 'interviews', 'philosophy', 'existentialism', 'trilogy']
      };
    }
  }

  updatePageTitle() {
    if (typeof i18n === 'undefined') return;

    const h1 = document.querySelector('.works-header h1');
    if (h1) {
      h1.textContent = i18n.t('works');
    }
    document.title = `${i18n.t('works')} – Magnús Pálsson`;
  }

  updateWorksCount() {
    const counter = document.getElementById('works-count');
    if (!counter) return;
    const totalWorks = this.allWorks.length;
    const filteredCount = this.filteredWorks.length;
    const lang = this.getCurrentLanguage();
    const worksWord = lang === 'is' ? 'verk' : 'works';
    const ofWord = lang === 'is' ? 'af' : 'of';
    const worksTotal = lang === 'is' ? 'verkum' : 'works';
    if (filteredCount === totalWorks) {
      counter.textContent = `${totalWorks} ${worksWord}`;
    } else {
      counter.textContent = `${filteredCount} ${ofWord} ${totalWorks} ${worksTotal}`;
    }
  }

  // Helper to get current language
  getCurrentLanguage() {
    return (typeof i18n !== 'undefined' && i18n.currentLang) ? i18n.currentLang : 'en';
  }

  // Helper to get localized value from bilingual field
  getLocalizedValue(field) {
    if (!field) return '';
    if (typeof field === 'string') return field; // Legacy fallback
    const lang = this.getCurrentLanguage();
    return field[lang] || field.en || field.is || '';
  }

  // Helper to look up exhibition by ID from exhibitions.json
  lookupExhibition(exhibitionId) {
    if (!this.exhibitionsData) return null;

    // Search in both solo and group exhibitions
    const allExhibitions = [
      ...(this.exhibitionsData.solo || []),
      ...(this.exhibitionsData.group || [])
    ];

    return allExhibitions.find(ex => ex.id === exhibitionId);
  }

  // Helper to get translated work data
  getTranslatedWork(work) {
    return {
      ...work,
      title: this.getLocalizedValue(work.title),
      description: this.getLocalizedValue(work.description),
      materials: typeof work.materials === 'object' && !Array.isArray(work.materials)
        ? this.getLocalizedValue(work.materials)
        : work.materials,
      images: work.images.map(img => ({
        ...img,
        caption: this.getLocalizedValue(img.caption)
      })),
      exhibitions: work.exhibitions ? work.exhibitions.map(ex => {
        // Handle exhibition ID reference (new format)
        if (typeof ex === 'string' && this.exhibitionsData) {
          // Look up exhibition by ID
          const exhibition = this.lookupExhibition(ex);
          if (exhibition) {
            return {
              title: this.getLocalizedValue(exhibition.title),
              venue: this.getLocalizedValue(exhibition.venue),
              location: exhibition.location,
              year: exhibition.year
            };
          }
          // If not found, return the ID as-is (legacy string exhibition)
          return ex;
        }
        // Handle bilingual object format (unmatched exhibitions)
        if (typeof ex === 'object') {
          return {
            ...ex,
            title: this.getLocalizedValue(ex.title),
            venue: this.getLocalizedValue(ex.venue),
            location: ex.location,
            year: ex.year
          };
        }
        // Handle legacy string format
        return ex;
      }) : [],
      ownership: work.ownership,
      model3d: work.model3d ? {
        ...work.model3d,
        caption: this.getLocalizedValue(work.model3d.caption)
      } : null
    };
  }

  // Refresh all content when language changes
  refreshAll() {
    this.updatePageTitle();
    this.renderFilterPanel();
    this.updateFilterToggleLabel();
    this.updateWorksCount();
    this.updateWorkCardsLanguage(); // Fast update instead of full re-render
    // If modal is open, refresh it
    const modal = document.getElementById('work-modal');
    if (modal && modal.style.display === 'block') {
      const modalBody = document.getElementById('modal-body');
      const currentWorkId = modalBody.querySelector('[data-work-id]')?.dataset.workId;
      if (currentWorkId) {
        this.showWorkModal(currentWorkId);
      }
    }
  }

  // Fast language update - only changes text, doesn't rebuild DOM
  updateWorkCardsLanguage() {
    const grid = document.getElementById('works-grid');
    if (!grid) return;

    const cards = grid.querySelectorAll('.work-card');
    cards.forEach(card => {
      const workId = card.dataset.workId;
      const work = this.allWorks.find(w => w.id === workId);
      if (!work) return;

      const translatedWork = this.getTranslatedWork(work);

      // Update title in overlay
      const overlayTitle = card.querySelector('.work-overlay h3');
      if (overlayTitle) overlayTitle.textContent = translatedWork.title;

      // Update title in info section
      const infoTitle = card.querySelector('.work-info .work-title');
      if (infoTitle) infoTitle.textContent = translatedWork.title;
    });
  }

  async loadExhibitions() {
    try {
      const response = await fetch('exhibitions.json');
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      this.exhibitionsData = await response.json();
    } catch (error) {
      console.error('Error loading exhibitions:', error);
      this.exhibitionsData = { solo: [], group: [] };
    }
  }

  async loadWorks() {
    try {
      const response = await fetch('works.json');
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const data = await response.json();
      this.allWorks = data.works;
      this.filteredWorks = [...this.allWorks];
    } catch (error) {
      console.error('Error loading works:', error);
      this.showErrorMessage('Unable to load works. Please refresh the page or try again later.');
      this.allWorks = [];
      this.filteredWorks = [];
    }
  }

  showErrorMessage(message) {
    const grid = document.getElementById('works-grid');
    if (grid) {
      grid.innerHTML = `
        <div class="error-message" style="padding: 2rem; text-align: center; color: #721c24; background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 4px;">
          <h3>⚠️ Error</h3>
          <p>${message}</p>
        </div>
      `;
    }
  }

  setupEventListeners() {
    // Modal functionality
    const modal = document.getElementById('work-modal');
    const closeBtn = modal.querySelector('.close');

    const closeModal = () => {
      // Stop all videos and audio
      const videos = modal.querySelectorAll('video');
      const audios = modal.querySelectorAll('audio');

      videos.forEach(video => {
        video.pause();
        video.currentTime = 0;
      });

      audios.forEach(audio => {
        audio.pause();
        audio.currentTime = 0;
      });

      // Remove work parameter from URL
      const url = new URL(window.location);
      url.searchParams.delete('work');
      window.history.pushState({}, '', url);

      modal.style.display = 'none';
      modal.setAttribute('aria-hidden', 'true');
      this.refreshWorkCards();
    };

    closeBtn.addEventListener('click', closeModal);

    window.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeModal();
      }
    });

    // Keyboard accessibility for modal
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.style.display === 'block') {
        closeModal();
      }
    });
  }

  // Extract first valid year number from complex year strings
  parseYearNumber(year) {
    if (typeof year === 'number') return year;
    if (!year) return null;
    const str = String(year);
    const match = str.match(/\d{4}/);
    return match ? parseInt(match[0]) : null;
  }

  // Inject filter toggle links into navbar (desktop) and works-header (mobile)
  injectNavFilterToggle() {
    const labels = this.getFilterLabels();
    const toggleHandler = (e) => {
      e.preventDefault();
      const panel = document.getElementById('filter-panel');
      if (!panel) return;
      this.filterPanelOpen = !this.filterPanelOpen;
      panel.classList.toggle('open', this.filterPanelOpen);
      panel.setAttribute('aria-hidden', !this.filterPanelOpen);
      this.updateFilterToggleLabel();
    };

    // Desktop: inject into navbar next to search
    const desktopSearch = document.querySelector('.desktop-search');
    if (desktopSearch) {
      const link = document.createElement('a');
      link.href = '#';
      link.className = 'nav-filter-toggle';
      link.id = 'nav-filter-toggle';
      link.textContent = `${labels.toggle} ▾`;
      desktopSearch.parentNode.insertBefore(link, desktopSearch);
      link.addEventListener('click', toggleHandler);
    }

    // Mobile: inject into works-header next to count
    const worksHeader = document.querySelector('.works-header');
    if (worksHeader) {
      const mobileLink = document.createElement('a');
      mobileLink.href = '#';
      mobileLink.className = 'mobile-filter-toggle';
      mobileLink.id = 'mobile-filter-toggle';
      mobileLink.textContent = `${labels.toggle} ▾`;
      worksHeader.appendChild(mobileLink);
      mobileLink.addEventListener('click', toggleHandler);
    }
  }

  getCategoryLabels() {
    const lang = this.getCurrentLanguage();
    const labels = {
      en: {
        sculpture: 'Sculpture', sound: 'Sound', painting: 'Painting', print: 'Print',
        book: 'Book', performance: 'Performance', video: 'Video',
        installation: 'Installation', stage: 'Stage'
      },
      is: {
        sculpture: 'Skúlptúr', sound: 'Hljóð', painting: 'Málverk', print: 'Prent',
        book: 'Bók', performance: 'Gjörningur', video: 'Vídeó',
        installation: 'Innsetning', stage: 'Sviðslist'
      }
    };
    return labels[lang] || labels.en;
  }

  getFilterLabels() {
    const lang = this.getCurrentLanguage();
    return lang === 'is'
      ? { toggle: 'Sía verk', category: 'Flokkur', medium: 'Miðill', themes: 'Þemu', decades: 'Áratugir', clear: 'Hreinsa' }
      : { toggle: 'Filter works', category: 'Category', medium: 'Medium', themes: 'Themes', decades: 'Decades', clear: 'Clear' };
  }

  setupFilterToggle() {
    // Clear button
    const clearBtn = document.getElementById('filter-clear');
    if (clearBtn) {
      clearBtn.addEventListener('click', (e) => {
        e.preventDefault();
        this.currentFilters = { categories: [], mediums: [], tags: [], decades: [] };
        this.renderFilterPanel();
        this.updateFilterToggleLabel();
        this.filterWorks();
      });
    }

    // Close button (X)
    const closeBtn = document.getElementById('filter-close-btn');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        const panel = document.getElementById('filter-panel');
        if (panel) {
          this.filterPanelOpen = false;
          panel.classList.remove('open');
          panel.setAttribute('aria-hidden', 'true');
          this.updateFilterToggleLabel();
        }
      });
    }
  }

  updateFilterToggleLabel() {
    const labels = this.getFilterLabels();
    const activeCount = this.currentFilters.categories.length + this.currentFilters.mediums.length + this.currentFilters.tags.length + this.currentFilters.decades.length;
    const arrow = this.filterPanelOpen ? '▴' : '▾';
    const text = activeCount > 0 ? `${labels.toggle} (${activeCount}) ${arrow}` : `${labels.toggle} ${arrow}`;

    // Update all toggles (desktop nav + mobile header)
    const navToggle = document.getElementById('nav-filter-toggle');
    if (navToggle) navToggle.textContent = text;
    const mobileToggle = document.getElementById('mobile-filter-toggle');
    if (mobileToggle) mobileToggle.textContent = text;
  }

  renderFilterPanel() {
    const catLabels = this.getCategoryLabels();
    const labels = this.getFilterLabels();
    const lang = this.getCurrentLanguage();

    // Categories
    const catContainer = document.getElementById('filter-categories');
    if (catContainer) {
      catContainer.innerHTML = `
        <span class="filter-label">${labels.category}</span>
        <div class="filter-pills">
          ${this.categories.map(cat => `
            <button class="filter-pill${this.currentFilters.categories.includes(cat) ? ' active' : ''}"
                    data-filter="category" data-value="${cat}">${catLabels[cat] || cat}</button>
          `).join('')}
        </div>
      `;
    }

    // Medium — collect from actual works data (medium.en arrays)
    const allMediums = [...new Set(this.allWorks.flatMap(w => {
      if (!w.medium) return [];
      const m = w.medium.en || w.medium;
      return Array.isArray(m) ? m : [];
    }))].sort();
    const medContainer = document.getElementById('filter-mediums');
    if (medContainer && allMediums.length > 0) {
      medContainer.innerHTML = `
        <span class="filter-label">${labels.medium}</span>
        <div class="filter-pills">
          ${allMediums.map(m => {
            const display = lang === 'is' ? (this.mediumTranslations[m] || m) : m;
            return `<button class="filter-pill${this.currentFilters.mediums.includes(m) ? ' active' : ''}"
                    data-filter="medium" data-value="${m}">${display}</button>`;
          }).join('')}
        </div>
      `;
    }

    // Tags — collect from actual works data, translate for Icelandic
    const allTags = [...new Set(this.allWorks.flatMap(w => w.tags || []))].sort();
    const tagContainer = document.getElementById('filter-tags');
    if (tagContainer && allTags.length > 0) {
      tagContainer.innerHTML = `
        <span class="filter-label">${labels.themes}</span>
        <div class="filter-pills">
          ${allTags.map(tag => {
            const display = lang === 'is' ? (this.tagTranslations[tag] || tag) : tag;
            return `<button class="filter-pill${this.currentFilters.tags.includes(tag) ? ' active' : ''}"
                    data-filter="tag" data-value="${tag}">${display}</button>`;
          }).join('')}
        </div>
      `;
    }

    // Decades — parse year safely, filter out NaN
    const decades = [...new Set(this.allWorks.map(w => {
      const y = this.parseYearNumber(w.year);
      return y ? Math.floor(y / 10) * 10 : null;
    }).filter(d => d !== null))].sort();
    const decContainer = document.getElementById('filter-decades');
    if (decContainer) {
      decContainer.innerHTML = `
        <span class="filter-label">${labels.decades}</span>
        <div class="filter-pills">
          ${decades.map(d => `
            <button class="filter-pill${this.currentFilters.decades.includes(d) ? ' active' : ''}"
                    data-filter="decade" data-value="${d}">${d}s</button>
          `).join('')}
        </div>
      `;
    }

    // Clear label
    const clearBtn = document.getElementById('filter-clear');
    if (clearBtn) clearBtn.textContent = labels.clear;

    // Attach pill click handlers
    document.querySelectorAll('#filter-panel .filter-pill').forEach(pill => {
      pill.addEventListener('click', () => {
        const type = pill.dataset.filter;
        const value = type === 'decade' ? parseInt(pill.dataset.value) : pill.dataset.value;

        let arr;
        if (type === 'category') arr = this.currentFilters.categories;
        else if (type === 'medium') arr = this.currentFilters.mediums;
        else if (type === 'tag') arr = this.currentFilters.tags;
        else arr = this.currentFilters.decades;

        const idx = arr.indexOf(value);
        if (idx >= 0) {
          arr.splice(idx, 1);
          pill.classList.remove('active');
        } else {
          arr.push(value);
          pill.classList.add('active');
        }

        this.updateFilterToggleLabel();
        this.filterWorks();
      });
    });
  }

  filterWorks() {
    this.filteredWorks = this.allWorks.filter(work => {
      // Category filter (OR within group)
      if (this.currentFilters.categories.length > 0) {
        const workCats = Array.isArray(work.category) ? work.category : [];
        if (!this.currentFilters.categories.some(c => workCats.includes(c))) return false;
      }

      // Medium filter (OR within group)
      if (this.currentFilters.mediums.length > 0) {
        const workMediums = work.medium ? (Array.isArray(work.medium.en) ? work.medium.en : []) : [];
        if (!this.currentFilters.mediums.some(m => workMediums.includes(m))) return false;
      }

      // Tag filter (OR within group)
      if (this.currentFilters.tags.length > 0) {
        const workTags = work.tags || [];
        if (!this.currentFilters.tags.some(t => workTags.includes(t))) return false;
      }

      // Decade filter (OR within group)
      if (this.currentFilters.decades.length > 0) {
        const y = this.parseYearNumber(work.year);
        if (!y) return false;
        const workDecade = Math.floor(y / 10) * 10;
        if (!this.currentFilters.decades.includes(workDecade)) return false;
      }

      return true;
    });

    this.renderWorks();
  }

  renderWorks() {
    const grid = document.getElementById('works-grid');
    if (!grid) {
      console.error('Works grid element not found');
      return;
    }

    this.updateWorksCount();

    if (this.filteredWorks.length === 0) {
      const lang = this.getCurrentLanguage();
      const noResults = lang === 'is' ? 'Engin verk fundust sem passa við leitarskilyrði.' : 'No works found matching your criteria.';
      grid.innerHTML = `<p class="no-results">${noResults}</p>`;
      return;
    }

    grid.innerHTML = this.filteredWorks.map(work => {
      const translatedWork = this.getTranslatedWork(work);
      const firstMedia = translatedWork.images.length > 0 ? translatedWork.images[0] : null;
      const isVideo = firstMedia && this.isVideoFile(firstMedia.url);
      const isAudio = firstMedia && this.isAudioFile(firstMedia.url);
      
      // For audio works, try to find a visual image to display instead
      let displayMedia = firstMedia;
      if (isAudio && translatedWork.images.length > 1) {
        displayMedia = translatedWork.images.find(img => !this.isAudioFile(img.url)) || firstMedia;
      }
      
      return `
        <div class="work-card" data-work-id="${work.id}">
          <div class="work-image">
            ${firstMedia ? (
              isVideo ? 
                `<video src="${firstMedia.url}" poster="${firstMedia.thumbnail || ''}" muted loop preload="metadata">
                   <source src="${firstMedia.url}" type="video/mp4">
                   Your browser does not support video.
                 </video>
                 <div class="video-indicator">▶</div>` :
              isAudio && displayMedia !== firstMedia ?
                `<img src="${displayMedia.url}" alt="${translatedWork.title}" loading="lazy" />
                 <div class="audio-indicator">♪</div>` :
              isAudio ?
                `<div class="audio-placeholder">
                   <div class="audio-icon">♪</div>
                   <div class="audio-title">${translatedWork.title}</div>
                 </div>` :
                `<img src="${firstMedia.url}" alt="${translatedWork.title}" loading="lazy" />`
            ) : '<div class="no-image">No media available</div>'}
            <div class="work-overlay">
              <h3>${translatedWork.title}</h3>
              <p>${translatedWork.year}</p>
              <div class="work-tags">
                ${translatedWork.tags.slice(0, 3).map(tag => `<span class="tag">${tag}</span>`).join('')}
              </div>
            </div>
          </div>
          <div class="work-info">
            <h3 class="work-title">${translatedWork.title}</h3>
            <p class="work-year">${translatedWork.year}</p>
          </div>
        </div>
      `;
    }).join('');

    // Add click listeners to work cards
    grid.querySelectorAll('.work-card').forEach(card => {
      card.addEventListener('click', (e) => {
        const workId = card.dataset.workId;
        this.showWorkModal(workId);
      });

      // Add hover play for videos
      const video = card.querySelector('video');
      if (video) {
        card.addEventListener('mouseenter', () => {
          video.play().catch(() => {}); // Ignore play errors
        });
        card.addEventListener('mouseleave', () => {
          video.pause();
        });
      }
    });
  }

  isVideoFile(url) {
    const videoExtensions = ['.mp4', '.webm', '.ogg', '.mov', '.avi'];
    return videoExtensions.some(ext => url.toLowerCase().includes(ext));
  }

  isAudioFile(url) {
    const audioExtensions = ['.mp3', '.wav', '.aiff', '.m4a', '.flac'];
    return audioExtensions.some(ext => url.toLowerCase().includes(ext));
  }

  isPDFFile(url) {
    return url.toLowerCase().includes('.pdf');
  }

  // Helper functions for optimized images
  getThumbPath(url) {
    // Skip non-images (video, audio, PDF)
    if (this.isVideoFile(url) || this.isAudioFile(url) || this.isPDFFile(url)) {
      return url;
    }

    // If URL already contains '/thumbs/' or ends with '-thumb.jpg', return as-is
    if (url.includes('/thumbs/') || url.endsWith('-thumb.jpg')) {
      return url;
    }

    // Check if this is a medium path that should be converted to thumbs
    if (url.includes('/medium/')) {
      const parts = url.split('/');
      const fileName = parts[parts.length - 1];

      // Handle medium files: extract base name without -medium suffix
      let fileBase;
      if (fileName.includes('-medium.')) {
        fileBase = fileName.replace('-medium.', '.');
        fileBase = fileBase.substring(0, fileBase.lastIndexOf('.'));
      } else {
        fileBase = fileName.substring(0, fileName.lastIndexOf('.'));
      }

      // Replace 'medium' with 'thumbs' in path, removing the filename first
      const pathParts = parts.slice(0, -1); // Remove filename
      for (let i = 0; i < pathParts.length; i++) {
        if (pathParts[i] === 'medium') {
          pathParts[i] = 'thumbs';
          break;
        }
      }

      return pathParts.join('/') + '/' + fileBase + '-thumb.jpg';
    }

    // For older works without medium/thumbs structure, try standard conversion
    const parts = url.split('/');
    if (parts.length >= 3) {
      const fileName = parts[parts.length - 1];
      const fileBase = fileName.substring(0, fileName.lastIndexOf('.'));

      // Return the legacy path (this maintains old behavior for non-optimized works)
      return parts.slice(0, -1).join('/') + '/' + fileBase + '-thumb.jpg';
    }
    return url;
  }

  getMediumPath(url) {
    // Skip non-images (video, audio, PDF)
    if (this.isVideoFile(url) || this.isAudioFile(url) || this.isPDFFile(url)) {
      return url;
    }

    // If URL already contains '/medium/' or ends with '-medium.jpg', return as-is
    if (url.includes('/medium/') || url.endsWith('-medium.jpg')) {
      return url;
    }

    // Convert image path to medium version
    const parts = url.split('/');
    if (parts.length >= 3) {
      const fileName = parts[parts.length - 1];
      const fileBase = fileName.substring(0, fileName.lastIndexOf('.'));
      parts[parts.length - 1] = 'medium';
      return parts.join('/') + '/' + fileBase + '-medium.jpg';
    }
    return url;
  }


  getOwnershipInfo(workId) {
    // Legacy function - ownership info now stored in works.json
    // Keeping this for backwards compatibility
    return null;
  }

  showWorkModal(workId) {
    const work = this.allWorks.find(w => w.id === workId);
    if (!work) return;

    // Update URL with work parameter
    const url = new URL(window.location);
    url.searchParams.set('work', workId);
    window.history.pushState({}, '', url);

    // Get translated work data
    const translatedWork = this.getTranslatedWork(work);

    // Use ownership from work.json if available, otherwise fall back to legacy map
    const ownershipRaw = translatedWork.ownership || this.getOwnershipInfo(workId);
    // Resolve localized owner name
    const ownership = ownershipRaw ? {
      ...ownershipRaw,
      owner: (this.getCurrentLanguage() === 'is' && ownershipRaw.owner_is) ? ownershipRaw.owner_is : (ownershipRaw.owner_en || ownershipRaw.owner)
    } : null;
    const modalBody = document.getElementById('modal-body');
    
    // Reset modal scroll position to top
    const modalContent = document.querySelector('.modal-content');
    if (modalContent) {
      modalContent.scrollTop = 0;
    }
    modalBody.innerHTML = `
      <div class="modal-header-sticky">
        <h2 class="modal-work-title">${translatedWork.title}</h2>
        <span class="work-year-header">${translatedWork.year}</span>
      </div>
      <div class="work-detail" data-work-id="${workId}">
        <div class="work-images">
          ${translatedWork.images.map(media => {
            const isVideo = this.isVideoFile(media.url);
            const isAudio = this.isAudioFile(media.url);
            const isPDF = this.isPDFFile(media.url);
            return isVideo ? `
              <video controls width="100%">
                <source src="${media.url}" type="video/mp4">
                Your browser does not support video.
              </video>
              <p class="image-caption">${media.caption}</p>
            ` : isAudio ? `
              <audio controls width="100%">
                <source src="${media.url}" type="audio/mpeg">
                Your browser does not support audio.
              </audio>
              <p class="image-caption">${media.caption}</p>
            ` : isPDF ? `
              <div class="pdf-download">
                <a href="${media.url}" target="_blank" download>
                  <div class="pdf-icon">📄</div>
                  <div class="pdf-title">Download PDF</div>
                </a>
              </div>
              <p class="image-caption">${media.caption}</p>
            ` : `
              <img src="${this.getMediumPath(media.url)}" alt="${media.caption}" />
              <p class="image-caption">${media.caption}</p>
              ${media.photographer || media.copyright ? `
                <p class="photo-credit">
                  ${media.photographer ? `Photo: ${media.photographer}` : ''}
                  ${media.photographer && media.copyright ? '<br>' : ''}
                  ${media.copyright ? `${media.copyright}` : ''}
                </p>
              ` : ''}
            `;
          }).join('')}
          ${translatedWork.model3d ? `
            <div class="model-viewer-container">
              <model-viewer
                src="${translatedWork.model3d.url}"
                alt="${translatedWork.title} - 3D model"
                camera-controls
                touch-action="pan-y"
                auto-rotate
                shadow-intensity="0.5"
                exposure="0.5"
                environment-image="neutral"
                tone-mapping="commerce"
              ></model-viewer>
              <p class="model-caption">${translatedWork.model3d.caption}</p>
              ${translatedWork.model3d.credit ? `<p class="model-credit">${translatedWork.model3d.credit}</p>` : ''}
            </div>
          ` : ''}
        </div>
        <div class="work-info">
          <h2>${translatedWork.title}</h2>
          ${work.alternativeTitles ? `
            <p class="work-alt-titles">
              ${Object.entries(work.alternativeTitles).map(([lang, title]) => {
                const langNames = { de: 'German', en: 'English', is: 'Icelandic', fr: 'French' };
                return `<em>${langNames[lang] || lang}: ${title}</em>`;
              }).join(' · ')}
            </p>
          ` : ''}
          <p class="work-year">${translatedWork.year}${work.dimensions ? ` · ${work.dimensions}` : ''}</p>
          <p class="work-description">${translatedWork.description}</p>
          ${translatedWork.materials && translatedWork.materials.length > 0 ? `
            <p class="work-materials"><strong>${i18n.t('materials')}:</strong> ${Array.isArray(translatedWork.materials) ? translatedWork.materials.join(', ') : translatedWork.materials}</p>
          ` : ''}
          ${work.collaboration ? `
            <div class="collaboration-info">
              <p class="work-collaboration"><strong>${this.getCurrentLanguage() === 'is' ? 'Samstarf' : 'Collaboration'}:</strong>
                ${work.collaboration.type === 'student' ? (this.getCurrentLanguage() === 'is' ? 'Nemendaverk' : 'Student work') : work.collaboration.type}
                ${work.collaboration.institution ? ` · ${work.collaboration.institution}` : ''}
                ${work.collaboration.location ? `, ${work.collaboration.location}` : ''}
                ${work.collaboration.producer ? ` · ${this.getCurrentLanguage() === 'is' ? 'Framleiðandi' : 'Producer'}: ${work.collaboration.producer}` : ''}
              </p>
            </div>
          ` : ''}
          ${work.source ? `
            <div class="source-info">
              <p class="source-attribution"><em>Source: <a href="${work.source.url}" target="_blank">${work.source.name}</a></em></p>
            </div>
          ` : ''}
          ${ownership ? `
            <div class="ownership-info">
              <p><strong>${i18n.t('ownedBy')}</strong> ${ownership.url ? `<a href="${ownership.url}" target="_blank">${ownership.owner}</a>` : ownership.owner}</p>
              ${ownership.catalogNumber ? `<p class="catalog-number">${i18n.t('catalog')}: ${ownership.catalogNumber}</p>` : ''}
              ${ownership.notes ? `<p class="ownership-notes">${ownership.notes}</p>` : ''}
              ${ownership.altTitle ? `<p class="alt-title">${i18n.t('alsoListedAs')}: "${ownership.altTitle}"</p>` : ''}
              ${ownership.url ? `<p><a href="collections.html">${i18n.t('viewCollectionsPage')} →</a></p>` : ''}
            </div>
          ` : ''}
          <div class="work-tags">
            ${translatedWork.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
          </div>
          ${translatedWork.collaborators && translatedWork.collaborators.length > 0 ? `
            <div class="collaborators">
              <h3>Collaborators</h3>
              <ul>
                ${translatedWork.collaborators.map(collab => `
                  <li><strong>${collab.name}</strong> - ${collab.role}${collab.description ? `: ${collab.description}` : ''}</li>
                `).join('')}
              </ul>
            </div>
          ` : ''}
          ${translatedWork.exhibitions.length > 0 ? `
            <div class="exhibitions">
              <h3>Exhibitions</h3>
              <ul>
                ${translatedWork.exhibitions.map(ex => {
                  // Handle both string and object format
                  if (typeof ex === 'string') return `<li>${ex}</li>`;
                  return `<li>${ex.title}, ${ex.venue}, ${ex.location || ex.city} (${ex.year})</li>`;
                }).join('')}
              </ul>
            </div>
          ` : ''}
        </div>
      </div>
    `;

    const modal = document.getElementById('work-modal');
    modal.style.display = 'block';
    modal.setAttribute('aria-hidden', 'false');
  }


  checkForDirectWorkLink() {
    const urlParams = new URLSearchParams(window.location.search);
    const workId = urlParams.get('work');
    
    if (workId) {
      // Small delay to ensure everything is rendered
      setTimeout(() => {
        this.showWorkModal(workId);
      }, 100);
    }
  }

  refreshWorkCards() {
    // Force complete re-render of the works grid to fix rendering issues
    setTimeout(() => {
      this.renderWorks();
    }, 100);
  }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  if (!window.worksManagerInstance) {
    window.worksManagerInstance = new WorksManager();
  }
});