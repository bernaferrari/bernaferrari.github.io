// GitHub Pages does not provide configurable response headers. This worker is
// served inside each SQLite demo so its scope stays within that demo's directory.
self.addEventListener("install", event => event.waitUntil(self.skipWaiting()));
self.addEventListener("activate", event => event.waitUntil(self.clients.claim()));

self.addEventListener("fetch", event => {
  if (!event.request.url.startsWith(self.registration.scope)) return;
  event.respondWith(fetch(event.request).then(response => {
    if (!response.ok || response.type === "opaque") return response;
    const headers = new Headers(response.headers);
    headers.set("Cross-Origin-Opener-Policy", "same-origin");
    headers.set("Cross-Origin-Embedder-Policy", "require-corp");
    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers,
    });
  }));
});
