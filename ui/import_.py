import pandas as pd
import streamlit as st

from zipfile import BadZipFile
from core import read_file


def render_import() -> pd.DataFrame | None:
    uploaded_file = st.file_uploader(
        "Upload your file",
        type=["csv", "xlsx"]
    )

    is_excel = (
        uploaded_file is not None
        and uploaded_file.name.lower().endswith(".xlsx")
    )

    with st.expander("Import options", expanded=False):
        if is_excel:
            st.info(
                "Excel file detected: "
                "only the first worksheet will be imported."
            )
            separator_mode = "Excel"
            separator = None
        else:
            separator_mode = st.radio(
                "Delimiter detection",
                ["Automatic", "Manual"],
                horizontal=True
            )

            if separator_mode == "Manual":
                separator = st.selectbox(
                    "Delimiter",
                    options=[",", ";", "\t", "|"],
                    format_func=lambda x: {
                        ",": "Comma (,)",
                        ";": "Semicolon (;)",
                        "\t": "Tab",
                        "|": "Pipe (|)"
                    }[x]
                )
            else:
                separator = None

    if uploaded_file is None:
        st.session_state.pop("import_settings", None)
        return None

    file_bytes = uploaded_file.getvalue()

    try:
        data, detected_encoding = read_file(
            uploaded_file.name,
            file_bytes,
            separator
        )

    except pd.errors.EmptyDataError:
        st.error("The file is empty.")
        st.stop()

    except pd.errors.ParserError:
        st.error("The file is malformed.")
        st.stop()

    except UnicodeDecodeError:
        st.error("The file encoding is not supported.")
        st.stop()

    except (BadZipFile, ValueError):
        st.error("Unable to read the file.")
        st.stop()

    if data.empty:
        st.warning("The file contains no data rows.")
        st.stop()

    if is_excel:
        st.caption("Imported format: Excel (.xlsx)")
    else:
        st.caption(f"Detected encoding: {detected_encoding}")

    if not is_excel and len(data.columns) == 1:
        st.warning(
            "Only one column was detected. "
            "Please check that the delimiter is correct."
        )

    import_settings = (
        file_bytes,
        uploaded_file.name,
        separator_mode,
        separator
    )

    if st.session_state.get("import_settings") != import_settings:
        st.session_state.import_settings = import_settings
        st.session_state.cleaned_data = data.copy()
        st.session_state.history = []
        st.session_state.edit_version = (
            st.session_state.get("edit_version", 0) + 1
        )

        st.session_state.pop("duplicate_columns", None)
        st.session_state.pop("missing_columns", None)

    return data
