/** Shared Reveal + KaTeX boot for JM24 Manim-style decks (JM25-27 preset size) */
(function () {
  "use strict";

  function renderMath() {
    if (!window.renderMathInElement) return;
    renderMathInElement(document.body, {
      delimiters: [
        { left: "\\(", right: "\\)", display: false },
        { left: "\\[", right: "\\]", display: true }
      ],
      throwOnError: false
    });
  }

  /* Auto-index .token / .digit / .pv-token fragments inside a row for sequential fade */
  function staggerTokens() {
    document.querySelectorAll("[data-stagger]").forEach(function (row) {
      var base = parseInt(row.getAttribute("data-stagger"), 10);
      if (isNaN(base)) base = 0;
      var i = 0;
      row.querySelectorAll(".token, .digit, .dp, .pv-token").forEach(function (el) {
        el.classList.add("fragment");
        el.setAttribute("data-fragment-index", String(base + i));
        i += 1;
      });
    });
  }

  staggerTokens();

  Reveal.initialize({
    width: 1280,
    height: 720,
    margin: 0.06,
    minScale: 0.2,
    maxScale: 1.6,
    controls: false,
    progress: false,
    slideNumber: false,
    history: false,
    keyboard: true,
    touch: true,
    center: true,
    embedded: false,
    transition: "none",
    backgroundTransition: "none",
    fragments: true
  });

  function afterReady() {
    renderMath();
    try { Reveal.layout(); } catch (e) { /* ignore */ }
  }

  if (Reveal.isReady && Reveal.isReady()) afterReady();
  else if (Reveal.on) Reveal.on("ready", afterReady);
  else setTimeout(afterReady, 60);

  document.addEventListener("selectstart", function (e) { e.preventDefault(); });
  document.addEventListener("mousedown", function (e) {
    if (e.detail > 1) e.preventDefault();
  });
})();
