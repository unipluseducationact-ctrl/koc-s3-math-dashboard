window.JM24_GAME_EXTRA = {
  rules: [
    {
      id: "rules-q4",
      questionEn: "Simplify x⁵ ÷ x².",
      questionZh: "化簡 x⁵ ÷ x²。",
      choices: [
        { textEn: "x³", textZh: "x³", correct: true },
        { textEn: "x⁷", textZh: "x⁷", correct: false },
        { textEn: "x²·⁵", textZh: "x²·⁵", correct: false },
        { textEn: "x¹⁰", textZh: "x¹⁰", correct: false },
      ],
      whyEn: "Quotient rule: x⁵ ÷ x² = x⁵⁻² = x³. Subtract the indices; do not multiply or divide them.",
      whyZh: "商定律：x⁵ ÷ x² = x⁵⁻² = x³。指數相減，不要相乘或相除。",
    },
    {
      id: "rules-q5",
      questionEn: "Simplify (x²)³.",
      questionZh: "化簡 (x²)³。",
      choices: [
        { textEn: "x⁶", textZh: "x⁶", correct: true },
        { textEn: "x⁵", textZh: "x⁵", correct: false },
        { textEn: "x⁸", textZh: "x⁸", correct: false },
        { textEn: "x⁹", textZh: "x⁹", correct: false },
      ],
      whyEn: "Power of a power: (x²)³ = x^(2×3) = x⁶. Multiply the indices.",
      whyZh: "冪的冪：(x²)³ = x^(2×3) = x⁶。指數相乘。",
    },
    {
      id: "rules-q6",
      questionEn: "Evaluate 2⁻³.",
      questionZh: "求 2⁻³ 的值。",
      choices: [
        { textEn: "1/8", textZh: "1/8", correct: true },
        { textEn: "8", textZh: "8", correct: false },
        { textEn: "-8", textZh: "-8", correct: false },
        { textEn: "1/6", textZh: "1/6", correct: false },
      ],
      whyEn: "Negative index: 2⁻³ = 1 / 2³ = 1/8. The minus sign is not a minus in front of the number.",
      whyZh: "負指數：2⁻³ = 1 / 2³ = 1/8。負號不是把答案變成負數。",
    },
    {
      id: "rules-q7",
      questionEn: "Evaluate x⁰ (x ≠ 0).",
      questionZh: "求 x⁰ 的值（x ≠ 0）。",
      choices: [
        { textEn: "1", textZh: "1", correct: true },
        { textEn: "0", textZh: "0", correct: false },
        { textEn: "x", textZh: "x", correct: false },
        { textEn: "Undefined", textZh: "無意義", correct: false },
      ],
      whyEn: "Zero exponent: x⁰ = 1 when x ≠ 0. Only 0⁰ is undefined.",
      whyZh: "零指數：當 x ≠ 0 時，x⁰ = 1。只有 0⁰ 無意義。",
    },
    {
      id: "rules-q8",
      questionEn: "Simplify 8ⁿ × 2.",
      questionZh: "化簡 8ⁿ × 2。",
      choices: [
        { textEn: "2³ⁿ⁺¹", textZh: "2³ⁿ⁺¹", correct: true },
        { textEn: "16ⁿ", textZh: "16ⁿ", correct: false },
        { textEn: "2³ⁿ", textZh: "2³ⁿ", correct: false },
        { textEn: "8ⁿ⁺²", textZh: "8ⁿ⁺²", correct: false },
      ],
      whyEn: "8 = 2³, so 8ⁿ × 2 = (2³)ⁿ × 2¹ = 2³ⁿ × 2 = 2³ⁿ⁺¹.",
      whyZh: "8 = 2³，所以 8ⁿ × 2 = (2³)ⁿ × 2¹ = 2³ⁿ × 2 = 2³ⁿ⁺¹。",
    },
  ],
  "scientific-notation": [
    {
      id: "sci-q4",
      questionEn: "Write 0.000562 in standard form.",
      questionZh: "將 0.000562 寫成標準式。",
      choices: [
        { textEn: "5.62 × 10⁻⁴", textZh: "5.62 × 10⁻⁴", correct: true },
        { textEn: "5.62 × 10⁴", textZh: "5.62 × 10⁴", correct: false },
        { textEn: "56.2 × 10⁻⁵", textZh: "56.2 × 10⁻⁵", correct: false },
        { textEn: "0.562 × 10⁻³", textZh: "0.562 × 10⁻³", correct: false },
      ],
      whyEn: "Move the decimal 4 places right until one non-zero digit is in front: 0.000562 = 5.62 × 10⁻⁴.",
      whyZh: "小數點向右移 4 位，直到前面只剩一個非零數字：0.000562 = 5.62 × 10⁻⁴。",
    },
    {
      id: "sci-q5",
      questionEn: "Evaluate (2 × 10¹²)(6 × 10⁹).",
      questionZh: "計算 (2 × 10¹²)(6 × 10⁹)。",
      choices: [
        { textEn: "1.2 × 10²²", textZh: "1.2 × 10²²", correct: true },
        { textEn: "12 × 10²¹", textZh: "12 × 10²¹", correct: false },
        { textEn: "8 × 10²¹", textZh: "8 × 10²¹", correct: false },
        { textEn: "1.2 × 10²¹", textZh: "1.2 × 10²¹", correct: false },
      ],
      whyEn: "Multiply coefficients 2 × 6 = 12 and add indices 12 + 9 = 21. Then 12 × 10²¹ = 1.2 × 10²².",
      whyZh: "係數 2 × 6 = 12，指數 12 + 9 = 21。再寫成標準式：12 × 10²¹ = 1.2 × 10²²。",
    },
    {
      id: "sci-q6",
      questionEn: "Evaluate 3 × 10⁹ + 2 × 10¹⁰.",
      questionZh: "計算 3 × 10⁹ + 2 × 10¹⁰。",
      choices: [
        { textEn: "2.3 × 10¹⁰", textZh: "2.3 × 10¹⁰", correct: true },
        { textEn: "5 × 10¹⁹", textZh: "5 × 10¹⁹", correct: false },
        { textEn: "5 × 10¹⁰", textZh: "5 × 10¹⁰", correct: false },
        { textEn: "2.3 × 10⁹", textZh: "2.3 × 10⁹", correct: false },
      ],
      whyEn: "Match the power first: 2 × 10¹⁰ = 20 × 10⁹, so 3 × 10⁹ + 20 × 10⁹ = 23 × 10⁹ = 2.3 × 10¹⁰.",
      whyZh: "先統一次方：2 × 10¹⁰ = 20 × 10⁹，所以 3 × 10⁹ + 20 × 10⁹ = 23 × 10⁹ = 2.3 × 10¹⁰。",
    },
    {
      id: "sci-q7",
      questionEn: "Which is larger: 7.2 × 10⁵ or 3.8 × 10⁶?",
      questionZh: "7.2 × 10⁵ 同 3.8 × 10⁶ 邊個較大？",
      choices: [
        { textEn: "3.8 × 10⁶", textZh: "3.8 × 10⁶", correct: true },
        { textEn: "7.2 × 10⁵", textZh: "7.2 × 10⁵", correct: false },
        { textEn: "They are equal", textZh: "兩者相等", correct: false },
        { textEn: "Cannot compare", textZh: "無法比較", correct: false },
      ],
      whyEn: "Compare the powers of 10 first. 10⁶ is 10 times 10⁵, so 3.8 × 10⁶ is larger than 7.2 × 10⁵.",
      whyZh: "先比較 10 的次方。10⁶ 是 10⁵ 的 10 倍，所以 3.8 × 10⁶ 較大。",
    },
    {
      id: "sci-q8",
      questionEn: "Write 4560 in standard form.",
      questionZh: "將 4560 寫成標準式。",
      choices: [
        { textEn: "4.56 × 10³", textZh: "4.56 × 10³", correct: true },
        { textEn: "45.6 × 10²", textZh: "45.6 × 10²", correct: false },
        { textEn: "4.56 × 10²", textZh: "4.56 × 10²", correct: false },
        { textEn: "456 × 10¹", textZh: "456 × 10¹", correct: false },
      ],
      whyEn: "Move the decimal 3 places left: 4560 = 4.56 × 10³. The coefficient must satisfy 1 ≤ a < 10.",
      whyZh: "小數點向左移 3 位：4560 = 4.56 × 10³。係數必須滿足 1 ≤ a < 10。",
    },
  ],
  binary: [
    {
      id: "bin-q4",
      questionEn: "Convert 1101₂ to decimal.",
      questionZh: "將 1101₂ 轉換為十進制。",
      choices: [
        { textEn: "13", textZh: "13", correct: true },
        { textEn: "11", textZh: "11", correct: false },
        { textEn: "15", textZh: "15", correct: false },
        { textEn: "12", textZh: "12", correct: false },
      ],
      whyEn: "1101₂ = 1×2³ + 1×2² + 0×2¹ + 1×2⁰ = 8 + 4 + 0 + 1 = 13.",
      whyZh: "1101₂ = 1×2³ + 1×2² + 0×2¹ + 1×2⁰ = 8 + 4 + 0 + 1 = 13。",
    },
    {
      id: "bin-q5",
      questionEn: "Convert 15₁₀ to binary.",
      questionZh: "將 15₁₀ 轉換為二進制。",
      choices: [
        { textEn: "1111₂", textZh: "1111₂", correct: true },
        { textEn: "1110₂", textZh: "1110₂", correct: false },
        { textEn: "1011₂", textZh: "1011₂", correct: false },
        { textEn: "1101₂", textZh: "1101₂", correct: false },
      ],
      whyEn: "15 = 8 + 4 + 2 + 1 = 2³ + 2² + 2¹ + 2⁰, so 15₁₀ = 1111₂.",
      whyZh: "15 = 8 + 4 + 2 + 1 = 2³ + 2² + 2¹ + 2⁰，所以 15₁₀ = 1111₂。",
    },
    {
      id: "bin-q6",
      questionEn: "Evaluate 101₂ + 110₂.",
      questionZh: "計算 101₂ + 110₂。",
      choices: [
        { textEn: "1011₂", textZh: "1011₂", correct: true },
        { textEn: "1000₂", textZh: "1000₂", correct: false },
        { textEn: "111₂", textZh: "111₂", correct: false },
        { textEn: "1101₂", textZh: "1101₂", correct: false },
      ],
      whyEn: "Convert first: 101₂ = 5 and 110₂ = 6. Then 5 + 6 = 11 = 1011₂.",
      whyZh: "先轉十進制：101₂ = 5，110₂ = 6。5 + 6 = 11 = 1011₂。",
    },
    {
      id: "bin-q7",
      questionEn: "Convert 1010₂ to decimal.",
      questionZh: "將 1010₂ 轉換為十進制。",
      choices: [
        { textEn: "10", textZh: "10", correct: true },
        { textEn: "8", textZh: "8", correct: false },
        { textEn: "12", textZh: "12", correct: false },
        { textEn: "1010", textZh: "1010", correct: false },
      ],
      whyEn: "1010₂ = 1×2³ + 0×2² + 1×2¹ + 0×2⁰ = 8 + 2 = 10. Do not read the digits as a denary number.",
      whyZh: "1010₂ = 1×2³ + 0×2² + 1×2¹ + 0×2⁰ = 8 + 2 = 10。不要把二進制數字直接當成十進制。",
    },
    {
      id: "bin-q8",
      questionEn: "Convert 100000₂ to decimal.",
      questionZh: "將 100000₂ 轉換為十進制。",
      choices: [
        { textEn: "32", textZh: "32", correct: true },
        { textEn: "16", textZh: "16", correct: false },
        { textEn: "64", textZh: "64", correct: false },
        { textEn: "20", textZh: "20", correct: false },
      ],
      whyEn: "100000₂ has a 1 in the 2⁵ place: 1×2⁵ = 32.",
      whyZh: "100000₂ 的 1 在 2⁵ 位：1×2⁵ = 32。",
    },
  ],
};

