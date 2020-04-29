'use strict';
const CACHE_NAME = 'flutter-app-cache';
const RESOURCES = {
  "index.html": "5f70a9060418ac1cf47c2d0652dc04d8",
"/": "5f70a9060418ac1cf47c2d0652dc04d8",
"main.dart.js": "8ec1945fbce69e02a66bf4e3a342be57",
"favicon.png": "4c24c0cb9ff4c1b19e5715b2ef672fb4",
"icons/Icon-192.png": "c245c8ef7d5c1d92c3f33d121dd16776",
"icons/Icon-512.png": "f23f03f8c5fa298d006028e4cc7fe803",
"manifest.json": "d475bff0a03e56d733e7dd675e551368",
"assets/LICENSE": "4a76a2b91f3a2d23d166d0b617637448",
"assets/AssetManifest.json": "d42c612ee655100a095de4a54a5523e1",
"assets/FontManifest.json": "8a636fd7e85453a42a4ef7cedaf53812",
"assets/packages/flutter_feather_icons/fonts/feather.ttf": "c96dc22ca29a082af83cce866d35cebc",
"assets/fonts/MaterialIcons-Regular.ttf": "56d3ffdef7a25659eab6a68a3fbfaf16"
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
