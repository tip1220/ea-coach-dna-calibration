from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

SQL_DIR = PROJECT_ROOT / "sql"
PYTHON_DIR = PROJECT_ROOT / "python"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
OUTPUT_TABLES_DIR = OUTPUTS_DIR / "tables"
OUTPUT_FIGURES_DIR = OUTPUTS_DIR / "figures"


# =========================================================
# PROJECT SCOPE
# =========================================================

PROFILE_SEASON = 2025
BASELINE_START_SEASON = 2023
BASELINE_END_SEASON = 2025
BASELINE_SEASONS = (2023, 2024, 2025)

RAW_SEASONS = (2023, 2024, 2025)

TEAM_PROFILE_TABLE = "team_offense_profiles_2025"
LEAGUE_BASELINE_TABLE = "league_offense_baselines_2023_2025"
CLEAN_PLAY_TABLE = "clean_pbp"
RAW_PLAY_TABLE = "raw_pbp"


# =========================================================
# SITUATION + FIELD-ZONE ORDERING
# =========================================================

SITUATION_ORDER = [
    "all_offense",
    "early_down",
    "third_down",
    "fourth_down",
    "short_yardage",
    "red_zone",
    "goal_to_go",
    "goal_line",
    "two_minute_half",
    "two_minute_game",
    "one_score",
    "neutral_early_down",
    "tied",
    "leading",
    "trailing",
    "leading_one_score",
    "leading_two_plus_scores",
    "trailing_one_score",
    "trailing_two_plus_scores",
    "tied_early_down",
    "leading_early_down",
    "trailing_early_down",
]

SITUATION_ORDER_MAP = {
    situation_name: idx + 1
    for idx, situation_name in enumerate(SITUATION_ORDER)
}

FIELD_ZONE_ORDER = [
    "backed_up",
    "own_territory",
    "fringe",
    "red_zone",
]

FIELD_ZONE_ORDER_MAP = {
    field_zone: idx + 1
    for idx, field_zone in enumerate(FIELD_ZONE_ORDER)
}


# =========================================================
# PRESENTATION / EXPORT SETTINGS
# =========================================================

AVG_TEAM_PLAY_COUNT_DISPLAY_DECIMALS = 1
RATE_DISPLAY_DECIMALS = 4
VALUE_DISPLAY_DECIMALS = 4
SUMMARY_SCORE_DISPLAY_DECIMALS = 4


# =========================================================
# DATABASE CONFIG
# =========================================================

@dataclass(frozen=True)
class MySQLConfig:
    host: str
    port: int
    user: str
    password: str
    database: str

    @classmethod
    def from_env(cls) -> "MySQLConfig":
        return cls(
            host=os.getenv("COACH_DNA_DB_HOST", "localhost"),
            port=int(os.getenv("COACH_DNA_DB_PORT", "3306")),
            user=os.getenv("COACH_DNA_DB_USER", "root"),
            password=os.getenv("COACH_DNA_DB_PASSWORD", ""),
            database=os.getenv("COACH_DNA_DB_NAME", "ea_coach_dna_calibration"),
        )


MYSQL_CONFIG = MySQLConfig.from_env()


# =========================================================
# HELPERS
# =========================================================

def ensure_output_dirs() -> None:
    OUTPUT_TABLES_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


def project_summary() -> dict:
    return {
        "project_root": str(PROJECT_ROOT),
        "profile_season": PROFILE_SEASON,
        "baseline_seasons": BASELINE_SEASONS,
        "database": MYSQL_CONFIG.database,
        "team_profile_table": TEAM_PROFILE_TABLE,
        "league_baseline_table": LEAGUE_BASELINE_TABLE,
        "situation_count": len(SITUATION_ORDER),
        "field_zone_count": len(FIELD_ZONE_ORDER),
        "situation_order": SITUATION_ORDER,
        "field_zone_order": FIELD_ZONE_ORDER,
    }


if __name__ == "__main__":
    ensure_output_dirs()
    print(project_summary())