from __future__ import annotations

from typing import Dict, List

import numpy as np
import pandas as pd

from build_features import build_team_baseline_features
from config import (
    OUTPUT_TABLES_DIR,
    PROCESSED_DATA_DIR,
    PROFILE_SEASON,
    SUMMARY_SCORE_DISPLAY_DECIMALS,
    ensure_output_dirs,
)


# =========================================================
# SCORING CONFIG
# =========================================================

TENDENCY_METRICS: List[str] = [
    "dropback_rate_delta",
    "shotgun_rate_delta",
    "no_huddle_rate_delta",
    "pass_attempt_rate_delta",
]

EFFICIENCY_METRICS: List[str] = [
    "avg_epa_delta",
    "success_rate_delta",
    "first_down_rate_delta",
    "touchdown_rate_delta",
]

EXPLOSIVE_METRICS: List[str] = [
    "explosive_play_rate_delta",
    "explosive_dropback_rate_delta",
    "explosive_run_rate_delta",
]

STABILITY_METRICS: List[str] = [
    "turnover_rate_delta",
    "sack_rate_delta",
]

SAMPLE_SCORE_MAP: Dict[str, float] = {
    "strong": 100.0,
    "good": 80.0,
    "thin": 55.0,
    "very_thin": 30.0,
}

SAMPLE_MULTIPLIER_MAP: Dict[str, float] = {
    "strong": 1.00,
    "good": 0.90,
    "thin": 0.75,
    "very_thin": 0.50,
}

# Core weighted situations for overall team scoring.
# All field-zone rows for these situations are included.
CORE_SITUATION_WEIGHTS: Dict[str, float] = {
    "neutral_early_down": 1.50,
    "third_down": 1.25,
    "red_zone": 1.15,
    "goal_to_go": 1.10,
    "goal_line": 1.20,
    "short_yardage": 1.00,
    "fourth_down": 0.90,
    "two_minute_half": 0.85,
    "two_minute_game": 0.85,
    "tied_early_down": 1.00,
    "leading_early_down": 1.00,
    "trailing_early_down": 1.00,
    "leading_one_score": 0.75,
    "trailing_one_score": 0.75,
}

RANK_GROUP_COLS: List[str] = ["situation_name", "field_zone"]


# =========================================================
# HELPERS
# =========================================================

def rank_within_context(
    df: pd.DataFrame,
    value_col: str,
    *,
    use_abs: bool = False,
    higher_is_better: bool = True,
) -> pd.Series:
    """
    Convert a delta metric into a 0-100 percentile-style score
    within each situation + field_zone context.
    """
    values = df[value_col].abs() if use_abs else df[value_col]

    def _rank(series: pd.Series) -> pd.Series:
        working = series.fillna(0)
        if not higher_is_better:
            working = -working
        return working.rank(pct=True, method="average") * 100

    group_keys = [df[col] for col in RANK_GROUP_COLS]
    return values.groupby(group_keys).transform(_rank)


def weighted_average(values: pd.Series, weights: pd.Series) -> float:
    """
    Compute a weighted average safely.
    """
    valid = values.notna() & weights.notna()
    if valid.sum() == 0:
        return np.nan

    v = values[valid].astype(float)
    w = weights[valid].astype(float)

    if w.sum() == 0:
        return np.nan

    return float(np.average(v, weights=w))


def round_score(value: float) -> float:
    """
    Standard rounding helper for exported score fields.
    """
    if pd.isna(value):
        return np.nan
    return round(float(value), SUMMARY_SCORE_DISPLAY_DECIMALS)


def build_context_label(situation_name: str, field_zone: str) -> str:
    """
    Build a compact context label for summaries.
    """
    return f"{situation_name} | {field_zone}"


# =========================================================
# SITUATION-LEVEL SCORING
# =========================================================

