from __future__ import annotations

import pandas as pd

from config import OUTPUT_TABLES_DIR, PROFILE_SEASON, ensure_output_dirs
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
    if score >= 75:
        return "elite_signal"
    if score >= 65:
        return "strong_signal"
    if score >= 55:
        return "solid_signal"
    if score >= 45:
        return "moderate_signal"
    return "developing_signal"


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
        "top_signal_situation",
        "top_signal_score",
        "lowest_signal_situation",
        "lowest_signal_score",
    ]
    return ranked[cols].copy()


def build_ranked_situation_scores(situation_scores: pd.DataFrame) -> pd.DataFrame:
    """
    Create a ranked situation-level export across all team-situation rows.
    """
    ranked = situation_scores.copy()
    ranked = ranked.sort_values(
        ["coach_dna_score_adjusted", "team", "situation_order"],
        ascending=[False, True, True],
    ).reset_index(drop=True)

    ranked.insert(0, "rank", ranked.index + 1)

    cols = [
        "rank",
        "team",
        "situation_order",
        "situation_name",
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


def build_top_signal_situations_by_team(situation_scores: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
    """
    For each team, keep the top N highest Coach DNA scoring situations.
    """
    ranked = situation_scores.copy()
    ranked = ranked.sort_values(
        ["team", "coach_dna_score_adjusted", "situation_order"],
        ascending=[True, False, True],
    ).reset_index(drop=True)

    ranked["team_rank_within_top_signals"] = ranked.groupby("team").cumcount() + 1
    ranked = ranked.loc[ranked["team_rank_within_top_signals"] <= top_n].copy()

    cols = [
        "team",
        "team_rank_within_top_signals",
        "situation_name",
        "team_play_count",
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


def build_team_summary_presentation_table(team_summary: pd.DataFrame) -> pd.DataFrame:
    """
    Build a compact presentation-friendly team summary.
    """
    table = build_ranked_team_summary(team_summary).copy()

    table["overall_coach_dna_score"] = table["overall_coach_dna_score"].round(2)
    table["tendency_signal_score_avg"] = table["tendency_signal_score_avg"].round(2)
    table["efficiency_signal_score_avg"] = table["efficiency_signal_score_avg"].round(2)
    table["explosiveness_signal_score_avg"] = table["explosiveness_signal_score_avg"].round(2)
    table["stability_signal_score_avg"] = table["stability_signal_score_avg"].round(2)
    table["sample_reliability_score_avg"] = table["sample_reliability_score_avg"].round(2)
    table["top_signal_score"] = table["top_signal_score"].round(2)
    table["lowest_signal_score"] = table["lowest_signal_score"].round(2)

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
    presentation_team_summary = build_team_summary_presentation_table(team_summary)

    file_map = {
        f"coach_dna_ranked_team_summary_{PROFILE_SEASON}.csv": ranked_team_summary,
        f"coach_dna_ranked_situation_scores_{PROFILE_SEASON}.csv": ranked_situation_scores,
        f"coach_dna_top_signal_situations_by_team_{PROFILE_SEASON}.csv": top_signal_situations,
        f"coach_dna_team_summary_presentation_{PROFILE_SEASON}.csv": presentation_team_summary,
    }

    print("\nSaving packaged exports:")
    for filename, df in file_map.items():
        path = OUTPUT_TABLES_DIR / filename
        df.to_csv(path, index=False)
        print(path)

    print("\nPreview: ranked team summary")
    print(ranked_team_summary.head(10))

    print("\nPreview: top signal situations by team")
    print(top_signal_situations.head(15))


if __name__ == "__main__":
    export_outputs()