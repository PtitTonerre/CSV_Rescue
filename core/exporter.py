from io import BytesIO
import pandas as pd


def export_data(
    df: pd.DataFrame,
    export_format: str
) -> tuple[bytes, str, str]:

    if export_format == "Excel (.xlsx)":
        buffer = BytesIO()
        df.to_excel(buffer, index=False, engine="openpyxl")

        return (
            buffer.getvalue(),
            "xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    separators = {
        "International CSV (,)": ",",
        "French CSV (;)": ";",
        "TSV (tabulation)": "\t"
    }

    if export_format not in separators:
        raise ValueError("Format d'exportation non reconnu")

    separator = separators[export_format]

    content = df.to_csv(
        index=False,
        sep=separator
    ).encode("utf-8-sig")

    extension = "tsv" if separator == "\t" else "csv"

    mime = (
        "text/tab-separated-values"
        if extension == "tsv"
        else "text/csv"
    )

    return content, extension, mime