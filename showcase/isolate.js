// Load the Compose app after the first navigation controlled by the local worker.
const boot = document.currentScript;
const status = document.querySelector("#loading");

async function start() {
  if (!crossOriginIsolated) {
    if (!navigator.serviceWorker) {
      throw new Error("This demo needs a browser with service worker support.");
    }
    if (navigator.serviceWorker.controller) {
      throw new Error("Cross-origin isolation is unavailable in this browser.");
    }
    const controlled = new Promise((resolve, reject) => {
      const timeout = setTimeout(() => reject(new Error("Browser storage setup timed out.")), 10000);
      navigator.serviceWorker.addEventListener("controllerchange", () => {
        clearTimeout(timeout);
        resolve();
      }, { once: true });
    });
    await Promise.all([
      controlled,
      navigator.serviceWorker.register("./isolation-worker.js"),
    ]);
    location.reload();
    return;
  }
  const app = document.createElement("script");
  app.src = boot.dataset.app;
  app.onerror = () => { status.textContent = "The demo could not load. Refresh to try again."; };
  document.body.append(app);
}

start().catch(error => {
  status.textContent = `${error.message} Open the demo directly in a current browser and try again.`;
});