window.JM24_GAME_PRESETS = [
  { id: "all", labelEn: "All", labelZh: "全部" },
  { id: "rules", labelEn: "Rules", labelZh: "指數定律" },
  { id: "scientific-notation", labelEn: "Scientific Notation", labelZh: "科學記數法" },
  { id: "binary", labelEn: "Binary", labelZh: "二進制" },
];

window.buildJM24GameBank = function buildJM24GameBank() {
  var quiz = window.JM24_COMICS_QUIZ || { rules: [], "scientific-notation": [], binary: [] };
  var extra = window.JM24_GAME_EXTRA;
  return {
    rules: (quiz.rules || []).concat(extra.rules),
    "scientific-notation": (quiz["scientific-notation"] || []).concat(extra["scientific-notation"]),
    binary: (quiz.binary || []).concat(extra.binary),
  };
};

window.tagJM24GameQuestions = function tagJM24GameQuestions(list, topic) {
  return list.map(function (question) {
    return Object.assign({}, question, { topic: topic });
  });
};

window.getJM24GameTopicLabel = function getJM24GameTopicLabel(topicId, lang) {
  var keyMap = {
    rules: "comic.rules",
    "scientific-notation": "comic.sciNotation",
    binary: "comic.binary",
  };
  var key = keyMap[topicId];
  if (key && window.I18n && typeof window.I18n.t === "function") {
    return window.I18n.t(key);
  }
  var preset = (window.JM24_GAME_PRESETS || []).find(function (p) {
    return p.id === topicId;
  });
  if (!preset) return topicId;
  return lang === "zh" ? preset.labelZh : preset.labelEn;
};

window.getJM24GameQuestions = function getJM24GameQuestions(presetId) {
  var bank = window.buildJM24GameBank();
  var tag = window.tagJM24GameQuestions;
  if (presetId === "rules") return tag(bank.rules.slice(), "rules");
  if (presetId === "scientific-notation") {
    return tag(bank["scientific-notation"].slice(), "scientific-notation");
  }
  if (presetId === "binary") return tag(bank.binary.slice(), "binary");
  return tag(bank.rules.slice(), "rules")
    .concat(tag(bank["scientific-notation"].slice(), "scientific-notation"))
    .concat(tag(bank.binary.slice(), "binary"));
};
