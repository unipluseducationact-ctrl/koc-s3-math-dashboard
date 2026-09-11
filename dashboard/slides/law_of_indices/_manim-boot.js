/** Shared Reveal + KaTeX boot for JM24 Manim-style decks (fly / expand / cancel) */
(function () {
  "use strict";

  var FLY_MS = 560;

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

  function syncCancelState() {
    var f = -1;
    try {
      if (window.Reveal && Reveal.getIndices) f = Reveal.getIndices().f;
    } catch (e) { /* ignore */ }

    document.querySelectorAll(".frac-stack[data-cancel-at]").forEach(function (frac) {
      var at = parseInt(frac.getAttribute("data-cancel-at"), 10);
      if (isNaN(at)) return;
      frac.classList.toggle("cancelled", f >= at);
    });
  }

  function clearSourceMarks() {
    document.querySelectorAll(".example-row .src").forEach(function (el) {
      el.classList.remove("is-source", "is-spent");
    });
  }

  function markSource(sel, spent) {
    if (!sel) return;
    var src = document.querySelector(sel);
    if (!src) return;
    if (spent) {
      src.classList.remove("is-source");
      src.classList.add("is-spent");
    } else {
      src.classList.remove("is-spent");
      src.classList.add("is-source");
    }
  }

  /** JM32-style TransformFromCopy: ghost flies from source → target */
  function flyFromTo(fromEl, toEl, delay) {
    if (!fromEl || !toEl) {
      if (toEl) {
        toEl.classList.remove("fly-wait");
        toEl.classList.add("fly-land");
      }
      return;
    }

    toEl.classList.add("fly-wait");
    toEl.classList.remove("fly-land");

    window.setTimeout(function () {
      var from = fromEl.getBoundingClientRect();
      var to = toEl.getBoundingClientRect();
      if (!from.width || !to.width) {
        toEl.classList.remove("fly-wait");
        toEl.classList.add("fly-land");
        return;
      }

      var ghost = fromEl.cloneNode(true);
      ghost.classList.add("fly-ghost", "flying");
      ghost.style.left = from.left + "px";
      ghost.style.top = from.top + "px";
      ghost.style.width = from.width + "px";
      ghost.style.height = from.height + "px";
      document.body.appendChild(ghost);

      var dx = to.left - from.left + (to.width - from.width) / 2;
      var dy = to.top - from.top + (to.height - from.height) / 2;

      window.requestAnimationFrame(function () {
        window.requestAnimationFrame(function () {
          ghost.style.transform = "translate(" + dx + "px, " + dy + "px) scale(1.05)";
        });
      });

      window.setTimeout(function () {
        toEl.classList.remove("fly-wait");
        toEl.classList.add("fly-land");
        if (ghost.parentNode) ghost.parentNode.removeChild(ghost);
      }, FLY_MS);
    }, delay || 0);
  }

  function runFlyIns(fragmentEl) {
    if (!fragmentEl) return;
    clearSourceMarks();

    var nodes = fragmentEl.querySelectorAll("[data-fly-from]");
    if (!nodes.length && fragmentEl.getAttribute("data-fly-from")) {
      nodes = [fragmentEl];
    }

    Array.prototype.forEach.call(nodes, function (toEl, i) {
      var sel = toEl.getAttribute("data-fly-from");
      if (!sel) return;
      markSource(sel, false);
      var fromEl = document.querySelector(sel);
      flyFromTo(fromEl, toEl, i * 70);
      window.setTimeout(function () {
        markSource(sel, true);
      }, FLY_MS + i * 70 + 40);
    });
  }

  function syncWorkChains() {
    document.querySelectorAll(".work-chain").forEach(function (chain) {
      var rows = Array.prototype.slice.call(chain.querySelectorAll(".work-row"));
      var visible = rows.filter(function (r) {
        return r.classList.contains("visible");
      });
      var current =
        chain.querySelector(".work-row.current-fragment") ||
        visible[visible.length - 1] ||
        null;
      rows.forEach(function (row) {
        var hide = row.classList.contains("visible") && row !== current;
        row.classList.toggle("chain-hidden", hide);
      });
    });
  }

  function onFragmentShown(ev) {
    syncCancelState();
    syncWorkChains();
    try {
      runFlyIns(ev && ev.fragment);
    } catch (err) { /* ignore */ }
  }

  function onFragmentHidden() {
    syncCancelState();
    syncWorkChains();
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
    center: false,
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
    Reveal.on("fragmentshown", onFragmentShown);
    Reveal.on("fragmenthidden", onFragmentHidden);
    Reveal.on("slidechanged", function () {
      syncCancelState();
      syncWorkChains();
      clearSourceMarks();
      document.querySelectorAll(".fly-ghost").forEach(function (g) {
        if (g.parentNode) g.parentNode.removeChild(g);
      });
    });
  }

  document.addEventListener("selectstart", function (e) { e.preventDefault(); });
  document.addEventListener("mousedown", function (e) {
    if (e.detail > 1) e.preventDefault();
  });
})();
