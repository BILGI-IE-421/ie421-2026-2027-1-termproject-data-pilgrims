
"""Create clear, course-aligned visuals from the merged analysis dataset.

Run:
    python scripts/figures.py

Design goals
------------
- Use one clearly defined merged dataset (`data/merged_dataset.csv`).
- Prefer honest encodings: position, length, and direct comparison over decorative effects.
- Use colour-blind-safe colours and redundant encodings (shape / line style).
- Keep labels, captions, and units explicit.
- Make the figures useful for the project's three research questions.

Outputs
-------
- fig1_relationship_rq1.png / .svg
- fig2_trend_rq3.png / .svg
- fig3_period_relationships_rq2.png / .svg
- supporting summary CSV files in `visuals/`
"""
from __future__ import annotations

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "merged_dataset.csv"
OUTPUT = ROOT / "visuals"

# Okabe-Ito palette: accessible for many common forms of colour-vision deficiency.
BLUE = "#0072B2"
ORANGE = "#E69F00"
GREEN = "#009E73"
VERMILION = "#D55E00"
PURPLE = "#CC79A7"
INK = "#253242"
GREY = "#6B7280"
GRID = "#E6EAF0"
LIGHT_FILL = "#F7F9FC"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#CBD2DB",
    "axes.labelcolor": INK,
    "axes.titleweight": "bold",
    "axes.titlecolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "savefig.dpi": 220,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})


