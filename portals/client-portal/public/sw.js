/**
 * AGGRESSIVE SERVICE WORKER TERMINATOR
 * This service worker immediately unregisters itself and clears all caches
 */

console.log('[SW] Terminator activated - destroying all caches');

self.addEventListener('install', (event) => {
  console.log('[SW] Install - forcing immediate activation');
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  console.log('[SW] Activate - clearing all caches and unregistering');

  event.waitUntil(
    Promise.all([
      // Delete all caches
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            console.log('[SW] Deleting cache:', cacheName);
            return caches.delete(cacheName);
          })
        );
      }),
      // Claim all clients
      self.clients.claim(),
    ]).then(() => {
      console.log('[SW] All caches cleared');
      // Unregister this service worker
      return self.registration.unregister();
    }).then(() => {
      console.log('[SW] Service worker unregistered');
      // Reload all clients
      return self.clients.matchAll();
    }).then((clients) => {
      clients.forEach((client) => {
        console.log('[SW] Reloading client:', client.url);
        client.postMessage({ type: 'CACHE_CLEARED', action: 'reload' });
      });
    })
  );
});

// Intercept all fetch requests and bypass cache
self.addEventListener('fetch', (event) => {
  console.log('[SW] Bypassing cache for:', event.request.url);
  event.respondWith(
    fetch(event.request, { cache: 'no-store' })
  );
});

// Listen for messages from clients
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
