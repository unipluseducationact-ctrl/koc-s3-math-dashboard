/* Inequality — topic page wiring + interactive grapher.
 *
 * Tab 1 (Concept & Formula): two Manim-Slides decks shown in an iframe.
 * Tab 2 (Interactive Tool): a Desmos-style grapher with three modes:
 *
 *   1d  — plot y = f(x); the solution of  f(x) <rel> 0  is shown on the x-axis
 *         (number line) as intervals with open / closed dots, tying back to the
 *         concept decks.
 *   2d  — an inequality in x and y; the solution is a *region* of the plane,
 *         shaded, with its boundary curve (line, parabola, circle, ellipse,
 *         heart, ...) drawn solid (included) or dashed (excluded).
 *   3d  — the same equation in space: its solution becomes a *surface*
 *         (e.g. x + 4 = 0 is the plane x = -4), drawn in isometric 3D.
 *
 * Sign / accent colours match the Manim decks.
 */
(function () {
  "use strict";

  const COL = {
    bg: "#0b1222", grid: "#1b2748", grid2: "#243456", axis: "#6679a0",
    ink: "#e5e7eb", dim: "#94a3b8",
    curve: "#4FC3F7",
    region: "rgba(79,195,247,0.16)", regionEdge: "#4FC3F7",
    sol: "#FFD54F", solFill: "rgba(255,213,79,0.16)",
    plane: "rgba(79,195,247,0.18)", planeEdge: "#4FC3F7",
    z: "#66BB6A", arrow: "#FFD54F",
  };

  let DPR = 1;

  // ── tiny helpers ──────────────────────────────────────────────────────────
  function km(el, tex) {
    try { katex.render(tex, el, { throwOnError: false, displayMode: false }); }
    catch (e) { el.textContent = tex; }
  }
  const REL_TEX = { "=": "=", ">": ">", "<": "<", ">=": "\\ge", "<=": "\\le" };
  const REL_LABEL = { "=": "=", ">": ">", "<": "<", ">=": "\u2265", "<=": "\u2264" };

  function fmtNum(v) {
    if (!isFinite(v)) return v > 0 ? "\\infty" : "-\\infty";
    const r = Math.round(v * 100) / 100;
    if (Math.abs(r) < 1e-9) return "0";
    if (Math.abs(r - Math.round(r)) < 1e-9) return String(Math.round(r));
    return String(r);
  }

  function holds(v, rel) {
    if (rel === ">") return v > 0;
    if (rel === "<") return v < 0;
    if (rel === ">=") return v >= 0;
    if (rel === "<=") return v <= 0;
    return false; // "=" handled separately
  }

  // ── presets ────────────────────────────────────────────────────────────────
  const P1 = [
    { id: "lin1", label: "Line:  x + 4", tex: "x+4", f: (x) => x + 4,
      b: { xmin: -10, xmax: 6, ymin: -6, ymax: 8 }, rel: ">" },
    { id: "lin2", label: "Line:  2x \u2212 6", tex: "2x-6", f: (x) => 2 * x - 6,
      b: { xmin: -4, xmax: 10, ymin: -10, ymax: 8 }, rel: ">" },
    { id: "linNeg", label: "Line (negative):  \u2212x + 1", tex: "-x+1", f: (x) => -x + 1,
      b: { xmin: -8, xmax: 8, ymin: -8, ymax: 8 }, rel: ">=" },
    { id: "quad1", label: "Parabola:  x\u00b2 \u2212 4", tex: "x^2-4", f: (x) => x * x - 4,
      b: { xmin: -6, xmax: 6, ymin: -6, ymax: 10 }, rel: ">" },
    { id: "quad2", label: "Parabola:  x\u00b2 + 2x \u2212 3", tex: "x^2+2x-3", f: (x) => x * x + 2 * x - 3,
      b: { xmin: -6, xmax: 5, ymin: -6, ymax: 10 }, rel: "<" },
    { id: "quadN", label: "Parabola (\u2229):  9 \u2212 x\u00b2", tex: "9-x^2", f: (x) => 9 - x * x,
      b: { xmin: -6, xmax: 6, ymin: -8, ymax: 11 }, rel: ">" },
    { id: "cubic", label: "Cubic:  x\u00b3 \u2212 x", tex: "x^3-x", f: (x) => x * x * x - x,
      b: { xmin: -3, xmax: 3, ymin: -4, ymax: 4 }, rel: ">" },
    { id: "abs", label: "Absolute:  |x| \u2212 2", tex: "|x|-2", f: (x) => Math.abs(x) - 2,
      b: { xmin: -8, xmax: 8, ymin: -4, ymax: 8 }, rel: "<" },
    { id: "quartic", label: "Quartic:  x\u2074 \u2212 5x\u00b2 + 4", tex: "x^4-5x^2+4",
      f: (x) => x * x * x * x - 5 * x * x + 4, b: { xmin: -3, xmax: 3, ymin: -4, ymax: 8 }, rel: ">" },
  ];

  const P2 = [
    { id: "half1", label: "Half-plane:  y vs x + 4", lhs: "y", rhs: "x+4",
      F: (x, y) => y - (x + 4), b: { xmin: -9, xmax: 5, ymin: -5, ymax: 9 }, rel: ">",
      shape: "half-plane" },
    { id: "half2", label: "Half-plane:  y vs \u22122x + 3", lhs: "y", rhs: "-2x+3",
      F: (x, y) => y - (-2 * x + 3), b: { xmin: -6, xmax: 6, ymin: -6, ymax: 6 }, rel: "<=",
      shape: "half-plane" },
    { id: "disk", label: "Circle:  x\u00b2 + y\u00b2 vs 16", lhs: "x^2+y^2", rhs: "16",
      F: (x, y) => x * x + y * y - 16, b: { xmin: -6, xmax: 6, ymin: -6, ymax: 6 }, rel: "<",
      shape: "disk" },
    { id: "ellipse", label: "Ellipse:  x\u00b2/9 + y\u00b2/4 vs 1", lhs: "\\frac{x^2}{9}+\\frac{y^2}{4}", rhs: "1",
      F: (x, y) => x * x / 9 + y * y / 4 - 1, b: { xmin: -5, xmax: 5, ymin: -4, ymax: 4 }, rel: "<=",
      shape: "ellipse" },
    { id: "parab", label: "Parabola region:  y vs x\u00b2 \u2212 4", lhs: "y", rhs: "x^2-4",
      F: (x, y) => y - (x * x - 4), b: { xmin: -5, xmax: 5, ymin: -6, ymax: 8 }, rel: ">",
      shape: "parabola" },
    { id: "strip", label: "Strip:  |x| vs 3", lhs: "|x|", rhs: "3",
      F: (x, y) => Math.abs(x) - 3, b: { xmin: -7, xmax: 7, ymin: -5, ymax: 5 }, rel: "<",
      shape: "vertical strip" },
    { id: "heart", label: "Heart \u2661", lhs: "(x^2+y^2-1)^3", rhs: "x^2y^3",
      F: (x, y) => Math.pow(x * x + y * y - 1, 3) - x * x * Math.pow(y, 3),
      b: { xmin: -1.8, xmax: 1.8, ymin: -1.7, ymax: 1.7 }, rel: "<", shape: "heart" },
  ];

  const P3 = [
    { id: "planeX", label: "x + 4 = 0   \u2192 plane x = \u22124", tex: "x+4", kind: "planeAxis",
      axis: 0, val: -4, rel: "=" },
    { id: "planeY", label: "y \u2212 2 = 0   \u2192 plane y = 2", tex: "y-2", kind: "planeAxis",
      axis: 1, val: 2, rel: "=" },
    { id: "planeG", label: "z = x + y   \u2192 tilted plane", tex: "z-(x+y)", kind: "planeGraph",
      g: (x, y) => x + y, rel: "=" },
    { id: "sphere", label: "x\u00b2 + y\u00b2 + z\u00b2 = 25   \u2192 sphere", tex: "x^2+y^2+z^2-25",
      kind: "sphere", r: 5, rel: "=" },
  ];

  const RELS = { "1d": ["=", ">", "<", ">=", "<="], "2d": [">", "<", ">=", "<=", "="], "3d": ["=", ">", "<"] };
  const PRESETS = { "1d": P1, "2d": P2, "3d": P3 };

  // ── view transform (equal scale on both axes) ───────────────────────────────
  function equalize(b, w, h) {
    const A = w / h;
    let xr = b.xmax - b.xmin, yr = b.ymax - b.ymin;
    const cx = (b.xmin + b.xmax) / 2, cy = (b.ymin + b.ymax) / 2;
    if (xr / yr < A) xr = yr * A; else yr = xr / A;
    return { xmin: cx - xr / 2, xmax: cx + xr / 2, ymin: cy - yr / 2, ymax: cy + yr / 2 };
  }
  function makeView(w, h, b) {
    return {
      w, h, b,
      X: (x) => (x - b.xmin) / (b.xmax - b.xmin) * w,
      Y: (y) => h - (y - b.ymin) / (b.ymax - b.ymin) * h,
      ix: (px) => b.xmin + px / w * (b.xmax - b.xmin),
      iy: (py) => b.ymin + (h - py) / h * (b.ymax - b.ymin),
    };
  }
  function niceStep(raw) {
    const p = Math.pow(10, Math.floor(Math.log10(raw)));
    const n = raw / p;
    return (n < 1.5 ? 1 : n < 3 ? 2 : n < 7 ? 5 : 10) * p;
  }

  function drawGrid(ctx, V) {
    ctx.fillStyle = COL.bg;
    ctx.fillRect(0, 0, V.w, V.h);
    const step = niceStep((V.b.xmax - V.b.xmin) / 12);
    ctx.lineWidth = 1;
    ctx.strokeStyle = COL.grid;
    for (let x = Math.ceil(V.b.xmin / step) * step; x <= V.b.xmax; x += step) {
      const px = V.X(x);
      ctx.beginPath(); ctx.moveTo(px, 0); ctx.lineTo(px, V.h); ctx.stroke();
    }
    for (let y = Math.ceil(V.b.ymin / step) * step; y <= V.b.ymax; y += step) {
      const py = V.Y(y);
      ctx.beginPath(); ctx.moveTo(0, py); ctx.lineTo(V.w, py); ctx.stroke();
    }
    // axes
    ctx.strokeStyle = COL.axis; ctx.lineWidth = 1.8 * DPR;
    const y0 = V.Y(0), x0 = V.X(0);
    if (V.b.ymin < 0 && V.b.ymax > 0) { ctx.beginPath(); ctx.moveTo(0, y0); ctx.lineTo(V.w, y0); ctx.stroke(); }
    if (V.b.xmin < 0 && V.b.xmax > 0) { ctx.beginPath(); ctx.moveTo(x0, 0); ctx.lineTo(x0, V.h); ctx.stroke(); }
    // labels
    ctx.fillStyle = COL.dim;
    ctx.font = `${Math.round(12 * DPR)}px "JetBrains Mono", monospace`;
    ctx.textAlign = "center"; ctx.textBaseline = "top";
    const labY = V.b.ymin < 0 && V.b.ymax > 0 ? y0 + 4 * DPR : V.h - 16 * DPR;
    for (let x = Math.ceil(V.b.xmin / step) * step; x <= V.b.xmax; x += step) {
      if (Math.abs(x) < 1e-9) continue;
      ctx.fillText(fmtNum(x), V.X(x), labY);
    }
    ctx.textAlign = "right"; ctx.textBaseline = "middle";
    const labX = V.b.xmin < 0 && V.b.xmax > 0 ? x0 - 6 * DPR : V.w - 6 * DPR;
    for (let y = Math.ceil(V.b.ymin / step) * step; y <= V.b.ymax; y += step) {
      if (Math.abs(y) < 1e-9) continue;
      ctx.fillText(fmtNum(y), labX, V.Y(y));
    }
  }

  function arrowHead(ctx, x, y, dir, color, s) {
    s = s || 9 * DPR;
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x - dir * s, y - s * 0.7);
    ctx.lineTo(x - dir * s, y + s * 0.7);
    ctx.closePath(); ctx.fill();
  }

  // ── 1-variable: solution on the x-axis ──────────────────────────────────────
  function bisect(f, a, b) {
    let fa = f(a);
    for (let k = 0; k < 60; k++) {
      const m = (a + b) / 2, fm = f(m);
      if (fa === 0) return a;
      if ((fa < 0) !== (fm < 0)) b = m; else { a = m; fa = fm; }
    }
    return (a + b) / 2;
  }
  function findRoots(f, xmin, xmax) {
    const N = 3000; let roots = []; let px = xmin, pv = f(xmin);
    for (let i = 1; i <= N; i++) {
      const x = xmin + (xmax - xmin) * i / N, v = f(x);
      if (pv === 0) roots.push(px);
      else if ((pv < 0) !== (v < 0)) roots.push(bisect(f, px, x));
      px = x; pv = v;
    }
    roots.sort((a, b) => a - b);
    const out = [];
    for (const r of roots) if (!out.length || Math.abs(out[out.length - 1] - r) > 1e-6) out.push(r);
    return out;
  }
  function analyze1D(f, b, rel) {
    const roots = findRoots(f, b.xmin, b.xmax);
    if (rel === "=") return { roots, parts: [], points: roots };
    const cuts = [-Infinity, ...roots, Infinity];
    const inc = rel === ">=" || rel === "<=";
    const raw = [];
    for (let i = 0; i < cuts.length - 1; i++) {
      const a = cuts[i], c = cuts[i + 1];
      const mid = a === -Infinity ? c - 1 : (c === Infinity ? a + 1 : (a + c) / 2);
      if (holds(f(mid), rel)) raw.push([a, c]);
    }
    const parts = [];
    for (const iv of raw) {
      const last = parts[parts.length - 1];
      if (last && inc && isFinite(last[1]) && Math.abs(last[1] - iv[0]) < 1e-9) last[1] = iv[1];
      else parts.push([iv[0], iv[1]]);
    }
    return { roots, parts, inc };
  }
  function solTex(an, rel) {
    if (rel === "=") {
      if (!an.roots.length) return "\\text{no real solution}";
      return an.roots.map((r) => "x = " + fmtNum(r)).join(",\\quad ");
    }
    if (!an.parts.length) return "\\text{no solution}";
    const inc = an.inc;
    const pieces = an.parts.map(([a, c]) => {
      const aF = isFinite(a), cF = isFinite(c);
      if (!aF && !cF) return "\\text{all real } x";
      if (!aF) return "x " + (inc ? "\\le" : "<") + " " + fmtNum(c);
      if (!cF) return "x " + (inc ? "\\ge" : ">") + " " + fmtNum(a);
      const s = inc ? "\\le" : "<";
      return fmtNum(a) + " " + s + " x " + s + " " + fmtNum(c);
    });
    return pieces.join("\\quad\\text{or}\\quad ");
  }

  function render1D(ctx, canvas, preset, rel) {
    const V = makeView(canvas.width, canvas.height, preset.b);
    drawGrid(ctx, V);
    const f = preset.f, an = analyze1D(f, V.b, rel);
    const y0 = V.Y(0);

    // area between curve and x-axis where the inequality holds
    if (rel !== "=") {
      ctx.fillStyle = COL.solFill;
      for (let px = 0; px <= V.w; px += 1) {
        const x = V.ix(px), v = f(x);
        if (!holds(v, rel)) continue;
        const yc = V.Y(Math.max(V.b.ymin, Math.min(V.b.ymax, v)));
        ctx.fillRect(px, Math.min(y0, yc), 1, Math.abs(yc - y0));
      }
    }

    // the curve y = f(x)
    ctx.strokeStyle = COL.curve; ctx.lineWidth = 2.6 * DPR;
    ctx.beginPath();
    let started = false;
    for (let px = 0; px <= V.w; px += 1) {
      const y = f(V.ix(px)), py = V.Y(y);
      if (!isFinite(py)) { started = false; continue; }
      if (!started) { ctx.moveTo(px, py); started = true; } else ctx.lineTo(px, py);
    }
    ctx.stroke();

    // solution on the x-axis
    ctx.strokeStyle = COL.sol; ctx.lineWidth = 6 * DPR; ctx.lineCap = "round";
    for (const [a, c] of an.parts) {
      const ax = isFinite(a) ? V.X(a) : 0;
      const cx = isFinite(c) ? V.X(c) : V.w;
      const x1 = Math.max(0, Math.min(ax, cx)), x2 = Math.min(V.w, Math.max(ax, cx));
      ctx.beginPath(); ctx.moveTo(x1, y0); ctx.lineTo(x2, y0); ctx.stroke();
      if (!isFinite(a)) arrowHead(ctx, 2 * DPR, y0, -1, COL.sol);
      if (!isFinite(c)) arrowHead(ctx, V.w - 2 * DPR, y0, 1, COL.sol);
    }
    ctx.lineCap = "butt";

    // dots at the boundary values
    const dots = [];
    if (rel === "=") { for (const r of an.roots) dots.push([r, true]); }
    else { for (const [a, c] of an.parts) { if (isFinite(a)) dots.push([a, an.inc]); if (isFinite(c)) dots.push([c, an.inc]); } }
    for (const [r, closed] of dots) {
      const px = V.X(r);
      ctx.beginPath(); ctx.arc(px, y0, 6 * DPR, 0, Math.PI * 2);
      if (closed) { ctx.fillStyle = COL.sol; ctx.fill(); }
      else { ctx.fillStyle = COL.bg; ctx.fill(); ctx.lineWidth = 3 * DPR; ctx.strokeStyle = COL.sol; ctx.stroke(); }
    }
    return an;
  }

  // ── 2-variable: shaded region + marching-squares boundary ───────────────────
  function marchingSquares(F, b, nx, ny) {
    const xs = new Array(nx), ys = new Array(ny), val = [];
    for (let i = 0; i < nx; i++) xs[i] = b.xmin + (b.xmax - b.xmin) * i / (nx - 1);
    for (let j = 0; j < ny; j++) ys[j] = b.ymin + (b.ymax - b.ymin) * j / (ny - 1);
    for (let i = 0; i < nx; i++) { val[i] = new Array(ny); for (let j = 0; j < ny; j++) val[i][j] = F(xs[i], ys[j]); }
    const segs = [];
    const ix = (xa, xb, va, vb, y) => ({ x: xa + (xb - xa) * (va / (va - vb)), y });
    const iy = (x, ya, yb, va, vb) => ({ x, y: ya + (yb - ya) * (va / (va - vb)) });
    for (let i = 0; i < nx - 1; i++) {
      for (let j = 0; j < ny - 1; j++) {
        const v00 = val[i][j], v10 = val[i + 1][j], v11 = val[i + 1][j + 1], v01 = val[i][j + 1];
        const pts = [];
        if ((v00 < 0) !== (v10 < 0)) pts.push(ix(xs[i], xs[i + 1], v00, v10, ys[j]));
        if ((v10 < 0) !== (v11 < 0)) pts.push(iy(xs[i + 1], ys[j], ys[j + 1], v10, v11));
        if ((v01 < 0) !== (v11 < 0)) pts.push(ix(xs[i], xs[i + 1], v01, v11, ys[j + 1]));
        if ((v00 < 0) !== (v01 < 0)) pts.push(iy(xs[i], ys[j], ys[j + 1], v00, v01));
        if (pts.length === 2) segs.push([pts[0], pts[1]]);
        else if (pts.length === 4) { segs.push([pts[0], pts[1]]); segs.push([pts[2], pts[3]]); }
      }
    }
    return segs;
  }

  function render2D(ctx, canvas, preset, rel) {
    const V = makeView(canvas.width, canvas.height, equalize(preset.b, canvas.width, canvas.height));
    drawGrid(ctx, V);
    const F = preset.F;

    if (rel !== "=") {
      const S = Math.max(2, Math.round(2 * DPR));
      ctx.fillStyle = COL.region;
      for (let py = 0; py < V.h; py += S) {
        const y = V.iy(py);
        for (let px = 0; px < V.w; px += S) {
          if (holds(F(V.ix(px), y), rel)) ctx.fillRect(px, py, S, S);
        }
      }
    }

    const segs = marchingSquares(F, V.b, 240, Math.round(240 * V.h / V.w));
    ctx.strokeStyle = COL.regionEdge; ctx.lineWidth = 2.6 * DPR;
    ctx.setLineDash(rel === ">" || rel === "<" ? [9 * DPR, 6 * DPR] : []);
    ctx.beginPath();
    for (const [p, q] of segs) { ctx.moveTo(V.X(p.x), V.Y(p.y)); ctx.lineTo(V.X(q.x), V.Y(q.y)); }
    ctx.stroke();
    ctx.setLineDash([]);
  }

  // ── 3D: isometric surfaces ──────────────────────────────────────────────────
  function render3D(ctx, canvas, preset, rel) {
    const w = canvas.width, h = canvas.height;
    ctx.fillStyle = COL.bg; ctx.fillRect(0, 0, w, h);
    const R = 6, cx = w / 2, cy = h / 2 + 0.10 * h;
    const scale = Math.min(w, h) / (2 * R * 1.45);
    const P = (x, y, z) => ({ x: cx + (x - y) * 0.866 * scale, y: cy + ((x + y) * 0.5 - z) * scale });
    const line = (a, b, color, lw) => {
      ctx.strokeStyle = color; ctx.lineWidth = (lw || 1) * DPR;
      ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
    };

    // floor grid on z = 0
    for (let g = -R; g <= R; g += 2) {
      line(P(g, -R, 0), P(g, R, 0), COL.grid, 1);
      line(P(-R, g, 0), P(R, g, 0), COL.grid, 1);
    }
    // axes
    line(P(-R, 0, 0), P(R, 0, 0), COL.axis, 1.6);
    line(P(0, -R, 0), P(0, R, 0), COL.axis, 1.6);
    line(P(0, 0, 0), P(0, 0, R), COL.axis, 1.6);
    ctx.fillStyle = COL.dim;
    ctx.font = `${Math.round(13 * DPR)}px "JetBrains Mono", monospace`;
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    let p;
    p = P(R + 0.6, 0, 0); ctx.fillText("x", p.x, p.y);
    p = P(0, R + 0.6, 0); ctx.fillText("y", p.x, p.y);
    p = P(0, 0, R + 0.6); ctx.fillText("z", p.x, p.y);

    const fillQuad = (c, edge) => {
      ctx.fillStyle = COL.plane; ctx.beginPath();
      ctx.moveTo(c[0].x, c[0].y); for (let i = 1; i < c.length; i++) ctx.lineTo(c[i].x, c[i].y);
      ctx.closePath(); ctx.fill();
      ctx.strokeStyle = edge || COL.planeEdge; ctx.lineWidth = 2 * DPR; ctx.stroke();
    };

    if (preset.kind === "planeAxis") {
      const v = preset.val, ax = preset.axis;
      let corners;
      if (ax === 0) corners = [P(v, -R, -R), P(v, R, -R), P(v, R, R), P(v, -R, R)];
      else corners = [P(-R, v, -R), P(R, v, -R), P(R, v, R), P(-R, v, R)];
      fillQuad(corners);
      if (rel !== "=") {
        const s = rel === ">" ? 1 : -1;
        const o = ax === 0 ? P(v, 0, 0) : P(0, v, 0);
        const t = ax === 0 ? P(v + s * 2.4, 0, 0) : P(0, v + s * 2.4, 0);
        line(o, t, COL.arrow, 3);
        arrowHead(ctx, t.x, t.y, t.x > o.x ? 1 : -1, COL.arrow);
      }
    } else if (preset.kind === "planeGraph") {
      const D = 3, g = preset.g;
      const corners = [P(-D, -D, g(-D, -D)), P(D, -D, g(D, -D)), P(D, D, g(D, D)), P(-D, D, g(-D, D))];
      fillQuad(corners, COL.z);
      // grid lines on the plane
      for (let t = -D; t <= D; t += 1.5) {
        line(P(t, -D, g(t, -D)), P(t, D, g(t, D)), "rgba(102,187,106,0.5)", 1);
        line(P(-D, t, g(-D, t)), P(D, t, g(D, t)), "rgba(102,187,106,0.5)", 1);
      }
    } else if (preset.kind === "sphere") {
      const r = preset.r;
      ctx.strokeStyle = COL.planeEdge; ctx.lineWidth = 1.4 * DPR;
      for (let k = -2; k <= 2; k++) {       // latitudes
        const z = (r * k) / 3, rho = Math.sqrt(Math.max(0, r * r - z * z));
        ctx.beginPath();
        for (let a = 0; a <= 64; a++) {
          const t = (a / 64) * Math.PI * 2, pt = P(rho * Math.cos(t), rho * Math.sin(t), z);
          a ? ctx.lineTo(pt.x, pt.y) : ctx.moveTo(pt.x, pt.y);
        }
        ctx.stroke();
      }
      for (let m = 0; m < 6; m++) {          // longitudes
        const ph = (m / 6) * Math.PI;
        ctx.beginPath();
        for (let a = 0; a <= 64; a++) {
          const t = (a / 64) * Math.PI * 2;
          const pt = P(r * Math.sin(t) * Math.cos(ph), r * Math.sin(t) * Math.sin(ph), r * Math.cos(t));
          a ? ctx.lineTo(pt.x, pt.y) : ctx.moveTo(pt.x, pt.y);
        }
        ctx.stroke();
      }
    }
  }

  // ── readout text ─────────────────────────────────────────────────────────────
  function setReadout(mode, preset, rel, an) {
    const eqEl = document.getElementById("gr-eq");
    const solEl = document.getElementById("gr-sol");
    const noteEl = document.getElementById("gr-note");
    const legEl = document.getElementById("gr-legend");
    legEl.innerHTML = "";

    if (mode === "1d") {
      km(eqEl, `${preset.tex} \\;${REL_TEX[rel]}\\; 0`);
      km(solEl, solTex(an, rel));
      noteEl.textContent = rel === "="
        ? "The roots are where the curve crosses the x-axis."
        : "Read it off the x-axis: where the curve is " +
          (rel === ">" || rel === ">=" ? "above" : "below") + " the axis" +
          (rel === ">=" || rel === "<=" ? " (boundary included \u2192 closed dot)." : " (boundary excluded \u2192 open dot).");
      legEl.innerHTML =
        `<span class="li"><i class="sw" style="background:${COL.curve}"></i>y = f(x)</span>` +
        `<span class="li"><i class="sw" style="background:${COL.sol}"></i>solution on the x-axis</span>` +
        `<span class="li"><i class="dotmark" style="background:${COL.sol}"></i>included</span>` +
        `<span class="li"><i class="dotmark" style="background:${COL.bg};border:3px solid ${COL.sol}"></i>excluded</span>`;
    } else if (mode === "2d") {
      km(eqEl, `${preset.lhs} \\;${REL_TEX[rel]}\\; ${preset.rhs}`);
      if (rel === "=") { km(solEl, "\\text{the boundary curve}"); }
      else { solEl.textContent = "the shaded region"; }
      const incl = rel === ">=" || rel === "<=";
      noteEl.textContent = rel === "="
        ? `The solution is just the ${preset.shape} boundary itself.`
        : `Every point (x, y) in the shaded region satisfies it. Boundary is ` +
          (incl ? "solid (included)." : "dashed (excluded).");
      legEl.innerHTML =
        `<span class="li"><i class="sw" style="background:${COL.regionEdge};opacity:.5"></i>solution region</span>` +
        `<span class="li"><i class="sw" style="background:${COL.regionEdge}"></i>boundary (${preset.shape})</span>`;
    } else {
      km(eqEl, `${preset.tex} \\;${REL_TEX[rel]}\\; 0`);
      if (preset.kind === "sphere") {
        km(solEl, rel === "=" ? "\\text{a sphere (surface)}" : (rel === "<" ? "\\text{the solid ball inside}" : "\\text{outside the sphere}"));
        noteEl.textContent = "In space, x\u00b2+y\u00b2+z\u00b2 = 25 is a 2-D surface; the inequality fills a 3-D region.";
      } else {
        km(solEl, rel === "=" ? "\\text{a plane}" : "\\text{a half-space}");
        noteEl.textContent = preset.kind === "planeAxis"
          ? "Same equation, different worlds: x + 4 = 0 is a point on a line, a line in the plane, and a plane in space."
          : "z = x + y is a tilted plane; '>' / '<' pick the half-space above or below it.";
      }
      legEl.innerHTML = `<span class="li"><i class="sw" style="background:${COL.planeEdge};opacity:.6"></i>solution surface</span>`;
    }
  }

  // ── grapher controller ───────────────────────────────────────────────────────
  function initGrapher() {
    const canvas = document.getElementById("gr-canvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const presetSel = document.getElementById("gr-preset");
    const relBox = document.getElementById("gr-relations");

    const state = { mode: "1d", preset: P1[0], rel: P1[0].rel };

    function populatePresets() {
      presetSel.innerHTML = "";
      P1.forEach((p) => presetSel.add(new Option(p.label, p.id)));
      presetSel.value = state.preset.id;
    }
    function populateRelations() {
      relBox.innerHTML = "";
      RELS["1d"].forEach((r) => {
        const btn = document.createElement("button");
        btn.textContent = REL_LABEL[r];
        btn.classList.toggle("active", r === state.rel);
        btn.addEventListener("click", () => { state.rel = r; syncRelations(); render(); });
        relBox.appendChild(btn);
      });
    }
    function syncRelations() {
      [...relBox.children].forEach((btn, i) => btn.classList.toggle("active", RELS["1d"][i] === state.rel));
    }

    function render() {
      const panel = document.getElementById("panel-tools");
      if (!panel || panel.classList.contains("hidden")) return;
      const rect = canvas.getBoundingClientRect();
      if (rect.width < 2) return;
      DPR = window.devicePixelRatio || 1;
      canvas.width = Math.round(rect.width * DPR);
      canvas.height = Math.round(rect.height * DPR);
      const an = render1D(ctx, canvas, state.preset, state.rel);
      setReadout("1d", state.preset, state.rel, an);
    }

    presetSel.addEventListener("change", () => {
      state.preset = P1.find((p) => p.id === presetSel.value);
      state.rel = state.preset.rel;
      populateRelations(); render();
    });
    window.addEventListener("resize", render);

    populatePresets(); populateRelations();
    // expose a hook so the tab switch can trigger the first paint
    initGrapher._render = render;
  }

  // ── tab / deck wiring ─────────────────────────────────────────────────────────
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
      for (const k in panels) if (panels[k]) panels[k].classList.toggle("hidden", k !== t.dataset.tab);
      if (t.dataset.tab === "tools" && initGrapher._render) requestAnimationFrame(initGrapher._render);
      if (t.dataset.tab === "game" && window.IneqGame) requestAnimationFrame(window.IneqGame.onShow);
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
  function applyDeepLink() {
    const q = new URLSearchParams(location.search);
    const tab = q.get("tab"), deck = q.get("deck");
    if (tab) { const b = document.querySelector(`[data-tab="${tab}"]`); if (b) b.click(); }
    if (deck) { const b = document.querySelector(`[data-deck*="/${deck}/"]`); if (b) b.click(); }
  }

  function start() { initTabs(); initDecks(); initGrapher(); applyDeepLink(); }
  if (window.katex) window.addEventListener("DOMContentLoaded", start);
  else window.addEventListener("DOMContentLoaded", () => {
    (function wait() { if (window.katex) start(); else setTimeout(wait, 30); })();
  });
})();
