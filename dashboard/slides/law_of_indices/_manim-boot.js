/** Shared Reveal + KaTeX boot for JM24 Manim-style decks */
(function () {
  "use strict";

  var FLY_MS = 520;
  var PEEL_MS = 640;
  var STAGE_MS = 580;
  var CANCEL_MS = 480;
  var JUMP_MS = 560;
  var autoTimers = [];
  var rafIds = [];
  var playToken = 0;

  /** Current micro-animation; advance while busy → finish immediately */
  var anim = {
    busy: false,
    skip: false,
    finish: null,
    slot: null
  };

  function renderMath(root) {
    if (!window.renderMathInElement) return;
    renderMathInElement(root || document.body, {
      delimiters: [
        { left: "\\(", right: "\\)", display: false },
        { left: "\\[", right: "\\]", display: true }
      ],
      throwOnError: false
    });
  }

  function clearAutoTimers() {
    autoTimers.forEach(function (id) { window.clearTimeout(id); });
    autoTimers = [];
    rafIds.forEach(function (id) { try { cancelAnimationFrame(id); } catch (e) { /* */ } });
    rafIds = [];
    playToken += 1;
    anim.busy = false;
    anim.skip = false;
    anim.finish = null;
  }

  function later(fn, ms) {
    var token = playToken;
    var id = window.setTimeout(function () {
      if (token !== playToken) return;
      fn();
    }, ms);
    autoTimers.push(id);
    return id;
  }

  function raf(fn) {
    var id = window.requestAnimationFrame(fn);
    rafIds.push(id);
    return id;
  }

  function purgeGhosts() {
    document.querySelectorAll(
      ".fly-ghost, .peel-ghost, .times-ghost, .dp-ghost, .pv-drag-box, .expand-halo"
    ).forEach(function (g) {
      if (g.parentNode) g.parentNode.removeChild(g);
    });
  }

  function clearSourceMarks() {
    document.querySelectorAll(".example-row .src").forEach(function (el) {
      el.classList.remove("is-source", "is-spent", "expand-framed");
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

  function setExpandFrame(el, on) {
    if (!el) return;
    el.classList.toggle("expand-framed", !!on);
  }

  function restoreVisualState(scope) {
    var root = scope || document;
    root.querySelectorAll(".token, .src, .c, .expand-term, .conv-extra, .sci-jump-eq").forEach(function (t) {
      t.classList.remove(
        "struck", "gather-left", "gather-right", "gather-mid", "is-remaining",
        "expand-framed", "framed", "dragged", "landed", "awaiting",
        "dragging", "spent", "is-on", "fly-wait", "fly-land", "combined"
      );
    });
    root.querySelectorAll(".frac-stack, .frac-build").forEach(function (f) {
      f.classList.remove("cancelled", "cancel-done", "gathering", "gathered", "phase-bar", "phase-num", "phase-den", "phase-cancel", "phase-result");
      f.removeAttribute("data-cancel-step");
      f.removeAttribute("data-phase");
    });
    root.querySelectorAll("sup.pow, .pow").forEach(function (p) { p.style.opacity = ""; });
    root.querySelectorAll(".cancel-result").forEach(function (r) { r.classList.remove("show"); });
    root.querySelectorAll(".sci-rhs-live").forEach(function (el) {
      el.removeAttribute("data-jump-step");
    });
    root.querySelectorAll(".conv-row").forEach(function (r) {
      r.classList.remove("recv-extra", "rhs-in");
    });
    clearSourceMarks();
    purgeGhosts();
  }

  function syncCancelState() {
    var f = -1;
    try {
      if (window.Reveal && Reveal.getIndices) f = Reveal.getIndices().f;
    } catch (e) { /* */ }
    document.querySelectorAll(".frac-stack[data-cancel-at]").forEach(function (frac) {
      var at = parseInt(frac.getAttribute("data-cancel-at"), 10);
      if (isNaN(at) || frac.getAttribute("data-cancel-seq") != null) return;
      frac.classList.toggle("cancelled", f >= at);
    });
  }

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
      raf(function () {
        raf(function () {
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
    Array.prototype.forEach.call(nodes, function (toEl, i) {
      var sel = toEl.getAttribute("data-fly-from");
      if (!sel) return;
      markSource(sel, false);
      flyFromTo(document.querySelector(sel), toEl, i * 60);
      later(function () { markSource(sel, true); }, FLY_MS + i * 60 + 40);
    });
  }

  function activateStage(slot, index, opts) {
    opts = opts || {};
    var panes = slot.querySelectorAll(".stage-pane");
    var active = panes[index];
    if (!active) return;
    panes.forEach(function (pane, i) {
      if (i !== index) pane.classList.remove("is-active", "peel-arrive", "is-measure");
    });
    active.classList.add("is-active");
    if (opts.peel) active.classList.add("peel-arrive");
    var flyNodes = active.querySelectorAll("[data-fly-from]");
    if (flyNodes.length) {
      clearSourceMarks();
      Array.prototype.forEach.call(flyNodes, function (toEl, i) {
        var sel = toEl.getAttribute("data-fly-from");
        if (!sel) return;
        markSource(sel, false);
        flyFromTo(document.querySelector(sel), toEl, i * 60);
        later(function () { markSource(sel, true); }, FLY_MS + i * 60 + 40);
      });
    }
  }

  /**
   * Power jumps to the NEXT factor on the right (not leftmost).
   * × appears mid-air. Yellow frame stays on the expanding term until done.
   */
  function peelToStage(slot, fromIndex, toIndex, done) {
    var panes = slot.querySelectorAll(".stage-pane");
    var fromPane = panes[fromIndex];
    var toPane = panes[toIndex];
    if (!fromPane || !toPane) {
      activateStage(slot, toIndex);
      if (done) done();
      return;
    }

    var expandTok = fromPane.querySelector(".token.expand-src, .token[data-fly-from], .token");
    setExpandFrame(expandTok, true);

    var pow = fromPane.querySelector("sup.pow.outer");
    if (!pow) {
      var pows = fromPane.querySelectorAll("sup.pow");
      pow = pows.length ? pows[pows.length - 1] : null;
    }
    if (!pow) {
      activateStage(slot, toIndex, { peel: true });
      later(function () {
        setExpandFrame(expandTok, false);
        toPane.classList.remove("peel-arrive");
        if (done) done();
      }, 400);
      return;
    }

    toPane.classList.add("is-measure");
    /* Target = next upcoming factor on the RIGHT (has remaining power or is the new copy) */
    var rightFactor = toPane.querySelector(".token.next-factor, .token.peel-target");
    if (!rightFactor) {
      var toks = toPane.querySelectorAll(".token:not(.op)");
      rightFactor = toks.length >= 2 ? toks[1] : toks[0];
    }
    var timesEl = toPane.querySelector(".token.op.peel-times");
    var fromR = pow.getBoundingClientRect();
    var targetR = rightFactor
      ? (rightFactor.querySelector("sup.pow") || rightFactor).getBoundingClientRect()
      : { left: fromR.left + 90, top: fromR.top, width: 20, height: 20 };
    var midX = timesEl
      ? timesEl.getBoundingClientRect().left + timesEl.getBoundingClientRect().width / 2
      : (fromR.left + fromR.width / 2 + targetR.left + targetR.width / 2) / 2;
    var midY = timesEl
      ? timesEl.getBoundingClientRect().top + timesEl.getBoundingClientRect().height / 2
      : (fromR.top + targetR.top) / 2 + 8;
    var landX = targetR.left + targetR.width / 2;
    var landY = targetR.top + targetR.height / 2;
    toPane.classList.remove("is-measure");

    var startX = fromR.left + fromR.width / 2;
    var startY = fromR.top + fromR.height / 2;
    var dip = Math.max(32, Math.abs(landX - startX) * 0.32);

    var ghost = document.createElement("span");
    ghost.className = "peel-ghost";
    ghost.textContent = pow.textContent;
    ghost.style.left = fromR.left + "px";
    ghost.style.top = fromR.top + "px";
    ghost.style.fontSize = window.getComputedStyle(pow).fontSize;
    document.body.appendChild(ghost);
    pow.style.opacity = "0";

    var timesGhost = document.createElement("span");
    timesGhost.className = "times-ghost";
    timesGhost.textContent = "×";
    timesGhost.style.left = midX + "px";
    timesGhost.style.top = midY + "px";
    timesGhost.style.opacity = "0";
    document.body.appendChild(timesGhost);

    var peelToken = playToken;
    var finished = false;
    function cleanup(skipToEnd) {
      if (finished) return;
      finished = true;
      if (ghost.parentNode) ghost.parentNode.removeChild(ghost);
      if (timesGhost.parentNode) timesGhost.parentNode.removeChild(timesGhost);
      fromPane.classList.remove("is-active");
      pow.style.opacity = "";
      activateStage(slot, toIndex, { peel: true });
      setExpandFrame(expandTok, false);
      /* Keep frame on the new right factor being expanded if it still has a power */
      var nextExpand = toPane.querySelector(".token.peel-target, .token.next-factor");
      if (nextExpand && nextExpand.querySelector("sup.pow")) {
        setExpandFrame(nextExpand, true);
        later(function () { setExpandFrame(nextExpand, false); }, skipToEnd ? 80 : 500);
      }
      later(function () {
        toPane.classList.remove("peel-arrive");
        anim.busy = false;
        anim.finish = null;
        if (done) done();
      }, skipToEnd ? 40 : 360);
    }

    anim.busy = true;
    anim.finish = function () { cleanup(true); };

    var t0 = null;
    function frame(now) {
      if (playToken !== peelToken || finished) return;
      if (anim.skip) {
        cleanup(true);
        return;
      }
      if (t0 == null) t0 = now;
      var p = Math.min(1, (now - t0) / PEEL_MS);
      var ease = 1 - Math.pow(1 - p, 2.4);
      /* Path: start → mid (with ×) → land on next a */
      var x1 = midX - startX;
      var y1 = midY - startY + Math.sin(Math.PI * Math.min(1, ease * 1.15)) * dip;
      var x2 = landX - startX;
      var y2 = landY - startY;
      var x, y;
      if (ease < 0.55) {
        var u = ease / 0.55;
        x = x1 * u;
        y = (midY - startY) * u + Math.sin(Math.PI * u) * dip;
      } else {
        var v = (ease - 0.55) / 0.45;
        x = x1 + (x2 - x1) * v;
        y = (midY - startY) + (y2 - (midY - startY)) * v;
      }
      ghost.style.transform = "translate(" + x + "px, " + y + "px) scale(" + (1 + 0.18 * Math.sin(Math.PI * ease)) + ")";
      if (ease >= 0.35 && ease <= 0.75) {
        timesGhost.style.opacity = String(Math.min(1, (ease - 0.35) / 0.15));
        timesGhost.style.transform = "translate(-50%, -50%) scale(" + (0.75 + 0.35 * Math.min(1, (ease - 0.35) / 0.2)) + ")";
      } else if (ease > 0.75) {
        timesGhost.style.opacity = String(Math.max(0, 1 - (ease - 0.75) / 0.25));
      }
      if (p < 1) raf(frame);
      else cleanup(false);
    }
    raf(frame);
  }

  function runGatherFactors(pane, done) {
    var list = Array.prototype.slice.call(pane.querySelectorAll(".token.factor"));
    if (list.length < 3) {
      if (done) done();
      return;
    }
    anim.busy = true;
    var n = list.length;
    function clearG() {
      list.forEach(function (t) {
        t.classList.remove("gather-left", "gather-right", "gather-mid");
      });
    }
    function end() {
      clearG();
      anim.busy = false;
      anim.finish = null;
      if (done) done();
    }
    anim.finish = end;
    if (n === 6) {
      list[0].classList.add("gather-right");
      list[5].classList.add("gather-left");
      list[2].classList.add("gather-right");
      list[3].classList.add("gather-left");
      later(function () {
        if (anim.skip) { end(); return; }
        clearG();
        list[1].classList.add("gather-mid");
        list[4].classList.add("gather-mid");
        list[2].classList.add("gather-mid");
        list[3].classList.add("gather-mid");
        later(function () {
          if (anim.skip) { end(); return; }
          clearG();
          list[0].classList.add("gather-right");
          list[5].classList.add("gather-left");
          later(end, 520);
        }, 520);
      }, 520);
      return;
    }
    list.forEach(function (t, i) {
      if (i === 0) t.classList.add("gather-right");
      else if (i === n - 1) t.classList.add("gather-left");
      else if (i < n / 2) t.classList.add("gather-right");
      else t.classList.add("gather-left");
    });
    later(end, 640);
  }

  /** Multi-phase fraction build driven by data-phase on successive fragments */
  function runFracPhase(root) {
    if (!root) return;
    var build = root.closest(".frac-build") || root;
    var phase = root.getAttribute("data-phase") || build.getAttribute("data-phase");
    if (!phase && root.classList.contains("frac-phase")) {
      phase = root.getAttribute("data-phase");
    }
    var frac = build.querySelector(".frac-stack") || build;
    if (phase === "bar") {
      frac.classList.add("phase-bar");
      var bar = frac.querySelector(".frac-bar");
      if (bar) bar.classList.add("bar-in");
      return;
    }
    if (phase === "num") {
      frac.classList.add("phase-num");
      var num = frac.querySelector(".num");
      if (num) {
        num.classList.add("show-row");
        runFlyIns(num);
        later(function () {
          /* expand powers already laid out as separate a tokens */
          num.classList.add("expanded");
        }, FLY_MS + 200);
      }
      return;
    }
    if (phase === "den") {
      frac.classList.add("phase-den");
      var den = frac.querySelector(".den");
      if (den) {
        den.classList.add("show-row");
        runFlyIns(den);
        later(function () { den.classList.add("expanded"); }, FLY_MS + 200);
      }
      return;
    }
    if (phase === "cancel") {
      runCancelOnly(frac);
      return;
    }
    if (phase === "result") {
      runGatherToResult(frac);
      return;
    }
  }

  function runCancelOnly(frac) {
    if (!frac) return;
    anim.busy = true;
    var numCancels = frac.querySelectorAll(".num .token.cancelable");
    var denCancels = frac.querySelectorAll(".den .token.cancelable");
    var pairs = Math.min(numCancels.length, denCancels.length);
    var steps = [];
    var i;
    for (i = 0; i < pairs; i++) {
      steps.push(numCancels[i]);
      steps.push(denCancels[i]);
    }
    var step = 0;
    function finishAll() {
      while (step < steps.length) {
        if (steps[step]) steps[step].classList.add("struck");
        step += 1;
      }
      frac.classList.add("cancelled", "cancel-done");
      frac.querySelectorAll(".token.remain").forEach(function (t) {
        t.classList.add("is-remaining");
      });
      anim.busy = false;
      anim.finish = null;
    }
    anim.finish = finishAll;
    function next() {
      if (anim.skip) { finishAll(); return; }
      if (step >= steps.length) {
        finishAll();
        return;
      }
      if (steps[step]) steps[step].classList.add("struck");
      step += 1;
      later(next, CANCEL_MS);
    }
    later(next, 180);
  }

  function runGatherToResult(frac) {
    if (!frac) return;
    anim.busy = true;
    frac.classList.add("gathering");
    var rem = frac.querySelectorAll(".token.remain, .token.is-remaining");
    Array.prototype.forEach.call(rem, function (t) { t.classList.add("is-remaining"); });
    if (rem.length >= 2) {
      rem[0].classList.add("gather-right");
      rem[rem.length - 1].classList.add("gather-left");
      if (rem.length === 3) rem[1].classList.add("gather-mid");
    }
    var eq = frac.querySelector(".gather-eq");
    if (eq) eq.classList.add("show");
    function end() {
      frac.classList.add("gathered");
      var result = frac.querySelector(".cancel-result");
      if (result) {
        result.classList.add("show");
        renderMath(result);
      }
      Array.prototype.forEach.call(rem, function (t) {
        t.classList.remove("gather-left", "gather-right", "gather-mid");
      });
      anim.busy = false;
      anim.finish = null;
    }
    anim.finish = end;
    later(end, 700);
  }

  function runAutoSlot(slot) {
    if (!slot || !slot.classList.contains("work-slot")) return;
    clearAutoTimers();
    clearSourceMarks();
    purgeGhosts();
    var panes = slot.querySelectorAll(".stage-pane");
    if (!panes.length) {
      runFlyIns(slot);
      return;
    }
    slot.classList.add("playing");
    anim.slot = slot;
    activateStage(slot, 0);
    var first = panes[0].querySelector(".token");
    if (first) setExpandFrame(first, true);

    var i = 1;
    function step() {
      if (i >= panes.length) {
        slot.classList.remove("playing");
        anim.slot = null;
        slot.querySelectorAll(".expand-framed").forEach(function (el) {
          el.classList.remove("expand-framed");
        });
        return;
      }
      var prev = panes[i - 1];
      var next = panes[i];
      var nextHasFly = !!(next && next.querySelector("[data-fly-from]"));
      var prevHasPow = !!(prev && prev.querySelector(".pow"));
      var gather = next && next.getAttribute("data-gather") === "1";

      function after() {
        i += 1;
        if (i < panes.length) {
          later(step, anim.skip ? 80 : STAGE_MS * 0.85);
        } else {
          later(function () {
            slot.classList.remove("playing");
            anim.slot = null;
          }, 200);
        }
      }

      if (gather) {
        activateStage(slot, i);
        runGatherFactors(next, after);
      } else if (prevHasPow && !nextHasFly && next.querySelector(".peel-times, .next-factor, .peel-target")) {
        peelToStage(slot, i - 1, i, after);
      } else {
        activateStage(slot, i);
        after();
      }
    }
    later(step, FLY_MS + 280);
  }

  function resetAutoSlots(scope) {
    clearAutoTimers();
    (scope || document).querySelectorAll(".work-slot").forEach(function (slot) {
      slot.classList.remove("playing");
      var panes = slot.querySelectorAll(".stage-pane");
      panes.forEach(function (pane, idx) {
        pane.classList.remove("peel-arrive", "is-measure", "expand-framed");
        pane.classList.toggle("is-active", idx === 0 && slot.classList.contains("visible"));
        if (!slot.classList.contains("visible")) pane.classList.remove("is-active");
      });
    });
  }

  /** Animate decimal inside the big RHS equation (not a separate digit row) */
  function runSciJump(root) {
    if (!root) return;
    clearAutoTimers();
    var eqs = root.querySelectorAll(".sci-jump-eq");
    if (!eqs.length) return;
    eqs.forEach(function (el) { el.classList.remove("is-on"); });
    eqs[0].classList.add("is-on");
    var step = 1;

    function doJump() {
      if (step >= eqs.length) {
        anim.busy = false;
        anim.finish = null;
        return;
      }
      anim.busy = true;
      var cur = eqs[step - 1];
      var nxt = eqs[step];
      var dp = cur && cur.querySelector(".dp-live");
      var dpTo = nxt && nxt.querySelector(".dp-live");

      function finishJump() {
        eqs.forEach(function (el) { el.classList.remove("is-on"); });
        nxt.classList.add("is-on");
        root.setAttribute("data-jump-step", String(step));
        step += 1;
        later(doJump, anim.skip ? 60 : 640);
      }
      anim.finish = finishJump;

      if (dp && dpTo && !anim.skip) {
        var fr = dp.getBoundingClientRect();
        var tr = dpTo.getBoundingClientRect();
        /* Force leftward jump: if target is to the right, still use lower arc */
        var ghost = document.createElement("span");
        ghost.className = "dp-ghost";
        ghost.textContent = ".";
        ghost.style.left = fr.left + "px";
        ghost.style.top = fr.top + "px";
        document.body.appendChild(ghost);
        dp.style.opacity = "0";
        var dx = tr.left - fr.left;
        var dy = tr.top - fr.top;
        var dip = Math.max(30, Math.abs(dx) * 0.4);
        var t0 = null;
        var token = playToken;
        function frame(now) {
          if (token !== playToken) {
            if (ghost.parentNode) ghost.parentNode.removeChild(ghost);
            return;
          }
          if (anim.skip) {
            if (ghost.parentNode) ghost.parentNode.removeChild(ghost);
            dp.style.opacity = "";
            finishJump();
            return;
          }
          if (t0 == null) t0 = now;
          var p = Math.min(1, (now - t0) / JUMP_MS);
          var ease = 1 - Math.pow(1 - p, 2.2);
          ghost.style.transform = "translate(" + (dx * ease) + "px, " + (dy * ease + Math.sin(Math.PI * ease) * dip) + "px)";
          if (p < 1) raf(frame);
          else {
            if (ghost.parentNode) ghost.parentNode.removeChild(ghost);
            dp.style.opacity = "";
            finishJump();
          }
        }
        raf(frame);
      } else {
        finishJump();
      }
    }
    later(doJump, 700);
  }

  /** Two separate boxes drag down; at landing bottom slides right to combine with ×; frames fade */
  function runPvDrag(root) {
    if (!root) return;
    clearAutoTimers();
    var cells = root.querySelectorAll("[data-pv-pair]");
    var terms = root.querySelectorAll(".expand-term");
    if (!cells.length) return;
    var order = [];
    var map = {};
    Array.prototype.forEach.call(cells, function (cell) {
      var key = cell.getAttribute("data-pv-pair");
      if (!map[key]) {
        map[key] = [];
        order.push(key);
      }
      map[key].push(cell);
    });
    var i = 0;

    function next() {
      if (i >= order.length) {
        anim.busy = false;
        anim.finish = null;
        return;
      }
      anim.busy = true;
      var group = map[order[i]] || [];
      var term = terms[i];
      var digit = group[0];
      var place = group[1] || group[0];
      digit.classList.add("framed");
      place.classList.add("framed");

      function finishPair() {
        digit.classList.remove("framed");
        place.classList.remove("framed");
        digit.classList.add("dragged");
        place.classList.add("dragged");
        if (term) {
          term.classList.remove("awaiting", "combining");
          term.classList.add("landed");
        }
        document.querySelectorAll(".pv-drag-box").forEach(function (b) {
          if (b.parentNode) b.parentNode.removeChild(b);
        });
        i += 1;
        later(next, anim.skip ? 80 : 420);
      }
      anim.finish = finishPair;

      later(function () {
        if (anim.skip) { finishPair(); return; }
        if (!term) { finishPair(); return; }
        term.classList.add("awaiting");
        var dR = digit.getBoundingClientRect();
        var pR = place.getBoundingClientRect();
        var tR = term.getBoundingClientRect();

        function makeBox(rect, html) {
          var box = document.createElement("div");
          box.className = "pv-drag-box";
          box.innerHTML = html;
          box.style.left = rect.left + "px";
          box.style.top = rect.top + "px";
          box.style.width = rect.width + "px";
          box.style.height = rect.height + "px";
          document.body.appendChild(box);
          return box;
        }
        var boxD = makeBox(dR, digit.innerHTML);
        var boxP = makeBox(pR, place.innerHTML);
        /* Keep relative offset between digit and place */
        var relDy = pR.top - dR.top;
        var landX = tR.left;
        var landY = tR.top;
        raf(function () {
          raf(function () {
            boxD.style.transform = "translate(" + (landX - dR.left) + "px, " + (landY - dR.top) + "px)";
            boxP.style.transform = "translate(" + (landX - pR.left) + "px, " + (landY - pR.top + relDy * 0.15) + "px)";
          });
        });
        later(function () {
          if (anim.skip) { finishPair(); return; }
          /* Bottom box slides right under digit; × appears; frames fade */
          term.classList.add("combining");
          boxP.style.transform = "translate(" + (landX - pR.left + dR.width * 0.85) + "px, " + (landY - pR.top) + "px)";
          boxD.classList.add("fade-frame");
          boxP.classList.add("fade-frame");
          later(finishPair, 480);
        }, FLY_MS);
      }, 360);
    }
    later(next, 360);
  }

  function runConvStep(row) {
    if (!row) return;
    anim.busy = true;
    row.classList.add("rhs-in");
    var extra = row.querySelector(".conv-extra");
    var nextRow = row.nextElementSibling;
    while (nextRow && !nextRow.classList.contains("conv-row")) {
      nextRow = nextRow.nextElementSibling;
    }
    function end() {
      if (extra) {
        extra.classList.add("spent");
        if (nextRow) {
          var subj = nextRow.querySelector(".conv-subj");
          if (subj) {
            flyFromTo(extra, subj, 0);
            nextRow.classList.add("recv-extra");
          }
        }
      }
      anim.busy = false;
      anim.finish = null;
    }
    anim.finish = end;
    if (extra) {
      later(function () {
        extra.classList.add("dragging");
        later(end, 560);
      }, 500);
    } else {
      later(end, 400);
    }
  }

  function syncWorkChains() {
    document.querySelectorAll(".work-chain").forEach(function (chain) {
      var rows = Array.prototype.slice.call(chain.querySelectorAll(".work-row"));
      var visible = rows.filter(function (r) { return r.classList.contains("visible"); });
      var current = chain.querySelector(".work-row.current-fragment") || visible[visible.length - 1] || null;
      rows.forEach(function (row) {
        row.classList.toggle("chain-hidden", row.classList.contains("visible") && row !== current);
      });
    });
  }

  function trySkipAnim() {
    if (!anim.busy) return false;
    anim.skip = true;
    if (typeof anim.finish === "function") anim.finish();
    return true;
  }

  function onFragmentShown(ev) {
    syncCancelState();
    syncWorkChains();
    try {
      var frag = ev && ev.fragment;
      if (!frag) return;
      if (frag.classList.contains("work-slot")) {
        runAutoSlot(frag);
        return;
      }
      if (frag.classList.contains("frac-phase") || frag.getAttribute("data-phase")) {
        runFracPhase(frag);
        return;
      }
      if (frag.classList.contains("cancel-seq")) {
        runFlyIns(frag);
        later(function () { runCancelOnly(frag); }, FLY_MS + 100);
        return;
      }
      if (frag.classList.contains("sci-jump")) {
        runSciJump(frag);
        return;
      }
      if (frag.classList.contains("pv-expand")) {
        runPvDrag(frag);
        return;
      }
      if (frag.classList.contains("conv-row") && frag.closest(".conv-seq")) {
        runConvStep(frag);
        return;
      }
      clearSourceMarks();
      runFlyIns(frag);
    } catch (err) { /* */ }
  }

  function onFragmentHidden(ev) {
    syncCancelState();
    syncWorkChains();
    clearAutoTimers();
    purgeGhosts();
    var frag = ev && ev.fragment;
    if (frag) {
      restoreVisualState(frag);
      if (frag.classList.contains("work-slot")) {
        frag.classList.remove("playing");
        var panes = frag.querySelectorAll(".stage-pane");
        panes.forEach(function (pane, idx) {
          pane.classList.remove("is-active", "peel-arrive", "is-measure");
          if (idx === 0) pane.classList.add("is-active");
        });
      }
    }
  }

  Reveal.initialize({
    width: 1280,
    height: 720,
    margin: 0.04,
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
    try { Reveal.layout(); } catch (e) { /* */ }
    syncCancelState();

    /* Advance while animating → finish current step, then allow next advance */
    if (Reveal.next) {
      var origNext = Reveal.next.bind(Reveal);
      Reveal.next = function () {
        if (trySkipAnim()) return;
        return origNext();
      };
    }
  }

  if (Reveal.isReady && Reveal.isReady()) afterReady();
  else if (Reveal.on) Reveal.on("ready", afterReady);
  else setTimeout(afterReady, 60);

  if (Reveal.on) {
    Reveal.on("fragmentshown", onFragmentShown);
    Reveal.on("fragmenthidden", onFragmentHidden);
    Reveal.on("slidechanged", function () {
      clearAutoTimers();
      restoreVisualState(document);
      syncCancelState();
      syncWorkChains();
      resetAutoSlots(document);
    });
  }

  document.addEventListener("selectstart", function (e) { e.preventDefault(); });
  document.addEventListener("mousedown", function (e) {
    if (e.detail > 1) e.preventDefault();
  });
})();
