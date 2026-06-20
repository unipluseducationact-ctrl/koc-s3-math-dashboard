#!/usr/bin/env node
/**
 * Label overlap audit for triSim + paraSim in output/index.html.
 *
 * Mirrors layout/label-position math and sweeps:
 *   3 tri configs × 5 steps × 3 slider corners
 *   3 para modes × 5 steps × 3 slider corners
 *
 * Run: node scripts/audit-label-overlap.js
 * Exit 1 if any failure.
 */

const LABEL_PAD = 20;
const LABEL_GAP = 4;

// ── Shared geometry (mirrors LabelGeom in index.html) ──

function estimateLabelBBox(x, y, text, size, anchor = 'middle', dx = 0, dy = 0) {
    const px = Math.round(size * 0.38);
    const py = Math.round(size * 0.22);
    const estW = text.length * size * 0.68;
    const tx = x + dx;
    const ty = y + dy;
    let left;
    if (anchor === 'start') left = tx - px;
    else if (anchor === 'end') left = tx - estW - px;
    else left = tx - estW / 2 - px;
    const top = ty - size - py + 2;
    const width = estW + px * 2;
    const height = size + py * 2;
    return { left, top, width, height, right: left + width, bottom: top + height };
}

function minDistToSegment(p, a, b) {
    const dx = b.x - a.x;
    const dy = b.y - a.y;
    const len2 = dx * dx + dy * dy;
    if (len2 < 1e-9) return Math.hypot(p.x - a.x, p.y - a.y);
    let t = ((p.x - a.x) * dx + (p.y - a.y) * dy) / len2;
    t = Math.max(0, Math.min(1, t));
    return Math.hypot(p.x - (a.x + t * dx), p.y - (a.y + t * dy));
}

function pointInTri(p, a, b, c) {
    const v0x = c.x - a.x;
    const v0y = c.y - a.y;
    const v1x = b.x - a.x;
    const v1y = b.y - a.y;
    const v2x = p.x - a.x;
    const v2y = p.y - a.y;
    const dot00 = v0x * v0x + v0y * v0y;
    const dot01 = v0x * v1x + v0y * v1y;
    const dot02 = v0x * v2x + v0y * v2y;
    const dot11 = v1x * v1x + v1y * v1y;
    const dot12 = v1x * v2x + v1y * v2y;
    const denom = dot00 * dot11 - dot01 * dot01;
    if (Math.abs(denom) < 1e-9) return false;
    const inv = 1 / denom;
    const u = (dot11 * dot02 - dot01 * dot12) * inv;
    const v = (dot00 * dot12 - dot01 * dot02) * inv;
    return u >= 0 && v >= 0 && u + v <= 1;
}

function interiorWithPad(p, a, b, c, pad = LABEL_PAD) {
    if (!pointInTri(p, a, b, c)) return false;
    return minDistToSegment(p, a, b) >= pad
        && minDistToSegment(p, b, c) >= pad
        && minDistToSegment(p, c, a) >= pad;
}

function triCentroid(a, b, c) {
    return { x: (a.x + b.x + c.x) / 3, y: (a.y + b.y + c.y) / 3 };
}

function triLabelPoint(a, b, c, wA = 0.34, wB = 0.33, wC = 0.33) {
    return { x: a.x * wA + b.x * wB + c.x * wC, y: a.y * wA + b.y * wB + c.y * wC };
}

function nudgeToInterior(pt, a, b, c, pad = LABEL_PAD) {
    for (const pTry of [pad, 14, 10, 6, 0]) {
        let p = { x: pt.x, y: pt.y };
        if (interiorWithPad(p, a, b, c, pTry)) return p;
        const center = triCentroid(a, b, c);
        for (let i = 0; i < 28; i++) {
            p.x += (center.x - p.x) * 0.38;
            p.y += (center.y - p.y) * 0.38;
            if (interiorWithPad(p, a, b, c, pTry)) return p;
        }
    }
    return triCentroid(a, b, c);
}