def save_figure(fig: plt.Figure, stem: str, caption: str) -> None:
    """Save both PNG and SVG versions with a readable caption."""
    fig.text(0.07, 0.02, caption, ha="left", va="bottom", fontsize=8.2, color=GREY)
    fig.savefig(OUTPUT / f"{stem}.png", bbox_inches="tight", facecolor="white")
    fig.savefig(OUTPUT / f"{stem}.svg", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def linear_fit(x: pd.Series, y: pd.Series) -> tuple[np.ndarray, np.ndarray] | tuple[None, None]:
    """Return a simple linear fit for plotting; skip if there are too few points."""
    valid = pd.concat([x, y], axis=1).dropna()
    if len(valid) < 2:
        return None, None
    xvals = valid.iloc[:, 0].to_numpy(dtype=float)
    yvals = valid.iloc[:, 1].to_numpy(dtype=float)
    slope, intercept = np.polyfit(xvals, yvals, 1)
    line_x = np.linspace(xvals.min(), xvals.max(), 100)
    line_y = slope * line_x + intercept
    return line_x, line_y


def build_edition_summary(panel: pd.DataFrame) -> pd.DataFrame:
    """One record per Big Mac edition for the Brent-vs-gap-change relationship.

    Brent movement is common to all countries inside an edition. Using one country per row
    would duplicate the same Brent movement many times and would overstate the amount of
    independent evidence. Therefore, we aggregate to one row per edition.
    """
    valid = panel.dropna(subset=["USD_raw_chg", "brent_logchg_since_prev", "oil_regime"]).copy()
    edition = (
        valid.groupby(["date", "oil_regime"], observed=True)
        .agg(
            mean_gap_change=("USD_raw_chg", "mean"),
            median_gap_change=("USD_raw_chg", "median"),
            n_countries=("iso_a3", "nunique"),
            brent_log_change=("brent_logchg_since_prev", "first"),
        )
        .reset_index()
        .sort_values("date")
    )
    edition["gap_change_pp"] = 100 * edition["mean_gap_change"]
    edition["brent_change_pct"] = 100 * np.expm1(edition["brent_log_change"])
    edition["year"] = pd.to_datetime(edition["date"]).dt.year
    return edition


def build_role_summary(panel: pd.DataFrame) -> pd.DataFrame:
    """Summarise valuation gaps by oil role, preserving one series per role and edition."""
    core = panel.dropna(subset=["oil_role", "USD_raw"]).copy()
    summary = (
        core.groupby(["date", "oil_role"], observed=True)
        .agg(
            median_gap=("USD_raw", "median"),
            mean_gap=("USD_raw", "mean"),
            count=("iso_a3", "nunique"),
        )
        .reset_index()
        .sort_values(["date", "oil_role"])
    )
    summary["gap_pct"] = 100 * summary["median_gap"]
    return summary


def plot_rq1_relationship(edition: pd.DataFrame) -> None:
    """Figure 1: edition-level scatter with fitted lines and labelled extremes."""
    fig, ax = plt.subplots(figsize=(10.8, 6.6))
    ax.set_facecolor(LIGHT_FILL)

    style_map = {
        "calm": {"color": GREEN, "marker": "o", "label": "Calm intervals"},
        "high": {"color": VERMILION, "marker": "s", "label": "High-move intervals"},
    }

    for regime, style in style_map.items():
        d = edition[edition["oil_regime"] == regime].copy()
        ax.scatter(
            d["brent_change_pct"],
            d["gap_change_pp"],
            s=65,
            color=style["color"],
            marker=style["marker"],
            edgecolors="white",
            linewidths=0.8,
            alpha=0.9,
            label=f'{style["label"]} (n={len(d)})',
            zorder=3,
        )
        line_x, line_y = linear_fit(d["brent_change_pct"], d["gap_change_pp"])
        if line_x is not None:
            ax.plot(line_x, line_y, color=style["color"], linewidth=2.0, alpha=0.95, zorder=2)

    # Label a few of the most extreme Brent movements for interpretability.
    label_data = edition.loc[edition["brent_change_pct"].abs().nlargest(5).index].copy()
    for _, row in label_data.iterrows():
        label = pd.to_datetime(row["date"]).strftime("%Y-%m")
        ax.annotate(
            label,
            (row["brent_change_pct"], row["gap_change_pp"]),
            xytext=(6, 6),
            textcoords="offset points",
            fontsize=8.5,
            color=INK,
            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.8),
        )

    ax.axhline(0, color=GREY, linewidth=1)
    ax.axvline(0, color=GREY, linewidth=1)
    ax.grid(color=GRID, linewidth=0.9)
    ax.set_axisbelow(True)
    ax.set_xlabel("Brent 30-day average change since previous edition (%)")
    ax.set_ylabel("Mean change in Big Mac valuation gap (percentage points)")
    ax.legend(frameon=False, loc="upper left")
    fig.suptitle(
        "RQ1. Do valuation gaps move differently when oil markets are calm versus volatile?",
        x=0.07,
        ha="left",
        y=0.98,
        fontsize=14,
        fontweight="bold",
        color=INK,
    )
    fig.text(
        0.07,
        0.93,
        "One point per Big Mac edition. Lines show simple within-group trend lines; descriptive, not causal.",
        ha="left",
        va="center",
        fontsize=9.8,
        color=GREY,
    )
    fig.tight_layout(rect=[0.03, 0.06, 1, 0.90])
    save_figure(
        fig,
        "fig1_relationship_rq1",
        "Sources: The Economist Big Mac Index; EIA Brent data. High-move intervals are above the median standardized absolute Brent change.",
    )


def direct_end_label(ax: plt.Axes, x, y, text: str, color: str) -> None:
    """Place a direct label at the final valid observation of a time series."""
    series = pd.DataFrame({"x": x, "y": y}).dropna()
    if series.empty:
        return
    last = series.iloc[-1]
    ax.annotate(
        text,
        (last["x"], last["y"]),
        xytext=(6, 0),
        textcoords="offset points",
        va="center",
        ha="left",
        fontsize=9,
        color=color,
        fontweight="bold",
    )


