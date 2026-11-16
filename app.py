import streamlit as st

from ui import (
    render_import,
    render_cleaning,
    render_export,
    render_stats,
    render_comparison,
    render_editor
)


def main() -> None:
    st.set_page_config(
        page_title="CSV Rescue",
        layout="wide"
    )

    st.title("CSV Rescue")

    st.write(
        "Importez un fichier CSV ou Excel "
        "pour analyser et nettoyer ses données."
    )

    data = render_import()

    if data is None:
        return

    render_cleaning(data)
    original_stats, cleaned_stats = render_stats(data)
    render_export()
    render_editor(data)
    render_comparison(original_stats, cleaned_stats)


if __name__ == "__main__":
    main()