function bboxGap(a, b) {
    const gx = Math.max(0, Math.max(a.left, b.left) - Math.min(a.right, b.right));
    const gy = Math.max(0, Math.max(a.top, b.top) - Math.min(a.bottom, b.bottom));
    return Math.max(gx, gy);
}

function segmentIntersectsBBox(a, b, bb, buffer = 3) {
    const expanded = {
        left: bb.left - buffer,
        top: bb.top - buffer,
        right: bb.right + buffer,
        bottom: bb.bottom + buffer,
    };
    const samples = 12;
    for (let i = 0; i <= samples; i++) {
        const t = i / samples;
        const px = a.x + t * (b.x - a.x);
        const py = a.y + t * (b.y - a.y);
        if (px >= expanded.left && px <= expanded.right && py >= expanded.top && py <= expanded.bottom) {
            return true;
        }
    }
    return false;
}

// ── triSim layout (mirrors output/index.html) ──

const VB = { w: 900, h: 660 };
const PAD = { t: 64, r: 96, b: 82, l: 64 };
const TRI_FONT = { caption: 16, dim: 17, area: 18, apex: 16 };
const H_DIM_RESERVE = 80;
const H_REF = 200;
const B_REF = 220;

function centroid(x1, y1, x2, y2, x3, y3) {
    return { x: (x1 + x2 + x3) / 3, y: (y1 + y2 + y3) / 3 };
}

function heightModeLayout(data) {
    const gap = 56;
    const hPx = (VB.h - PAD.t - PAD.b) * 0.92 * (data.h1 / H_REF);
    const availW = VB.w - PAD.l - PAD.r - H_DIM_RESERVE;
    const rawSpan = data.b1 + gap + data.b2;
    const scale = availW / Math.max(rawSpan, 240);
    const b1 = data.b1 * scale;
    const b2 = data.b2 * scale;
    const startX = PAD.l + (availW - (b1 + gap + b2)) / 2;
    const baseY = VB.h - PAD.b;
    const apexY = baseY - hPx;
    const b1x1 = startX;
    const b1x2 = startX + b1;
    const b2x1 = b1x2 + gap;
    const b2x2 = b2x1 + b2;
    const apexX = (b1x1 + b2x2) / 2;
    const c1 = centroid(apexX, apexY, b1x1, baseY, b1x2, baseY);
    const c2 = centroid(apexX, apexY, b2x1, baseY, b2x2, baseY);
    return { b1x1, b1x2, b2x1, b2x2, apexX, apexY, baseY, hPx, c1, c2, b1, b2 };
}

function baseSameLayout(data) {
    const availW = VB.w - PAD.l - PAD.r;
    const bPx = availW * 0.68 * (data.b1 / B_REF);
    const vAvail = VB.h - PAD.t - PAD.b - 88;
    const hScale = (vAvail * 0.92) / 180;
    const h1Px = data.h1 * hScale;
    const h2Px = data.h2 * hScale;
    const midX = VB.w / 2;
    const baseY = VB.h - PAD.b;
    const bx1 = midX - bPx / 2;
    const bx2 = midX + bPx / 2;
    const spread = Math.max(118, bPx * 0.36);
    const ax1 = midX - spread;
    const ax2 = midX + spread;
    const ay1 = baseY - h1Px;
    const ay2 = baseY - h2Px;
    const c1 = centroid(ax1, ay1, bx1, baseY, bx2, baseY);
    const c2 = centroid(ax2, ay2, bx1, baseY, bx2, baseY);
    return { bPx, midX, baseY, bx1, bx2, ax1, ax2, ay1, ay2, c1, c2, h1Px, h2Px, spread };
}

