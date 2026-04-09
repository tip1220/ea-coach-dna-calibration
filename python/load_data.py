from __future__ import annotations

from typing import Dict, Optional

import pandas as pd

from config import (
    CLEAN_PLAY_TABLE,
    LEAGUE_BASELINE_TABLE,
    MYSQL_CONFIG,
    RAW_PLAY_TABLE,
    TEAM_PROFILE_TABLE,
    project_summary,
)

try:
    import mysql.connector
except ImportError as exc:
    raise ImportError(
        "mysql-connector-python is not installed. "
        "Install it with: pip install mysql-connector-python"
    ) from exc


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    """
    Create and return a MySQL connection using config.py settings.
    """
    return mysql.connector.connect(
        host=MYSQL_CONFIG.host,
        port=MYSQL_CONFIG.port,
        user=MYSQL_CONFIG.user,
        password=MYSQL_CONFIG.password,
        database=MYSQL_CONFIG.database,
    )


# =========================================================
# GENERIC SQL LOADER
# =========================================================

def load_sql_query(query: str) -> pd.DataFrame:
    """
    Run a SQL query and return the results as a pandas DataFrame.
    """
    connection = get_connection()
    try:
        return pd.read_sql(query, connection)
    finally:
        connection.close()


def load_table(table_name: str, limit: Optional[int] = None) -> pd.DataFrame:
    """
    Load an entire table, with an optional LIMIT for quick checks.
    """
    query = f"SELECT * FROM {table_name}"
    if limit is not None:
        query += f" LIMIT {int(limit)}"
    return load_sql_query(query)


# =========================================================
# PROJECT-SPECIFIC LOADERS
# =========================================================

def load_clean_pbp(limit: Optional[int] = None) -> pd.DataFrame:
    """
    Load the cleaned offensive play table.
    """
    return load_table(CLEAN_PLAY_TABLE, limit=limit)


def load_team_profiles(limit: Optional[int] = None) -> pd.DataFrame:
    """
    Load the 2025 team profile table.
    """
    return load_table(TEAM_PROFILE_TABLE, limit=limit)


def load_league_baselines(limit: Optional[int] = None) -> pd.DataFrame:
    """
    Load the 2023-2025 league baseline table.
    """
    return load_table(LEAGUE_BASELINE_TABLE, limit=limit)


def load_raw_pbp(limit: Optional[int] = None) -> pd.DataFrame:
    """
    Load the raw staging table.
    Mostly useful for QA, not day-to-day analysis.
    """
    return load_table(RAW_PLAY_TABLE, limit=limit)


def load_project_data(include_raw: bool = False) -> Dict[str, pd.DataFrame]:
    """
    Load the main project tables into a dictionary of DataFrames.
    """
    data = {
        "clean_pbp": load_clean_pbp(),
        "team_profiles": load_team_profiles(),
        "league_baselines": load_league_baselines(),
    }

    if include_raw:
        data["raw_pbp"] = load_raw_pbp()

    return data


# =========================================================
# QA HELPERS
# =========================================================

def print_dataframe_summary(name: str, df: pd.DataFrame) -> None:
    """
    Print a simple shape and column summary for a DataFrame.
    """
    print(f"\n{name}")
    print(f"rows: {len(df):,}")
    print(f"columns: {len(df.columns)}")
    print(f"column names: {list(df.columns)}")


def smoke_test() -> None:
    """
    Quick test to confirm Python can connect to MySQL and load
    the core project tables.
    """
    print("Project summary:")
    print(project_summary())

    clean_pbp = load_clean_pbp(limit=5)
    team_profiles = load_team_profiles(limit=5)
    league_baselines = load_league_baselines(limit=5)

    print_dataframe_summary("clean_pbp_sample", clean_pbp)
    print_dataframe_summary("team_profiles_sample", team_profiles)
    print_dataframe_summary("league_baselines_sample", league_baselines)

    print("\nclean_pbp sample:")
    print(clean_pbp.head())

    print("\nteam_profiles sample:")
    print(team_profiles.head())

    print("\nleague_baselines sample:")
    print(league_baselines.head())


if __name__ == "__main__":
    smoke_test()