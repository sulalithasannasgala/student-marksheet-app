// This is the "Offline copy of pages" service worker

const CACHE = "pwabuilder-offline";

// Load Workbox from CDN
importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');

// Activate immediately on update
self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }
});

// Cache all navigation and static requests
workbox.routing.registerRoute(
  ({request}) => request.destination === 'document' || request.destination === 'script' || request.destination === 'style' || request.destination === 'image' || request.destination === 'font',
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: CACHE,
  })
);
