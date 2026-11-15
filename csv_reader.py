
from io import BytesIO
import pandas as pd


def read_csv_file(
    file_bytes: bytes,
    separator: str | None
) -> tuple[pd.DataFrame, str]:

    engine = "python" if separator is None else "c"

    try:
        df = pd.read_csv(
            BytesIO(file_bytes),
            sep=separator,
            engine=engine,
            encoding="utf-8-sig"
        )
        return df, "UTF-8"

    except UnicodeDecodeError:
        df = pd.read_csv(
            BytesIO(file_bytes),
            sep=separator,
            engine=engine,
            encoding="cp1252"
        )
        return df, "Windows-1252"

def read_excel_file(file_bytes: bytes) -> pd.DataFrame:
    return pd.read_excel(
        BytesIO(file_bytes),
        engine="openpyxl"
    )