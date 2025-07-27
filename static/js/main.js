// === static/js/main.js ===

// 🌗 Gestion du thème clair/sombre (basée sur localStorage + préférence système)
function applyTheme() {
  const theme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const useDark = theme === 'dark' || (!theme && prefersDark);

  document.documentElement.classList.toggle('dark', useDark);
  toggleIcons(useDark);
}

function toggleIcons(isDark) {
  const darkIcon = document.getElementById('theme-toggle-dark-icon');
  const lightIcon = document.getElementById('theme-toggle-light-icon');
  if (darkIcon && lightIcon) {
    darkIcon.classList.toggle('hidden', isDark);
    lightIcon.classList.toggle('hidden', !isDark);
  }
}

function setupThemeToggle() {
  const toggleBtn = document.getElementById('theme-toggle');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      const isDark = document.documentElement.classList.toggle('dark');
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
      toggleIcons(isDark);
    });
  }
}

// 📱 Menu mobile toggle
function setupMobileMenu() {
  const mobileBtn = document.getElementById('mobile-menu-button');
  const mobileMenu = document.getElementById('mobile-menu');
  if (mobileBtn && mobileMenu) {
    mobileBtn.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');
    });

    document.addEventListener('click', (e) => {
      if (!mobileBtn.contains(e.target) && !mobileMenu.contains(e.target)) {
        mobileMenu.classList.add('hidden');
      }
    });
  }
}

// ✨ Suppression auto des flash messages
function setupFlashMessages() {
  const messages = document.querySelectorAll('.flash-message');
  messages.forEach((msg) => {
    setTimeout(() => {
      msg.style.opacity = '0';
      setTimeout(() => msg.remove(), 300);
    }, 5000);
  });
}

// 🧠 Exemple d’appel API et tri
async function fetchAndSortData() {
  const targetUrl = "/api/data"; // adapte à ta route Flask

  try {
    const response = await fetch(targetUrl);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    console.log("📦 Données reçues :", data);

    const sorted = sortBy(data, 'title');
    console.log("📊 Données triées :", sorted);
  } catch (error) {
    console.error("❌ Erreur lors du fetch:", error);
  }
}

// 🧰 Utilitaire de tri générique
function sortBy(array, key) {
  return array.sort((a, b) => {
    const aVal = a[key] ?? '';
    const bVal = b[key] ?? '';
    return aVal.localeCompare(bVal);
  });
}

// 🚀 Init
document.addEventListener('DOMContentLoaded', () => {
  applyTheme();
  setupThemeToggle();
  setupMobileMenu();
  setupFlashMessages();
  fetchAndSortData(); // appelle l’API et affiche les résultats triés
});