def plot_rq3_trend(panel: pd.DataFrame, role_summary: pd.DataFrame) -> None:
    """Figure 2: Brent context + exporter/importer median gap trends."""
    prices = panel.groupby("date")["brent_avg_30d"].first().dropna().sort_index()

    exporter = role_summary[role_summary["oil_role"] == "exporter"].copy()
    importer = role_summary[role_summary["oil_role"] == "importer"].copy()

    fig, (ax1, ax2) = plt.subplots(
        2,
        1,
        figsize=(11.2, 7.8),
        sharex=True,
        gridspec_kw={"height_ratios": [1.0, 1.6]},
    )
    for ax in (ax1, ax2):
        ax.set_facecolor(LIGHT_FILL)
        ax.grid(color=GRID, linewidth=0.9)
        ax.set_axisbelow(True)

    ax1.plot(prices.index, prices.to_numpy(), color=GREY, linewidth=2.0)
    ax1.fill_between(prices.index, prices.to_numpy(), 0, color="#D1D7E0", alpha=0.25)
    ax1.set_ylabel("USD per barrel")
    ax1.set_title("Brent price context", loc="left", fontsize=10.8)

    ax2.plot(exporter["date"], exporter["gap_pct"], color=ORANGE, linewidth=2.4)
    ax2.plot(importer["date"], importer["gap_pct"], color=BLUE, linewidth=2.4, linestyle="--")
    ax2.axhline(0, color=GREY, linewidth=1)
    ax2.set_ylabel("Median valuation gap vs. US (%)")
    ax2.set_xlabel("Big Mac edition")
    ax2.set_title("Median Big Mac valuation gap by estimated oil role", loc="left", fontsize=10.8)

    # Show the vertical difference without hiding the line values.
    merged = exporter[["date", "gap_pct"]].merge(
        importer[["date", "gap_pct"]], on="date", suffixes=("_exporter", "_importer")
    )
    ax2.fill_between(
        merged["date"],
        merged["gap_pct_exporter"],
        merged["gap_pct_importer"],
        where=merged["gap_pct_exporter"] >= merged["gap_pct_importer"],
        color=ORANGE,
        alpha=0.10,
        interpolate=True,
    )
    ax2.fill_between(
        merged["date"],
        merged["gap_pct_exporter"],
        merged["gap_pct_importer"],
        where=merged["gap_pct_exporter"] < merged["gap_pct_importer"],
        color=BLUE,
        alpha=0.08,
        interpolate=True,
    )

    direct_end_label(ax2, exporter["date"], exporter["gap_pct"], "Exporter median", ORANGE)
    direct_end_label(ax2, importer["date"], importer["gap_pct"], "Importer median", BLUE)

    ax2.xaxis.set_major_locator(mdates.YearLocator(base=4))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    fig.suptitle(
        "RQ3. Do oil exporters and importers show different valuation-gap patterns over time?",
        x=0.08,
        ha="left",
        y=0.98,
        fontsize=14,
        fontweight="bold",
        color=INK,
    )
    fig.text(
        0.08,
        0.93,
        "Top panel shows oil-market context; bottom panel compares medians to reduce sensitivity to outliers.",
        ha="left",
        va="center",
        fontsize=9.8,
        color=GREY,
    )
    fig.tight_layout(rect=[0.03, 0.06, 1, 0.92], h_pad=2.3)
    save_figure(
        fig,
        "fig2_trend_rq3",
        "Sources: The Economist; EIA; Energy Institute. Oil role is a prior-year production-minus-consumption proxy.",
    )


def assign_period(year: int) -> str:
    """Create interpretable subperiods for RQ2 small multiples."""
    if 2001 <= year <= 2006:
        return "2001–2006"
    if 2007 <= year <= 2013:
        return "2007–2013"
    if 2014 <= year <= 2019:
        return "2014–2019"
    return "2020–2026"


