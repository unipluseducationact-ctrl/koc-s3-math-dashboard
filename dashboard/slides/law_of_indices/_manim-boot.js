/** Shared Reveal + KaTeX boot for JM24 Manim-style decks */
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

  /** Sync graphical cancel state from current fragment index */
  function syncCancelState() {
    var f = -1;
    try {
      if (window.Reveal && Reveal.getIndices) f = Reveal.getIndices().f;
    } catch (e) { /* ignore */ }

    document.querySelectorAll(".frac-stack[data-cancel-at]").forEach(function (frac) {
      var at = parseInt(frac.getAttribute("data-cancel-at"), 10);
      if (isNaN(at)) return;
      var on = f >= at;
      frac.classList.toggle("cancelled", on);
    });
  }

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
    syncCancelState();
  }

  if (Reveal.isReady && Reveal.isReady()) afterReady();
  else if (Reveal.on) Reveal.on("ready", afterReady);
  else setTimeout(afterReady, 60);

  if (Reveal.on) {
    Reveal.on("fragmentshown", syncCancelState);
    Reveal.on("fragmenthidden", syncCancelState);
    Reveal.on("slidechanged", syncCancelState);
  }

  document.addEventListener("selectstart", function (e) { e.preventDefault(); });
  document.addEventListener("mousedown", function (e) {
    if (e.detail > 1) e.preventDefault();
  });
})();