def build_situation_scores() -> pd.DataFrame:
    """
    Build team-by-situation-by-field-zone Coach DNA scores
    from the feature table.
    """
    df = build_team_baseline_features().copy()

    # -----------------------------------------------------
    # Tendency scores
    # Higher absolute deviation = stronger tendency signal
    # -----------------------------------------------------
    tendency_score_cols = []
    for metric in TENDENCY_METRICS:
        score_col = metric.replace("_delta", "_signal_score")
        df[score_col] = rank_within_context(
            df,
            metric,
            use_abs=True,
            higher_is_better=True,
        )
        tendency_score_cols.append(score_col)

    df["tendency_signal_score"] = df[tendency_score_cols].mean(axis=1)

    # -----------------------------------------------------
    # Efficiency scores
    # Higher positive delta = better
    # -----------------------------------------------------
    efficiency_score_cols = []
    for metric in EFFICIENCY_METRICS:
        score_col = metric.replace("_delta", "_score")
        df[score_col] = rank_within_context(
            df,
            metric,
            use_abs=False,
            higher_is_better=True,
        )
        efficiency_score_cols.append(score_col)

    df["efficiency_signal_score"] = df[efficiency_score_cols].mean(axis=1)

    # -----------------------------------------------------
    # Explosiveness scores
    # Higher positive delta = better
    # -----------------------------------------------------
    explosive_score_cols = []
    for metric in EXPLOSIVE_METRICS:
        score_col = metric.replace("_delta", "_score")
        df[score_col] = rank_within_context(
            df,
            metric,
            use_abs=False,
            higher_is_better=True,
        )
        explosive_score_cols.append(score_col)

    df["explosiveness_signal_score"] = df[explosive_score_cols].mean(axis=1)

    # -----------------------------------------------------
    # Stability scores
    # Lower turnover/sack deltas are better
    # -----------------------------------------------------
    stability_score_cols = []
    for metric in STABILITY_METRICS:
        score_col = metric.replace("_delta", "_score")
        df[score_col] = rank_within_context(
            df,
            metric,
            use_abs=False,
            higher_is_better=False,
        )
        stability_score_cols.append(score_col)

    df["stability_signal_score"] = df[stability_score_cols].mean(axis=1)

    # -----------------------------------------------------
    # Sample reliability
    # -----------------------------------------------------
    df["sample_reliability_score"] = (
        df["team_sample_quality"].map(SAMPLE_SCORE_MAP).fillna(30.0)
    )
    df["sample_multiplier"] = (
        df["team_sample_quality"].map(SAMPLE_MULTIPLIER_MAP).fillna(0.50)
    )

    # -----------------------------------------------------
    # Overall situation-level Coach DNA score
    # -----------------------------------------------------
    df["coach_dna_score_raw"] = (
        0.45 * df["tendency_signal_score"]
        + 0.25 * df["efficiency_signal_score"]
        + 0.15 * df["explosiveness_signal_score"]
        + 0.10 * df["stability_signal_score"]
        + 0.05 * df["sample_reliability_score"]
    )

    df["coach_dna_score_adjusted"] = (
        df["coach_dna_score_raw"] * df["sample_multiplier"]
    )

    # -----------------------------------------------------
    # Useful labels
    # -----------------------------------------------------
    df["tendency_profile_label"] = np.select(
        [
            df["dropback_rate_delta"] >= 0.05,
            df["dropback_rate_delta"] <= -0.05,
        ],
        [
            "more_dropback_heavy_than_baseline",
            "more_run_heavy_than_baseline",
        ],
        default="close_to_baseline_run_pass_split",
    )

    df["tempo_profile_label"] = np.select(
        [
            df["no_huddle_rate_delta"] >= 0.02,
            df["no_huddle_rate_delta"] <= -0.02,
        ],
        [
            "faster_than_baseline",
            "slower_than_baseline",
        ],
        default="close_to_baseline_tempo",
    )

    df["formation_profile_label"] = np.select(
        [
            df["shotgun_rate_delta"] >= 0.05,
            df["shotgun_rate_delta"] <= -0.05,
        ],
        [
            "more_shotgun_than_baseline",
            "less_shotgun_than_baseline",
        ],
        default="close_to_baseline_shotgun_usage",
    )

    df["efficiency_profile_label"] = np.select(
        [
            df["avg_epa_delta"] >= 0.03,
            df["avg_epa_delta"] <= -0.03,
        ],
        [
            "more_efficient_than_baseline",
            "less_efficient_than_baseline",
        ],
        default="close_to_baseline_efficiency",
    )

    df["situation_field_zone_context"] = df.apply(
        lambda row: build_context_label(row["situation_name"], row["field_zone"]),
        axis=1,
    )

    ordered_cols = [
        "profile_season",
        "team",
        "situation_order",
        "situation_name",
        "field_zone_order",
        "field_zone",
        "situation_field_zone_context",
        "team_play_count",
        "team_sample_quality",
        "sample_vs_baseline_context",
        "sample_reliability_score",
        "sample_multiplier",
        "tendency_signal_score",
        "efficiency_signal_score",
        "explosiveness_signal_score",
        "stability_signal_score",
        "coach_dna_score_raw",
        "coach_dna_score_adjusted",
        "tendency_profile_label",
        "tempo_profile_label",
        "formation_profile_label",
        "efficiency_profile_label",
    ]

    keep_metric_cols = [
        "dropback_rate_team",
        "dropback_rate_baseline",
        "dropback_rate_delta",
        "rush_rate_team",
        "rush_rate_baseline",
        "rush_rate_delta",
        "pass_attempt_rate_team",
        "pass_attempt_rate_baseline",
        "pass_attempt_rate_delta",
        "shotgun_rate_team",
        "shotgun_rate_baseline",
        "shotgun_rate_delta",
        "no_huddle_rate_team",
        "no_huddle_rate_baseline",
        "no_huddle_rate_delta",
        "avg_epa_team",
        "avg_epa_baseline",
        "avg_epa_delta",
        "success_rate_team",
        "success_rate_baseline",
        "success_rate_delta",
        "explosive_play_rate_team",
        "explosive_play_rate_baseline",
        "explosive_play_rate_delta",
        "turnover_rate_team",
        "turnover_rate_baseline",
        "turnover_rate_delta",
        "sack_rate_team",
        "sack_rate_baseline",
        "sack_rate_delta",
    ]

    signal_component_cols = (
        tendency_score_cols
        + efficiency_score_cols
        + explosive_score_cols
        + stability_score_cols
    )

    df = df[ordered_cols + keep_metric_cols + signal_component_cols].copy()
    df = df.sort_values(
        ["team", "situation_order", "field_zone_order"]
    ).reset_index(drop=True)

    return df


