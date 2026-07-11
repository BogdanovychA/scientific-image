/* random-articles.js — блок «Випадкові статті» у лівому сайдбарі.
   При кожному завантаженні сторінки вибирає 10 випадкових
   посилань на статті (концепції/сутності/архіви) з навігації
   і показує їх у окремому блоці. Оновлюється при F5. */
(function () {
  "use strict";

  function pickRandom(arr, n) {
    var pool = arr.slice();
    var out = [];
    while (out.length < n && pool.length) {
      var i = Math.floor(Math.random() * pool.length);
      out.push(pool.splice(i, 1)[0]);
    }
    return out;
  }

  // Посилання на статті в навігації можуть мати вигляд:
  //   "concepts/masa/"         (з головної)
  //   "../antymateriia/"      (з іншої статті — Material опускає каталог)
  //   "raw/.../"              (ДЖЕРЕЛО — виключаємо)
  //   "#anchor" / "wiki/index" (навігаційні — виключаємо)
  function isArticle(href) {
    if (!href) return false;
    if (/raw\//.test(href)) return false;   // джерела
    if (/#/.test(href)) return false;       // якорі
    if (/index/.test(href)) return false;   // головна
    return /\/$/.test(href);                 // сторінка вікі (закінч. на /)
  }

  function buildRandom() {
    var nav = document.querySelector(".md-nav--primary");
    if (!nav) return;

    var all = Array.prototype.slice.call(nav.querySelectorAll("a"));
    var links = all.filter(function (a) {
      return isArticle(a.getAttribute("href"));
    });
    if (!links.length) return;

    var chosen = pickRandom(links, Math.min(10, links.length));

    var wrap = document.getElementById("random-articles");
    if (!wrap) {
      wrap = document.createElement("nav");
      wrap.id = "random-articles";
      wrap.className = "md-nav random-articles";
      wrap.setAttribute("aria-label", "Випадкові статті");

      var title = document.createElement("div");
      title.className = "random-articles__title";
      title.textContent = "Випадкові статті";
      wrap.appendChild(title);

      var list = document.createElement("ul");
      list.className = "md-nav__list random-articles__list";
      list.id = "random-articles-list";
      wrap.appendChild(list);

      // Вставляємо НАД основною навігацією (на початок лівого сайдбару),
      // щоб блок був завжди видимий зверху без прокрутки
      var sidebar =
        document.querySelector(".md-sidebar--primary") ||
        document.querySelector(".md-sidebar");
      if (sidebar) {
        sidebar.insertBefore(wrap, sidebar.firstElementChild);
      } else {
        var main = document.querySelector(".md-main");
        if (main && main.parentNode) main.parentNode.insertBefore(wrap, main);
      }
    }

    var ul = document.getElementById("random-articles-list");
    ul.innerHTML = "";
    chosen.forEach(function (a) {
      if (!a.getAttribute("href")) return;
      var li = document.createElement("li");
      li.className = "md-nav__item";
      var clone = a.cloneNode(true);
      clone.className = "md-nav__link";
      li.appendChild(clone);
      ul.appendChild(li);
    });
  }

  var tries = 0;
  function tryBuild() {
    buildRandom();
    var ra = document.getElementById("random-articles");
    var n = ra ? ra.querySelectorAll("li").length : 0;
    // Якщо набралось менше 2 — Material ще не зібрав навігацію, повторюємо
    if (n < 2 && tries < 20) {
      tries++;
      setTimeout(tryBuild, 100);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      setTimeout(tryBuild, 50);
    });
  } else {
    setTimeout(tryBuild, 50);
  }
})();
