import pytest
import pandas as pd

from core import read_csv_file


def test_read_csv_windows1252():
    content = "name;city\nAlice;Évry\n"
    file_bytes = content.encode("cp1252")

    df, encoding = read_csv_file(file_bytes, ";")

    assert encoding == "Windows-1252"
    assert len(df) == 1
    assert df.loc[0, "city"] == "Évry"

def test_read_csv_utf8():
    content = "name;city\nAlice;Évry\nBob;Paris\n"

    file_bytes = content.encode("utf-8")

    df, encoding = read_csv_file(file_bytes, ";")

    assert encoding == "UTF-8"
    assert len(df) == 2
    assert df.loc[0, "city"] == "Évry"
    assert df.loc[1, "city"] == "Paris"

def test_read_empty_csv():
    file_bytes = b""

    with pytest.raises(pd.errors.EmptyDataError):
        read_csv_file(file_bytes, ",")


def test_read_malformed_csv():
    content = 'name,age\n"Alice,25\nBob,30\n'
    file_bytes = content.encode("utf-8")

    with pytest.raises(pd.errors.ParserError):
        read_csv_file(file_bytes, ",")

def test_read_header_only_csv():
    file_bytes = b"name,age,city\n"

    df, encoding = read_csv_file(file_bytes, ",")

    assert len(df) == 0
    assert len(df.columns) == 3
    assert df.empty