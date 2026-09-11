/** Shared Reveal + KaTeX boot for JM24 Manim-style decks (fly / auto-expand / cancel) */
(function () {
  "use strict";

  var FLY_MS = 560;
  var STAGE_MS = 720;
  var autoTimers = [];

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

  function clearAutoTimers() {
    autoTimers.forEach(function (id) { window.clearTimeout(id); });
    autoTimers = [];
    document.querySelectorAll(".work-slot.playing").forEach(function (el) {
      el.classList.remove("playing");
    });
  }

  function later(fn, ms) {
    var id = window.setTimeout(fn, ms);
    autoTimers.push(id);
    return id;
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

    later(function () {
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

      later(function () {
        toEl.classList.remove("fly-wait");
        toEl.classList.add("fly-land");
        if (ghost.parentNode) ghost.parentNode.removeChild(ghost);
      }, FLY_MS);
    }, delay || 0);
  }

  function runFlyIns(root) {
    if (!root) return;
    var nodes = root.querySelectorAll("[data-fly-from]");
    if (!nodes.length && root.getAttribute && root.getAttribute("data-fly-from")) {
      nodes = [root];
    }

    Array.prototype.forEach.call(nodes, function (toEl, i) {
      var sel = toEl.getAttribute("data-fly-from");
      if (!sel) return;
      markSource(sel, false);
      flyFromTo(document.querySelector(sel), toEl, i * 70);
      later(function () {
        markSource(sel, true);
      }, FLY_MS + i * 70 + 40);
    });
  }

  function activateStage(slot, index) {
    var panes = slot.querySelectorAll(".stage-pane");
    panes.forEach(function (pane, i) {
      pane.classList.toggle("is-active", i === index);
    });
    var active = panes[index];
    if (!active) return;
    // Only fly tokens that belong to this newly shown pane
    var flyNodes = active.querySelectorAll("[data-fly-from]");
    if (flyNodes.length) {
      clearSourceMarks();
      Array.prototype.forEach.call(flyNodes, function (toEl, i) {
        var sel = toEl.getAttribute("data-fly-from");
        if (!sel) return;
        markSource(sel, false);
        flyFromTo(document.querySelector(sel), toEl, i * 70);
        later(function () {
          markSource(sel, true);
        }, FLY_MS + i * 70 + 40);
      });
    }
  }

  /** One Reveal step → auto play stage-pane 0 → 1 → 2… in a fixed frame */
  function runAutoSlot(slot) {
    if (!slot || !slot.classList.contains("work-slot")) return;
    clearAutoTimers();
    clearSourceMarks();

    var panes = slot.querySelectorAll(".stage-pane");
    if (!panes.length) {
      runFlyIns(slot);
      return;
    }

    slot.classList.add("playing");
    activateStage(slot, 0);

    var i = 1;
    function scheduleNext(delay) {
      later(function () {
        if (i >= panes.length) {
          slot.classList.remove("playing");
          return;
        }
        activateStage(slot, i);
        i += 1;
        if (i < panes.length) {
          var active = panes[i - 1];
          var hasFly = active && active.querySelector("[data-fly-from]");
          scheduleNext(hasFly ? FLY_MS + STAGE_MS * 0.65 : STAGE_MS);
        } else {
          later(function () { slot.classList.remove("playing"); }, STAGE_MS * 0.4);
        }
      }, delay);
    }

    scheduleNext(FLY_MS + STAGE_MS * 0.55);
  }

  function resetAutoSlots(scope) {
    clearAutoTimers();
    (scope || document).querySelectorAll(".work-slot").forEach(function (slot) {
      slot.classList.remove("playing");
      var panes = slot.querySelectorAll(".stage-pane");
      panes.forEach(function (pane, i) {
        pane.classList.toggle("is-active", i === 0 && slot.classList.contains("visible"));
        if (!slot.classList.contains("visible")) pane.classList.remove("is-active");
      });
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
      var frag = ev && ev.fragment;
      if (frag && frag.classList.contains("work-slot")) {
        runAutoSlot(frag);
      } else {
        clearSourceMarks();
        runFlyIns(frag);
      }
    } catch (err) { /* ignore */ }
  }

  function onFragmentHidden() {
    syncCancelState();
    syncWorkChains();
    clearAutoTimers();
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
      resetAutoSlots(document);
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
