import pandas as pd

def analyze_csv(df: pd.DataFrame) -> dict:
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "duplicates": df.duplicated().sum(),
        "missing_values": df.isna().sum().sum()
    }

def remove_duplicates(
    df: pd.DataFrame,
    columns: list[str]
) -> pd.DataFrame:
    return df.drop_duplicates(subset=columns)


def remove_missing(
    df: pd.DataFrame,
    columns: list[str]
) -> pd.DataFrame:
    return df.dropna(subset=columns)

def split_missing(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return df.dropna(), df[df.isna().any(axis=1)]