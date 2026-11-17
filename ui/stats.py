import pandas as pd
import streamlit as st

from core import analyze_csv


def render_stats(data: pd.DataFrame) -> tuple[dict, dict]:
    original_stats = analyze_csv(data)
    cleaned_stats = analyze_csv(st.session_state.cleaned_data)

    removed_rows = (
        original_stats["rows"] - cleaned_stats["rows"]
    )

    if original_stats["rows"] > 0:
        removed_percent = (
            removed_rows / original_stats["rows"] * 100
        )
    else:
        removed_percent = 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Original rows",
            original_stats["rows"]
        )

    with col2:
        st.metric(
            "Current rows   ",
            cleaned_stats["rows"]
        )

    with col3:
        st.metric(
            "Removed rows",
            removed_rows,
            delta=f"{removed_percent:.1f}% of original file",
            delta_color="off",
            delta_arrow="off"
        )

    return original_stats, cleaned_stats


def render_comparison(
    original_stats: dict,
    cleaned_stats: dict
) -> None:
    st.subheader("Dataset Comparison")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Original Data")
        st.write("Rows: ", original_stats["rows"])
        st.write("Duplicates: ", original_stats["duplicates"])
        st.write(
            "Missing values: ",
            original_stats["missing_values"]
        )

    with col2:
        st.write("### Current Data")
        st.write("Rows: ", cleaned_stats["rows"])
        st.write("Duplicates: ", cleaned_stats["duplicates"])
        st.write(
            "Missing values: ",
            cleaned_stats["missing_values"]
        )
