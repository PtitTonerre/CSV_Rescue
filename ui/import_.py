import pandas as pd
import streamlit as st

from zipfile import BadZipFile
from core import read_file


def render_import() -> pd.DataFrame | None:
    uploaded_file = st.file_uploader(
        "Importez votre fichier",
        type=["csv", "xlsx"]
    )

    is_excel = (
        uploaded_file is not None
        and uploaded_file.name.lower().endswith(".xlsx")
    )

    with st.expander("Options d'importation", expanded=False):
        if is_excel:
            st.info(
                "Fichier Excel détecté : "
                "la première feuille sera importée."
            )
            separator_mode = "Excel"
            separator = None
        else:
            separator_mode = st.radio(
                "Détection du séparateur",
                ["Automatique", "Manuel"],
                horizontal=True
            )

            if separator_mode == "Manuel":
                separator = st.selectbox(
                    "Séparateur",
                    options=[",", ";", "\t", "|"],
                    format_func=lambda x: {
                        ",": "Virgule (,)",
                        ";": "Point-virgule (;)",
                        "\t": "Tabulation",
                        "|": "Barre verticale (|)"
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
        st.error("Le fichier est vide.")
        st.stop()

    except pd.errors.ParserError:
        st.error("Le fichier est mal formaté.")
        st.stop()

    except UnicodeDecodeError:
        st.error("L'encodage du fichier n'est pas reconnu.")
        st.stop()

    except (BadZipFile, ValueError):
        st.error("Impossible de lire le fichier.")
        st.stop()

    if data.empty:
        st.warning("Le fichier ne contient aucune ligne.")
        st.stop()

    if is_excel:
        st.caption("Format importé : Excel (.xlsx)")
    else:
        st.caption(f"Encodage utilisé : {detected_encoding}")

    if not is_excel and len(data.columns) == 1:
        st.warning(
            "Une seule colonne a été détectée. "
            "Vérifiez que le séparateur est correct."
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
