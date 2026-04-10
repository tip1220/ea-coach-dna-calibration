from __future__ import annotations

import pandas as pd

from config import (
    AVG_TEAM_PLAY_COUNT_DISPLAY_DECIMALS,
    OUTPUT_TABLES_DIR,
    PROFILE_SEASON,
    SUMMARY_SCORE_DISPLAY_DECIMALS,
    ensure_output_dirs,
)
from score_profiles import build_situation_scores, build_team_summary_scores


# =========================================================
# HELPERS
# =========================================================

def add_score_tier(score: float) -> str:
    """
    Convert a numeric overall Coach DNA score into a simple tier label.
    """
    if pd.isna(score):
        return "unscored"
    if score >= 55:
        return "strong_signal"
    if score >= 47:
        return "solid_signal"
    if score >= 40:
        return "moderate_signal"
    return "developing_signal"


def round_score_columns(
    df: pd.DataFrame,
    score_cols: list[str],
    decimals: int = SUMMARY_SCORE_DISPLAY_DECIMALS,
) -> pd.DataFrame:
    """
    Round selected score columns for export readability.
    """
    out = df.copy()
    for col in score_cols:
        if col in out.columns:
            out[col] = out[col].round(decimals)
    return out


# =========================================================
# EXPORT BUILDERS
# =========================================================

def build_ranked_team_summary(team_summary: pd.DataFrame) -> pd.DataFrame:
    """
    Create a clean ranked team summary export.
    """
    ranked = team_summary.copy()
    ranked = ranked.sort_values(
        ["overall_coach_dna_score", "team"],
        ascending=[False, True],
    ).reset_index(drop=True)

    ranked.insert(0, "rank", ranked.index + 1)
    ranked["score_tier"] = ranked["overall_coach_dna_score"].apply(add_score_tier)

    cols = [
        "rank",
        "team",
        "overall_coach_dna_score",
        "score_tier",
        "scored_situations",
        "tendency_signal_score_avg",
        "efficiency_signal_score_avg",
        "explosiveness_signal_score_avg",
        "stability_signal_score_avg",
        "sample_reliability_score_avg",
        "top_signal_context",
        "top_signal_situation",
        "top_signal_field_zone",
        "top_signal_score",
        "lowest_signal_context",
        "lowest_signal_situation",
        "lowest_signal_field_zone",
        "lowest_signal_score",
    ]
    return ranked[cols].copy()


def build_ranked_situation_scores(situation_scores: pd.DataFrame) -> pd.DataFrame:
    """
    Create a ranked situation-level export across all team-context rows.
    """
    ranked = situation_scores.copy()
    ranked = ranked.sort_values(
        [
            "coach_dna_score_adjusted",
            "team",
            "situation_order",
            "field_zone_order",
        ],
        ascending=[False, True, True, True],
    ).reset_index(drop=True)

    ranked.insert(0, "rank", ranked.index + 1)

    cols = [
        "rank",
        "team",
        "situation_order",
        "situation_name",
        "field_zone_order",
        "field_zone",
        "situation_field_zone_context",
        "team_play_count",
        "team_sample_quality",
        "coach_dna_score_adjusted",
        "coach_dna_score_raw",
        "tendency_signal_score",
        "efficiency_signal_score",
        "explosiveness_signal_score",
        "stability_signal_score",
        "sample_reliability_score",
        "dropback_rate_delta",
        "rush_rate_delta",
        "shotgun_rate_delta",
        "no_huddle_rate_delta",
        "avg_epa_delta",
        "success_rate_delta",
        "explosive_play_rate_delta",
        "tendency_profile_label",
        "formation_profile_label",
        "tempo_profile_label",
        "efficiency_profile_label",
    ]
    return ranked[cols].copy()


def build_top_signal_situations_by_team(
    situation_scores: pd.DataFrame,
    top_n: int = 3,
) -> pd.DataFrame:
    """
    For each team, keep the top N highest Coach DNA scoring contexts.
    """
    ranked = situation_scores.copy()
    ranked = ranked.sort_values(
        [
            "team",
            "coach_dna_score_adjusted",
            "situation_order",
            "field_zone_order",
        ],
        ascending=[True, False, True, True],
    ).reset_index(drop=True)

    ranked["team_rank_within_top_signals"] = ranked.groupby("team").cumcount() + 1
    ranked = ranked.loc[ranked["team_rank_within_top_signals"] <= top_n].copy()

    cols = [
        "team",
        "team_rank_within_top_signals",
        "situation_name",
        "field_zone",
        "situation_field_zone_context",
        "team_play_count",
        "team_sample_quality",
        "coach_dna_score_adjusted",
        "tendency_signal_score",
        "efficiency_signal_score",
        "explosiveness_signal_score",
        "stability_signal_score",
        "dropback_rate_delta",
        "rush_rate_delta",
        "shotgun_rate_delta",
        "no_huddle_rate_delta",
        "avg_epa_delta",
        "success_rate_delta",
        "explosive_play_rate_delta",
        "tendency_profile_label",
        "formation_profile_label",
        "tempo_profile_label",
        "efficiency_profile_label",
    ]
    return ranked[cols].copy()


