'use strict';
const CACHE_NAME = 'flutter-app-cache';
const RESOURCES = {
  "/index.html": "2fb3749791b10c3c8b7e4e7bc921f50b",
"/main.dart.js": "c011832f816d714c610ad25a6d53d887",
"/favicon.png": "4c24c0cb9ff4c1b19e5715b2ef672fb4",
"/icons/Icon-192.png": "c245c8ef7d5c1d92c3f33d121dd16776",
"/icons/Icon-512.png": "f23f03f8c5fa298d006028e4cc7fe803",
"/manifest.json": "d475bff0a03e56d733e7dd675e551368",
"/assets/LICENSE": "b0513b62240548a6f242d0eaddb5e69f",
"/assets/AssetManifest.json": "d42c612ee655100a095de4a54a5523e1",
"/assets/FontManifest.json": "8a636fd7e85453a42a4ef7cedaf53812",
"/assets/packages/flutter_feather_icons/fonts/feather.ttf": "c96dc22ca29a082af83cce866d35cebc",
"/assets/fonts/MaterialIcons-Regular.ttf": "56d3ffdef7a25659eab6a68a3fbfaf16"
};

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (cacheName) {
      return caches.delete(cacheName);
    }).then(function (_) {
      return caches.open(CACHE_NAME);
    }).then(function (cache) {
      return cache.addAll(Object.keys(RESOURCES));
    })
  );
});

self.addEventListener('fetch', function (event) {
  event.respondWith(
    caches.match(event.request)
      .then(function (response) {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});