# =========================================================
# TEAM SUMMARY SCORING
# =========================================================

def build_team_summary_scores(situation_scores: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate situation-level scores into one team-level
    Coach DNA score.
    """
    scoring_df = situation_scores[
        situation_scores["situation_name"].isin(CORE_SITUATION_WEIGHTS.keys())
    ].copy()

    scoring_df["situation_weight"] = scoring_df["situation_name"].map(
        CORE_SITUATION_WEIGHTS
    )
    scoring_df["aggregation_weight"] = (
        scoring_df["situation_weight"]
        * np.sqrt(scoring_df["team_play_count"].clip(lower=1))
    )

    rows = []
    for team, grp in scoring_df.groupby("team", sort=True):
        top_idx = grp["coach_dna_score_adjusted"].idxmax()
        low_idx = grp["coach_dna_score_adjusted"].idxmin()

        rows.append(
            {
                "profile_season": PROFILE_SEASON,
                "team": team,
                "scored_situations": int(len(grp)),
                "overall_coach_dna_score": round_score(
                    weighted_average(
                        grp["coach_dna_score_adjusted"],
                        grp["aggregation_weight"],
                    )
                ),
                "tendency_signal_score_avg": round_score(
                    weighted_average(
                        grp["tendency_signal_score"],
                        grp["aggregation_weight"],
                    )
                ),
                "efficiency_signal_score_avg": round_score(
                    weighted_average(
                        grp["efficiency_signal_score"],
                        grp["aggregation_weight"],
                    )
                ),
                "explosiveness_signal_score_avg": round_score(
                    weighted_average(
                        grp["explosiveness_signal_score"],
                        grp["aggregation_weight"],
                    )
                ),
                "stability_signal_score_avg": round_score(
                    weighted_average(
                        grp["stability_signal_score"],
                        grp["aggregation_weight"],
                    )
                ),
                "sample_reliability_score_avg": round_score(
                    weighted_average(
                        grp["sample_reliability_score"],
                        grp["aggregation_weight"],
                    )
                ),
                "top_signal_situation": grp.loc[top_idx, "situation_name"],
                "top_signal_field_zone": grp.loc[top_idx, "field_zone"],
                "top_signal_context": grp.loc[
                    top_idx, "situation_field_zone_context"
                ],
                "top_signal_score": round_score(
                    grp.loc[top_idx, "coach_dna_score_adjusted"]
                ),
                "lowest_signal_situation": grp.loc[low_idx, "situation_name"],
                "lowest_signal_field_zone": grp.loc[low_idx, "field_zone"],
                "lowest_signal_context": grp.loc[
                    low_idx, "situation_field_zone_context"
                ],
                "lowest_signal_score": round_score(
                    grp.loc[low_idx, "coach_dna_score_adjusted"]
                ),
            }
        )

    summary = (
        pd.DataFrame(rows)
        .sort_values(
            ["overall_coach_dna_score", "team"],
            ascending=[False, True],
        )
        .reset_index(drop=True)
    )

    return summary


# =========================================================
# EXPORTS
# =========================================================

def export_scores(
    situation_scores: pd.DataFrame,
    team_summary: pd.DataFrame,
) -> None:
    """
    Save scoring outputs to processed data and final output folders.
    """
    ensure_output_dirs()

    processed_situation_path = (
        PROCESSED_DATA_DIR / f"coach_dna_situation_scores_{PROFILE_SEASON}.csv"
    )
    processed_summary_path = (
        PROCESSED_DATA_DIR / f"coach_dna_team_summary_{PROFILE_SEASON}.csv"
    )

    output_situation_path = (
        OUTPUT_TABLES_DIR / f"coach_dna_situation_scores_{PROFILE_SEASON}.csv"
    )
    output_summary_path = (
        OUTPUT_TABLES_DIR / f"coach_dna_team_summary_{PROFILE_SEASON}.csv"
    )

    situation_scores.to_csv(processed_situation_path, index=False)
    situation_scores.to_csv(output_situation_path, index=False)

    team_summary.to_csv(processed_summary_path, index=False)
    team_summary.to_csv(output_summary_path, index=False)

    print("\nSaved files:")
    print(processed_situation_path)
    print(output_situation_path)
    print(processed_summary_path)
    print(output_summary_path)


# =========================================================
# SMOKE TEST
# =========================================================

def smoke_test() -> None:
    """
    Build Coach DNA situation and team summary scores,
    print quick checks, and export outputs.
    """
    situation_scores = build_situation_scores()
    team_summary = build_team_summary_scores(situation_scores)

    print("\ncoach_dna_situation_scores")
    print(f"rows: {len(situation_scores):,}")
    print(f"columns: {len(situation_scores.columns)}")

    print("\ncoach_dna_team_summary")
    print(f"rows: {len(team_summary):,}")
    print(f"columns: {len(team_summary.columns)}")

    print("\nTop 10 team summary scores:")
    print(
        team_summary[
            [
                "team",
                "overall_coach_dna_score",
                "tendency_signal_score_avg",
                "efficiency_signal_score_avg",
                "top_signal_context",
                "top_signal_score",
            ]
        ].head(10)
    )

    print("\nBUF situation sample:")
    buf_sample = (
        situation_scores.loc[
            situation_scores["team"] == "BUF",
            [
                "team",
                "situation_order",
                "situation_name",
                "field_zone_order",
                "field_zone",
                "team_play_count",
                "coach_dna_score_adjusted",
                "tendency_signal_score",
                "efficiency_signal_score",
                "explosiveness_signal_score",
                "stability_signal_score",
                "sample_reliability_score",
                "tendency_profile_label",
                "efficiency_profile_label",
            ],
        ]
        .sort_values(["situation_order", "field_zone_order"])
        .head(12)
        .drop(columns=["situation_order", "field_zone_order"])
    )
    print(buf_sample)

    export_scores(situation_scores, team_summary)


if __name__ == "__main__":
    smoke_test()