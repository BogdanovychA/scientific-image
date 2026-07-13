/* external-links.js — автоматичне відкриття зовнішніх посилань у новому вікні.
   Додає target="_blank" та rel="noopener noreferrer" до всіх зовнішніх посилань. */
(function () {
  "use strict";

  function makeExternalLinksOpenInNewTab() {
    var links = document.querySelectorAll("a");
    var currentHost = window.location.hostname;

    links.forEach(function (link) {
      var href = link.getAttribute("href");
      if (!href) return;

      // Перевіряємо, чи посилання починається з http:// або https://
      var isExternal = false;
      if (/^(https?:)?\/\//.test(href)) {
        try {
          if (link.hostname && link.hostname !== currentHost) {
            isExternal = true;
          }
        } catch (e) {
          // У разі помилки розбору ігноруємо
        }
      }

      if (isExternal) {
        link.setAttribute("target", "_blank");
        link.setAttribute("rel", "noopener noreferrer");
      }
    });
  }

  // Реєструємо через Material RxJS observable (якщо є), для сумісності з instant loading
  if (typeof document$ !== "undefined") {
    document$.subscribe(makeExternalLinksOpenInNewTab);
  } else {
    // Стандартний резервний варіант для звичайного завантаження сторінки
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", makeExternalLinksOpenInNewTab);
    } else {
      makeExternalLinksOpenInNewTab();
    }
  }
})();
