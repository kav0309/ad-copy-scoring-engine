# 📊 Meta Ad Copy Scoring Engine — D2C Brands

A Python-based tool that scores real D2C brand ad copies across **6 direct-response marketing dimensions**, inspired by Meta Ad Library data.

Built as part of a performance marketing + creative strategy portfolio.

---

## 🎯 What It Does

Analyses 40 paid ad copies from 20+ D2C brands (Indē Wild, Plum, Minimalist, Yoga Bar, boAt, etc.) and scores each one algorithmically across:

| Dimension | Max Score | What It Measures |
|---|---|---|
| Hook Strength | 20 | Question openers, numbers, pattern interrupts, personalisation |
| Problem Agitation | 20 | PAS structure, pain-point language, frustration triggers |
| Offer Clarity | 20 | Price anchor, discount, shipping, risk reversal, urgency |
| CTA Strength | 15 | Specificity of call-to-action, delivery promise |
| Social Proof | 15 | Volume claims, certifications, time-bound results |
| Brand Voice | 10 | Penalises generic language, rewards personality & POV |
| **Total** | **100** | — |

---

## 📈 Key Findings

- **Conversion-stage ads score 73% higher** on average than Awareness ads (38.0 vs 21.9) — they use more concrete proof, pricing, and urgency
- **Reel format outperforms Static** (29.5 vs 23.8 avg) due to stronger hooks and storytelling structure
- The #1 scoring ad (Indē Wild Carousel, 59/100) combines a problem-aware hook, price anchor, time-bound claim, and risk reversal
- Generic brand ads scored 9–14/100 — failing on hook, proof, and brand voice simultaneously
- **Biggest gap between top and bottom ads**: Offer Clarity (avg 18 vs 0) and Brand Voice (avg 9 vs 2)

---

## 🗂️ Files

```
├── ad_copy_data.py       # 40 ad copies dataset (manually curated from Meta Ad Library)
├── scoring_engine.py     # Core scoring logic — 6 dimension scorers
├── visualise.py          # 5 matplotlib charts + CSV export
├── ad_copy_scores.csv    # Full ranked output
├── chart1_leaderboard.png
├── chart2_radar.png
├── chart3_funnel_format.png
├── chart4_dimensions.png
└── chart5_insight_card.png
```

---

## 🚀 Run It

```bash
pip install pandas matplotlib
python3 visualise.py
```

---

## 🧠 Methodology Notes

- Scoring is rule-based NLP (keyword matching + structural analysis), not ML
- Designed to mirror how a creative strategist evaluates copy — not just sentiment
- Dataset intentionally includes "generic" brand ads as a baseline contrast
- Scores reflect direct-response performance potential, not brand-building value

---

## 🔗 Related Project

[Competitive Ad Creative Analysis — Indē Wild vs Plum](https://kav0309.github.io/ad-creative-analysis)  
Analysed 24 paid ads across format, copy style, offer type and creative age using Python.

---

*MBA Marketing Portfolio · 2026*
