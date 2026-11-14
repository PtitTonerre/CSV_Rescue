import pandas as pd
import streamlit as st
from cleaner import analyze_csv, remove_duplicates, remove_missing
from cleaner import split_missing
from csv_reader import read_csv_file

def save_history():
    history = st.session_state.history

    history.append(
        st.session_state.cleaned_data.copy(deep=True)
    )

    if len(history) > 5:
        history.pop(0)

st.set_page_config(page_title="CSV Rescue", layout="wide")

st.title("CSV Rescue")
st.write("Importez un fichier CSV pour analyser ses données.")

uploaded_file = st.file_uploader(
    "Choisissez un fichier CSV",
    type=["csv"]
)

with st.expander("Options d'importation", expanded=False):
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

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()

    try:
        data, detected_encoding = read_csv_file(
            file_bytes,
            separator
        )
    except pd.errors.EmptyDataError:
        st.error("Le fichier CSV est vide.")
        st.stop()
    except pd.errors.ParserError:
        st.error("Le fichier CSV est mal formaté.")
        st.stop()
    except UnicodeDecodeError:
        st.error("L'encodage du fichier n'est pas reconnu.")
        st.stop()

    if data.empty:
        st.warning("Le fichier ne contient aucune ligne.")
        st.stop()

    st.caption(f"Encodage utilisé : {detected_encoding}")

    file_bytes = uploaded_file.getvalue()

    import_settings = (
        file_bytes,
        separator_mode,
        separator
    )

    if len(data.columns) == 1:
        st.warning(
            "Une seule colonne a été détectée. "
            "Vérifiez que le séparateur est correct."
        )

    if st.session_state.get("import_settings") != import_settings:
        st.session_state.import_settings = import_settings
        st.session_state.cleaned_data = data.copy()
        st.session_state.history = []
        st.session_state.edit_version = (
            st.session_state.get("edit_version", 0) + 1
        )

    all_columns = st.session_state.cleaned_data.columns.tolist()
    col1, col2, col3, col4 = st.columns([3.5,3.5,1.5,1.5])

    with col1:
        duplicate_columns = st.multiselect(
            "Colonnes à comparer pour les doublons",
            options=all_columns,
            default=all_columns,
            key="duplicate_columns"
        )

        if st.button(
            "Supprimer les doublons",
            use_container_width=True,
            disabled=not duplicate_columns
        ):
            save_history()  
            st.session_state.cleaned_data = remove_duplicates(
                st.session_state.cleaned_data,
                duplicate_columns
            )
            st.session_state.edit_version += 1

    with col2:
        missing_columns = st.multiselect(
            "Colonnes à vérifier pour les valeurs manquantes",
            options=all_columns,
            default=all_columns,
            key="missing_columns"
        )

        if st.button(
            "Supprimer les valeurs manquantes",
            use_container_width=True,
            disabled=not missing_columns
        ):
            save_history()

            st.session_state.cleaned_data = remove_missing(
                st.session_state.cleaned_data,
                missing_columns
            )
            st.session_state.edit_version += 1

    with col3:
        if st.button(
            "Annuler la dernière modification",
            disabled=not st.session_state.history
        ):
            st.session_state.cleaned_data = (
                st.session_state.history.pop()
            )

            st.session_state.edit_version += 1
            st.rerun()

    with col4:
        if st.button("Réinitialiser les données"):
            save_history()

            st.session_state.cleaned_data = data.copy()
            st.session_state.edit_version += 1

    csv = st.session_state.cleaned_data.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="Télécharger le CSV nettoyé",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

    original_stats = analyze_csv(data)
    cleaned_stats = analyze_csv(st.session_state.cleaned_data)

    removed_rows = original_stats["rows"] - cleaned_stats["rows"]

    if original_stats["rows"] > 0:
        removed_percent = removed_rows / original_stats["rows"] * 100
    else:
        removed_percent = 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Lignes originales", original_stats["rows"])

    with col2:
        st.metric("Lignes nettoyées", cleaned_stats["rows"])

    with col3:
        st.metric(
            "Lignes supprimées",
            removed_rows,
            delta=f"{removed_percent:.1f}% du fichier",
            delta_color="off"
        )

    with st.expander("Aperçu du fichier après modifications", expanded=False):
        st.dataframe(
            st.session_state.cleaned_data,
            height="auto",
            width="stretch"
        )

    complete, incomplete = split_missing(st.session_state.cleaned_data)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Original",
        "Toutes les données",
        "Lignes complètes",
        "Lignes incomplètes"
    ])

    with tab1:
        st.subheader("Données originales")
        st.dataframe(data)

    with tab2:
        st.subheader("Toutes les données")

        edited_all = st.data_editor(
            st.session_state.cleaned_data,
            num_rows="fixed",
            key=f"all_{st.session_state.edit_version}"
        )

        if st.button("Enregistrer", key="save_all"):
            st.session_state.cleaned_data = edited_all.copy()
            st.session_state.edit_version += 1
            st.rerun()

    with tab3:
        st.subheader("Lignes complètes")

        edited_complete = st.data_editor(
            complete,
            num_rows="fixed",
            key=f"complete_{st.session_state.edit_version}"
        )

        if st.button("Enregistrer", key="save_complete"):
            st.session_state.cleaned_data.loc[
                edited_complete.index,
                edited_complete.columns
            ] = edited_complete

            st.session_state.edit_version += 1
            st.rerun()

    with tab4:
        st.subheader("Lignes incomplètes")

        if incomplete.empty:
            st.success("Aucune ligne incomplète !")
        else:
            edited_incomplete = st.data_editor(
                incomplete,
                num_rows="fixed",
                key=f"incomplete_{st.session_state.edit_version}"
            )

            if st.button("Enregistrer", key="save_incomplete"):
                st.session_state.cleaned_data.loc[
                    edited_incomplete.index,
                    edited_incomplete.columns
                ] = edited_incomplete
                st.session_state.edit_version += 1
                st.rerun()

    st.subheader("Comparaison avant / après")

    col1, col2 = st.columns(2)
    with col1:
        st.write("### Données originales")
        st.write("Lignes :", original_stats["rows"])
        st.write("Doublons :", original_stats["duplicates"])
        st.write("Valeurs manquantes :", original_stats["missing_values"])

    with col2:
        st.write("### Données nettoyées")
        st.write("Lignes :", cleaned_stats["rows"])
        st.write("Doublons :", cleaned_stats["duplicates"])
        st.write("Valeurs manquantes :", cleaned_stats["missing_values"])
