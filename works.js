class WorksManager {
  constructor() {
    this.allWorks = [];
    this.filteredWorks = [];
    this.currentFilters = {
      search: '',
      yearRange: { min: 1960, max: 2024 },
      tags: []
    };
    
    this.init();
  }

  async init() {
    await this.loadWorks();
    this.setupEventListeners();
    this.renderWorks();
    this.renderTagFilters();
    this.checkForDirectWorkLink();
  }

  async loadWorks() {
    try {
      const response = await fetch('works.json');
      const data = await response.json();
      this.allWorks = data.works;
      this.filteredWorks = [...this.allWorks];
    } catch (error) {
      console.error('Error loading works:', error);
      this.allWorks = [];
      this.filteredWorks = [];
    }
  }

  setupEventListeners() {
    // Search input
    const searchInput = document.getElementById('search-input');
    searchInput.addEventListener('input', (e) => {
      this.currentFilters.search = e.target.value.toLowerCase();
      this.filterWorks();
    });

    // Year range slider
    const yearRange = document.getElementById('year-range');
    yearRange.addEventListener('input', (e) => {
      this.currentFilters.yearRange.max = parseInt(e.target.value);
      this.filterWorks();
    });

    // Clear filters
    const clearFilters = document.getElementById('clear-filters');
    clearFilters.addEventListener('click', () => {
      this.clearAllFilters();
    });

    // Modal functionality
    const modal = document.getElementById('work-modal');
    const closeBtn = modal.querySelector('.close');
    
    closeBtn.addEventListener('click', () => {
      modal.style.display = 'none';
      this.refreshWorkCards();
    });
    
    window.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.style.display = 'none';
        this.refreshWorkCards();
      }
    });
  }

  filterWorks() {
    this.filteredWorks = this.allWorks.filter(work => {
      // Search filter
      if (this.currentFilters.search) {
        const searchMatch = work.searchText.toLowerCase().includes(this.currentFilters.search) ||
                           work.title.toLowerCase().includes(this.currentFilters.search) ||
                           work.description.toLowerCase().includes(this.currentFilters.search);
        if (!searchMatch) return false;
      }

      // Year filter
      if (work.year > this.currentFilters.yearRange.max) return false;

      // Tags filter
      if (this.currentFilters.tags.length > 0) {
        const hasTag = this.currentFilters.tags.some(tag => work.tags.includes(tag));
        if (!hasTag) return false;
      }

      return true;
    });

    this.renderWorks();
  }

  renderWorks() {
    const grid = document.getElementById('works-grid');
    
    if (this.filteredWorks.length === 0) {
      grid.innerHTML = '<p class="no-results">No works found matching your criteria.</p>';
      return;
    }

    grid.innerHTML = this.filteredWorks.map(work => {
      const firstMedia = work.images.length > 0 ? work.images[0] : null;
      const isVideo = firstMedia && this.isVideoFile(firstMedia.url);
      const isAudio = firstMedia && this.isAudioFile(firstMedia.url);
      
      // For audio works, try to find a visual image to display instead
      let displayMedia = firstMedia;
      if (isAudio && work.images.length > 1) {
        displayMedia = work.images.find(img => !this.isAudioFile(img.url)) || firstMedia;
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
                `<img src="${this.getThumbPath(displayMedia.thumbnail || displayMedia.url)}" alt="${work.title}" loading="lazy" />
                 <div class="audio-indicator">♪</div>` :
              isAudio ?
                `<div class="audio-placeholder">
                   <div class="audio-icon">♪</div>
                   <div class="audio-title">${work.title}</div>
                 </div>` :
                `<img src="${this.getThumbPath(firstMedia.thumbnail || firstMedia.url)}" alt="${work.title}" loading="lazy" />`
            ) : '<div class="no-image">No media available</div>'}
            <div class="work-overlay">
              <h3>${work.title}</h3>
              <p>${work.year}</p>
              <div class="work-tags">
                ${work.tags.slice(0, 3).map(tag => `<span class="tag">${tag}</span>`).join('')}
              </div>
            </div>
          </div>
          <div class="work-info">
            <h3 class="work-title">${work.title}</h3>
            <p class="work-year">${work.year}</p>
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
    
    // Convert image path to thumbnail version
    const parts = url.split('/');
    if (parts.length >= 3) {
      const fileName = parts[parts.length - 1];
      const fileBase = fileName.substring(0, fileName.lastIndexOf('.'));
      parts[parts.length - 1] = 'thumbs';
      return parts.join('/') + '/' + fileBase + '-thumb.jpg';
    }
    return url;
  }

  getMediumPath(url) {
    // Skip non-images (video, audio, PDF)
    if (this.isVideoFile(url) || this.isAudioFile(url) || this.isPDFFile(url)) {
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
    const tagsFilter = document.getElementById('tags-filter');
    const allTags = [...new Set(this.allWorks.flatMap(work => work.tags))].sort();
    
    tagsFilter.innerHTML = allTags.map(tag => `
      <label class="tag-checkbox">
        <input type="checkbox" value="${tag}" />
        <span>${tag}</span>
      </label>
    `).join('');

    // Add event listeners to tag checkboxes
    tagsFilter.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
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

  getOwnershipInfo(workId) {
    const ownershipMap = {
      'bestu_stykkin': {
        owner: 'The Living Art Museum (Nýlistasafnið)',
        url: 'https://sarpur.is/Adfang.aspx?AdfangID=1396243',
        catalogNumber: 'N-277'
      },
      'vidtol_um_daudann_2011': {
        owner: 'National Gallery of Iceland (Listasafn Íslands)',
        url: 'https://www.listasafn.is/list/safneign/li-8249/',
        catalogNumber: 'LÍ-8249'
      },
      'thyrlulending': {
        owner: 'Reykjavík Art Museum',
        url: 'https://listasafnreykjavikur.is/safneign?q=Sekúndurnar',
        altTitle: 'Sekúndurnar þar til Sikorskyþyrlan snertir'
      }
    };
    return ownershipMap[workId] || null;
  }

  showWorkModal(workId) {
    const work = this.allWorks.find(w => w.id === workId);
    if (!work) return;

    const ownership = this.getOwnershipInfo(workId);
    const modalBody = document.getElementById('modal-body');
    modalBody.innerHTML = `
      <div class="work-detail">
        <div class="work-images">
          ${work.images.map(media => {
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
          <h2>${work.title}</h2>
          <p class="work-year">${work.year}</p>
          <p class="work-description">${work.description}</p>
          ${ownership ? `
            <div class="ownership-info">
              <h3>Collection</h3>
              <p><strong>Owned by:</strong> <a href="${ownership.url}" target="_blank">${ownership.owner}</a></p>
              ${ownership.catalogNumber ? `<p class="catalog-number">Catalog: ${ownership.catalogNumber}</p>` : ''}
              ${ownership.altTitle ? `<p class="alt-title">Also listed as: "${ownership.altTitle}"</p>` : ''}
              <p><a href="collections.html">View full collections page →</a></p>
            </div>
          ` : ''}
          <div class="work-tags">
            ${work.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
          </div>
          ${work.exhibitions.length > 0 ? `
            <div class="exhibitions">
              <h3>Exhibitions</h3>
              <ul>
                ${work.exhibitions.map(ex => `
                  <li>${ex.title}, ${ex.venue}, ${ex.city} (${ex.year})</li>
                `).join('')}
              </ul>
            </div>
          ` : ''}
          <div class="search-related">
            <button class="search-button" onclick='window.searchForWork(${JSON.stringify({
              primary: work.title.split('(')[0].trim(),
              alternative: ownership?.altTitle || null,
              workId: work.id
            })})'>
              🔍 Search archive for this work
            </button>
            <p class="search-help">Find exhibitions, reviews, and other references to this work</p>
          </div>
        </div>
      </div>
    `;

    document.getElementById('work-modal').style.display = 'block';
  }

  clearAllFilters() {
    // Reset search
    document.getElementById('search-input').value = '';
    this.currentFilters.search = '';

    // Reset year range
    document.getElementById('year-range').value = 2024;
    this.currentFilters.yearRange.max = 2024;

    // Reset tag checkboxes
    document.querySelectorAll('#tags-filter input[type="checkbox"]').forEach(cb => {
      cb.checked = false;
    });
    this.currentFilters.tags = [];

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
  new WorksManager();
});