def plot_rq2_periods(edition: pd.DataFrame) -> None:
    """Figure 3: small multiples to show whether the relationship changes over time."""
    d = edition.copy()
    d["period"] = d["year"].map(assign_period)
    period_order = ["2001–2006", "2007–2013", "2014–2019", "2020–2026"]

    xlim = (
        np.floor(d["brent_change_pct"].min() / 10) * 10 - 5,
        np.ceil(d["brent_change_pct"].max() / 10) * 10 + 5,
    )
    ylim = (
        np.floor(d["gap_change_pp"].min() / 5) * 5 - 2,
        np.ceil(d["gap_change_pp"].max() / 5) * 5 + 2,
    )

    fig, axes = plt.subplots(2, 2, figsize=(11.4, 8.2), sharex=True, sharey=True)
    axes = axes.flatten()

    for ax, period in zip(axes, period_order):
        sub = d[d["period"] == period].copy()
        ax.set_facecolor(LIGHT_FILL)
        ax.grid(color=GRID, linewidth=0.9)
        ax.set_axisbelow(True)
        ax.axhline(0, color=GREY, linewidth=1)
        ax.axvline(0, color=GREY, linewidth=1)

        # Plot both regimes with redundant shape encoding.
        for regime, color, marker in [("calm", GREEN, "o"), ("high", VERMILION, "s")]:
            part = sub[sub["oil_regime"] == regime]
            ax.scatter(part["brent_change_pct"], part["gap_change_pp"],
                       color=color, marker=marker, s=52, edgecolors="white", linewidths=0.8, alpha=0.9)

        # Overall fit per panel.
        line_x, line_y = linear_fit(sub["brent_change_pct"], sub["gap_change_pp"])
        if line_x is not None:
            ax.plot(line_x, line_y, color=PURPLE, linewidth=2.0)

        corr = sub[["brent_change_pct", "gap_change_pp"]].corr().iloc[0, 1] if len(sub) >= 2 else np.nan
        corr_text = f"r = {corr:.2f}" if pd.notna(corr) else "r = n/a"
        ax.set_title(f"{period}  ·  {len(sub)} editions", loc="left", fontsize=11)
        ax.text(0.02, 0.96, corr_text, transform=ax.transAxes, ha="left", va="top",
                fontsize=9, color=PURPLE,
                bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.85))
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

    for ax in axes[2:]:
        ax.set_xlabel("Brent change (%)")
    for ax in [axes[0], axes[2]]:
        ax.set_ylabel("Mean gap change (pp)")

    # Add a compact figure-level legend.
    handles = [
        plt.Line2D([0], [0], marker="o", color="none", markerfacecolor=GREEN, markeredgecolor="white", markersize=8, label="Calm"),
        plt.Line2D([0], [0], marker="s", color="none", markerfacecolor=VERMILION, markeredgecolor="white", markersize=8, label="High-move"),
        plt.Line2D([0], [0], color=PURPLE, linewidth=2, label="Within-period trend"),
    ]
    fig.legend(handles=handles, frameon=False, loc="upper right", bbox_to_anchor=(0.98, 0.98))
    fig.suptitle(
        "RQ2. Does the Brent–valuation-gap relationship remain stable over time?",
        x=0.07,
        ha="left",
        y=0.99,
        fontsize=14,
        fontweight="bold",
        color=INK,
    )
    fig.text(
        0.07,
        0.955,
        "Small multiples support period-by-period comparison without overloading one chart.",
        ha="left",
        va="center",
        fontsize=9.8,
        color=GREY,
    )
    fig.tight_layout(rect=[0.03, 0.06, 1, 0.92])
    save_figure(
        fig,
        "fig3_period_relationships_rq2",
        "Sources: The Economist; EIA. Pearson r is shown only as a descriptive summary within each subperiod.",
    )

    period_summary = (
        d.groupby(["period", "oil_regime"], observed=True)
        .agg(
            editions=("date", "count"),
            mean_brent_change_pct=("brent_change_pct", "mean"),
            mean_gap_change_pp=("gap_change_pp", "mean"),
        )
        .reset_index()
    )
    period_summary.to_csv(OUTPUT / "fig3_period_summary.csv", index=False)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if not DATA.exists():
        raise FileNotFoundError("Missing data/merged_dataset.csv. Run scripts/preprocess.py first.")

    panel = pd.read_csv(DATA, parse_dates=["date"])
    required = {
        "date", "iso_a3", "USD_raw", "USD_raw_chg", "oil_role",
        "oil_regime", "brent_logchg_since_prev", "brent_avg_30d"
    }
    missing = required.difference(panel.columns)
    if missing:
        raise ValueError(f"Merged dataset is missing required columns: {sorted(missing)}")

    edition = build_edition_summary(panel)
    role_summary = build_role_summary(panel)
    edition.to_csv(OUTPUT / "fig1_edition_summary.csv", index=False)
    role_summary.to_csv(OUTPUT / "fig2_role_summary.csv", index=False)

    plot_rq1_relationship(edition)
    plot_rq3_trend(panel, role_summary)
    plot_rq2_periods(edition)
    print("Generated 3 figure sets in visuals/: fig1, fig2, fig3 (PNG + SVG).")


if __name__ == "__main__":
    main()
