"""
Ad Copy Scoring Engine — Visualisation & Report
================================================
Generates 5 charts + saves a clean summary CSV.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import numpy as np
import textwrap
import warnings
warnings.filterwarnings("ignore")

from scoring_engine import run_engine

# ── Palette ────────────────────────────────────────────────────────────────
COLORS = {
    "primary"   : "#1A1A2E",
    "accent"    : "#E94560",
    "mid"       : "#16213E",
    "soft"      : "#0F3460",
    "gold"      : "#F5A623",
    "green"     : "#2ECC71",
    "light"     : "#F8F9FA",
    "grey"      : "#ADB5BD",
    "Awareness" : "#4CC9F0",
    "Consideration": "#F72585",
    "Conversion": "#7209B7",
}

DIMS = ["Hook Strength", "Problem Agitation", "Offer Clarity",
        "CTA Strength",  "Social Proof",      "Brand Voice"]
DIM_MAX = [20, 20, 20, 15, 15, 10]   # max scores per dimension

def wrap(text, width=55):
    return "\n".join(textwrap.wrap(text, width))


# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 1 — Leaderboard: Top 15 by Total Score
# ─────────────────────────────────────────────────────────────────────────────
def fig_leaderboard(df):
    top = df.head(15).copy()
    fig, ax = plt.subplots(figsize=(13, 8))
    fig.patch.set_facecolor(COLORS["primary"])
    ax.set_facecolor(COLORS["mid"])

    bars = ax.barh(range(len(top)), top["Total Score"],
                   color=[COLORS[s] for s in top["funnel_stage"]],
                   edgecolor="none", height=0.65)

    for i, (_, row) in enumerate(top.iterrows()):
        ax.text(row["Total Score"] + 0.5, i,
                f'{row["Total Score"]} / 100',
                va="center", ha="left", color="white", fontsize=9, fontweight="bold")
        label = f'{row["brand"]}  ·  {row["format"]}  ·  {row["category"]}'
        ax.text(-1, i, label, va="center", ha="right",
                color=COLORS["light"], fontsize=8.5)

    ax.set_yticks([])
    ax.set_xlim(-32, 75)
    ax.set_xlabel("Total Score (out of 100)", color=COLORS["grey"], fontsize=10)
    ax.tick_params(colors=COLORS["grey"])
    ax.spines[:].set_visible(False)
    ax.set_title("Ad Copy Leaderboard — Top 15", color="white",
                 fontsize=15, fontweight="bold", pad=15)

    # legend
    patches = [mpatches.Patch(color=COLORS[s], label=s)
               for s in ["Awareness", "Consideration", "Conversion"]]
    ax.legend(handles=patches, loc="lower right",
              facecolor=COLORS["mid"], labelcolor="white",
              framealpha=0.8, fontsize=9)

    plt.tight_layout()
    plt.savefig("/home/claude/chart1_leaderboard.png", dpi=150, bbox_inches="tight",
                facecolor=COLORS["primary"])
    plt.close()
    print("✅ Chart 1 saved")


# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 2 — Radar: Top 3 vs Bottom 3 on all 6 dimensions
# ─────────────────────────────────────────────────────────────────────────────
def fig_radar(df):
    top3    = df.head(3)
    bottom3 = df.tail(3)

    def normalise(group):
        vals = []
        for row_idx in range(len(group)):
            r = [group.iloc[row_idx][d] / m * 100
                 for d, m in zip(DIMS, DIM_MAX)]
            vals.append(r)
        return np.array(vals).mean(axis=0)

    t_vals = normalise(top3)
    b_vals = normalise(bottom3)

    angles = np.linspace(0, 2 * np.pi, len(DIMS), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(COLORS["primary"])
    ax.set_facecolor(COLORS["mid"])

    for vals, color, label in [
        (t_vals, COLORS["green"],  "Top 3 Ads"),
        (b_vals, COLORS["accent"], "Bottom 3 Ads"),
    ]:
        v = np.append(vals, vals[0])
        ax.plot(angles, v, color=color, linewidth=2.5)
        ax.fill(angles, v, color=color, alpha=0.15)
        ax.scatter(angles[:-1], vals, color=color, s=60, zorder=5)

    ax.set_thetagrids(np.degrees(angles[:-1]),
                      [d.replace(" ", "\n") for d in DIMS],
                      color="white", fontsize=10)
    ax.set_ylim(0, 100)
    ax.yaxis.set_tick_params(labelcolor=COLORS["grey"])
    ax.grid(color=COLORS["soft"], linewidth=0.8)
    ax.spines["polar"].set_color(COLORS["soft"])

    patches = [mpatches.Patch(color=COLORS["green"], label="Top 3 Ads (avg)"),
               mpatches.Patch(color=COLORS["accent"], label="Bottom 3 Ads (avg)")]
    ax.legend(handles=patches, loc="upper right", bbox_to_anchor=(1.3, 1.15),
              facecolor=COLORS["mid"], labelcolor="white", fontsize=10)

    ax.set_title("Dimension Radar: Top 3 vs Bottom 3", color="white",
                 fontsize=14, fontweight="bold", pad=25)

    plt.tight_layout()
    plt.savefig("/home/claude/chart2_radar.png", dpi=150, bbox_inches="tight",
                facecolor=COLORS["primary"])
    plt.close()
    print("✅ Chart 2 saved")


# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 3 — Avg score by funnel stage + format heatmap
# ─────────────────────────────────────────────────────────────────────────────
def fig_funnel_format(df):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor(COLORS["primary"])

    # Left: avg by funnel stage
    ax1 = axes[0]
    ax1.set_facecolor(COLORS["mid"])
    stage_avg = df.groupby("funnel_stage")["Total Score"].mean().sort_values()
    bars = ax1.barh(stage_avg.index, stage_avg.values,
                    color=[COLORS[s] for s in stage_avg.index],
                    height=0.5, edgecolor="none")
    for bar, val in zip(bars, stage_avg.values):
        ax1.text(val + 0.3, bar.get_y() + bar.get_height()/2,
                 f'{val:.1f}', va="center", color="white", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Avg Total Score", color=COLORS["grey"])
    ax1.tick_params(colors="white")
    ax1.spines[:].set_visible(False)
    ax1.set_title("Avg Score by Funnel Stage", color="white",
                  fontsize=13, fontweight="bold")
    ax1.set_xlim(0, 65)

    # Right: heatmap of avg score by format × funnel stage
    ax2 = axes[1]
    pivot = df.pivot_table(values="Total Score",
                           index="format", columns="funnel_stage",
                           aggfunc="mean")
    im = ax2.imshow(pivot.values, cmap="RdYlGn", aspect="auto",
                    vmin=0, vmax=60)

    ax2.set_xticks(range(len(pivot.columns)))
    ax2.set_xticklabels(pivot.columns, color="white", fontsize=10)
    ax2.set_yticks(range(len(pivot.index)))
    ax2.set_yticklabels(pivot.index, color="white", fontsize=10)
    ax2.set_facecolor(COLORS["mid"])
    ax2.set_title("Avg Score: Format × Funnel Stage", color="white",
                  fontsize=13, fontweight="bold")

    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            val = pivot.values[i, j]
            if not np.isnan(val):
                ax2.text(j, i, f'{val:.0f}', ha="center", va="center",
                         color="black" if val > 30 else "white",
                         fontsize=12, fontweight="bold")

    plt.colorbar(im, ax=ax2, label="Avg Score")
    plt.tight_layout(pad=3)
    plt.savefig("/home/claude/chart3_funnel_format.png", dpi=150, bbox_inches="tight",
                facecolor=COLORS["primary"])
    plt.close()
    print("✅ Chart 3 saved")


# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 4 — Dimension breakdown stacked bar for top 10 ads
# ─────────────────────────────────────────────────────────────────────────────
def fig_dimension_breakdown(df):
    top10 = df.head(10).copy()
    labels = [f'{r["brand"]}\n({r["format"]})' for _, r in top10.iterrows()]

    dim_colors = ["#4CC9F0","#F72585","#7209B7","#F5A623","#2ECC71","#FF6B6B"]

    fig, ax = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor(COLORS["primary"])
    ax.set_facecolor(COLORS["mid"])

    bottom = np.zeros(len(top10))
    for dim, color in zip(DIMS, dim_colors):
        vals = top10[dim].values
        ax.bar(range(len(top10)), vals, bottom=bottom, color=color,
               label=dim, edgecolor=COLORS["primary"], linewidth=0.5)
        # label inside bar if tall enough
        for i, (v, b) in enumerate(zip(vals, bottom)):
            if v >= 3:
                ax.text(i, b + v/2, str(int(v)), ha="center", va="center",
                        color="white", fontsize=7.5, fontweight="bold")
        bottom += vals

    ax.set_xticks(range(len(top10)))
    ax.set_xticklabels(labels, color="white", fontsize=8)
    ax.set_ylabel("Score", color=COLORS["grey"])
    ax.tick_params(colors=COLORS["grey"])
    ax.spines[:].set_visible(False)
    ax.set_title("Dimension Breakdown — Top 10 Ads", color="white",
                 fontsize=14, fontweight="bold", pad=12)
    ax.legend(loc="upper right", facecolor=COLORS["mid"],
              labelcolor="white", fontsize=8.5, ncol=2)
    ax.set_ylim(0, 110)

    plt.tight_layout()
    plt.savefig("/home/claude/chart4_dimensions.png", dpi=150, bbox_inches="tight",
                facecolor=COLORS["primary"])
    plt.close()
    print("✅ Chart 4 saved")


# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 5 — Strategic insight card: best & worst copy side-by-side
# ─────────────────────────────────────────────────────────────────────────────
def fig_insight_card(df):
    best  = df.iloc[0]
    worst = df.iloc[-1]

    fig = plt.figure(figsize=(14, 8))
    fig.patch.set_facecolor(COLORS["primary"])

    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.06)

    for idx, (ad, title, color) in enumerate([
        (best,  "🏆  #1 Highest Scoring Ad",   COLORS["green"]),
        (worst, "📉  Lowest Scoring Ad",        COLORS["accent"]),
    ]):
        ax = fig.add_subplot(gs[idx])
        ax.set_facecolor(COLORS["mid"])
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis("off")

        # Title bar
        ax.add_patch(plt.Rectangle((0, 8.6), 10, 1.4, color=color, clip_on=False))
        ax.text(5, 9.3, title, ha="center", va="center", fontsize=12,
                fontweight="bold", color="white")

        # Meta info
        meta = f'{ad["brand"]}  ·  {ad["category"]}  ·  {ad["format"]}  ·  {ad["funnel_stage"]}'
        ax.text(0.3, 8.2, meta, ha="left", va="center", fontsize=9,
                color=COLORS["grey"])

        # Score badge
        ax.text(9.7, 8.2, f'{ad["Total Score"]} / 100',
                ha="right", va="center", fontsize=13, fontweight="bold",
                color=color)

        # Copy text
        wrapped = wrap(ad["copy"], 58)
        ax.text(0.3, 7.5, wrapped, ha="left", va="top", fontsize=9.5,
                color="white", linespacing=1.6,
                bbox=dict(boxstyle="round,pad=0.5", facecolor=COLORS["soft"],
                          edgecolor=color, linewidth=1.5))

        # Dimension bars
        y = 3.8
        for dim, maxv in zip(DIMS, DIM_MAX):
            raw   = ad[dim]
            pct   = raw / maxv
            bar_w = pct * 8

            ax.text(0.3, y + 0.08, dim, fontsize=8, color=COLORS["grey"], va="bottom")
            ax.add_patch(plt.Rectangle((0.3, y - 0.18), 8, 0.22,
                                       color=COLORS["soft"], clip_on=False))
            ax.add_patch(plt.Rectangle((0.3, y - 0.18), bar_w, 0.22,
                                       color=color, alpha=0.85, clip_on=False))
            ax.text(8.5, y - 0.07, f'{raw}/{maxv}', fontsize=8,
                    color="white", va="center")
            y -= 0.8

        # Why it works / fails note
        if idx == 0:
            note = "Why it works: price anchor + urgency + social proof + PAS structure"
        else:
            note = "Why it fails: vague hook, no price, no proof, weak CTA, generic language"
        ax.text(5, 0.35, note, ha="center", va="center", fontsize=9,
                color=color, style="italic",
                bbox=dict(boxstyle="round,pad=0.4", facecolor=COLORS["primary"],
                          edgecolor=color, linewidth=1))

    fig.suptitle("Best vs Worst Ad Copy — What Makes the Difference",
                 color="white", fontsize=14, fontweight="bold", y=1.01)

    plt.savefig("/home/claude/chart5_insight_card.png", dpi=150, bbox_inches="tight",
                facecolor=COLORS["primary"])
    plt.close()
    print("✅ Chart 5 saved")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = run_engine()

    # Save CSV
    df.to_csv("/home/claude/ad_copy_scores.csv", index_label="Rank")
    print("✅ CSV saved\n")

    fig_leaderboard(df)
    fig_radar(df)
    fig_funnel_format(df)
    fig_dimension_breakdown(df)
    fig_insight_card(df)

    print("\n🎉 All charts generated!")
    print("\n📈 QUICK INSIGHTS")
    print("="*50)
    print(f"Top scoring ad:   {df.iloc[0]['brand']} ({df.iloc[0]['Total Score']}/100)")
    print(f"Lowest scoring:   {df.iloc[-1]['brand']} ({df.iloc[-1]['Total Score']}/100)")
    by_stage = df.groupby("funnel_stage")["Total Score"].mean().round(1)
    print(f"\nAvg score by funnel stage:\n{by_stage.to_string()}")
    by_format = df.groupby("format")["Total Score"].mean().sort_values(ascending=False).round(1)
    print(f"\nAvg score by format:\n{by_format.to_string()}")
