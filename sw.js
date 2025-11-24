const CACHE_NAME = "americano-cache-v1";
const ASSETS = ["/", "/index.html"];

// Installation : on met en cache le shell de l'app
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    })
  );
  self.skipWaiting();
});

// Activation : on nettoie les anciens caches
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

// Fetch : cache-first pour la page, on laisse passer le reste (API, etc.)
self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);

  // On ne gère que les requêtes vers le même domaine
  if (url.origin === self.location.origin) {
    if (url.pathname === "/" || url.pathname === "/index.html") {
      event.respondWith(
        caches.match(event.request).then((cached) => {
          if (cached) return cached;
          return fetch(event.request).then((response) => {
            const respClone = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, respClone);
            });
            return response;
          });
        })
      );
    }
  }
});
