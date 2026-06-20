/* Factorization interactive tools — area-model widgets + cross-method.
 * Consistent colours with the Manim slides:
 *   x/a -> blue   b -> amber   ab / middle-term -> green   removed -> red
 * ALL maths/symbols render as LaTeX via KaTeX (figure labels use SVG <foreignObject>).
 */
(function () {
  "use strict";

  const C = {
    a: "#4FC3F7",   // a / x
    b: "#FFD54F",   // b / added constant
    ab: "#81C784",  // ab / middle-term cells
    rm: "#E57373",  // removed / minus
    ink: "#e5e7eb",
    dim: "#94a3b8",
    cellA: "#06283d",  // dark text on blue
    cellAB: "#11321d", // dark text on green
    cellB: "#3a2f06",  // dark text on amber
  };
  const NS = "http://www.w3.org/2000/svg";

  function E(tag, attrs) {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    return e;
  }
  function clear(n) { while (n.firstChild) n.removeChild(n.firstChild); }
  function rectSvg(p, x, y, w, h, fill, op, stroke, sw, dash) {
    const a = {
      x, y, width: Math.max(0, w), height: Math.max(0, h), fill,
      "fill-opacity": op == null ? 0.42 : op,
      stroke: stroke || fill, "stroke-width": sw == null ? 1.5 : sw,
    };
    if (dash) a["stroke-dasharray"] = dash;
    const el = E("rect", a);
    p.appendChild(el);
    return el;
  }
  function lineSvg(p, x1, y1, x2, y2, col, w, dash) {
    const a = { x1, y1, x2, y2, stroke: col, "stroke-width": w || 2 };
    if (dash) a["stroke-dasharray"] = dash;
    p.appendChild(E("line", a));
  }
  function plainText(p, x, y, s, col, size) {
    const t = E("text", {
      x, y, fill: col, "font-size": size || 13, "text-anchor": "middle",
      "dominant-baseline": "middle", "font-family": "Hanken Grotesk, sans-serif",
    });
    t.textContent = s;
    p.appendChild(t);
  }
  // LaTeX label centred at (cx, cy) inside the SVG via <foreignObject>.
  function tex(p, cx, cy, latex, color, size, w, h) {
    w = w || 170; h = h || 46;
    const fo = E("foreignObject", { x: cx - w / 2, y: cy - h / 2, width: w, height: h });
    fo.setAttribute("overflow", "visible");
    const div = document.createElement("div");
    div.style.cssText = "width:" + w + "px;height:" + h + "px;display:flex;align-items:center;" +
      "justify-content:center;color:" + color + ";font-size:" + (size || 16) + "px;line-height:1;" +
      "white-space:nowrap;";
    try { katex.render(latex, div, { throwOnError: false, displayMode: false }); }
    catch (e) { div.textContent = latex; }
    fo.appendChild(div);
    p.appendChild(fo);
    return fo;
  }
  // Like tex(), but shrinks the font so the label fits inside a cell of size
  // cw×ch. Keeps value labels readable (and non-overlapping) when the figure
  // becomes small as the user drags the sliders down.
  function fitTex(p, cx, cy, latex, color, cw, ch, opts) {
    opts = opts || {};
    const maxFs = opts.max == null ? 16 : opts.max;
    const minFs = opts.min == null ? 7 : opts.min;
    // Rough rendered-length estimate: drop LaTeX markup, keep visible glyphs.
    // Estimate rendered width in "em": glyphs ~0.55em, relation/operators wider.
    const glyphs = latex.replace(/[\\{}^]/g, "");
    const ops = (glyphs.match(/[=+\-]/g) || []).length;
    const em = glyphs.length * 0.55 + ops * 0.45;
    const availW = Math.max(0, cw - (opts.padX == null ? 10 : opts.padX));
    const availH = Math.max(0, ch - (opts.padY == null ? 8 : opts.padY));
    let fs = Math.min(maxFs, availW / em, availH * 0.8);
    fs = Math.max(minFs, fs);
    const boxW = Math.max(cw, em * fs + 12);
    return tex(p, cx, cy, latex, color, fs, boxW, fs * 1.9);
  }
  // ── click-to-focus helpers (used by the (a+b)^2 / (a-b)^2 tools) ──
  // Make an element selectable; clicking toggles the cell highlight.
  function pickable(el, idx, api) {
    if (!el || !api || idx == null) return el;
    el.style.cursor = "pointer";
    el.addEventListener("click", (e) => { e.stopPropagation(); api.select(idx); });
    return el;
  }
  // Dim an element when another cell is focused.
  function fade(el, off) { if (el) el.style.opacity = off ? 0.16 : 1; }
  // Make a decorative overlay ignore clicks so the pickable cell beneath it
  // still receives them.
  function noHit(el) { if (el) el.style.pointerEvents = "none"; return el; }
  // True when intervals [a0,a1] and [b0,b1] genuinely overlap (not just touch).
  function span(a0, a1, b0, b1) { return Math.min(a1, b1) - Math.max(a0, b0) > 0.5; }
  const tc = (c, s) => `\\textcolor{${c}}{${s}}`;
  // Diagonal-hatch + dashed-outline overlay used to flag a region as "shared"
  // (e.g. the b² corner that both ab strips of (a-b)² cover twice).
  function hatchOverlay(svg, x, y, w, h, color) {
    if (w <= 0 || h <= 0) return;
    const pid = "hatch-" + Math.random().toString(36).slice(2);
    const defs = E("defs", {});
    const pat = E("pattern", {
      id: pid, width: 7, height: 7,
      patternUnits: "userSpaceOnUse", patternTransform: "rotate(45)",
    });
    pat.appendChild(E("line", { x1: 0, y1: 0, x2: 0, y2: 7, stroke: color, "stroke-width": 1.4 }));
    defs.appendChild(pat);
    svg.appendChild(defs);
    rectSvg(svg, x, y, w, h, "url(#" + pid + ")", 1, color, 2, "4 3").style.pointerEvents = "none";
  }
  // Diagonal-stripe fill (no border) used to texture a region so it reads as a
  // single strip. `angle` sets the slant; opposite angles cross-hatch on overlap.
  function hatchFill(svg, x, y, w, h, color, angle, op) {
    if (w <= 0 || h <= 0) return;
    const pid = "hf-" + Math.random().toString(36).slice(2);
    const defs = E("defs", {});
    const pat = E("pattern", {
      id: pid, width: 9, height: 9,
      patternUnits: "userSpaceOnUse", patternTransform: "rotate(" + angle + ")",
    });
    pat.appendChild(E("line", {
      x1: 0, y1: 0, x2: 0, y2: 9, stroke: color, "stroke-width": 2,
      "stroke-opacity": op == null ? 1 : op,
    }));
    defs.appendChild(pat);
    svg.appendChild(defs);
    rectSvg(svg, x, y, w, h, "url(#" + pid + ")", 1, "none", 0).style.pointerEvents = "none";
  }

  /* ───────────────────────── Tool 1: (a+b)^2 ───────────────────────── */
  const toolSum = {
    name: "(a+b)^2",
    viewBox: "0 0 410 380",
    defaults: { a: 3, b: 2 },
    sliders: [
      { key: "a", label: "a", min: 1, max: 7, step: 1, color: C.a },
      { key: "b", label: "b", min: 1, max: 5, step: 1, color: C.b },
    ],
    clamp() {},
    draw(svg, st, api) {
      // Scale the figure to fill the canvas so cells stay large & legible
      // regardless of how small a/b are; proportions still reflect a:b.
      const ml = 46, mr = 24, mt = 40, mb = 24;
      const aw = 410 - ml - mr, ah = 380 - mt - mb;
      const S = Math.min(aw, ah), unit = S / (st.a + st.b);
      const A = st.a * unit, B = st.b * unit;
      const ox = ml + (aw - S) / 2, top = mt + (ah - S) / 2;
      const sel = api ? api.sel : null;
      const cells = [
        { x: ox, y: top, w: A, h: A, fill: C.a, op: 0.5, lt: `a^2=${st.a * st.a}`, tc: C.cellA },
        { x: ox + A, y: top, w: B, h: A, fill: C.ab, op: 0.5, lt: `ab=${st.a * st.b}`, tc: C.cellAB },
        { x: ox, y: top + A, w: A, h: B, fill: C.ab, op: 0.5, lt: `ab=${st.a * st.b}`, tc: C.cellAB },
        { x: ox + A, y: top + A, w: B, h: B, fill: C.b, op: 0.6, lt: `b^2=${st.b * st.b}`, tc: C.cellB },
      ];
      cells.forEach((c, i) => {
        const on = sel === i, dim = sel != null && !on;
        const op = on ? Math.min(0.92, c.op + 0.28) : c.op;
        const r = rectSvg(svg, c.x, c.y, c.w, c.h, c.fill, op, on ? "#fff" : c.fill, on ? 3 : 1.5);
        fade(r, dim); pickable(r, i, api);
        const f = fitTex(svg, c.x + c.w / 2, c.y + c.h / 2, c.lt, c.tc, c.w, c.h);
        fade(f, dim); pickable(f, i, api);
      });
      rectSvg(svg, ox, top, S, S, "none", 0, C.ink, 2.5);
      const sc = sel != null ? cells[sel] : null;
      const tops = [
        { cx: ox + A / 2, s: ox, e: ox + A, t: "a", col: C.a },
        { cx: ox + A + B / 2, s: ox + A, e: ox + A + B, t: "b", col: C.b },
      ];
      const lefts = [
        { cy: top + A / 2, s: top, e: top + A, t: "a", col: C.a },
        { cy: top + A + B / 2, s: top + A, e: top + A + B, t: "b", col: C.b },
      ];
      tops.forEach((L) => {
        fade(tex(svg, L.cx, top - 20, L.t, L.col, 18, 60, 30), sc && !span(sc.x, sc.x + sc.w, L.s, L.e));
      });
      lefts.forEach((L) => {
        fade(tex(svg, ox - 24, L.cy, L.t, L.col, 18, 40, 30), sc && !span(sc.y, sc.y + sc.h, L.s, L.e));
      });
    },
    latex(st) {
      const a = st.a, b = st.b;
      return [
        `(${tc(C.a, "a")}+${tc(C.b, "b")})^2 = ${tc(C.a, "a^2")} + ${tc(C.ab, "2ab")} + ${tc(C.b, "b^2")}`,
        `(${tc(C.a, a)}+${tc(C.b, b)})^2 = ${tc(C.a, a * a)} + ${tc(C.ab, 2 * a * b)} + ${tc(C.b, b * b)} = ${(a + b) * (a + b)}`,
      ];
    },
  };

  /* ───────────────────────── Tool 2: (a-b)^2 ───────────────────────── */
  const toolDiff = {
    name: "(a-b)^2",
    viewBox: "0 0 410 380",
    defaults: { a: 5, b: 2 },
    sliders: [
      { key: "a", label: "a", min: 3, max: 8, step: 1, color: C.a },
      { key: "b", label: "b", min: 1, max: 7, step: 1, color: C.b },
    ],
    clamp(st) { if (st.b > st.a - 1) st.b = st.a - 1; },
    draw(svg, st, api) {
      const ml = 56, mr = 66, mt = 40, mb = 44;
      const aw = 410 - ml - mr, ah = 380 - mt - mb;
      const A = Math.min(aw, ah), unit = A / st.a;
      const B = st.b * unit, IN = A - B;
      const ox = ml + (aw - A) / 2, top = mt + (ah - A) / 2;
      const sel = api ? api.sel : null, anySel = sel != null;
      const bg = rectSvg(svg, ox, top, A, A, C.a, 0.16, C.a, 1);
      fade(bg, anySel);
      const ab = st.a * st.b;
      // The two "ab" pieces are full-length strips (each area = a·b) that
      // overlap in the b² corner — that is what the (a-b)² proof shows.
      const cells = [
        { x: ox + IN, y: top, w: B, h: A, fill: C.ab, op: 0.42,
          lx: ox + IN + B / 2, ly: top + IN / 2, lw: B, lh: IN, lt: `ab=${ab}`, tc: C.ink },
        { x: ox, y: top + IN, w: A, h: B, fill: C.ab, op: 0.42,
          lx: ox + IN / 2, ly: top + IN + B / 2, lw: IN, lh: B, lt: `ab=${ab}`, tc: C.ink },
        { x: ox + IN, y: top + IN, w: B, h: B, fill: C.b, op: 0.5,
          lx: ox + IN + B / 2, ly: top + IN + B / 2, lw: B, lh: B, lt: `b^2=${st.b * st.b}`, tc: C.cellB },
        { x: ox, y: top, w: IN, h: IN, fill: C.a, op: 0.55,
          lx: ox + IN / 2, ly: top + IN / 2, lw: IN, lh: IN, lt: `(a-b)^2=${(st.a - st.b) * (st.a - st.b)}`, tc: C.ink },
      ];
      cells.forEach((c, i) => {
        const on = sel === i, dim = anySel && !on;
        const op = on ? Math.min(0.92, c.op + 0.28) : c.op;
        const r = rectSvg(svg, c.x, c.y, c.w, c.h, c.fill, op, on ? "#fff" : c.fill, on ? 3 : 1);
        fade(r, dim); pickable(r, i, api);
        const f = fitTex(svg, c.lx, c.ly, c.lt, c.tc, c.lw, c.lh);
        fade(f, dim); pickable(f, i, api);
      });
      // Hint before any click: stripe each FULL ab strip with slanted lines
      // (bottom strip one way, right strip the other). The stripes run through
      // the b² corner, so the corner shows a cross-hatch — making it obvious
      // each ab strip is the whole a×b band and the corner is shared by both.
      if (sel == null) {
        const stripe = "#dcedc8";
        hatchFill(svg, ox, top + IN, A, B, stripe, 45, 0.85);      // bottom ab strip "/"
        hatchFill(svg, ox + IN, top, B, A, stripe, -45, 0.85);     // right ab strip "\"
        // redraw labels so they stay crisp above the stripes (non-interactive
        // so the cells underneath stay clickable)
        noHit(fitTex(svg, ox + IN + B / 2, top + IN / 2, `ab=${ab}`, C.ink, B, IN));
        noHit(fitTex(svg, ox + IN / 2, top + IN + B / 2, `ab=${ab}`, C.ink, IN, B));
        noHit(fitTex(svg, ox + IN + B / 2, top + IN + B / 2, `b^2=${st.b * st.b}`, C.cellB, B, B));
      }
      // When an ab strip is picked, reveal that it continues *through* the b²
      // corner — paint the corner in the strip colour so the full a×b extent is
      // visible, then hatch it to flag the corner as the shared (double-counted)
      // piece. This corrects the static look where ab seems to be only one cell.
      if (sel === 0 || sel === 1) {
        rectSvg(svg, ox + IN, top + IN, B, B, C.ab, Math.min(0.92, 0.42 + 0.28)).style.pointerEvents = "none";
        hatchOverlay(svg, ox + IN, top + IN, B, B, C.rm);
        noHit(fitTex(svg, ox + IN + B / 2, top + IN + B / 2, "\\text{shared}", C.rm, B, B, { max: 12 }));
      }
      rectSvg(svg, ox, top, A, A, "none", 0, C.ink, 2.5);
      const sc = sel != null ? cells[sel] : null;
      const tops = [
        { cx: ox + IN / 2, s: ox, e: ox + IN, t: "a-b", col: C.a, fz: 15 },
        { cx: ox + IN + B / 2, s: ox + IN, e: ox + A, t: "b", col: C.b, fz: 18 },
      ];
      const rights = [
        { cy: top + IN / 2, s: top, e: top + IN, t: "a-b", col: C.a, fz: 15 },
        { cy: top + IN + B / 2, s: top + IN, e: top + A, t: "b", col: C.b, fz: 16 },
      ];
      tops.forEach((L) => {
        fade(tex(svg, L.cx, top - 20, L.t, L.col, L.fz, 60, 30), sc && !span(sc.x, sc.x + sc.w, L.s, L.e));
      });
      rights.forEach((L) => {
        fade(tex(svg, ox + A + 28, L.cy, L.t, L.col, L.fz, 60, 30), sc && !span(sc.y, sc.y + sc.h, L.s, L.e));
      });
      // total side length a = (a-b) + b, shown on the otherwise-empty left &
      // bottom sides; lit when the selected piece spans that whole side (i.e.
      // makes clear each ab strip is a full a×b rectangle).
      const fullV = sc && sc.y <= top + 0.5 && sc.y + sc.h >= top + A - 0.5;
      const fullH = sc && sc.x <= ox + 0.5 && sc.x + sc.w >= ox + A - 0.5;
      fade(tex(svg, ox - 30, top + A / 2, "a", C.a, 18, 44, 30), sc && !fullV);
      fade(tex(svg, ox + A / 2, top + A + 22, "a", C.a, 18, 60, 30), sc && !fullH);
    },
    latex(st) {
      const a = st.a, b = st.b, m = a - b;
      return [
        `(${tc(C.a, "a")}-${tc(C.b, "b")})^2 = ${tc(C.a, "a^2")} - ${tc(C.ab, "2ab")} + ${tc(C.b, "b^2")}`,
        `(${tc(C.a, a)}-${tc(C.b, b)})^2 = ${tc(C.a, a * a)} - ${tc(C.ab, 2 * a * b)} + ${tc(C.b, b * b)} = ${m * m}`,
      ];
    },
  };

  /* ──────────────────── Tool 3: a^2 - b^2 = (a+b)(a-b) ──────────────────── */
  const toolDoS = {
    name: "a^2-b^2",
    viewBox: "0 0 450 380",
    defaults: { a: 5, b: 2, mode: 0 },
    sliders: [
      { key: "a", label: "a", min: 3, max: 8, step: 1, color: C.a },
      { key: "b", label: "b", min: 1, max: 7, step: 1, color: C.b },
    ],
    buttons: [{ label: "Rearrange \u27f3", toggle: "mode" }],
    clamp(st) { if (st.b > st.a - 1) st.b = st.a - 1; },
    draw(svg, st) {
      if (!st.mode) {
        const ml = 34, mr = 36, mt = 40, mb = 52;
        const aw = 450 - ml - mr, ah = 380 - mt - mb;
        const A = Math.min(aw, ah), unit = A / st.a;
        const B = st.b * unit, IN = A - B;
        const ox = ml + (aw - A) / 2, top = mt + (ah - A) / 2;
        rectSvg(svg, ox, top, A, IN, C.a, 0.5, C.a, 1);
        rectSvg(svg, ox, top + IN, IN, B, C.a, 0.5, C.a, 1);
        rectSvg(svg, ox + IN, top + IN, B, B, C.b, 0.25, C.rm, 2, "4 3");
        rectSvg(svg, ox, top, A, A, "none", 0, C.ink, 2.5);
        fitTex(svg, ox + A / 2, top + IN / 2, `a^2-b^2=${st.a * st.a - st.b * st.b}`, C.ink, A, IN);
        fitTex(svg, ox + IN + B / 2, top + IN + B / 2, `b^2=${st.b * st.b}`, C.rm, B, B);
        tex(svg, ox + A / 2, top - 20, "a", C.a, 18, 60, 30);
        tex(svg, ox - 24, top + A / 2, "a", C.a, 18, 40, 30);
        plainText(svg, ox + A / 2, top + A + 30, "drag a, b — then press Rearrange", C.dim, 13);
      } else {
        const ml = 42, mr = 42, mt = 44, mb = 36;
        const aw = 450 - ml - mr, ah = 380 - mt - mb;
        const unit = Math.min(aw / (st.a + st.b), ah / (st.a - st.b));
        const A = st.a * unit, B = st.b * unit, IN = A - B;
        const W = A + B, H = IN;
        const ox = ml + (aw - W) / 2, top = mt + (ah - H) / 2;
        rectSvg(svg, ox, top, A, H, C.a, 0.5, C.a, 1);
        rectSvg(svg, ox + A, top, B, H, C.a, 0.5, C.a, 1);
        lineSvg(svg, ox + A, top, ox + A, top + H, C.ink, 1, "3 3");
        rectSvg(svg, ox, top, W, H, "none", 0, C.ink, 2.5);
        fitTex(svg, ox + W / 2, top + H / 2, `a^2-b^2=${st.a * st.a - st.b * st.b}`, C.ink, W, H);
        tex(svg, ox + W / 2, top - 20, "a+b", C.a, 16, 80, 30);
        tex(svg, ox - 28, top + H / 2, "a-b", C.a, 15, 60, 30);
      }
    },
    latex(st) {
      const a = st.a, b = st.b;
      return [
        `${tc(C.a, "a^2")} - ${tc(C.b, "b^2")} = (${tc(C.a, "a")}+${tc(C.b, "b")})(${tc(C.a, "a")}-${tc(C.b, "b")})`,
        `${tc(C.a, a * a)} - ${tc(C.b, b * b)} = (${a}+${b})(${a}-${b}) = ${a * a - b * b}`,
      ];
    },
  };

  /* ───────────────────── Tool 4: cross method ───────────────────── */
  const toolCross = {
    name: "cross",
    viewBox: "0 0 560 360",
    defaults: { p: 2, q: 3 },
    sliders: [
      { key: "p", label: "p", min: 1, max: 6, step: 1, color: C.b },
      { key: "q", label: "q", min: 1, max: 6, step: 1, color: C.b },
    ],
    clamp() {},
    draw(svg, st) {
      const p = st.p, q = st.q;
      // ---- left: cross diagram ----
      const xL = 56, xR = 176, yT = 118, yB = 208;
      tex(svg, xL, yT, "x", C.a, 22, 50, 34);
      tex(svg, xL, yB, "x", C.a, 22, 50, 34);
      tex(svg, xR, yT, `+${p}`, C.b, 20, 60, 34);
      tex(svg, xR, yB, `+${q}`, C.b, 20, 60, 34);
      lineSvg(svg, xL + 18, yT + 8, xR - 24, yB - 8, C.ab, 2.5);
      lineSvg(svg, xL + 18, yB - 8, xR - 24, yT + 8, C.ab, 2.5);
      tex(svg, 116, 268, `${tc(C.ab, q + "x")}+${tc(C.ab, p + "x")}=${tc(C.ab, (p + q) + "x")}\\;\\checkmark`, C.ink, 15, 200, 34);
      tex(svg, 116, 66, `\\text{product}=${p * q},\\ \\text{sum}=${p + q}`, C.dim, 13, 220, 30);
      // ---- right: area rectangle ----
      const unit = 22, xpix = 86, ox = 300, bottom = 300;
      const P = p * unit, Q = q * unit, W = xpix + P, H = xpix + Q, top = bottom - H;
      rectSvg(svg, ox, top, xpix, xpix, C.a, 0.5);
      rectSvg(svg, ox + xpix, top, P, xpix, C.ab, 0.5);
      rectSvg(svg, ox, top + xpix, xpix, Q, C.ab, 0.5);
      rectSvg(svg, ox + xpix, top + xpix, P, Q, C.b, 0.6);
      rectSvg(svg, ox, top, W, H, "none", 0, C.ink, 2.5);
      tex(svg, ox + xpix / 2, top + xpix / 2, "x^2", C.cellA, 16, 60, 30);
      tex(svg, ox + xpix + P / 2, top + xpix / 2, `${p}x`, C.cellAB, 13, 50, 28);
      tex(svg, ox + xpix / 2, top + xpix + Q / 2, `${q}x`, C.cellAB, 13, 50, 28);
      tex(svg, ox + xpix + P / 2, top + xpix + Q / 2, String(p * q), C.cellB, 13, 40, 26);
      tex(svg, ox + xpix / 2, top - 17, "x", C.a, 17, 50, 30);
      tex(svg, ox + xpix + P / 2, top - 17, `+${p}`, C.b, 15, 50, 30);
      tex(svg, ox - 20, top + xpix / 2, "x", C.a, 17, 40, 30);
      tex(svg, ox - 20, top + xpix + Q / 2, `+${q}`, C.b, 15, 50, 30);
    },
    latex(st) {
      const p = st.p, q = st.q;
      return [
        `x^2 + ${tc(C.ab, (p + q) + "x")} + ${tc(C.b, p * q)} = (x+${tc(C.b, p)})(x+${tc(C.b, q)})`,
        `\\text{cross: } ${tc(C.ab, q + "x")} + ${tc(C.ab, p + "x")} = ${tc(C.ab, (p + q) + "x")}`,
      ];
    },
  };

  const TOOLS = { sum: toolSum, diff: toolDiff, dos: toolDoS, cross: toolCross };

  /* ───────────────────────── wiring ───────────────────────── */
  function renderEq(container, lines) {
    clear(container);
    lines.forEach((t) => {
      const d = document.createElement("div");
      d.className = "eq-line";
      try { katex.render(t, d, { throwOnError: false, displayMode: false }); }
      catch (e) { d.textContent = t; }
      container.appendChild(d);
    });
  }
  function renderTexAttrs(root) {
    (root || document).querySelectorAll("[data-tex]").forEach((el) => {
      try { katex.render(el.getAttribute("data-tex"), el, { throwOnError: false, displayMode: false }); }
      catch (e) {}
    });
  }

  function initTools() {
    const svg = document.getElementById("tool-svg");
    const controls = document.getElementById("tool-controls");
    const eqBox = document.getElementById("tool-eq");
    const toolBtns = document.querySelectorAll("[data-tool]");
    let current = null, state = {};

    const api = {
      get sel() { return state.sel == null ? null : state.sel; },
      select(i) { state.sel = (state.sel === i ? null : i); redraw(); },
    };

    function redraw() {
      if (current.clamp) current.clamp(state);
      clear(svg);
      current.draw(svg, state, api);
      renderEq(eqBox, current.latex(state));
      current.sliders.forEach((s) => {
        const badge = document.getElementById("val-" + s.key);
        if (badge) badge.textContent = state[s.key];
        const inp = document.getElementById("sl-" + s.key);
        if (inp && +inp.value !== state[s.key]) inp.value = state[s.key];
      });
    }

    function loadTool(key) {
      current = TOOLS[key];
      state = Object.assign({}, current.defaults);
      svg.setAttribute("viewBox", current.viewBox);
      clear(controls);
      current.sliders.forEach((s) => {
        const wrap = document.createElement("label");
        wrap.className = "slider-row";
        const name = document.createElement("span");
        name.className = "slider-name";
        name.style.color = s.color;
        try { katex.render(s.label, name, { throwOnError: false }); } catch (e) { name.textContent = s.label; }
        const inp = document.createElement("input");
        inp.id = "sl-" + s.key; inp.type = "range";
        inp.min = s.min; inp.max = s.max; inp.step = s.step; inp.value = state[s.key];
        inp.addEventListener("input", (e) => { state[s.key] = +e.target.value; redraw(); });
        const val = document.createElement("span");
        val.className = "slider-val"; val.id = "val-" + s.key; val.textContent = state[s.key];
        wrap.appendChild(name); wrap.appendChild(inp); wrap.appendChild(val);
        controls.appendChild(wrap);
      });
      (current.buttons || []).forEach((b) => {
        const btn = document.createElement("button");
        btn.className = "tool-action";
        btn.textContent = b.label;
        btn.addEventListener("click", () => { state[b.toggle] = state[b.toggle] ? 0 : 1; redraw(); });
        controls.appendChild(btn);
      });
      redraw();
      toolBtns.forEach((b) => b.classList.toggle("active", b.dataset.tool === key));
    }

    // Click empty canvas (or the outer border) to clear the focus.
    svg.addEventListener("click", (e) => {
      if ((e.target === svg || e.target.getAttribute("fill") === "none") && state.sel != null) {
        state.sel = null; redraw();
      }
    });

    // The cross-method calculator is a non-SVG tool; swap layouts when chosen.
    const toolLayout = document.querySelector(".tool-layout");
    const calcTool = document.getElementById("calc-tool");
    function activate(key) {
      toolBtns.forEach((b) => b.classList.toggle("active", b.dataset.tool === key));
      const isCalc = key === "calc";
      if (toolLayout) toolLayout.classList.toggle("hidden", isCalc);
      if (calcTool) calcTool.classList.toggle("hidden", !isCalc);
      if (!isCalc) loadTool(key);
    }
    toolBtns.forEach((b) => b.addEventListener("click", () => activate(b.dataset.tool)));
    activate("sum");
  }

  /* ───────────────── Cross-method calculator ───────────────── */
  function initCalc() {
    const aEl = document.getElementById("calc-a");
    const bEl = document.getElementById("calc-b");
    const cEl = document.getElementById("calc-c");
    const out = document.getElementById("calc-result");
    const go = document.getElementById("calc-go");
    if (!go || !out || !aEl) return;

    const posDivisors = (n) => {
      n = Math.abs(n); const ds = [];
      for (let d = 1; d <= n; d++) if (n % d === 0) ds.push(d);
      return ds;
    };
    // Render a coefficient*variable term (with sign); skip if zero.
    const term = (n, v, lead) => {
      if (n === 0) return "";
      const sign = n < 0 ? (lead ? "-" : " - ") : (lead ? "" : " + ");
      const m = Math.abs(n);
      return sign + (m === 1 ? "" : m) + v;
    };
    const polyTex = (A, B, C) => term(A, "x^2", true) + term(B, "xy", false) + term(C, "y^2", false);
    // One linear factor (px + qy); coefficients are always non-zero here.
    const factorTex = (p, q) => {
      const xs = p === 1 ? "x" : p === -1 ? "-x" : p + "x";
      const ym = Math.abs(q) === 1 ? "y" : Math.abs(q) + "y";
      return "(" + xs + (q < 0 ? " - " : " + ") + ym + ")";
    };
    const midTex = (m) => (m === 0 ? "0" : (m === 1 ? "" : m === -1 ? "-" : m) + "xy");
    const xTermTex = (p) => (p === 1 ? "x" : p === -1 ? "-x" : p + "x");
    const yTermTex = (q) => (q < 0 ? "-" : "+") + (Math.abs(q) === 1 ? "y" : Math.abs(q) + "y");

    // Cross diagram for (a1 x + c1 y)(a2 x + c2 y): the two diagonal products
    // a1·c2 and a2·c1 add to the xy coefficient.
    function crossDiagram(a1, c1, a2, c2, mid, ok) {
      const col = ok ? C.ab : C.dim;
      const svg = E("svg", { viewBox: "0 0 230 150" });
      svg.setAttribute("class", "calc-cross-svg");
      lineSvg(svg, 78, 46, 152, 92, col, 2.5);
      lineSvg(svg, 78, 92, 152, 46, col, 2.5);
      tex(svg, 48, 40, xTermTex(a1), C.a, 21, 84, 32);
      tex(svg, 182, 40, yTermTex(c1), C.b, 21, 84, 32);
      tex(svg, 48, 98, xTermTex(a2), C.a, 21, 84, 32);
      tex(svg, 182, 98, yTermTex(c2), C.b, 21, 84, 32);
      const p1 = a1 * c2, p2 = a2 * c1;
      const first = (p1 === 1 ? "" : p1 === -1 ? "-" : p1) + "xy";
      const next = (p2 < 0 ? " - " : " + ") + (Math.abs(p2) === 1 ? "" : Math.abs(p2)) + "xy";
      tex(svg, 115, 134, first + next + " = " + midTex(mid), col, 15, 224, 30);
      return svg;
    }

    const kx = (parent, latex, cls) => {
      const d = document.createElement("div");
      if (cls) d.className = cls;
      try { katex.render(latex, d, { throwOnError: false, displayMode: false }); }
      catch (e) { d.textContent = latex; }
      parent.appendChild(d);
      return d;
    };
    const invalid = (msg) => {
      clear(out);
      const box = document.createElement("div");
      box.className = "calc-invalid";
      const b = document.createElement("b"); b.textContent = "Invalid";
      const s = document.createElement("span"); s.textContent = msg;
      box.appendChild(b); box.appendChild(s);
      out.appendChild(box);
    };

    function calc() {
      const A = parseInt(aEl.value, 10), B = parseInt(bEl.value, 10), C = parseInt(cEl.value, 10);
      if (!Number.isInteger(A) || !Number.isInteger(B) || !Number.isInteger(C)) {
        return invalid("Please enter whole numbers for all three coefficients.");
      }
      if (A === 0 || C === 0) {
        return invalid("The x\u00b2 and y\u00b2 coefficients must be non-zero for the cross method.");
      }

      // (a1 x + c1 y)(a2 x + c2 y): a1·a2 = A, c1·c2 = C, middle = a1·c2 + a2·c1.
      const aPairs = posDivisors(A).map((d) => [d, A / d]);
      const cPairs = [];
      posDivisors(C).forEach((d) => { cPairs.push([d, C / d]); cPairs.push([-d, C / -d]); });

      const seen = new Set(), combos = [];
      aPairs.forEach(([a1, a2]) => cPairs.forEach(([c1, c2]) => {
        const key = [[a1, c1].join(","), [a2, c2].join(",")].sort().join("|");
        if (seen.has(key)) return;
        seen.add(key);
        let f1 = [a1, c1], f2 = [a2, c2];
        // Show the factor with the larger leading coefficient first (nicer form).
        if (f2[0] > f1[0] || (f2[0] === f1[0] && f2[1] > f1[1])) { const t = f1; f1 = f2; f2 = t; }
        const mid = f1[0] * f2[1] + f2[0] * f1[1];
        combos.push({ f1, f2, mid, ok: mid === B });
      }));

      if (!combos.some((c) => c.ok)) {
        return invalid("This trinomial cannot be factorised by the cross method over the integers.");
      }

      combos.sort((x, y) => (y.ok - x.ok) || (Math.abs(x.mid - B) - Math.abs(y.mid - B)));

      clear(out);
      const correct = combos.find((c) => c.ok);
      kx(out, polyTex(A, B, C) + " = " + factorTex(correct.f1[0], correct.f1[1]) +
        factorTex(correct.f2[0], correct.f2[1]), "calc-headline");
      const note = document.createElement("p");
      note.className = "calc-note";
      note.textContent = "All cross-method combinations (correct one highlighted)";
      out.appendChild(note);

      const grid = document.createElement("div");
      grid.className = "calc-grid";
      combos.forEach((c) => {
        const cell = document.createElement("div");
        cell.className = "calc-cell" + (c.ok ? " ok" : "");
        cell.appendChild(crossDiagram(c.f1[0], c.f1[1], c.f2[0], c.f2[1], c.mid, c.ok));
        kx(cell, factorTex(c.f1[0], c.f1[1]) + factorTex(c.f2[0], c.f2[1]), "calc-cell-form");
        const mark = document.createElement("div");
        mark.className = "calc-mark";
        mark.textContent = c.ok ? "\u2713" : "\u2717";
        cell.appendChild(mark);
        grid.appendChild(cell);
      });
      out.appendChild(grid);
    }

    go.addEventListener("click", calc);
    [aEl, bEl, cEl].forEach((el) => el.addEventListener("keydown", (e) => {
      if (e.key === "Enter") calc();
    }));
    calc();
  }

  function initTabs() {
    const tabs = document.querySelectorAll("[data-tab]");
    const panels = {
      slides: document.getElementById("panel-slides"),
      tools: document.getElementById("panel-tools"),
      game: document.getElementById("panel-game"),
      worked: document.getElementById("panel-worked"),
    };
    tabs.forEach((t) => t.addEventListener("click", () => {
      tabs.forEach((x) => x.classList.toggle("active", x === t));
      for (const k in panels) { if (panels[k]) panels[k].classList.toggle("hidden", k !== t.dataset.tab); }
      if (window.FactGame) { (t.dataset.tab === "game" ? window.FactGame.show() : window.FactGame.hide()); }
    }));
  }

  function initDecks() {
    const frame = document.getElementById("deck-frame");
    const btns = document.querySelectorAll("[data-deck]");
    btns.forEach((b) => b.addEventListener("click", () => {
      btns.forEach((x) => x.classList.toggle("active", x === b));
      frame.src = b.dataset.deck;
    }));
  }

  function start() { renderTexAttrs(); initTabs(); initDecks(); initTools(); initCalc(); }
  if (window.katex) { window.addEventListener("DOMContentLoaded", start); }
  else { window.addEventListener("DOMContentLoaded", () => {
    // KaTeX is deferred; ensure it is present before first render.
    (function wait() { if (window.katex) start(); else setTimeout(wait, 30); })();
  }); }
})();
