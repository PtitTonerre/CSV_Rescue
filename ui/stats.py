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
            "Lignes originales",
            original_stats["rows"]
        )

    with col2:
        st.metric(
            "Lignes nettoyées",
            cleaned_stats["rows"]
        )

    with col3:
        st.metric(
            "Lignes supprimées",
            removed_rows,
            delta=f"{removed_percent:.1f}% du fichier",
            delta_color="off",
            delta_arrow="off"
        )

    return original_stats, cleaned_stats


def render_comparison(
    original_stats: dict,
    cleaned_stats: dict
) -> None:
    st.subheader("Comparaison avant / après")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Données originales")
        st.write("Lignes :", original_stats["rows"])
        st.write("Doublons :", original_stats["duplicates"])
        st.write(
            "Valeurs manquantes :",
            original_stats["missing_values"]
        )

    with col2:
        st.write("### Données nettoyées")
        st.write("Lignes :", cleaned_stats["rows"])
        st.write("Doublons :", cleaned_stats["duplicates"])
        st.write(
            "Valeurs manquantes :",
            cleaned_stats["missing_values"]
        )
