import streamlit as st

from core import export_data


def render_export() -> None:
    st.subheader("Exporter les données")

    export_format = st.selectbox(
        "Choisissez le format de téléchargement",
        [
            "CSV français (;)",
            "CSV international (,)",
            "Excel (.xlsx)",
            "TSV (tabulation)"
        ]
    )

    export_content, extension, mime = export_data(
        st.session_state.cleaned_data,
        export_format
    )

    st.download_button(
        label="Télécharger le fichier",
        data=export_content,
        file_name=f"cleaned_data.{extension}",
        mime=mime,
        use_container_width=True
    )
