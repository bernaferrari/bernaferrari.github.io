'use strict';
const CACHE_NAME = 'flutter-app-cache';
const RESOURCES = {
  "/index.html": "88d31694c44dbb514f78eabe6521bba8",
"/main.dart.js": "bfe82f19a169b5b5ef189eef7efcfd45",
"/favicon.png": "1c5116bc5111c37d255ea1cb01ba77d0",
"/icons/Icon-192.png": "3e1643be07a280b74af9cba7df63d338",
"/icons/Icon-512.png": "f1aab63fa272b115cf84d879a7a3c3fa",
"/manifest.json": "e666fd8b78925a794012701939c6e302",
"/assets/LICENSE": "3feb547c8787e02e3807e9d1406200c0",
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