function baseOppositeLayout(data) {
    const availW = VB.w - PAD.l - PAD.r;
    const bPx = availW * 0.62 * (data.b1 / B_REF);
    const vRoom = (VB.h - PAD.t - PAD.b) * 0.9;
    const hScale = vRoom / Math.max(data.h1 + data.h2 + 60, 180);
    const h1Px = data.h1 * hScale;
    const h2Px = data.h2 * hScale;
    const midX = VB.w / 2;
    const baseY = PAD.t + h1Px + 48;
    const bx1 = midX - bPx / 2;
    const bx2 = midX + bPx / 2;
    const ay1 = baseY - h1Px;
    const ay2 = baseY + h2Px;
    const c1 = centroid(midX, ay1, bx1, baseY, bx2, baseY);
    const c2 = centroid(midX, ay2, bx1, baseY, bx2, baseY);
    return { bPx, midX, baseY, bx1, bx2, ay1, ay2, c1, c2, h1Px, h2Px };
}

function heightAreaLabelPos(L, triIndex) {
    const { apexX, apexY, baseY, b1x1, b1x2, b2x1, b2x2, c1, c2 } = L;
    const apex = { x: apexX, y: apexY };
    if (triIndex === 1) {
        return nudgeToInterior(c1, apex, { x: b1x1, y: baseY }, { x: b1x2, y: baseY });
    }
    return nudgeToInterior(c2, apex, { x: b2x1, y: baseY }, { x: b2x2, y: baseY });
}

function areaLabelPos(L, triIndex) {
    const { baseY, bx1, bx2, ax1, ay1, ax2, ay2, c1, c2 } = L;
    let p;
    if (triIndex === 1) {
        p = nudgeToInterior(c1, { x: ax1, y: ay1 }, { x: bx1, y: baseY }, { x: bx2, y: baseY });
        p = nudgeToInterior({ x: p.x - 14, y: p.y - 30 }, { x: ax1, y: ay1 }, { x: bx1, y: baseY }, { x: bx2, y: baseY });
    } else {
        p = nudgeToInterior(c2, { x: ax2, y: ay2 }, { x: bx1, y: baseY }, { x: bx2, y: baseY });
        p = nudgeToInterior({ x: p.x + 14, y: p.y + 6 }, { x: ax2, y: ay2 }, { x: bx1, y: baseY }, { x: bx2, y: baseY });
    }
    return p;
}

function areaLabelPosOpposite(L, triIndex) {
    const { midX, baseY, bx1, bx2, ay1, ay2, c1, c2 } = L;
    const apex = { x: midX, y: triIndex === 1 ? ay1 : ay2 };
    const cent = triIndex === 1 ? c1 : c2;
    return nudgeToInterior(cent, apex, { x: bx1, y: baseY }, { x: bx2, y: baseY });
}

function fmt(n) { return Number.isInteger(n) ? String(n) : n.toFixed(1); }

