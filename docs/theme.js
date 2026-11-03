/**
 * FloodWave-At · CoSE Theme Controller & Preference Sync
 * Adheres to modern-web-guidance: dark-mode and dark-mode-toggle
 * 
 * Supports:
 * - Direct localStorage override ('light' | 'dark')
 * - Automatic system preference matching when no override is set
 * - Two-state accessible toggle (sun / moon)
 * - Synchronous FOUC prevention in <head>
 * - Multi-tab cross-synchronization via window.storage event
 */
(function () {
  'use strict';

  function getResolvedScheme() {
    const meta = document.querySelector('meta[name="color-scheme"]');
    const metaVal = meta ? meta.content : null;
    if (metaVal === 'light' || metaVal === 'dark') return metaVal;
    const rootData = document.documentElement.getAttribute('data-theme');
    if (rootData === 'light' || rootData === 'dark') return rootData;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function updateToggleUI(resolved) {
    const toggleBtn = document.getElementById('theme-toggle');
    if (!toggleBtn) return;
    const isDark = resolved === 'dark';
    const nextTheme = isDark ? 'light' : 'dark';
    toggleBtn.setAttribute('aria-label', `Switch to ${nextTheme} theme`);
    toggleBtn.setAttribute('title', `Switch to ${nextTheme} theme`);
    const label = toggleBtn.querySelector('.theme-label');
    if (label) {
      label.textContent = isDark ? 'Light' : 'Dark';
    }
  }

  function applyTheme(target) {
    const system = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    const meta = document.querySelector('meta[name="color-scheme"]');

    if (target === system) {
      // User is reverting back to system preference
      try { localStorage.removeItem('color-scheme'); } catch (e) {}
      if (meta) meta.content = 'light dark';
      document.documentElement.removeAttribute('data-theme');
    } else {
      try { localStorage.setItem('color-scheme', target); } catch (e) {}
      if (meta) meta.content = target;
      document.documentElement.setAttribute('data-theme', target);
    }
    updateToggleUI(target);
  }

  function initTheme() {
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        const current = getResolvedScheme();
        const target = current === 'dark' ? 'light' : 'dark';
        applyTheme(target);
      });
    }

    // Cross-tab synchronization
    window.addEventListener('storage', (e) => {
      if (e.key === 'color-scheme') {
        const val = e.newValue;
        const meta = document.querySelector('meta[name="color-scheme"]');
        if (val === 'light' || val === 'dark') {
          if (meta) meta.content = val;
          document.documentElement.setAttribute('data-theme', val);
          updateToggleUI(val);
        } else {
          if (meta) meta.content = 'light dark';
          document.documentElement.removeAttribute('data-theme');
          updateToggleUI(getResolvedScheme());
        }
      }
    });

    // React to system OS preference changes if no manual override is pinned
    const mql = window.matchMedia('(prefers-color-scheme: dark)');
    mql.addEventListener('change', () => {
      let stored = null;
      try { stored = localStorage.getItem('color-scheme'); } catch (e) {}
      if (!stored) {
        updateToggleUI(getResolvedScheme());
      }
    });

    updateToggleUI(getResolvedScheme());
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTheme);
  } else {
    initTheme();
  }
})();
