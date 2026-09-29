/* JM24 Indices Space Shooter: randomised question bank.
 * Every round mixes many question types with fresh numbers and letters.
 * Question / explanation strings use \( ... \) for KaTeX; choice `tex` is raw TeX. */

(function () {
  var ROUND_SIZE = 15;
  var VARS = ["x", "y", "a", "m", "p", "k"];

  function rint(lo, hi) {
    return lo + Math.floor(Math.random() * (hi - lo + 1));
  }

  function pick(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i];
      a[i] = a[j];
      a[j] = t;
    }
    return a;
  }

  /** base^e with the usual simplifications (e = 1 -> base, e = 0 -> 1). */
  function pw(base, e) {
    if (e === 1) return String(base);
    if (e === 0) return "1";
    return base + "^{" + e + "}";
  }

  /** Coefficient times base^e, e.g. 6x^{5}. */
  function mono(c, v, e) {
    if (e === 0) return String(c);
    var body = pw(v, e);
    if (c === 1) return body;
    if (c === -1) return "-" + body;
    return c + body;
  }

  function frac(num, den) {
    return "\\frac{" + num + "}{" + den + "}";
  }

  function fmt(n) {
    return String(Math.round(n * 1000) / 1000);
  }

  /** Build a question; wrong candidates are de-duplicated and trimmed to three. */
  function make(o) {
    var seen = {};
    seen[o.correct] = true;
    var wrong = [];
    (o.wrong || []).forEach(function (w) {
      var key = typeof w === "string" ? w : w.tex;
      if (key == null || seen[key]) return;
      seen[key] = true;
      wrong.push(typeof w === "string" ? { tex: w } : w);
    });
    if (wrong.length < 3) return null;
    var choices = [{ tex: o.correct, texZh: o.correctZh, correct: true }].concat(
      shuffle(wrong).slice(0, 3).map(function (w) {
        return { tex: w.tex, texZh: w.texZh, correct: false };
      })
    );
    return {
      id: o.id,
      topic: o.topic || "rules",
      questionEn: o.qEn,
      questionZh: o.qZh,
      choices: choices,
      whyEn: o.whyEn,
      whyZh: o.whyZh,
    };
  }

  var T = "\\times ";
  var D = "\\div ";

  var GENERATORS = [
    function product() {
      var v = pick(VARS), a = rint(2, 9), b = rint(2, 9), s = a + b;
      var q = pw(v, a) + T + pw(v, b);
      return make({
        id: "product", qEn: "Simplify \\(" + q + "\\).", qZh: "化簡 \\(" + q + "\\)。",
        correct: pw(v, s),
        wrong: [pw(v, a * b), mono(s, v, 1), pw(v, s + 1), pw(v, Math.abs(a - b) || 1), mono(2, v, s)],
        whyEn: "Same base, multiplying: add the indices. \\(" + q + "=" + v + "^{" + a + "+" + b + "}=" + pw(v, s) + "\\).",
        whyZh: "底數相同，相乘時指數相加：\\(" + q + "=" + v + "^{" + a + "+" + b + "}=" + pw(v, s) + "\\)。",
      });
    },
    function productCoef() {
      var v = pick(VARS), c1 = rint(2, 6), c2 = rint(2, 6), a = rint(2, 7), b = rint(2, 7);
      var q = "(" + mono(c1, v, a) + ")(" + mono(c2, v, b) + ")";
      return make({
        id: "product-coef", qEn: "Simplify \\(" + q + "\\).", qZh: "化簡 \\(" + q + "\\)。",
        correct: mono(c1 * c2, v, a + b),
        wrong: [mono(c1 + c2, v, a + b), mono(c1 * c2, v, a * b), mono(c1 + c2, v, a * b), mono(c1 * c2, v, a + b + 1)],
        whyEn: "Multiply the numbers, add the indices: \\(" + c1 + T + c2 + "=" + c1 * c2 + "\\) and \\(" + a + "+" + b + "=" + (a + b) + "\\).",
        whyZh: "係數相乘，指數相加：\\(" + c1 + T + c2 + "=" + c1 * c2 + "\\)，\\(" + a + "+" + b + "=" + (a + b) + "\\)。",
      });
    },
    function quotient() {
      var v = pick(VARS), a = rint(6, 12), b = rint(2, a - 1), d = a - b;
      var q = pw(v, a) + D + pw(v, b);
      var w = [pw(v, a + b), pw(v, a * b), pw(v, b - a), pw(v, d + 1)];
      if (a % b === 0) w.push(pw(v, a / b));
      return make({
        id: "quotient", qEn: "Simplify \\(" + q + "\\).", qZh: "化簡 \\(" + q + "\\)。",
        correct: pw(v, d), wrong: w,
        whyEn: "Same base, dividing: subtract the indices. \\(" + q + "=" + v + "^{" + a + "-" + b + "}=" + pw(v, d) + "\\).",
        whyZh: "底數相同，相除時指數相減：\\(" + q + "=" + v + "^{" + a + "-" + b + "}=" + pw(v, d) + "\\)。",
      });
    },
    function quotientCoef() {
      var v = pick(VARS), c2 = rint(2, 5), k = rint(2, 6), c1 = c2 * k, a = rint(5, 10), b = rint(1, a - 1);
      var q = frac(mono(c1, v, a), mono(c2, v, b));
      return make({
        id: "quotient-coef", qEn: "Simplify \\(" + q + "\\).", qZh: "化簡 \\(" + q + "\\)。",
        correct: mono(k, v, a - b),
        wrong: [mono(k, v, a + b), mono(c1 - c2, v, a - b), mono(c1 - c2, v, a + b), mono(k, v, a * b)],
        whyEn: "Divide the numbers, subtract the indices: \\(" + c1 + D + c2 + "=" + k + "\\) and \\(" + a + "-" + b + "=" + (a - b) + "\\).",
        whyZh: "係數相除，指數相減：\\(" + c1 + D + c2 + "=" + k + "\\)，\\(" + a + "-" + b + "=" + (a - b) + "\\)。",
      });
    },
    function powerOfPower() {
      var v = pick(VARS), a = rint(2, 6), b = rint(2, 5);
      var q = "(" + pw(v, a) + ")^{" + b + "}";
      return make({
        id: "power-power", qEn: "Simplify \\(" + q + "\\).", qZh: "化簡 \\(" + q + "\\)。",
        correct: pw(v, a * b),
        wrong: [pw(v, a + b), pw(v, a * b + 1), mono(b, v, a), pw(v, a * b - 1)],
        whyEn: "Power of a power: multiply the indices. \\(" + q + "=" + v + "^{" + a + T + b + "}=" + pw(v, a * b) + "\\).",
        whyZh: "冪的冪，指數相乘：\\(" + q + "=" + v + "^{" + a + T + b + "}=" + pw(v, a * b) + "\\)。",
      });
    },
    function powerOfProduct() {
      var v = pick(VARS), k = rint(2, 4), a = rint(1, 4), n = rint(2, 3), kn = Math.pow(k, n);
      var q = "(" + mono(k, v, a) + ")^{" + n + "}";
      return make({
        id: "power-product", qEn: "Simplify \\(" + q + "\\).", qZh: "化簡 \\(" + q + "\\)。",
        correct: mono(kn, v, a * n),
        wrong: [mono(k, v, a * n), mono(k * n, v, a * n), mono(kn, v, a + n), mono(k * n, v, a + n)],
        whyEn: "Raise every factor to the power: \\(" + q + "=" + k + "^{" + n + "}" + T + pw(v, a * n) + "=" + mono(kn, v, a * n) + "\\).",
        whyZh: "每個因子都要乘方：\\(" + q + "=" + k + "^{" + n + "}" + T + pw(v, a * n) + "=" + mono(kn, v, a * n) + "\\)。",
      });
    },
    function powerOfFraction() {
      var pair = pick([["x", "y"], ["a", "b"], ["m", "n"], ["p", "q"]]);
      var u = pair[0], w = pair[1], a = rint(1, 3), n = rint(2, 4);
      var q = "\\left(" + frac(pw(u, a), w) + "\\right)^{" + n + "}";
      return make({
        id: "power-fraction", qEn: "Simplify \\(" + q + "\\).", qZh: "化簡 \\(" + q + "\\)。",
        correct: frac(pw(u, a * n), pw(w, n)),
        wrong: [frac(pw(u, a * n), w), frac(pw(u, a), pw(w, n)), frac(pw(u, a + n), pw(w, n)), frac(mono(n, u, a), n + w)],
        whyEn: "Raise the top and the bottom to the power: \\(" + q + "=" + frac(pw(u, a * n), pw(w, n)) + "\\).",
        whyZh: "分子和分母都要乘方：\\(" + q + "=" + frac(pw(u, a * n), pw(w, n)) + "\\)。",
      });
    },
    function zeroIndex() {
      var v = pick(VARS), c = rint(2, 9), kind = rint(0, 3);
      var undef = { tex: "\\text{Undefined}", texZh: "\\text{無意義}" };
      if (kind === 0) {
        var n = rint(2, 99);
        return make({
          id: "zero-num", qEn: "Evaluate \\(" + n + "^{0}\\).", qZh: "求 \\(" + n + "^{0}\\) 的值。",
          correct: "1", wrong: ["0", String(n), undef],
          whyEn: "Any non-zero number to the power 0 is 1.", whyZh: "任何非零數的 0 次方都是 1。",
        });
      }
      if (kind === 1) {
        return make({
          id: "zero-coef", qEn: "Simplify \\(" + c + v + "^{0}\\) (\\(" + v + "\\neq 0\\)).",
          qZh: "化簡 \\(" + c + v + "^{0}\\)（\\(" + v + "\\neq 0\\)）。",
          correct: String(c), wrong: ["1", "0", c + v],
          whyEn: "Only \\(" + v + "\\) has the power 0: \\(" + c + v + "^{0}=" + c + T + "1=" + c + "\\).",
          whyZh: "只有 \\(" + v + "\\) 是 0 次方：\\(" + c + v + "^{0}=" + c + T + "1=" + c + "\\)。",
        });
      }
      if (kind === 2) {
        return make({
          id: "zero-bracket", qEn: "Simplify \\((" + c + v + ")^{0}\\) (\\(" + v + "\\neq 0\\)).",
          qZh: "化簡 \\((" + c + v + ")^{0}\\)（\\(" + v + "\\neq 0\\)）。",
          correct: "1", wrong: [String(c), "0", c + v],
          whyEn: "The whole bracket has the power 0, so it equals 1.", whyZh: "整個括號是 0 次方，所以等於 1。",
        });
      }
      var a = rint(2, 9);
      return make({
        id: "zero-quotient", qEn: "Simplify \\(" + pw(v, a) + D + pw(v, a) + "\\).",
        qZh: "化簡 \\(" + pw(v, a) + D + pw(v, a) + "\\)。",
        correct: "1", wrong: ["0", v, pw(v, 2 * a)],
        whyEn: "\\(" + pw(v, a) + D + pw(v, a) + "=" + v + "^{0}=1\\) (for \\(" + v + "\\neq 0\\)).",
        whyZh: "\\(" + pw(v, a) + D + pw(v, a) + "=" + v + "^{0}=1\\)（\\(" + v + "\\neq 0\\)）。",
      });
    },
    function negativeEvaluate() {
      var opts = [[2, 2], [2, 3], [2, 4], [2, 5], [3, 2], [3, 3], [4, 2], [5, 2], [10, 2], [10, 3]];
      var o = pick(opts), b = o[0], n = o[1], val = Math.pow(b, n);
      var q = b + "^{-" + n + "}";
      return make({
        id: "neg-eval", qEn: "Evaluate \\(" + q + "\\).", qZh: "求 \\(" + q + "\\) 的值。",
        correct: frac(1, val),
        wrong: ["-" + val, "-" + frac(1, val), String(val), frac(1, b * n), "-" + b * n],
        whyEn: "A negative index means the reciprocal: \\(" + q + "=" + frac(1, b + "^{" + n + "}") + "=" + frac(1, val) + "\\).",
        whyZh: "負指數代表倒數：\\(" + q + "=" + frac(1, b + "^{" + n + "}") + "=" + frac(1, val) + "\\)。",
      });
    },
    function negativeRewrite() {
      var v = pick(VARS), a = rint(2, 9);
      if (Math.random() < 0.5) {
        return make({
          id: "neg-to", qEn: "Write \\(" + frac(1, pw(v, a)) + "\\) with a negative index.",
          qZh: "以負指數表示 \\(" + frac(1, pw(v, a)) + "\\)。",
          correct: v + "^{-" + a + "}",
          wrong: [pw(v, a), "-" + pw(v, a), v + "^{\\frac{1}{" + a + "}}", "-" + v + "^{-" + a + "}"],
          whyEn: "\\(" + frac(1, pw(v, a)) + "=" + v + "^{-" + a + "}\\).", whyZh: "\\(" + frac(1, pw(v, a)) + "=" + v + "^{-" + a + "}\\)。",
        });
      }
      var c = rint(2, 9);
      return make({
        id: "neg-from", qEn: "Write \\(" + c + v + "^{-" + a + "}\\) with a positive index.",
        qZh: "以正指數表示 \\(" + c + v + "^{-" + a + "}\\)。",
        correct: frac(c, pw(v, a)),
        wrong: [frac(1, c + pw(v, a)), "-" + c + pw(v, a), frac(pw(v, a), c), c + pw(v, a)],
        whyEn: "Only \\(" + v + "\\) has the negative index, so only \\(" + pw(v, a) + "\\) moves to the bottom.",
        whyZh: "只有 \\(" + v + "\\) 是負指數，所以只有 \\(" + pw(v, a) + "\\) 移到分母。",
      });
    },
    function negativeLaws() {
      var v = pick(VARS), a = rint(2, 7), b = rint(1, 9);
      if (b === a) b = a + 1;
      var q = v + "^{-" + a + "}" + T + pw(v, b), r = b - a;
      return make({
        id: "neg-product", qEn: "Simplify \\(" + q + "\\).", qZh: "化簡 \\(" + q + "\\)。",
        correct: pw(v, r),
        wrong: [pw(v, a + b), pw(v, -(a + b)), pw(v, -a * b), pw(v, -r)],
        whyEn: "Add the indices, keeping the sign: \\(-" + a + "+" + b + "=" + r + "\\).",
        whyZh: "指數相加，注意正負號：\\(-" + a + "+" + b + "=" + r + "\\)。",
      });
    },
    function fractionalIndex() {
      var rows = [
        [25, 1, 2, 5], [36, 1, 2, 6], [49, 1, 2, 7], [8, 1, 3, 2], [27, 1, 3, 3], [64, 1, 3, 4],
        [16, 1, 4, 2], [81, 1, 4, 3], [8, 2, 3, 4], [27, 2, 3, 9], [16, 3, 4, 8], [4, 3, 2, 8],
        [9, 3, 2, 27], [32, 1, 5, 2],
      ];
      var r = pick(rows), base = r[0], m = r[1], n = r[2], val = r[3];
      var root = Math.round(Math.pow(base, 1 / n));
      var q = base + "^{\\frac{" + m + "}{" + n + "}}";
      var why = m === 1
        ? "\\(" + q + "=\\sqrt[" + n + "]{" + base + "}=" + val + "\\)."
        : "\\(" + q + "=(\\sqrt[" + n + "]{" + base + "})^{" + m + "}=" + root + "^{" + m + "}=" + val + "\\).";
      return make({
        id: "fractional", qEn: "Evaluate \\(" + q + "\\).", qZh: "求 \\(" + q + "\\) 的值。",
        correct: String(val),
        wrong: [fmt(base * m / n), String(val * val), String(val + 1), String(root * n), fmt(base / n)],
        whyEn: "The bottom of the fraction is the root, the top is the power. " + why,
        whyZh: "分母是開方，分子是乘方。" + why.replace(/\.$/, "。"),
      });
    },
    function solveIndex() {
      var b = pick([2, 3, 5]), maxN = b === 2 ? 7 : b === 3 ? 5 : 3, n = rint(2, maxN), val = Math.pow(b, n);
      if (Math.random() < 0.5) {
        return make({
          id: "solve-plain", qEn: "Solve \\(" + b + "^{n}=" + val + "\\).", qZh: "解 \\(" + b + "^{n}=" + val + "\\)。",
          correct: "n=" + n,
          wrong: ["n=" + (n + 1), "n=" + (n - 1), "n=" + val / b, "n=" + 2 * n],
          whyEn: "\\(" + val + "=" + b + "^{" + n + "}\\), so \\(n=" + n + "\\).", whyZh: "\\(" + val + "=" + b + "^{" + n + "}\\)，所以 \\(n=" + n + "\\)。",
        });
      }
      var p = rint(2, 6), s = p + n;
      var q = b + "^{" + p + "}" + T + b + "^{n}=" + b + "^{" + s + "}";
      return make({
        id: "solve-product", qEn: "Solve \\(" + q + "\\).", qZh: "解 \\(" + q + "\\)。",
        correct: "n=" + n,
        wrong: ["n=" + (s + p), "n=" + (n + 1), "n=" + p, "n=" + s],
        whyEn: "Add the indices: \\(" + p + "+n=" + s + "\\), so \\(n=" + n + "\\).", whyZh: "指數相加：\\(" + p + "+n=" + s + "\\)，所以 \\(n=" + n + "\\)。",
      });
    },
    function sameBase() {
      var o = pick([[2, 2, 4], [2, 3, 8], [3, 2, 9], [2, 4, 16], [3, 3, 27]]);
      var b = o[0], k = o[1], big = o[2];
      var q = pw(big, "n") + T + b;
      var ans = b + "^{" + k + "n+1}";
      return make({
        id: "same-base", qEn: "Write \\(" + q + "\\) as a power of " + b + ".", qZh: "將 \\(" + q + "\\) 寫成 " + b + " 的次方。",
        correct: ans,
        wrong: [(big * b) + "^{n}", b + "^{" + k + "n}", big + "^{n+1}", b + "^{n+" + (k + 1) + "}"],
        whyEn: "\\(" + big + "=" + b + "^{" + k + "}\\), so \\(" + q + "=" + b + "^{" + k + "n}" + T + b + "^{1}=" + ans + "\\).",
        whyZh: "\\(" + big + "=" + b + "^{" + k + "}\\)，所以 \\(" + q + "=" + b + "^{" + k + "n}" + T + b + "^{1}=" + ans + "\\)。",
      });
    },
    function sciMultiply() {
      var m = rint(2, 8), n = rint(2, 8), a, b, coef, e;
      if (Math.random() < 0.5) {
        a = rint(2, 4); b = rint(2, Math.floor(9 / a)); coef = a * b; e = m + n;
      } else {
        var big = pick([[4, 5, 2], [5, 6, 3], [5, 8, 4], [2, 5, 1], [6, 5, 3]]);
        a = big[0]; b = big[1]; coef = big[2]; e = m + n + 1;
      }
      var q = "(" + a + T + "10^{" + m + "})" + T + "(" + b + T + "10^{" + n + "})";
      var sci = function (c, p) { return c + T + "10^{" + p + "}"; };
      return make({
        id: "sci-multiply", topic: "scientific-notation",
        qEn: "Give \\(" + q + "\\) in scientific notation.", qZh: "以科學記數法表示 \\(" + q + "\\)。",
        correct: sci(coef, e),
        wrong: [sci(coef, m * n), sci(a + b, m + n), sci(coef, e - 1), sci(coef, e + 1)],
        whyEn: "Multiply \\(" + a + T + b + "=" + a * b + "\\) and add the indices; then make sure \\(1\\le a<10\\).",
        whyZh: "先算 \\(" + a + T + b + "=" + a * b + "\\)，再把指數相加，最後確保 \\(1\\le a<10\\)。",
      });
    },
    function sciDivide() {
      var b = rint(2, 4), k = rint(2, Math.floor(9 / b)), a = b * k, m = rint(6, 12), n = rint(2, m - 2);
      var q = frac(a + T + "10^{" + m + "}", b + T + "10^{" + n + "}");
      var sci = function (c, p) { return c + T + "10^{" + p + "}"; };
      return make({
        id: "sci-divide", topic: "scientific-notation",
        qEn: "Give \\(" + q + "\\) in scientific notation.", qZh: "以科學記數法表示 \\(" + q + "\\)。",
        correct: sci(k, m - n),
        wrong: [sci(k, m + n), sci(a - b, m - n), sci(k, n - m), sci(a * b, m - n)],
        whyEn: "Divide \\(" + a + D + b + "=" + k + "\\) and subtract the indices: \\(" + m + "-" + n + "=" + (m - n) + "\\).",
        whyZh: "先算 \\(" + a + D + b + "=" + k + "\\)，再把指數相減：\\(" + m + "-" + n + "=" + (m - n) + "\\)。",
      });
    },
    function binaryToDenary() {
      var val = rint(17, 31), bits = val.toString(2);
      var flips = shuffle([0, 1, 2, 3]).map(function (i) { return String(val ^ (1 << i)); });
      var parts = [];
      for (var i = 0; i < bits.length; i++) {
        if (bits[i] === "1") parts.push("2^{" + (bits.length - 1 - i) + "}");
      }
      return make({
        id: "binary", topic: "binary",
        qEn: "Convert \\(" + bits + "_{(2)}\\) to denary.", qZh: "把 \\(" + bits + "_{(2)}\\) 化為十進制。",
        correct: String(val), wrong: flips.concat([bits]),
        whyEn: "Add the place values of the 1s: \\(" + parts.join("+") + "=" + val + "\\).",
        whyZh: "把 1 所在位值相加：\\(" + parts.join("+") + "=" + val + "\\)。",
      });
    },
  ];

  function buildRound() {
    var out = [];
    var used = {};
    var rulesGens = GENERATORS.slice(0, GENERATORS.length - 3);
    var extraGens = GENERATORS.slice(GENERATORS.length - 3);
    var plan = shuffle(rulesGens).concat(shuffle(extraGens).slice(0, 2));
    while (plan.length < ROUND_SIZE) plan = plan.concat(shuffle(rulesGens));
    plan = shuffle(plan.slice(0, ROUND_SIZE));
    plan.forEach(function (gen, idx) {
      for (var tries = 0; tries < 8; tries++) {
        var q = gen();
        if (!q || used[q.questionEn]) continue;
        used[q.questionEn] = true;
        q.id = "g" + (idx + 1) + "-" + q.id;
        out.push(q);
        return;
      }
    });
    return out;
  }

  window.JM24_GAME_PRESETS = [
    { id: "rules", labelEn: "Law of Indices", labelZh: "指數定律" },
    { id: "scientific-notation", labelEn: "Scientific Notation", labelZh: "科學記數法" },
    { id: "binary", labelEn: "Denary & Binary", labelZh: "十進制與二進制" },
  ];
  window.getJM24GameTopicLabel = function getJM24GameTopicLabel(topicId, lang) {
    if (topicId === "rules" && window.I18n && typeof window.I18n.t === "function") {
      var translated = window.I18n.t("comic.rules");
      if (translated && translated !== "comic.rules") return translated;
    }
    var preset = window.JM24_GAME_PRESETS.find(function (p) {
      return p.id === topicId;
    });
    if (!preset) return "Law of Indices";
    return lang === "zh" ? preset.labelZh : preset.labelEn;
  };

  window.getJM24GameQuestions = function getJM24GameQuestions() {
    return buildRound();
  };
})();