function collectTriLabels(config, step, sliders, knownTri = 1) {
    const labels = [];
    const known = 48;
    const unknown = 60;

    if (config === 'height') {
        const data = { b1: sliders.b1, b2: sliders.b2, h1: sliders.h, h2: sliders.h };
        const L = heightModeLayout(data);
        const { b1x1, b1x2, b2x1, b2x2, apexX, apexY, baseY } = L;
        const k = knownTri;
        const u = k === 1 ? 2 : 1;
        const apex = { x: apexX, y: apexY };
        if (step < 2) {
            labels.push({ id: 'apex', x: apexX + 14, y: apexY - 6, text: 'A (shared apex)', size: TRI_FONT.apex, anchor: 'start', kind: 'exterior' });
        }
        if (step >= 2 && step < 4) {
            const p = heightAreaLabelPos(L, k);
            const givenDy = step === 3 ? 16 : 0;
            labels.push({ id: 'area-known', x: p.x, y: p.y + givenDy, text: `A${k} = ${fmt(known)}`, size: TRI_FONT.area, anchor: 'middle', kind: 'interior', tri: [apex, { x: k === 1 ? b1x1 : b2x1, y: baseY }, { x: k === 1 ? b1x2 : b2x2, y: baseY }] });
        }
        if (step >= 3) {
            const bracketY = baseY + 32;
            labels.push({ id: 'b1', x: (b1x1 + b1x2) / 2, y: bracketY + 32, text: `b₁ = ${data.b1}`, size: TRI_FONT.dim, anchor: 'middle', kind: 'exterior' });
            labels.push({ id: 'b2', x: (b2x1 + b2x2) / 2, y: bracketY + 32, text: `b₂ = ${data.b2}`, size: TRI_FONT.dim, anchor: 'middle', kind: 'exterior' });
        }
        if (step >= 4) {
            const pk = heightAreaLabelPos(L, k);
            const pu = heightAreaLabelPos(L, u);
            labels.push({ id: 'area-k', x: pk.x, y: pk.y, text: `A${k} = ${fmt(known)}`, size: TRI_FONT.area, anchor: 'middle', kind: 'interior', tri: [apex, { x: k === 1 ? b1x1 : b2x1, y: baseY }, { x: k === 1 ? b1x2 : b2x2, y: baseY }] });
            labels.push({ id: 'area-u', x: pu.x, y: pu.y, text: `A${u} = ${fmt(unknown)}`, size: TRI_FONT.area, anchor: 'middle', kind: 'interior', tri: [apex, { x: u === 1 ? b1x1 : b2x1, y: baseY }, { x: u === 1 ? b1x2 : b2x2, y: baseY }] });
        }
    } else if (config === 'baseSame') {
        const data = { b1: sliders.b, b2: sliders.b, h1: sliders.h1, h2: sliders.h2 };
        const L = baseSameLayout(data);
        const { baseY, bx1, bx2, ax1, ax2, ay1, ay2 } = L;
        const k = knownTri;
        if (step < 2) {
            labels.push({ id: 'A1', x: ax1 - 14, y: ay1 - 24, text: 'A₁', size: TRI_FONT.apex, anchor: 'end', kind: 'exterior' });
            labels.push({ id: 'A2', x: ax2 + 14, y: ay2 - 24, text: 'A₂', size: TRI_FONT.apex, anchor: 'start', kind: 'exterior' });
        }
        if (step >= 2 && step < 4) {
            const p = areaLabelPos(L, k);
            const tri = k === 1
                ? [{ x: ax1, y: ay1 }, { x: bx1, y: baseY }, { x: bx2, y: baseY }]
                : [{ x: ax2, y: ay2 }, { x: bx1, y: baseY }, { x: bx2, y: baseY }];
            labels.push({ id: 'area-known', x: p.x, y: p.y, text: `A${k} = ${fmt(known)}`, size: TRI_FONT.area, anchor: 'middle', kind: 'interior', tri });
        }
        if (step >= 4) {
            const p1 = areaLabelPos(L, 1);
            const p2 = areaLabelPos(L, 2);
            labels.push({ id: 'area1', x: p1.x, y: p1.y, text: `A₁ = ${fmt(knownTri === 1 ? known : unknown)}`, size: TRI_FONT.area, anchor: 'middle', kind: 'interior', tri: [{ x: ax1, y: ay1 }, { x: bx1, y: baseY }, { x: bx2, y: baseY }] });
            labels.push({ id: 'area2', x: p2.x, y: p2.y, text: `A₂ = ${fmt(knownTri === 2 ? known : unknown)}`, size: TRI_FONT.area, anchor: 'middle', kind: 'interior', tri: [{ x: ax2, y: ay2 }, { x: bx1, y: baseY }, { x: bx2, y: baseY }] });
        }
    } else if (config === 'baseOpposite') {
        const data = { b1: sliders.b, b2: sliders.b, h1: sliders.h1, h2: sliders.h2 };
        const L = baseOppositeLayout(data);
        const { midX, baseY, bx1, bx2, ay1, ay2, bPx } = L;
        const sideX = midX + Math.max(78, bPx * 0.12 + 40);
        const k = knownTri;
        if (step >= 2 && step < 4) {
            const pk = areaLabelPosOpposite(L, k);
            labels.push({ id: 'area-known', x: sideX, y: pk.y, text: `A${k} = ${fmt(known)}`, size: TRI_FONT.area, anchor: 'start', kind: 'exterior' });
        }
        if (step >= 4) {
            const p1 = areaLabelPosOpposite(L, 1);
            const p2 = areaLabelPosOpposite(L, 2);
            labels.push({ id: 'area1', x: sideX, y: p1.y, text: `A₁ = ${fmt(knownTri === 1 ? known : unknown)}`, size: TRI_FONT.area, anchor: 'start', kind: 'exterior' });
            labels.push({ id: 'area2', x: sideX, y: p2.y, text: `A₂ = ${fmt(knownTri === 2 ? known : unknown)}`, size: TRI_FONT.area, anchor: 'start', kind: 'exterior' });
        }
    }
    return { labels };
}

