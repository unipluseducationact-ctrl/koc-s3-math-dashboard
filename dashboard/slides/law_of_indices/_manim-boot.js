/** Shared Reveal + KaTeX boot for JM24 Manim-style decks */
(function () {
  "use strict";

  var FLY_MS = 560;
  var PEEL_MS = 700;
  var STAGE_MS = 720;
  var CANCEL_MS = 420;
  var JUMP_MS = 620;
  var autoTimers = [];
  var playToken = 0;

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
    playToken += 1;
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

  function purgeGhosts() {
    document.querySelectorAll(".fly-ghost, .peel-ghost, .times-ghost, .dp-ghost, .pv-frame").forEach(function (g) {
      if (g.parentNode) g.parentNode.removeChild(g);
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

  function restoreVisualState(scope) {
    var root = scope || document;
    root.querySelectorAll(".token.cancelable, .token.struck").forEach(function (t) {
      t.classList.remove("struck", "gather-left", "gather-right", "gather-mid", "is-remaining");
    });
    root.querySelectorAll(".frac-stack").forEach(function (f) {
      f.classList.remove("cancelled", "cancel-done", "gathering", "gathered");
      f.removeAttribute("data-cancel-step");
    });
    root.querySelectorAll("sup.pow, .pow").forEach(function (p) {
      p.style.opacity = "";
    });
    root.querySelectorAll(".token.fly-wait, .token.fly-land").forEach(function (t) {
      t.classList.remove("fly-wait", "fly-land");
    });
    root.querySelectorAll(".sci-jump-eq").forEach(function (el) {
      el.classList.remove("is-on");
    });
    root.querySelectorAll(".dp-jump-row").forEach(function (row) {
      row.querySelectorAll(".dp").forEach(function (dp) {
        dp.classList.remove("jumping", "at-pos");
      });
      row.removeAttribute("data-jump-step");
    });
    root.querySelectorAll(".pv-pair, .pv-cell").forEach(function (c) {
      c.classList.remove("framed", "dragged");
    });
    root.querySelectorAll(".expand-term").forEach(function (t) {
      t.classList.remove("landed", "awaiting");
    });
    root.querySelectorAll(".conv-extra").forEach(function (e) {
      e.classList.remove("dragging", "spent");
    });
    clearSourceMarks();
    purgeGhosts();
  }

  function syncCancelState() {
    var f = -1;
    try {
      if (window.Reveal && Reveal.getIndices) f = Reveal.getIndices().f;
    } catch (e) { /* ignore */ }

    document.querySelectorAll(".frac-stack[data-cancel-at]").forEach(function (frac) {
      var at = parseInt(frac.getAttribute("data-cancel-at"), 10);
      if (isNaN(at)) return;
      if (frac.getAttribute("data-cancel-seq") != null) return;
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

  function activateStage(slot, index, opts) {
    opts = opts || {};
    var panes = slot.querySelectorAll(".stage-pane");
    var active = panes[index];
    if (!active) return;

    panes.forEach(function (pane, i) {
      if (i !== index) {
        pane.classList.remove("is-active", "peel-arrive", "is-measure");
      }
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
        flyFromTo(document.querySelector(sel), toEl, i * 70);
        later(function () {
          markSource(sel, true);
        }, FLY_MS + i * 70 + 40);
      });
    }
  }

  /** Lower-arc jump of power to mid-gap; × appears mid-air */
  function peelToStage(slot, fromIndex, toIndex, done) {
    var panes = slot.querySelectorAll(".stage-pane");
    var fromPane = panes[fromIndex];
    var toPane = panes[toIndex];
    if (!fromPane || !toPane) {
      activateStage(slot, toIndex);
      if (done) done();
      return;
    }

    var pow = fromPane.querySelector("sup.pow.outer, .token > .pow.outer");
    if (!pow) {
      var pows = fromPane.querySelectorAll("sup.pow, .token > .pow");
      pow = pows.length ? pows[pows.length - 1] : null;
    }
    if (!pow) {
      activateStage(slot, toIndex, { peel: true });
      later(function () {
        toPane.classList.remove("peel-arrive");
        if (done) done();
      }, 480);
      return;
    }

    /* Measure target mid-gap while keeping fromPane visible */
    toPane.classList.add("is-measure");
    var timesEl = toPane.querySelector(".token.op.peel-times, .token.op");
    var rightPow = null;
    var tokens = toPane.querySelectorAll(".token:not(.op)");
    if (tokens.length >= 2) rightPow = tokens[1];
    else if (tokens.length === 1) rightPow = tokens[0];

    var fromR = pow.getBoundingClientRect();
    var midX;
    var midY;
    if (timesEl) {
      var tr = timesEl.getBoundingClientRect();
      midX = tr.left + tr.width / 2;
      midY = tr.top + tr.height / 2;
    } else if (rightPow) {
      var rr = rightPow.getBoundingClientRect();
      midX = (fromR.left + fromR.width / 2 + rr.left + rr.width / 2) / 2;
      midY = (fromR.top + fromR.height / 2 + rr.top + rr.height / 2) / 2;
    } else {
      midX = fromR.left + fromR.width / 2 + 72;
      midY = fromR.top + fromR.height / 2 + 18;
    }
    toPane.classList.remove("is-measure");

    var startX = fromR.left + fromR.width / 2;
    var startY = fromR.top + fromR.height / 2;
    var dx = midX - startX;
    var dy = midY - startY;
    /* Lower semicircle: dip below the line */
    var dip = Math.max(36, Math.abs(dx) * 0.28);

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

    var t0 = null;
    function frame(now) {
      if (playToken !== peelToken) {
        if (ghost.parentNode) ghost.parentNode.removeChild(ghost);
        if (timesGhost.parentNode) timesGhost.parentNode.removeChild(timesGhost);
        return;
      }
      if (t0 == null) t0 = now;
      var p = Math.min(1, (now - t0) / PEEL_MS);
      var ease = 1 - Math.pow(1 - p, 2.4);
      var arcY = Math.sin(Math.PI * ease) * dip;
      var x = dx * ease;
      var y = dy * ease + arcY;
      ghost.style.transform = "translate(" + x + "px, " + y + "px) scale(" + (1 + 0.2 * Math.sin(Math.PI * ease)) + ")";
      if (p >= 0.42 && p <= 0.85) {
        timesGhost.style.opacity = String(Math.min(1, (p - 0.42) / 0.2));
        timesGhost.style.transform = "translate(-50%, -50%) scale(" + (0.7 + 0.4 * Math.min(1, (p - 0.42) / 0.25)) + ")";
      }
      if (p < 1) {
        window.requestAnimationFrame(frame);
      } else {
        ghost.style.opacity = "0";
        timesGhost.style.opacity = "0";
        fromPane.classList.remove("is-active");
        pow.style.opacity = "";
        activateStage(slot, toIndex, { peel: true });
        later(function () {
          if (ghost.parentNode) ghost.parentNode.removeChild(ghost);
          if (timesGhost.parentNode) timesGhost.parentNode.removeChild(timesGhost);
          toPane.classList.remove("peel-arrive");
          if (done) done();
        }, 420);
      }
    }
    var peelToken = playToken;
    window.requestAnimationFrame(frame);
  }

  function runGatherFactors(pane, done) {
    var factors = pane.querySelectorAll(".token.factor");
    if (!factors.length) {
      factors = pane.querySelectorAll(".token.sym-a, .token.sym-a2");
    }
    var list = Array.prototype.filter.call(factors, function (t) {
      return !t.classList.contains("op");
    });
    if (list.length < 3) {
      if (done) done();
      return;
    }
    var n = list.length;
    /* For 6 factors: 1→2, 6→5, 3+4→mid → three a², then sides → center */
    if (n === 6) {
      list[0].classList.add("gather-right");
      list[5].classList.add("gather-left");
      list[2].classList.add("gather-right");
      list[3].classList.add("gather-left");
      later(function () {
        list.forEach(function (t) {
          t.classList.remove("gather-left", "gather-right", "gather-mid");
        });
        list[0].classList.add("gather-right");
        list[1].classList.add("gather-mid");
        list[4].classList.add("gather-left");
        list[5].classList.add("gather-left");
        list[2].classList.add("gather-mid");
        list[3].classList.add("gather-mid");
        later(function () {
          list.forEach(function (t) {
            t.classList.remove("gather-left", "gather-right", "gather-mid");
          });
          list[0].classList.add("gather-right");
          list[5].classList.add("gather-left");
          list[1].classList.add("gather-right");
          list[4].classList.add("gather-left");
          later(function () {
            list.forEach(function (t) {
              t.classList.remove("gather-left", "gather-right", "gather-mid");
            });
            if (done) done();
          }, 650);
        }, 650);
      }, 650);
      return;
    }
    list.forEach(function (t, i) {
      if (i === 0) t.classList.add("gather-right");
      else if (i === n - 1) t.classList.add("gather-left");
      else if (i < n / 2) t.classList.add("gather-right");
      else t.classList.add("gather-left");
    });
    later(function () {
      list.forEach(function (t) {
        t.classList.remove("gather-left", "gather-right", "gather-mid");
      });
      if (done) done();
    }, 780);
  }

  function runCancelSeq(frac, done) {
    if (!frac) {
      if (done) done();
      return;
    }
    restoreVisualState(frac);
    var numCancels = frac.querySelectorAll(".num .token.cancelable");
    var denCancels = frac.querySelectorAll(".den .token.cancelable");
    var remaining = frac.querySelectorAll(".num .token.remain, .num .token:not(.cancelable):not(.op)");
    var pairs = Math.min(numCancels.length, denCancels.length);
    var steps = [];
    var i;
    for (i = 0; i < pairs; i++) {
      steps.push({ el: numCancels[i], side: "num" });
      steps.push({ el: denCancels[i], side: "den" });
    }

    var step = 0;
    function next() {
      if (step < steps.length) {
        var s = steps[step];
        if (s.el) s.el.classList.add("struck");
        frac.setAttribute("data-cancel-step", String(step + 1));
        step += 1;
        later(next, CANCEL_MS);
        return;
      }
      frac.classList.add("cancelled", "cancel-done");
      Array.prototype.forEach.call(remaining, function (t) {
        t.classList.add("is-remaining");
      });
      later(function () {
        frac.classList.add("gathering");
        var rem = frac.querySelectorAll(".num .token.is-remaining");
        if (rem.length >= 3) {
          rem[0].classList.add("gather-right");
          rem[rem.length - 1].classList.add("gather-left");
          if (rem.length === 3) rem[1].classList.add("gather-mid");
        } else {
          Array.prototype.forEach.call(rem, function (t, idx) {
            if (idx < rem.length / 2) t.classList.add("gather-right");
            else t.classList.add("gather-left");
          });
        }
        later(function () {
          frac.classList.add("gathered");
          var result = frac.querySelector(".cancel-result");
          if (result) result.classList.add("show");
          if (done) done();
        }, 700);
      }, 280);
    }
    later(next, 200);
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
    activateStage(slot, 0);

    var i = 1;
    function step() {
      if (i >= panes.length) {
        slot.classList.remove("playing");
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
          var cur = panes[i - 1];
          var wait = cur && cur.querySelector("[data-fly-from]")
            ? FLY_MS + STAGE_MS * 0.55
            : STAGE_MS * 0.9;
          if (gather) wait = 2200;
          later(step, wait);
        } else {
          later(function () { slot.classList.remove("playing"); }, 280);
        }
      }

      if (gather) {
        activateStage(slot, i);
        runGatherFactors(next, after);
      } else if (prevHasPow && !nextHasFly) {
        peelToStage(slot, i - 1, i, after);
      } else {
        activateStage(slot, i);
        after();
      }
    }

    later(step, FLY_MS + STAGE_MS * 0.55);
  }

  function resetAutoSlots(scope) {
    clearAutoTimers();
    (scope || document).querySelectorAll(".work-slot").forEach(function (slot) {
      slot.classList.remove("playing");
      var panes = slot.querySelectorAll(".stage-pane");
      panes.forEach(function (pane, i) {
        pane.classList.remove("peel-arrive", "is-measure");
        pane.classList.toggle("is-active", i === 0 && slot.classList.contains("visible"));
        if (!slot.classList.contains("visible")) pane.classList.remove("is-active");
      });
    });
  }

  /** Step-by-step lower-arc decimal jumps: 5000.=5000.×10^0 → … → 5×10^3 */
  function runSciJump(root) {
    if (!root) return;
    clearAutoTimers();
    var eqs = root.querySelectorAll(".sci-jump-eq");
    var row = root.querySelector(".dp-jump-row");
    if (!eqs.length) return;

    eqs.forEach(function (el) { el.classList.remove("is-on"); });
    if (eqs[0]) eqs[0].classList.add("is-on");

    var step = 1;
    function jump() {
      if (step >= eqs.length) return;
      var dp = row && row.querySelector(".dp");
      if (dp && row) {
        var slots = row.querySelectorAll("[data-dp-slot]");
        var fromSlot = slots[step - 1] || dp;
        var toSlot = slots[step] || slots[slots.length - 1];
        var fr = fromSlot.getBoundingClientRect();
        var tr = toSlot.getBoundingClientRect();
        var ghost = document.createElement("span");
        ghost.className = "dp-ghost";
        ghost.textContent = ".";
        ghost.style.left = fr.left + "px";
        ghost.style.top = fr.top + "px";
        document.body.appendChild(ghost);
        dp.style.opacity = "0";

        var dx = tr.left - fr.left;
        var dy = tr.top - fr.top;
        var dip = Math.max(28, Math.abs(dx) * 0.35);
        var t0 = null;
        var token = playToken;
        function frame(now) {
          if (token !== playToken) {
            if (ghost.parentNode) ghost.parentNode.removeChild(ghost);
            return;
          }
          if (t0 == null) t0 = now;
          var p = Math.min(1, (now - t0) / JUMP_MS);
          var ease = 1 - Math.pow(1 - p, 2.2);
          var y = dy * ease + Math.sin(Math.PI * ease) * dip;
          ghost.style.transform = "translate(" + (dx * ease) + "px, " + y + "px)";
          if (p < 1) {
            window.requestAnimationFrame(frame);
          } else {
            if (ghost.parentNode) ghost.parentNode.removeChild(ghost);
            dp.style.opacity = "";
            eqs.forEach(function (el) { el.classList.remove("is-on"); });
            if (eqs[step]) eqs[step].classList.add("is-on");
            if (row) row.setAttribute("data-jump-step", String(step));
            step += 1;
            later(jump, 520);
          }
        }
        window.requestAnimationFrame(frame);
      } else {
        eqs.forEach(function (el) { el.classList.remove("is-on"); });
        if (eqs[step]) eqs[step].classList.add("is-on");
        step += 1;
        later(jump, 700);
      }
    }
    later(jump, 700);
  }

  /** Yellow frame around digit+place (same data-pv-pair), drag down into expand term */
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
      if (i >= order.length) return;
      var group = map[order[i]] || [];
      var term = terms[i];
      group.forEach(function (c) { c.classList.add("framed"); });
      later(function () {
        if (!term || !group.length) {
          group.forEach(function (c) {
            c.classList.remove("framed");
            c.classList.add("dragged");
          });
          i += 1;
          later(next, 360);
          return;
        }
        term.classList.add("awaiting");
        var top = group[0].getBoundingClientRect();
        var bot = (group[1] || group[0]).getBoundingClientRect();
        var left = Math.min(top.left, bot.left);
        var right = Math.max(top.right, bot.right);
        var fromTop = top.top;
        var fromBottom = bot.bottom;
        var frame = document.createElement("div");
        frame.className = "fly-ghost flying pv-frame";
        frame.style.left = left + "px";
        frame.style.top = fromTop + "px";
        frame.style.width = (right - left) + "px";
        frame.style.height = (fromBottom - fromTop) + "px";
        frame.style.border = "2px solid #ffd54f";
        frame.style.borderRadius = "6px";
        frame.style.background = "rgba(255,213,79,0.12)";
        document.body.appendChild(frame);
        var to = term.getBoundingClientRect();
        var dx = to.left - left + (to.width - (right - left)) / 2;
        var dy = to.top - fromTop;
        window.requestAnimationFrame(function () {
          window.requestAnimationFrame(function () {
            frame.style.transform = "translate(" + dx + "px, " + dy + "px) scale(0.55)";
            frame.style.opacity = "0.35";
          });
        });
        later(function () {
          if (frame.parentNode) frame.parentNode.removeChild(frame);
          term.classList.remove("awaiting");
          term.classList.add("landed");
          group.forEach(function (c) {
            c.classList.remove("framed");
            c.classList.add("dragged");
          });
          i += 1;
          later(next, 420);
        }, FLY_MS);
      }, 380);
    }
    later(next, 400);
  }

  function runConvDrag(root) {
    if (!root) return;
    var extras = root.querySelectorAll(".conv-extra");
    extras.forEach(function (extra, idx) {
      later(function () {
        extra.classList.add("dragging");
        later(function () {
          extra.classList.add("spent");
          var nextRow = root.querySelectorAll(".conv-row")[idx + 1];
          if (nextRow) nextRow.classList.add("recv-extra");
        }, 500);
      }, 600 + idx * 1100);
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
      if (!frag) return;

      if (frag.classList.contains("work-slot")) {
        runAutoSlot(frag);
        return;
      }
      if (frag.classList.contains("cancel-seq") || frag.getAttribute("data-cancel-seq") != null) {
        runFlyIns(frag);
        later(function () { runCancelSeq(frag); }, FLY_MS + 120);
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
      if (frag.classList.contains("conv-seq")) {
        runFlyIns(frag);
        runConvDrag(frag);
        return;
      }
      clearSourceMarks();
      runFlyIns(frag);
    } catch (err) { /* ignore */ }
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
        panes.forEach(function (pane, i) {
          pane.classList.remove("is-active", "peel-arrive", "is-measure");
          if (i === 0) pane.classList.add("is-active");
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
