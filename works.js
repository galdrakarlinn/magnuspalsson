class WorksManager {
  constructor() {
    this.allWorks = [];
    this.filteredWorks = [];
    this.currentFilters = {
      decades: [],
      tags: [],
      statuses: []
    };
    this.tagCategories = null;

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
    await this.loadWorks();
    this.setupEventListeners();
    this.setupCategoryCollapse();

    // Set initial page title
    this.updatePageTitle();

    this.renderWorks();
    this.renderTagFilters();
    this.renderDecades();
    this.renderStatusFilters();
    this.setupClearButton(); // Setup clear button AFTER filters are rendered
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

  // Helper to get translated work data
  getTranslatedWork(work) {
    if (typeof i18n === 'undefined') return work;

    const translation = i18n.getWork(work.id);
    return {
      ...work,
      title: translation.title || work.title,
      description: translation.description || work.description,
      materials: translation.materials || work.materials,
      exhibitions: translation.exhibitions || work.exhibitions,
      images: work.images.map((img, idx) => ({
        ...img,
        caption: translation.images?.[idx]?.caption || img.caption
      })),
      ownership: work.ownership ? {
        ...work.ownership,
        owner: translation.ownership?.owner || work.ownership.owner,
        location: translation.ownership?.location || work.ownership.location
      } : null
    };
  }

  // Refresh all content when language changes
  refreshAll() {
    this.updatePageTitle();
    this.renderWorks();
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

  setupCategoryCollapse() {
    // Load pinned states from localStorage
    const pinnedCategories = JSON.parse(localStorage.getItem('pinnedCategories') || '[]');
    
    document.querySelectorAll('.filter-category').forEach(category => {
      const categoryName = category.dataset.category;
      const header = category.querySelector('.category-header');
      const content = category.querySelector('.category-content');
      const expandBtn = category.querySelector('.expand-btn');
      const pinBtn = category.querySelector('.pin-btn');
      
      // Set initial pinned state
      if (pinnedCategories.includes(categoryName)) {
        category.classList.add('pinned');
        content.classList.remove('collapsed');
        expandBtn.textContent = '▲';
        pinBtn.style.opacity = '1';
      }
      
      // Header click to expand/collapse
      header.addEventListener('click', (e) => {
        // Don't trigger on pin button clicks
        if (e.target === pinBtn) return;

        const isCollapsed = content.classList.contains('collapsed');
        const isPinned = category.classList.contains('pinned');

        if (isCollapsed) {
          // Expand
          content.classList.remove('collapsed');
          expandBtn.textContent = '▲';
          expandBtn.setAttribute('aria-expanded', 'true');

          // If not pinned, auto-collapse other categories
          if (!isPinned) {
            document.querySelectorAll('.filter-category:not(.pinned)').forEach(otherCategory => {
              if (otherCategory !== category) {
                const otherContent = otherCategory.querySelector('.category-content');
                const otherExpandBtn = otherCategory.querySelector('.expand-btn');
                otherContent.classList.add('collapsed');
                otherExpandBtn.textContent = '▼';
                otherExpandBtn.setAttribute('aria-expanded', 'false');
              }
            });
          }
        } else {
          // Collapse (only if not pinned)
          if (!isPinned) {
            content.classList.add('collapsed');
            expandBtn.textContent = '▼';
            expandBtn.setAttribute('aria-expanded', 'false');
          }
        }
      });
      
      // Pin button functionality
      pinBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const isPinned = category.classList.contains('pinned');
        
        if (isPinned) {
          // Unpin
          category.classList.remove('pinned');
          pinBtn.style.opacity = '0.3';
          const updatedPinned = pinnedCategories.filter(name => name !== categoryName);
          localStorage.setItem('pinnedCategories', JSON.stringify(updatedPinned));
        } else {
          // Pin
          category.classList.add('pinned');
          content.classList.remove('collapsed');
          expandBtn.textContent = '▲';
          pinBtn.style.opacity = '1';
          const updatedPinned = [...pinnedCategories, categoryName];
          localStorage.setItem('pinnedCategories', JSON.stringify(updatedPinned));
        }
      });
    });
  }

  filterWorks() {
    this.filteredWorks = this.allWorks.filter(work => {
      // Decade filter
      if (this.currentFilters.decades.length > 0) {
        const workDecade = Math.floor(work.year / 10) * 10;
        if (!this.currentFilters.decades.includes(workDecade)) return false;
      }

      // Tags filter
      if (this.currentFilters.tags.length > 0) {
        const hasTag = this.currentFilters.tags.some(tag => work.tags.includes(tag));
        if (!hasTag) return false;
      }

      // Status filter
      if (this.currentFilters.statuses.length > 0) {
        const workStatus = work.status || 'not-set';
        if (!this.currentFilters.statuses.includes(workStatus)) return false;
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

    const counter = document.getElementById('works-count');

    // Update count display
    if (counter) {
      const totalWorks = this.allWorks.length;
      const filteredCount = this.filteredWorks.length;
      if (filteredCount === totalWorks) {
        counter.textContent = `${totalWorks} works`;
      } else {
        counter.textContent = `${filteredCount} of ${totalWorks} works`;
      }
    }

    if (this.filteredWorks.length === 0) {
      grid.innerHTML = '<p class="no-results">No works found matching your criteria.</p>';
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
                `<img src="${this.getThumbPath(displayMedia.thumbnail || displayMedia.url)}" alt="${translatedWork.title}" loading="lazy" />
                 <div class="audio-indicator">♪</div>` :
              isAudio ?
                `<div class="audio-placeholder">
                   <div class="audio-icon">♪</div>
                   <div class="audio-title">${translatedWork.title}</div>
                 </div>` :
                `<img src="${this.getThumbPath(firstMedia.thumbnail || firstMedia.url)}" alt="${translatedWork.title}" loading="lazy" />`
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

  renderTagFilters() {
    if (!this.tagCategories) {
      console.error('Tag categories not loaded');
      return;
    }

    const allTags = [...new Set(this.allWorks.flatMap(work => work.tags))].sort();

    // Render medium tags
    this.renderTagCategory('medium-tags', allTags.filter(tag => this.tagCategories.medium.includes(tag)));

    // Render concept tags
    this.renderTagCategory('concept-tags', allTags.filter(tag => this.tagCategories.concepts.includes(tag)));

    // Render historical tags
    this.renderTagCategory('historical-tags', allTags.filter(tag => this.tagCategories.historical.includes(tag)));

    // Render remaining uncategorized tags in concepts
    const categorizedTags = [...this.tagCategories.medium, ...this.tagCategories.concepts, ...this.tagCategories.historical];
    const uncategorized = allTags.filter(tag => !categorizedTags.includes(tag));
    if (uncategorized.length > 0) {
      this.renderTagCategory('concept-tags', [...allTags.filter(tag => this.tagCategories.concepts.includes(tag)), ...uncategorized]);
    }
  }

  renderTagCategory(containerId, tags) {
    const container = document.getElementById(containerId);
    if (!container || tags.length === 0) return;
    
    container.innerHTML = tags.map(tag => `
      <label class="tag-checkbox" for="tag-${tag.replace(/\s+/g, '-')}">
        <input type="checkbox" id="tag-${tag.replace(/\s+/g, '-')}" value="${tag}" title="${tag}" />
        <span>${tag}</span>
      </label>
    `).join('');

    // Add event listeners to tag checkboxes
    container.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
      checkbox.addEventListener('change', (e) => {
        if (e.target.checked) {
          this.currentFilters.tags.push(e.target.value);
        } else {
          this.currentFilters.tags = this.currentFilters.tags.filter(tag => tag !== e.target.value);
        }
        this.filterWorks();
      });
    });
  }

  renderDecades() {
    const container = document.getElementById('decade-tags');
    if (!container) return;

    // Get all unique decades from works
    const decades = [...new Set(this.allWorks.map(work => Math.floor(work.year / 10) * 10))].sort();

    container.innerHTML = decades.map(decade => `
      <label class="tag-checkbox" for="decade-${decade}">
        <input type="checkbox" id="decade-${decade}" value="${decade}" title="${decade}s" />
        <span>${decade}s</span>
      </label>
    `).join('');

    // Add event listeners to decade checkboxes
    container.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
      checkbox.addEventListener('change', (e) => {
        if (e.target.checked) {
          this.currentFilters.decades.push(parseInt(e.target.value));
        } else {
          this.currentFilters.decades = this.currentFilters.decades.filter(decade => decade !== parseInt(e.target.value));
        }
        this.filterWorks();
      });
    });
  }

  renderStatusFilters() {
    const container = document.getElementById('status-tags');
    if (!container) return;

    // Define status options
    const statuses = [
      { value: 'complete', label: 'Complete' },
      { value: 'needs-review', label: 'Needs Review' },
      { value: 'incomplete', label: 'Incomplete' },
      { value: 'draft', label: 'Draft' },
      { value: 'not-set', label: 'Not Set' }
    ];

    container.innerHTML = statuses.map(status => `
      <label class="tag-checkbox" for="status-${status.value}">
        <input type="checkbox" id="status-${status.value}" value="${status.value}" title="${status.label}" />
        <span>${status.label}</span>
      </label>
    `).join('');

    // Add event listeners to status checkboxes
    container.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
      checkbox.addEventListener('change', (e) => {
        if (e.target.checked) {
          this.currentFilters.statuses.push(e.target.value);
        } else {
          this.currentFilters.statuses = this.currentFilters.statuses.filter(s => s !== e.target.value);
        }
        this.filterWorks();
      });
    });
  }

  setupClearButton() {
    const clearFilters = document.getElementById('clear-works-filters');
    
    if (clearFilters) {
      clearFilters.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        this.clearAllFilters();
      });
    }
  }

  getOwnershipInfo(workId) {
    // Legacy function - ownership info now stored in works.json
    // Keeping this for backwards compatibility
    return null;
  }

  showWorkModal(workId) {
    const work = this.allWorks.find(w => w.id === workId);
    if (!work) return;

    // Get translated work data
    const translatedWork = this.getTranslatedWork(work);

    // Use ownership from work.json if available, otherwise fall back to legacy map
    const ownership = translatedWork.ownership || this.getOwnershipInfo(workId);
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
                  ${media.photographer ? `Photo: ${media.photographer}${media.year ? `, ${media.year}` : ''}` : ''}
                  ${media.photographer && media.copyright ? '<br>' : ''}
                  ${media.copyright ? `${media.copyright}` : ''}
                </p>
              ` : ''}
            `;
          }).join('')}
        </div>
        <div class="work-info">
          <h2>${translatedWork.title}</h2>
          <p class="work-year">${translatedWork.year}</p>
          <p class="work-description">${translatedWork.description}</p>
          ${ownership ? `
            <div class="ownership-info">
              <h3>Collection</h3>
              <p><strong>Owned by:</strong> ${ownership.url ? `<a href="${ownership.url}" target="_blank">${ownership.owner}</a>` : ownership.owner}</p>
              ${ownership.catalogNumber ? `<p class="catalog-number">Catalog: ${ownership.catalogNumber}</p>` : ''}
              ${ownership.notes ? `<p class="ownership-notes">${ownership.notes}</p>` : ''}
              ${ownership.altTitle ? `<p class="alt-title">Also listed as: "${ownership.altTitle}"</p>` : ''}
              <p><a href="collections.html">View full collections page →</a></p>
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
                ${translatedWork.exhibitions.map(ex => `
                  <li>${ex.title}, ${ex.venue}, ${ex.city} (${ex.year})</li>
                `).join('')}
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

  clearAllFilters() {
    // Reset the filter state
    this.currentFilters.tags = [];
    this.currentFilters.decades = [];
    this.currentFilters.statuses = [];

    // Uncheck all checkboxes visually
    const allCheckboxes = document.querySelectorAll('.filter-sidebar input[type="checkbox"]');
    allCheckboxes.forEach(cb => {
      if (cb.checked) {
        cb.checked = false;
      }
    });

    // Collapse all unpinned categories after clearing
    document.querySelectorAll('.filter-category:not(.pinned)').forEach(category => {
      const content = category.querySelector('.category-content');
      const expandBtn = category.querySelector('.expand-btn');
      if (content && expandBtn) {
        content.classList.add('collapsed');
        expandBtn.textContent = '▼';
      }
    });

    // Re-render with empty filters
    this.filterWorks();
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