# Website Improvements TODO

## ✅ Completed (Quick Wins)

- [x] Extract hardcoded tag categories to config.json
- [x] Add error handling to works.js data loading
- [x] Add error handling to global-search.js
- [x] Move ownership map from works.js to works.json
- [x] Add ARIA labels to filter buttons and modals
- [x] Add keyboard navigation (Escape key for modal)
- [x] Create introduction landing page
- [x] Fix navigation structure (Home/Works)
- [x] Add "under construction" label to works page

---

## 🔨 Medium-Term Improvements (1-2 weeks effort)

### Code Organization & Maintainability

- [ ] **Refactor WorksManager into separate modules**
  - Split into: DataManager, FilterManager, ModalManager, ViewManager
  - Makes code easier to test and maintain
  - Estimated: 3-4 days
  - Priority: Medium

- [ ] **Create constants file for work types and repeated strings**
  - Replace string literals like "work", "solo-exhibition" with constants
  - Prevents typos and makes refactoring easier
  - Estimated: 2-3 hours
  - Priority: Medium

- [ ] **Add more comprehensive null checks**
  - Check all DOM element queries before use
  - Prevent edge case failures
  - Estimated: 1 day
  - Priority: Medium

### Performance Improvements

- [ ] **Implement virtual scrolling for works grid**
  - Only render visible work cards
  - Use IntersectionObserver API
  - Huge performance boost for large collections
  - Estimated: 2-3 days
  - Priority: High

- [ ] **Reduce full page re-renders**
  - Update only changed DOM elements instead of regenerating entire grid
  - Cache DOM query results
  - Estimated: 2 days
  - Priority: Medium

- [ ] **Implement proper event listener cleanup**
  - Track and remove event listeners on language change
  - Prevents memory leaks
  - Estimated: 1 day
  - Priority: Low

### Accessibility Enhancements

- [ ] **Add keyboard navigation for works grid**
  - Arrow keys to navigate between work cards
  - Enter to open modal
  - Estimated: 1-2 days
  - Priority: Medium

- [ ] **Improve modal focus management**
  - Trap focus inside modal when open
  - Return focus to triggering element on close
  - Estimated: 1 day
  - Priority: Medium

- [ ] **Add visible focus indicators**
  - Make keyboard navigation visually clear
  - Update CSS for better focus states
  - Estimated: 4-6 hours
  - Priority: Medium

- [ ] **Add skip navigation links**
  - Allow keyboard users to skip to main content
  - Estimated: 2-3 hours
  - Priority: Low

### SEO & Discoverability

- [ ] **Add meta descriptions to all pages**
  - Unique description for each page
  - Improves search engine results
  - Estimated: 2-3 hours
  - Priority: Medium

- [ ] **Implement structured data (Schema.org)**
  - Mark up artworks, exhibitions, person data
  - Better search engine understanding
  - Estimated: 1-2 days
  - Priority: Low

- [ ] **Create sitemap.xml**
  - Help search engines index all pages
  - Can be generated automatically
  - Estimated: 2-3 hours
  - Priority: Low

- [ ] **Add Open Graph meta tags**
  - Better previews when sharing on social media
  - Estimated: 3-4 hours
  - Priority: Low

---

## 🚀 Major Refactoring (2-4 weeks effort)

### Modern Build System

- [ ] **Set up Vite development environment**
  - Fast hot-reload during development
  - Automatic minification and bundling
  - Tree-shaking for smaller files
  - Estimated: 1 week
  - Priority: Low
  - Benefits: Much better developer experience

- [ ] **Migrate to ES modules**
  - Use modern import/export instead of global scripts
  - Better code organization
  - Works with Vite
  - Estimated: 1 week
  - Priority: Low

### Type Safety

- [ ] **Add TypeScript**
  - Catch bugs before they happen
  - Better IDE autocomplete
  - Self-documenting code
  - Estimated: 2 weeks
  - Priority: Low
  - Benefits: Reduces bugs by 15-20%

### Component Architecture

- [ ] **Convert to Web Components**
  - Work card component
  - Filter category component
  - Modal component
  - Makes code reusable
  - Estimated: 2 weeks
  - Priority: Low

### State Management

- [ ] **Implement lightweight state library**
  - Zustand or similar
  - Single source of truth
  - Better debugging
  - Estimated: 1 week
  - Priority: Low

### Testing

- [ ] **Add unit tests**
  - Test filter logic
  - Test search algorithm
  - Test data transformations
  - Use Vitest or Jest
  - Estimated: 1-2 weeks
  - Priority: Low
  - Benefits: Confidence when making changes

- [ ] **Add end-to-end tests**
  - Test critical user flows
  - Use Playwright
  - Estimated: 1 week
  - Priority: Low

---

## 📊 Monitoring & Analytics

- [ ] **Add Web Vitals monitoring**
  - Track page load performance
  - Largest Contentful Paint (LCP)
  - First Input Delay (FID)
  - Cumulative Layout Shift (CLS)
  - Estimated: 1 day
  - Priority: Low

- [ ] **Set up error tracking**
  - Sentry or similar
  - Get notified when users hit errors
  - Estimated: 1 day
  - Priority: Low

---

## 🎨 UI/UX Enhancements

- [ ] **Add loading states**
  - Show skeleton screens while loading
  - Better user feedback
  - Estimated: 2-3 days
  - Priority: Low

- [ ] **Improve mobile responsiveness**
  - Test on various devices
  - Refine touch interactions
  - Estimated: 3-4 days
  - Priority: Medium

- [ ] **Add animations and transitions**
  - Smooth filter transitions
  - Modal open/close animations
  - Estimated: 2-3 days
  - Priority: Low

---

## 📝 Documentation

- [ ] **Create CONTRIBUTING.md**
  - Guidelines for adding new works
  - Code style guide
  - How to test changes
  - Estimated: 1 day
  - Priority: Medium

- [ ] **Document the codebase**
  - JSDoc comments on key functions
  - Architecture overview
  - Data flow diagrams
  - Estimated: 2-3 days
  - Priority: Low

- [ ] **Create README.md**
  - Project overview
  - Setup instructions
  - Deployment process
  - Estimated: 4-6 hours
  - Priority: Medium

---

## 🔧 Development Workflow

- [ ] **Set up pre-commit hooks**
  - Auto-format code
  - Run linting
  - Estimated: 2-3 hours
  - Priority: Low

- [ ] **Add linting (ESLint)**
  - Catch code quality issues
  - Enforce consistent style
  - Estimated: 1 day
  - Priority: Low

- [ ] **Set up CI/CD pipeline**
  - Automatic testing on pull requests
  - Automatic deployment
  - GitHub Actions
  - Estimated: 2-3 days
  - Priority: Low

---

## Priority Recommendations

### Do Next (High Value, Medium Effort):
1. **Virtual scrolling** - Big performance win
2. **Refactor WorksManager** - Makes future work easier
3. **Keyboard navigation** - Accessibility is important
4. **Meta descriptions** - Easy SEO win

### Do When Time Permits:
- SEO improvements (structured data, sitemap)
- UI polish (animations, loading states)
- Documentation (README, CONTRIBUTING)

### Do If Planning Long-Term:
- TypeScript migration
- Modern build system (Vite)
- Comprehensive testing
- Web Components

---

## Notes

- **Quick wins are done!** The site is now more robust and accessible
- Focus on **content** first - getting artworks added is priority #1
- These improvements can be done incrementally
- No need to do everything at once
- Prioritize based on what problems you're actually experiencing

Last Updated: 2025-10-16