// ── paraSim layout ──

const FIT_PAD = 28;
const SCALE = 0.74;
const CENTER = { x: 0.25, y: 0 };
const PARA_FONT = { dim: 17, vertex: 17, vertexFocus: 19, annotation: 15 };

function lineIntersect(p1, p2, p3, p4) {
    const [x1, y1] = p1;
    const [x2, y2] = p2;
    const [x3, y3] = p3;
    const [x4, y4] = p4;
    const denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4);
    const t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom;
    return [x1 + t * (x2 - x1), y1 + t * (y2 - y1)];
}

function computeRaw(tE, tB) {
    const C = [-4, -2];
    const D = [-2, 2];
    const F = [4.5, -2];
    const dcX = D[0] - C[0];
    const dcY = D[1] - C[1];
    const B = [C[0] + tB * (F[0] - C[0]), -2];
    const A = [B[0] + dcX, B[1] + dcY];
    const E = [D[0] + tE * (A[0] - D[0]), 2];
    const G = lineIntersect(A, B, E, F);
    const H = lineIntersect(D, B, C, G);
    return { C, D, B, A, E, F, G, H };
}

function refToDisplay(pt) {
    return { x: (pt[0] - CENTER.x) * SCALE, y: -(pt[1] - CENTER.y) * SCALE };
}

function buildSvgPoints(raw) {
    const entries = Object.entries(raw);
    const disp = entries.map(([k, pt]) => [k, refToDisplay(pt)]);
    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    disp.forEach(([, p]) => {
        minX = Math.min(minX, p.x); maxX = Math.max(maxX, p.x);
        minY = Math.min(minY, p.y); maxY = Math.max(maxY, p.y);
    });
    const cw = maxX - minX || 1;
    const ch = maxY - minY || 1;
    const s = Math.min((VB.w - 2 * FIT_PAD) / cw, (VB.h - 2 * FIT_PAD) / ch);
    const cx = (minX + maxX) / 2;
    const cy = (minY + maxY) / 2;
    const pts = {};
    disp.forEach(([k, p]) => {
        pts[k] = { x: VB.w / 2 + (p.x - cx) * s, y: VB.h / 2 + (p.y - cy) * s };
    });
    return { pts, scale: s };
}

function dist(a, b) {
    return Math.hypot(b[0] - a[0], b[1] - a[1]);
}

