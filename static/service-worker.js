// Version du service worker
const CACHE_NAME = 'cybercrim-v1';
const OFFLINE_URL = '/offline.html';

// Fichiers à mettre en cache lors de l'installation
const CACHE_ASSETS = [
  '/',
  '/static/css/styles.css',
  '/static/img/icon-192.png',
  '/static/img/icon-512.png',
  '/static/img/favicon.svg',
  'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap',
  'https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap',
  'https://unpkg.com/alpinejs'
];

// Installation du Service Worker
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Cache ouvert');
        return cache.addAll(CACHE_ASSETS);
      })
  );
  // Active le nouveau service worker immédiatement
  self.skipWaiting();
});

// Activation du Service Worker
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            console.log('Suppression de l\'ancien cache :', cache);
            return caches.delete(cache);
          }
        })
      );
    })
  );
  // Prend le contrôle de toutes les pages
  event.waitUntil(clients.claim());
});

// Stratégie de mise en cache : Network First, Cache Fallback
self.addEventListener('fetch', (event) => {
  // Ignore les requêtes qui ne sont pas de type GET
  if (event.request.method !== 'GET') return;

  // Ignore les requêtes vers l'API ou d'autres domaines
  if (
    event.request.url.includes('/api/') ||
    !(event.request.url.startsWith('http') || event.request.url.startsWith('https'))
  ) {
    return;
  }

  // Gestion des requêtes de navigation (pages)
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          // Mise à jour du cache avec la nouvelle réponse
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
          return response;
        })
        .catch(() => {
          // En cas d'échec, retourne la page d'accueil depuis le cache
          return caches.match('/');
        })
    );
  } else {
    // Pour les autres ressources (CSS, JS, images, etc.)
    event.respondWith(
      caches.match(event.request)
        .then((cachedResponse) => {
          // Retourne la ressource en cache si elle existe
          if (cachedResponse) {
            return cachedResponse;
          }
          // Sinon, effectue la requête réseau et met en cache le résultat
          return fetch(event.request).then((response) => {
            // Vérifie que la réponse est valide
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            // Clone la réponse pour la mettre en cache
            const responseToCache = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, responseToCache);
            });
            return response;
          });
        })
    );
  }
});

// Gestion des messages (pour la mise à jour en arrière-plan)
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
