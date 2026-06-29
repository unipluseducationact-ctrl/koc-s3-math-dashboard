/* Factor Blaster — match factored <-> expanded forms by shooting the correct answer.
 * DOM-based shooter so every prompt/answer renders as real LaTeX (KaTeX).
 * Controls: <- -> move cannon, Space / ArrowUp shoot, or click an answer.
 * Modes: Expand (factored->expansion), Factorize (identities), Cross method (quadratics).
 * Round-based: choose mode + number of questions + speed; 3-2-1 countdown; end-of-round summary with ticks/crosses.
 */
(function () {
  "use strict";

  const C = { ink: "#e5e7eb" };

  // ── Bank (21): p = factored, c = correct expansion, d = expansion distractors, fd = factored distractors ──
  const BANK = [
    { p: "(x+5)^2",  c: "x^2+10x+25",  d: ["x^2+25", "x^2+5x+25", "x^2-10x+25"],              fd: ["(x-5)^2", "(x+5)(x-5)", "(x+10)^2"] },
    { p: "(x+3)^2",  c: "x^2+6x+9",    d: ["x^2+9", "x^2+3x+9", "x^2-6x+9"],                  fd: ["(x-3)^2", "(x+3)(x-3)", "(x+6)^2"] },
    { p: "(2x+1)^2", c: "4x^2+4x+1",   d: ["4x^2+1", "4x^2+2x+1", "4x^2-4x+1"],               fd: ["(2x-1)^2", "(2x+1)(2x-1)", "(4x+1)^2"] },
    { p: "(3x+2)^2", c: "9x^2+12x+4",  d: ["9x^2+4", "9x^2+6x+4", "9x^2-12x+4"],              fd: ["(3x-2)^2", "(3x+2)(3x-2)", "(9x+2)^2"] },
    { p: "(4x+3y)^2", c: "16x^2+24xy+9y^2", d: ["16x^2+9y^2", "16x^2+12xy+9y^2", "16x^2-24xy+9y^2"], fd: ["(4x-3y)^2", "(4x+3y)(4x-3y)", "(4x+9y)^2"] },
    { p: "(x+7)^2",  c: "x^2+14x+49",  d: ["x^2+49", "x^2+7x+49", "x^2-14x+49"],              fd: ["(x-7)^2", "(x+7)(x-7)", "(x+14)^2"] },
    { p: "(2x+5y)^2", c: "4x^2+20xy+25y^2", d: ["4x^2+25y^2", "4x^2+10xy+25y^2", "4x^2-20xy+25y^2"], fd: ["(2x-5y)^2", "(2x+5y)(2x-5y)", "(2x+10y)^2"] },
    { p: "(x-4)^2",  c: "x^2-8x+16",   d: ["x^2+8x+16", "x^2-4x+16", "x^2-16"],               fd: ["(x+4)^2", "(x-4)(x+4)", "(x-8)^2"] },
    { p: "(x-2)^2",  c: "x^2-4x+4",    d: ["x^2+4x+4", "x^2-2x+4", "x^2-4"],                  fd: ["(x+2)^2", "(x-2)(x+2)", "(x-4)^2"] },
    { p: "(3x-1)^2", c: "9x^2-6x+1",   d: ["9x^2+6x+1", "9x^2-3x+1", "9x^2-1"],               fd: ["(3x+1)^2", "(3x-1)(3x+1)", "(9x-1)^2"] },
    { p: "(2x-5)^2", c: "4x^2-20x+25", d: ["4x^2+20x+25", "4x^2-10x+25", "4x^2-25"],          fd: ["(2x+5)^2", "(2x-5)(2x+5)", "(4x-5)^2"] },
    { p: "(5x-2y)^2", c: "25x^2-20xy+4y^2", d: ["25x^2+20xy+4y^2", "25x^2-10xy+4y^2", "25x^2-4y^2"], fd: ["(5x+2y)^2", "(5x-2y)(5x+2y)", "(5x-4y)^2"] },
    { p: "(x-8)^2",  c: "x^2-16x+64",  d: ["x^2+16x+64", "x^2-8x+64", "x^2-64"],              fd: ["(x+8)^2", "(x-8)(x+8)", "(x-16)^2"] },
    { p: "(3x-4y)^2", c: "9x^2-24xy+16y^2", d: ["9x^2+24xy+16y^2", "9x^2-12xy+16y^2", "9x^2-16y^2"], fd: ["(3x+4y)^2", "(3x-4y)(3x+4y)", "(3x-8y)^2"] },
    { p: "(x+5)(x-5)",   c: "x^2-25",  d: ["x^2+25", "x^2-10x+25", "x^2+10x-25"],             fd: ["(x-5)^2", "(x+5)^2", "(5+x)(5-x)"] },
    { p: "(x+8)(x-8)",   c: "x^2-64",  d: ["x^2+64", "x^2-16x+64", "x^2+16x-64"],             fd: ["(x-8)^2", "(x+8)^2", "(8+x)(8-x)"] },
    { p: "(2x+3)(2x-3)", c: "4x^2-9",  d: ["4x^2+9", "4x^2-12x+9", "4x^2+12x-9"],             fd: ["(2x-3)^2", "(2x+3)^2", "(3+2x)(3-2x)"] },
    { p: "(3x+4)(3x-4)", c: "9x^2-16", d: ["9x^2+16", "9x^2-24x+16", "9x^2+24x-16"],          fd: ["(3x-4)^2", "(3x+4)^2", "(4+3x)(4-3x)"] },
    { p: "(x+6)(x-6)",   c: "x^2-36",  d: ["x^2+36", "x^2-12x+36", "x^2+12x-36"],             fd: ["(x-6)^2", "(x+6)^2", "(6+x)(6-x)"] },
    { p: "(4x+5y)(4x-5y)", c: "16x^2-25y^2", d: ["16x^2+25y^2", "16x^2-40xy+25y^2", "16x^2+40xy-25y^2"], fd: ["(4x-5y)^2", "(4x+5y)^2", "(5y+4x)(5y-4x)"] },
    { p: "(7x+1)(7x-1)", c: "49x^2-1", d: ["49x^2+1", "49x^2-14x+1", "49x^2+14x-1"],          fd: ["(7x-1)^2", "(7x+1)^2", "(1+7x)(1-7x)"] },
  ];

  // ── Cross method bank: p = factored, c = trinomial, fd = wrong factorisations ──
  const CROSS_BANK = [
    { p: "(x-7)(x+1)", c: "x^2-6x-7", fd: ["(x-7)(x-1)", "(x+1)(x+7)", "(x-6)(x+1)"] },
    { p: "(x+1)(x+3)", c: "x^2+4x+3", fd: ["(x+1)(x-3)", "(x+3)(x-1)", "(x+2)(x+2)"] },
    { p: "(x-1)(x-13)", c: "x^2-14x+13", fd: ["(x+1)(x-13)", "(x-1)(x+13)", "(x-7)(x-7)"] },
    { p: "(x+1)(x+7)", c: "x^2+8x+7", fd: ["(x+1)(x-7)", "(x+7)(x-1)", "(x+2)(x+5)"] },
    { p: "(y+6)(y-2)", c: "y^2+4y-12", fd: ["(y+6)(y+2)", "(y-6)(y-2)", "(y+3)(y-4)"] },
    { p: "(n+5)(n+7)", c: "n^2+12n+35", fd: ["(n+5)(n-7)", "(n+7)(n-5)", "(n+6)(n+6)"] },
    { p: "(x-7y)(x+5y)", c: "x^2-2xy-35y^2", fd: ["(x-7y)(x-5y)", "(x+7y)(x+5y)", "(x-5y)(x-7y)"] },
    { p: "(x-3y)(x-5y)", c: "x^2-8xy+15y^2", fd: ["(x-3y)(x+5y)", "(x+3y)(x-5y)", "(x-4y)(x-4y)"] },
    { p: "(p+3q)(p+5q)", c: "p^2+8pq+15q^2", fd: ["(p+3q)(p-5q)", "(p-3q)(p+5q)", "(p+5q)(p+5q)"] },
    { p: "(x+2y)(x+15y)", c: "x^2+17xy+30y^2", fd: ["(x+2y)(x-15y)", "(x+3y)(x+10y)", "(x+5y)(x+6y)"] },
    { p: "(a-4b)(a-14b)", c: "a^2-18ab+56b^2", fd: ["(a+4b)(a-14b)", "(a-4b)(a+14b)", "(a-7b)(a-8b)"] },
    { p: "(s+7)(s-13)", c: "s^2-6s-91", fd: ["(s+7)(s+13)", "(s-7)(s-13)", "(s+1)(s-91)"] },
    { p: "(n+8)(n+9)", c: "n^2+17n+72", fd: ["(n+8)(n-9)", "(n+9)(n-8)", "(n+6)(n+12)"] },
    { p: "(x+4y)(x-8y)", c: "x^2-4xy-32y^2", fd: ["(x+4y)(x+8y)", "(x-4y)(x-8y)", "(x+2y)(x-16y)"] },
    { p: "(x-3y)(x+5y)", c: "x^2+2xy-15y^2", fd: ["(x-3y)(x-5y)", "(x+3y)(x+5y)", "(x-y)(x+15y)"] },
    // leading coefficient ≠ 1 (from worked solutions + classics)
    { p: "(2x+1)(x+3)", c: "2x^2+7x+3", fd: ["(2x+3)(x+1)", "(x+1)(x+3)", "(2x-1)(x-3)"] },
    { p: "(x+2)(2x-5)", c: "2x^2-x-10", fd: ["(x-2)(2x+5)", "(x+5)(2x+2)", "(2x+1)(x-10)"] },
    { p: "(2x-3)(7x-2)", c: "14x^2-25x+6", fd: ["(2x+3)(7x+2)", "(2x-1)(7x-6)", "(x-3)(14x-2)"] },
    { p: "(x-4)(6x+1)", c: "6x^2-23x-4", fd: ["(x+4)(6x-1)", "(x-1)(6x+4)", "(2x-4)(3x+1)"] },
    { p: "(a-2c)(3a-c)", c: "3a^2-7ac+2c^2", fd: ["(a+2c)(3a+c)", "(a-c)(3a-2c)", "(3a-2c)(a-c)"] },
    { p: "(x-3y)(5x-2y)", c: "5x^2-17xy+6y^2", fd: ["(x+3y)(5x+2y)", "(x-2y)(5x-3y)", "(x-6y)(5x-y)"] },
    { p: "(a-6)(5a-1)", c: "5a^2-31a+6", fd: ["(a+6)(5a+1)", "(a-1)(5a-6)", "(a-2)(5a-3)"] },
    { p: "(3x+4y)(5x-7y)", c: "15x^2-xy-28y^2", fd: ["(3x-4y)(5x+7y)", "(3x+7y)(5x-4y)", "(x+4y)(15x-7y)"] },
    { p: "(b-6)(5b-1)", c: "5b^2-31b+6", fd: ["(b+6)(5b+1)", "(b-1)(5b-6)", "(b-2)(5b-3)"] },
    { p: "(2\\theta+7\\phi)(3\\theta-2\\phi)", c: "6\\theta^2+17\\theta\\phi-14\\phi^2", fd: ["(2\\theta-7\\phi)(3\\theta+2\\phi)", "(\\theta+7\\phi)(6\\theta-2\\phi)", "(3\\theta+7\\phi)(2\\theta-2\\phi)"] },
  ];

  // ── runtime state ──
  let stage, promptEl, enemiesEl, cannonEl, overlayEl, setupEl, summaryEl, countdownEl;
  let elScore, elAcc, elStreak, elQnum;
  let mode = "expand", numQ = 10, speed = 30, lanes = 4;
  let running = false, inRound = false, locked = false, activeFlag = false, rafId = null, lastT = 0;
  let cannonLane = 1, fireCooldown = 0;
  let enemies = [], roundQueue = [], results = [];
  let curPrompt = "", curCorrect = "";
  let qIndex = 0, score = 0, answered = 0, correctCount = 0, streak = 0;
  let soundOn = true, audioCtx = null;
  const Y0 = 78;

  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
    return a;
  }
  function kx(el, tex, color) {
    try { katex.render(tex, el, { throwOnError: false, displayMode: false }); }
    catch (e) { el.textContent = tex; }
    if (color) el.style.color = color;
  }
  function speedFromSlider(v) { return 12 * v + 6; }

  // ── audio ──
  function ensureAudio() { if (!audioCtx) { try { audioCtx = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) {} } }
  function tone(type, freqA, freqB, dur, gain, t0) {
    const t = t0 == null ? audioCtx.currentTime : t0;
    const o = audioCtx.createOscillator(), g = audioCtx.createGain();
    o.type = type; o.frequency.setValueAtTime(freqA, t);
    if (freqB) o.frequency.exponentialRampToValueAtTime(freqB, t + dur);
    g.gain.setValueAtTime(gain, t); g.gain.exponentialRampToValueAtTime(0.001, t + dur + 0.02);
    o.connect(g).connect(audioCtx.destination); o.start(t); o.stop(t + dur + 0.04);
  }
  function beep(type) {
    if (!soundOn || !audioCtx) return;
    if (type === "laser") tone("square", 880, 220, 0.12, 0.12);
    else if (type === "wrong") tone("sawtooth", 180, 70, 0.3, 0.16);
    else if (type === "tick") tone("triangle", 660, null, 0.1, 0.14);
    else if (type === "go") tone("triangle", 990, 1480, 0.25, 0.18);
    else if (type === "correct") {
      const t = audioCtx.currentTime;
      [523, 659, 784, 1047].forEach((f, i) => tone("triangle", f, null, 0.16, 0.16, t + i * 0.07));
    }
  }

  function laneCenter(lane) { return stage.clientWidth * (lane + 0.5) / lanes; }

  function specExpand(b) { return { promptTex: b.p, correctTex: b.c, pool: [b.c].concat(b.d) }; }
  function specFactorize(b) { return { promptTex: b.c, correctTex: b.p, pool: [b.p].concat(b.fd) }; }

  function basisFor(m) {
    if (m === "cross") return CROSS_BANK.map(specFactorize);
    if (m === "factorize") return BANK.map(specFactorize);
    return BANK.map(specExpand);
  }
  function buildRoundQueue() {
    const basis = basisFor(mode);
    const out = []; let pool = [];
    while (out.length < numQ) { if (pool.length === 0) pool = shuffle(basis); out.push(pool.pop()); }
    return out;
  }

  function spawnQuestion() {
    enemies.forEach((e) => e.el.remove()); enemies = [];
    if (qIndex >= numQ) { endRound(); return; }
    const cur = roundQueue[qIndex];
    curPrompt = cur.promptTex; curCorrect = cur.correctTex;
    lanes = cur.pool.length;
    kx(promptEl, cur.promptTex, C.ink);
    elQnum.textContent = (qIndex + 1) + "/" + numQ;
    cannonLane = Math.min(cannonLane, lanes - 1);
    const opts = shuffle(cur.pool.map((t) => ({ tex: t, correct: t === cur.correctTex })));
    opts.forEach((opt, lane) => {
      const el = document.createElement("div");
      el.className = "enemy";
      const inner = document.createElement("div"); el.appendChild(inner);
      kx(inner, opt.tex, null);
      enemiesEl.appendChild(el);
      const e = { el, lane, y: Y0, correct: opt.correct, tex: opt.tex, dead: false };
      el.addEventListener("click", () => { if (running && !locked) { cannonLane = lane; placeCannon(); fire(); } });
      enemies.push(e); placeEnemy(e);
    });
    placeCannon(); locked = false;
  }
  function placeEnemy(e) {
    const w = stage.clientWidth / lanes;
    e.el.style.width = (w - 18) + "px";
    e.el.style.left = (laneCenter(e.lane) - (w - 18) / 2) + "px";
    e.el.style.top = e.y + "px";
  }
  function placeCannon() { cannonEl.style.left = (laneCenter(cannonLane) - cannonEl.offsetWidth / 2) + "px"; }

  function flashLaser(lane) {
    const beam = document.createElement("div"); beam.className = "laser-beam";
    beam.style.left = (laneCenter(lane) - 3) + "px"; enemiesEl.appendChild(beam);
    setTimeout(() => beam.remove(), 140);
  }
  function boom(e, ok) {
    const fx = document.createElement("div"); fx.className = "boom " + (ok ? "boom-ok" : "boom-bad");
    fx.style.left = e.el.style.left; fx.style.top = e.el.style.top; fx.style.width = e.el.style.width;
    enemiesEl.appendChild(fx); setTimeout(() => fx.remove(), 420);
  }
  function shake() { stage.classList.add("shake"); setTimeout(() => stage.classList.remove("shake"), 300); }
  function highlightCorrect() {
    const c = enemies.find((e) => e.correct);
    if (c) { c.el.style.background = "linear-gradient(180deg,#bff3cf,#81e7a0)"; c.el.style.borderColor = "#d7ffe6"; }
  }

  function resolve(chosen, ok) {
    if (locked) return; locked = true;
    results.push({ p: curPrompt, correctTex: curCorrect, chosenTex: chosen, ok: ok });
    answered++;
    if (ok) { correctCount++; streak++; score += 100 + (streak - 1) * 20; }
    else { streak = 0; score = Math.max(0, score - 20); }
    updateHud(); qIndex++;
    setTimeout(spawnQuestion, ok ? 360 : 850);
  }
  function fire() {
    if (!running || locked || fireCooldown > 0) return;
    fireCooldown = 0.22; flashLaser(cannonLane); beep("laser");
    const target = enemies.find((e) => e.lane === cannonLane && !e.dead);
    if (!target) return;
    target.el.style.visibility = "hidden";
    if (target.correct) { boom(target, true); beep("correct"); resolve(target.tex, true); }
    else { boom(target, false); beep("wrong"); shake(); highlightCorrect(); resolve(target.tex, false); }
  }
  function miss() { if (locked) return; beep("wrong"); shake(); highlightCorrect(); resolve(null, false); }

  function updateHud() {
    elScore.textContent = score;
    elAcc.textContent = (answered ? Math.round((correctCount / answered) * 100) : 100) + "%";
    elStreak.textContent = streak;
  }

  function loop(t) {
    if (!running) return;
    const dt = Math.min(0.05, (t - lastT) / 1000 || 0); lastT = t;
    if (fireCooldown > 0) fireCooldown -= dt;
    const limit = stage.clientHeight - 96;
    let reached = false;
    if (!locked) {
      enemies.forEach((e) => { if (e.dead) return; e.y += speed * dt; e.el.style.top = e.y + "px"; if (e.y >= limit) reached = true; });
      if (reached) miss();
    }
    rafId = requestAnimationFrame(loop);
  }

  function runCountdown(done) {
    countdownEl.classList.remove("hidden");
    let n = 3;
    const step = () => {
      countdownEl.classList.remove("cd-pop"); void countdownEl.offsetWidth; countdownEl.classList.add("cd-pop");
      if (n > 0) { countdownEl.textContent = n; beep("tick"); n--; setTimeout(step, 700); }
      else { countdownEl.textContent = "Go!"; beep("go"); setTimeout(() => { countdownEl.classList.add("hidden"); done(); }, 520); }
    };
    step();
  }

  function startRound() {
    ensureAudio(); if (audioCtx && audioCtx.state === "suspended") audioCtx.resume();
    roundQueue = buildRoundQueue();
    results = []; qIndex = 0; score = 0; answered = 0; correctCount = 0; streak = 0;
    lanes = roundQueue[0] ? roundQueue[0].pool.length : 4;
    cannonLane = Math.floor(lanes / 2);
    overlayEl.classList.add("hidden");
    updateHud(); spawnQuestion(); // first question shown (static) during countdown
    running = false;
    runCountdown(() => {
      inRound = true;
      if (activeFlag) { running = true; lastT = performance.now(); cancelAnimationFrame(rafId); rafId = requestAnimationFrame(loop); }
    });
  }

  function endRound() {
    running = false; inRound = false;
    enemies.forEach((e) => e.el.remove()); enemies = [];
    kx(promptEl, "\\;", C.ink);
    showSummary();
  }
  function showSummary() {
    document.getElementById("sum-stats").textContent =
      "Score " + score + "  ·  " + correctCount + "/" + results.length + " correct  ·  " +
      (results.length ? Math.round((correctCount / results.length) * 100) : 0) + "% accuracy";
    const list = document.getElementById("sum-list"); list.innerHTML = "";
    results.forEach((r, i) => {
      const row = document.createElement("div"); row.className = "sum-row";
      const mark = document.createElement("span"); mark.className = "sum-mark " + (r.ok ? "sum-ok" : "sum-bad");
      mark.textContent = r.ok ? "\u2713" : "\u2717";
      const idx = document.createElement("span"); idx.textContent = (i + 1) + ".";
      const q = document.createElement("span"); q.className = "sum-q"; kx(q, r.p);
      const arrow = document.createElement("span"); arrow.className = "sum-arrow"; arrow.textContent = "\u2192";
      const ans = document.createElement("span"); ans.className = "sum-ans";
      if (r.chosenTex) kx(ans, r.chosenTex); else ans.textContent = "(missed)";
      row.appendChild(mark); row.appendChild(idx); row.appendChild(q); row.appendChild(arrow); row.appendChild(ans);
      if (!r.ok) { const cc = document.createElement("span"); cc.className = "sum-correct"; kx(cc, r.correctTex); row.appendChild(cc); }
      list.appendChild(row);
    });
    summaryEl.classList.remove("hidden"); setupEl.classList.add("hidden"); overlayEl.classList.remove("hidden");
  }
  function showSetup() { summaryEl.classList.add("hidden"); setupEl.classList.remove("hidden"); overlayEl.classList.remove("hidden"); }

  function onKey(ev) {
    if (!running) {
      if ((ev.key === " " || ev.key === "Enter") && !overlayEl.classList.contains("hidden") && !setupEl.classList.contains("hidden")) { startRound(); ev.preventDefault(); }
      return;
    }
    if (ev.key === "ArrowLeft") { cannonLane = Math.max(0, cannonLane - 1); placeCannon(); ev.preventDefault(); }
    else if (ev.key === "ArrowRight") { cannonLane = Math.min(lanes - 1, cannonLane + 1); placeCannon(); ev.preventDefault(); }
    else if (ev.key === " " || ev.key === "ArrowUp") { fire(); ev.preventDefault(); }
  }
  function resize() { if (!stage) return; enemies.forEach(placeEnemy); placeCannon(); }

  const Game = {
    mounted: false,
    mount() {
      if (this.mounted) return;
      stage = document.getElementById("game-stage"); promptEl = document.getElementById("game-prompt");
      enemiesEl = document.getElementById("game-enemies"); cannonEl = document.getElementById("game-cannon");
      overlayEl = document.getElementById("game-overlay"); setupEl = document.getElementById("ov-setup");
      summaryEl = document.getElementById("ov-summary"); countdownEl = document.getElementById("game-countdown");
      elScore = document.getElementById("g-score"); elAcc = document.getElementById("g-acc");
      elStreak = document.getElementById("g-streak"); elQnum = document.getElementById("g-qnum");
      if (!stage) return; this.mounted = true;

      document.getElementById("g-start").addEventListener("click", startRound);
      document.getElementById("g-again").addEventListener("click", startRound);
      document.getElementById("g-settings").addEventListener("click", showSetup);
      document.getElementById("g-restart").addEventListener("click", () => { running = false; inRound = false; cancelAnimationFrame(rafId); countdownEl.classList.add("hidden"); showSetup(); });

      const sBtn = document.getElementById("g-sound");
      sBtn.addEventListener("click", () => { soundOn = !soundOn; sBtn.textContent = soundOn ? "\uD83D\uDD0A" : "\uD83D\uDD07"; });

      const notes = {
        expand: "Expand: match the factored form to its expansion (4 answers).",
        factorize: "Factorize: match the expanded form back to its factorization (4 answers).",
        cross: "Cross method: factorise the quadratic by shooting the correct pair of factors (4 answers). Includes leading coefficient \u2260 1.",
      };
      document.querySelectorAll(".modebtn").forEach((b) => b.addEventListener("click", () => {
        document.querySelectorAll(".modebtn").forEach((x) => x.classList.toggle("active", x === b));
        mode = b.dataset.mode;
        document.getElementById("ov-mode-note").textContent = notes[mode];
      }));

      const countInp = document.getElementById("ov-count"), countVal = document.getElementById("ov-count-val");
      countInp.addEventListener("input", () => { numQ = +countInp.value; countVal.textContent = numQ; });
      numQ = +countInp.value;

      const ovSpeed = document.getElementById("ov-speed"), ovSpeedVal = document.getElementById("ov-speed-val"), hudSpeed = document.getElementById("g-speed");
      function setSpeed(v) { v = Math.max(1, Math.min(10, +v)); speed = speedFromSlider(v); ovSpeed.value = v; hudSpeed.value = v; ovSpeedVal.textContent = v; }
      ovSpeed.addEventListener("input", () => setSpeed(ovSpeed.value));
      hudSpeed.addEventListener("input", () => setSpeed(hudSpeed.value));
      setSpeed(ovSpeed.value);

      window.addEventListener("keydown", (e) => { if (activeFlag) onKey(e); });
      window.addEventListener("resize", resize);
    },
    show() { this.mount(); activeFlag = true; if (inRound && !running) { running = true; lastT = performance.now(); cancelAnimationFrame(rafId); rafId = requestAnimationFrame(loop); } },
    hide() { activeFlag = false; running = false; cancelAnimationFrame(rafId); },
  };

  window.FactGame = Game;
})();
