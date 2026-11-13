import pandas as pd

from cleaner import remove_duplicates, remove_missing, split_missing, analyze_csv


def test_remove_duplicates():
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Alice"],
        "age": [25, 30, 25]
    })

    result = remove_duplicates(df, ["name", "age"])

    assert len(result) == 2
    assert len(df) == 3

def test_remove_missing():
    df = pd.DataFrame({
        "name": ["Alice", "Jul", None],
        "age": [15, None, 46]
    })

    result = remove_missing(df, ["name", "age"])

    assert len(result) == 1
    assert len(df) == 3

def test_split_missing():
    df = pd.DataFrame({
        "name": ["Alice", "Jul", None],
        "age": [15, None, 46]
    })

    complete, incomplete = split_missing(df)

    assert len(complete) == 1
    assert complete.iloc[0]["name"] == "Alice"

    assert len(incomplete) == 2
    assert incomplete.iloc[0]["name"] == "Jul"
    assert incomplete.iloc[1]["age"] == 46

    assert len(df) == 3

def test_analyze_csv():
    df = pd.DataFrame({
        "name": ["Alice", "Jul", None, "Alice"],
        "age": [15, None, 46, 15]
    })

    result = analyze_csv(df)

    assert result["rows"] == 4
    assert result["columns"] == 2
    assert result["duplicates"] == 1
    assert result["missing_values"] == 2

    assert len(df) == 4

def test_analyze_empty_csv():
    df = pd.DataFrame()

    result = analyze_csv(df)

    assert result["rows"] == 0
    assert result["columns"] == 0
    assert result["duplicates"] == 0
    assert result["missing_values"] == 0

    assert len(df) == 0