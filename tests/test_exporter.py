
from io import BytesIO

import pandas as pd
import pytest

from core import export_data


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "name": ["Alice", "Émilie", "Bob"],
        "age": [25, 22, 30],
        "city": ["Paris", "Nice", "Lyon"]
    })


@pytest.mark.parametrize(
    "export_format, separator, expected_extension, expected_mime",
    [
        ("International CSV (,)", ",", "csv", "text/csv"),
        ("French CSV (;)", ";", "csv", "text/csv"),
        ("TSV (tabulation)", "\t", "tsv", "text/tab-separated-values")
    ]
)


def test_export_text_formats(
    sample_data,
    export_format,
    separator,
    expected_extension,
    expected_mime
):
    content, extension, mime = export_data(
        sample_data,
        export_format
    )

    assert extension == expected_extension
    assert mime == expected_mime

    result = pd.read_csv(
        BytesIO(content),
        sep=separator,
        encoding="utf-8-sig"
    )

    pd.testing.assert_frame_equal(result, sample_data)


def test_export_excel(sample_data):
    content, extension, mime = export_data(
        sample_data,
        "Excel (.xlsx)"
    )

    assert extension == "xlsx"
    assert mime == (
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    )

    result = pd.read_excel(
        BytesIO(content),
        engine="openpyxl"
    )

    pd.testing.assert_frame_equal(result, sample_data)


def test_export_invalid_format(sample_data):
    with pytest.raises(ValueError):
        export_data(sample_data, "PDF")