function computeLabelOffsets(pts, mode, step = 0) {
    const keys = Object.keys(pts);
    const cx = keys.reduce((s, k) => s + pts[k].x, 0) / keys.length;
    const cy = keys.reduce((s, k) => s + pts[k].y, 0) / keys.length;
    const extra = {
        D: { dx: -4, dy: -8, margin: 26 },
        E: { dx: 0, dy: -10, margin: 28 },
        A: { dx: 8, dy: -8, margin: 26 },
        C: { dx: -10, dy: 8, margin: 28 },
        B: { dx: 0, dy: 12, margin: 28 },
        F: { dx: 10, dy: 8, margin: 26 },
        G: { dx: 18, dy: -20, margin: 32 },
        H: { dx: -22, dy: -24, margin: 34 },
    };
    if (mode === 'bowtie-cdh') {
        extra.H = { dx: -26, dy: -30, margin: 38 };
        extra.G = { dx: 20, dy: 14, margin: 30 };
        extra.D = { dx: -12, dy: -10, margin: 28 };
    }
    if (mode === 'bowtie-eag') {
        extra.G = { dx: -12, dy: 18, margin: 22 };
        extra.E = { dx: -8, dy: -14, margin: 28 };
        extra.F = { dx: 12, dy: 10, margin: 28 };
    }
    if (mode === 'common-angle') {
        extra.C = { dx: -32, dy: -16, margin: 36 };
        extra.H = { dx: -18, dy: 10, margin: 28 };
        extra.G = { dx: 14, dy: 8, margin: 26 };
    }
    if (step >= 3) {
        if (mode === 'bowtie-eag') {
            extra.E = { dx: -8, dy: -20, margin: 26 };
            extra.A = { dx: 8, dy: -20, margin: 26 };
            extra.G = { dx: 0, dy: -34, margin: 0 };
            extra.B = { dx: -6, dy: 16, margin: 26 };
            extra.F = { dx: 8, dy: 16, margin: 26 };
        }
        if (mode === 'bowtie-cdh') {
            extra.H = { dx: -6, dy: -36, margin: 0 };
            extra.D = { dx: -12, dy: -18, margin: 28 };
            extra.C = { dx: -10, dy: -14, margin: 28 };
            extra.G = { dx: 8, dy: 14, margin: 26 };
            extra.B = { dx: 6, dy: 16, margin: 26 };
        }
        if (mode === 'common-angle') {
            extra.C = { dx: -24, dy: -36, margin: 0 };
            extra.H = { dx: -14, dy: 10, margin: 28 };
            extra.G = { dx: 12, dy: 10, margin: 26 };
            extra.F = { dx: 10, dy: 12, margin: 26 };
            extra.B = { dx: 0, dy: 14, margin: 28 };
        }
    }
    if (step >= 4) {
        if (mode === 'bowtie-eag') {
            extra.G = { dx: 2, dy: -46, margin: 0 };
            extra.E = { dx: -10, dy: -22, margin: 30 };
            extra.A = { dx: 10, dy: -22, margin: 30 };
            extra.F = { dx: 10, dy: 18, margin: 32 };
        }
        if (mode === 'bowtie-cdh') {
            extra.H = { dx: -8, dy: -48, margin: 0 };
            extra.D = { dx: -14, dy: -12, margin: 32 };
            extra.C = { dx: -12, dy: -16, margin: 30 };
        }
        if (mode === 'common-angle') {
            extra.C = { dx: -42, dy: -58, margin: 0 };
            extra.H = { dx: -20, dy: 12, margin: 30 };
            extra.G = { dx: 14, dy: 12, margin: 28 };
        }
    }
    const offsets = {};
    keys.forEach((k) => {
        const p = pts[k];
        const e = extra[k] || { dx: 0, dy: 0, margin: 20 };
        let vx = p.x - cx + e.dx * 0.3;
        let vy = p.y - cy + e.dy * 0.3;
        const vlen = Math.hypot(vx, vy) || 1;
        vx /= vlen;
        vy /= vlen;
        offsets[k] = { dx: vx * e.margin + e.dx, dy: vy * e.margin + e.dy };
    });
    return offsets;
}

function segmentBracketLabelPos(p1, p2, offset, labelNudge = 0) {
    const mx = (p1.x + p2.x) / 2;
    const my = (p1.y + p2.y) / 2;
    const dx = p2.x - p1.x;
    const dy = p2.y - p1.y;
    const len = Math.hypot(dx, dy) || 1;
    const nx = -dy / len;
    const ny = dx / len;
    const tx = dx / len;
    const ty = dy / len;
    const labelDist = Math.abs(offset) + 42;
    return { x: mx + nx * labelDist + tx * labelNudge, y: my + ny * labelDist + ty * labelNudge };
}

