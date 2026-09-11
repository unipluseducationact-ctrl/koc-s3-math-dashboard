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

  Reveal.initialize({
    width: "100%",
    height: "100%",
    margin: 0.06,
    minScale: 0.2,
    maxScale: 2.0,
    controls: false,
    progress: false,
    slideNumber: false,
    history: false,
    keyboard: true,
    touch: true,
    center: true,
    embedded: false,
    transition: "none",
    backgroundTransition: "none"
  });

  if (Reveal.isReady && Reveal.isReady()) renderMath();
  else if (Reveal.on) Reveal.on("ready", renderMath);
  else setTimeout(renderMath, 60);

  document.addEventListener("selectstart", function (e) { e.preventDefault(); });
  document.addEventListener("mousedown", function (e) {
    if (e.detail > 1) e.preventDefault();
  });
})();
