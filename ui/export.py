import streamlit as st

from core import export_data


def render_export() -> None:
    st.subheader("Export data")

    export_format = st.selectbox(
        "Export format",
        [
            "International CSV (,)",
            "French CSV (;)",
            "Excel (.xlsx)",
            "TSV (tabulation)"
        ]
    )

    export_content, extension, mime = export_data(
        st.session_state.cleaned_data,
        export_format
    )

    st.download_button(
        label="Download file",
        data=export_content,
        file_name=f"cleaned_data.{extension}",
        mime=mime,
        use_container_width=True,
        on_click="ignore"
    )