function collectParaLabels(mode, step, tE, tB) {
    const raw = computeRaw(tE, tB);
    const { pts } = buildSvgPoints(raw);
    const labels = [];

    if (mode === 'bowtie-eag') {
        if (step >= 1) {
            const cEag = nudgeToInterior(triLabelPoint(pts.E, pts.A, pts.G, 0.44, 0.44, 0.12), pts.E, pts.A, pts.G);
            const cGbf = nudgeToInterior(triLabelPoint(pts.G, pts.B, pts.F, 0.12, 0.44, 0.44), pts.G, pts.B, pts.F);
            labels.push({ id: 'EA', x: cEag.x, y: cEag.y, text: 'EA ≈ 1.50', size: PARA_FONT.dim, anchor: 'middle', kind: 'interior', tri: [pts.E, pts.A, pts.G] });
            labels.push({ id: 'BF', x: cGbf.x, y: cGbf.y, text: 'BF ≈ 1.50', size: PARA_FONT.dim, anchor: 'middle', kind: 'interior', tri: [pts.G, pts.B, pts.F] });
        }
    } else if (mode === 'bowtie-cdh') {
        if (step >= 1) {
            const cCdh = nudgeToInterior(triLabelPoint(pts.C, pts.D, pts.H, 0.40, 0.40, 0.20), pts.C, pts.D, pts.H);
            const cGbh = nudgeToInterior(triLabelPoint(pts.G, pts.B, pts.H, 0.20, 0.40, 0.40), pts.G, pts.B, pts.H);
            labels.push({ id: 'CD', x: cCdh.x, y: cCdh.y, text: 'CD ≈ 1.50', size: PARA_FONT.dim, anchor: 'middle', kind: 'interior', tri: [pts.C, pts.D, pts.H] });
            labels.push({ id: 'GB', x: cGbh.x, y: cGbh.y, text: 'GB ≈ 1.50', size: PARA_FONT.dim, anchor: 'middle', kind: 'interior', tri: [pts.G, pts.B, pts.H] });
        }
        if (step === 2) {
            labels.push({ id: 'ann-H', x: pts.H.x - 68, y: pts.H.y - 50, text: 'bowtie at H', size: PARA_FONT.annotation, anchor: 'end', kind: 'exterior' });
        }
    } else if (mode === 'common-angle') {
        if (step >= 3) {
            const cChb = nudgeToInterior(triCentroid(pts.C, pts.H, pts.B), pts.C, pts.H, pts.B);
            const cCgf = nudgeToInterior(triCentroid(pts.C, pts.G, pts.F), pts.C, pts.G, pts.F);
            labels.push({ id: 'HB', x: cChb.x, y: cChb.y, text: 'HB ≈ 1.50', size: PARA_FONT.dim, anchor: 'middle', kind: 'interior', tri: [pts.C, pts.H, pts.B] });
            labels.push({ id: 'GF', x: cCgf.x, y: cCgf.y, text: 'GF ≈ 1.50', size: PARA_FONT.dim, anchor: 'middle', kind: 'interior', tri: [pts.C, pts.G, pts.F] });
        }
        if (step === 1) {
            labels.push({ id: 'ann-C', x: pts.C.x - 72, y: pts.C.y - 44, text: '∠GCB common', size: PARA_FONT.annotation, anchor: 'end', kind: 'exterior' });
        }
    }

    const offsets = computeLabelOffsets(pts, mode, step);
    Object.entries(pts).forEach(([k, p]) => {
        const o = offsets[k] || { dx: 0, dy: 0 };
        labels.push({ id: `vertex-${k}`, x: p.x, y: p.y, dx: o.dx, dy: o.dy, text: k, size: PARA_FONT.vertexFocus, anchor: 'middle', kind: 'exterior' });
    });

    return { labels };
}

// ── Validation ──

function triEdges(tri) {
    const [a, b, c] = tri;
    return [{ a, b }, { a: b, b: c }, { a: c, b: a }];
}