def build_situation_strength_summary(situation_scores: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize how strong each situation + field-zone context is across teams.
    Useful for README, GitHub screenshots, and insight generation.
    """
    summary = (
        situation_scores.groupby(
            [
                "situation_order",
                "situation_name",
                "field_zone_order",
                "field_zone",
                "situation_field_zone_context",
            ],
            as_index=False,
        )
        .agg(
            avg_adjusted_score=("coach_dna_score_adjusted", "mean"),
            max_adjusted_score=("coach_dna_score_adjusted", "max"),
            min_adjusted_score=("coach_dna_score_adjusted", "min"),
            avg_team_play_count=("team_play_count", "mean"),
            team_count=("team", "nunique"),
            strong_sample_teams=("team_sample_quality", lambda s: int((s == "strong").sum())),
            good_or_better_teams=("team_sample_quality", lambda s: int(s.isin(["strong", "good"]).sum())),
        )
        .sort_values(
            ["avg_adjusted_score", "situation_order", "field_zone_order"],
            ascending=[False, True, True],
        )
        .reset_index(drop=True)
    )

    summary.insert(0, "rank", summary.index + 1)
    summary["avg_team_play_count"] = summary["avg_team_play_count"].round(
        AVG_TEAM_PLAY_COUNT_DISPLAY_DECIMALS
    )
    summary["avg_adjusted_score"] = summary["avg_adjusted_score"].round(
        SUMMARY_SCORE_DISPLAY_DECIMALS
    )
    summary["max_adjusted_score"] = summary["max_adjusted_score"].round(
        SUMMARY_SCORE_DISPLAY_DECIMALS
    )
    summary["min_adjusted_score"] = summary["min_adjusted_score"].round(
        SUMMARY_SCORE_DISPLAY_DECIMALS
    )

    cols = [
        "rank",
        "situation_order",
        "situation_name",
        "field_zone_order",
        "field_zone",
        "situation_field_zone_context",
        "avg_adjusted_score",
        "max_adjusted_score",
        "min_adjusted_score",
        "avg_team_play_count",
        "team_count",
        "strong_sample_teams",
        "good_or_better_teams",
    ]
    return summary[cols].copy()


def build_team_summary_presentation_table(team_summary: pd.DataFrame) -> pd.DataFrame:
    """
    Build a compact presentation-friendly team summary.
    """
    table = build_ranked_team_summary(team_summary).copy()

    round_cols = [
        "overall_coach_dna_score",
        "tendency_signal_score_avg",
        "efficiency_signal_score_avg",
        "explosiveness_signal_score_avg",
        "stability_signal_score_avg",
        "sample_reliability_score_avg",
        "top_signal_score",
        "lowest_signal_score",
    ]
    table = round_score_columns(table, round_cols, decimals=2)

    return table


# =========================================================
# EXPORT RUNNER
# =========================================================

def export_outputs() -> None:
    """
    Build scoring outputs and save packaged export tables.
    """
    ensure_output_dirs()

    situation_scores = build_situation_scores()
    team_summary = build_team_summary_scores(situation_scores)

    ranked_team_summary = build_ranked_team_summary(team_summary)
    ranked_situation_scores = build_ranked_situation_scores(situation_scores)
    top_signal_situations = build_top_signal_situations_by_team(situation_scores, top_n=3)
    situation_strength_summary = build_situation_strength_summary(situation_scores)
    presentation_team_summary = build_team_summary_presentation_table(team_summary)

    file_map = {
        f"coach_dna_ranked_team_summary_{PROFILE_SEASON}.csv": ranked_team_summary,
        f"coach_dna_ranked_situation_scores_{PROFILE_SEASON}.csv": ranked_situation_scores,
        f"coach_dna_top_signal_situations_by_team_{PROFILE_SEASON}.csv": top_signal_situations,
        f"coach_dna_situation_strength_summary_{PROFILE_SEASON}.csv": situation_strength_summary,
        f"coach_dna_team_summary_presentation_{PROFILE_SEASON}.csv": presentation_team_summary,
    }

    print("\nSaving packaged exports:")
    for filename, df in file_map.items():
        path = OUTPUT_TABLES_DIR / filename
        df.to_csv(path, index=False)
        print(path)

    print("\nPreview: ranked team summary")
    print(ranked_team_summary.head(10))

    print("\nPreview: situation strength summary")
    print(situation_strength_summary.head(10))

    print("\nPreview: top signal situations by team")
    print(top_signal_situations.head(15))


if __name__ == "__main__":
    export_outputs()