function validateScenario(tab, mode, step, corner, { labels }) {
    const failures = [];
    const nonVertex = labels.filter((l) => !l.id.startsWith('vertex-'));

    labels.forEach((lab) => {
        const bb = estimateLabelBBox(lab.x, lab.y, lab.text, lab.size, lab.anchor, lab.dx || 0, lab.dy || 0);
        const center = { x: (bb.left + bb.right) / 2, y: (bb.top + bb.bottom) / 2 };

        if (lab.kind === 'interior' && lab.tri) {
            const edges = triEdges(lab.tri);
            const minEdge = Math.min(...edges.map((e) => minDistToSegment(center, e.a, e.b)));
            if (!pointInTri(center, lab.tri[0], lab.tri[1], lab.tri[2])) {
                failures.push({ tab, mode, step, corner, labelId: lab.id, failureType: 'interior-outside', suggestion: 'move inside triangle' });
            } else if (minEdge < 10) {
                failures.push({ tab, mode, step, corner, labelId: lab.id, failureType: 'interior-too-close', suggestion: 'nudge toward centroid', minEdge });
            }
        }

        if (lab.kind === 'exterior' && lab.emphasis) {
            lab.emphasis.forEach((seg, i) => {
                if (segmentIntersectsBBox(seg.a, seg.b, bb, 2)) {
                    failures.push({ tab, mode, step, corner, labelId: lab.id, failureType: 'emphasis-overlap', suggestion: `avoid emphasis ${i}` });
                }
            });
        }
    });

    for (let i = 0; i < nonVertex.length; i++) {
        for (let j = i + 1; j < nonVertex.length; j++) {
            const bbi = estimateLabelBBox(nonVertex[i].x, nonVertex[i].y, nonVertex[i].text, nonVertex[i].size, nonVertex[i].anchor, nonVertex[i].dx || 0, nonVertex[i].dy || 0);
            const bbj = estimateLabelBBox(nonVertex[j].x, nonVertex[j].y, nonVertex[j].text, nonVertex[j].size, nonVertex[j].anchor, nonVertex[j].dx || 0, nonVertex[j].dy || 0);
            if (bboxGap(bbi, bbj) < LABEL_GAP) {
                failures.push({ tab, mode, step, corner, labelId: `${nonVertex[i].id}+${nonVertex[j].id}`, failureType: 'label-label-overlap', suggestion: 'separate labels' });
            }
        }
    }

    return failures;
}

// ── Audit matrix ──

const TRI_CORNERS = {
    min: { b1: 70, b2: 70, h: 120, b: 140, h1: 60, h2: 60 },
    default: { b1: 120, b2: 90, h: 200, b: 220, h1: 130, h2: 95 },
    max: { b1: 180, b2: 180, h: 280, b: 280, h1: 180, h2: 180 },
};

const PARA_CORNERS = {
    min: { te: 0.15, tb: 0.20 },
    default: { te: 0.70, tb: 59 / 85 },
    max: { te: 0.85, tb: 0.80 },
};

const failures = [];
let scenarioCount = 0;

for (const corner of ['min', 'default', 'max']) {
    for (let step = 0; step < 5; step++) {
        for (const config of ['height', 'baseSame', 'baseOpposite']) {
            scenarioCount++;
            const sliders = TRI_CORNERS[corner];
            const result = collectTriLabels(config, step, sliders);
            failures.push(...validateScenario('triSim', config, step, corner, result));
        }
    }
}

for (const corner of ['min', 'default', 'max']) {
    for (let step = 0; step < 5; step++) {
        for (const mode of ['bowtie-eag', 'bowtie-cdh', 'common-angle']) {
            scenarioCount++;
            const { te, tb } = PARA_CORNERS[corner];
            const result = collectParaLabels(mode, step, te, tb);
            failures.push(...validateScenario('paraSim', mode, step, corner, result));
        }
    }
}

console.log(`Label overlap audit: ${scenarioCount} scenarios checked`);

if (failures.length === 0) {
    console.log('PASS — 0 failures');
    process.exit(0);
}

console.log(`FAIL — ${failures.length} issue(s):\n`);
const grouped = new Map();
failures.forEach((f) => {
    const key = `${f.tab}|${f.mode}|step${f.step}|${f.corner}|${f.labelId}|${f.failureType}`;
    if (!grouped.has(key)) grouped.set(key, f);
});

grouped.forEach((f) => {
    console.log(`  [${f.tab}] ${f.mode} step ${f.step + 1} (${f.corner}) — ${f.labelId}: ${f.failureType} → ${f.suggestion}`);
});

process.exit(1);
