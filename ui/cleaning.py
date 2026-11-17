import pandas as pd
import streamlit as st

from core import remove_duplicates, remove_missing
from state import save_history, undo_history


def render_cleaning(data: pd.DataFrame) -> None:
    all_columns = st.session_state.cleaned_data.columns.tolist()

    col1, col2, col3, col4 = st.columns([3, 3, 2, 2])

    with col1:
        duplicate_columns = st.multiselect(
            "Columns to check for duplicates",
            options=all_columns,
            default=all_columns,
            key="duplicate_columns"
        )

        if st.button(
            "Remove duplicates",
            use_container_width=True,
            disabled=not duplicate_columns
        ):
            save_history()

            st.session_state.cleaned_data = remove_duplicates(
                st.session_state.cleaned_data,
                duplicate_columns
            )

            st.session_state.edit_version += 1
            st.rerun()

    with col2:
        missing_columns = st.multiselect(
            "Columns to check for missing data",
            options=all_columns,
            default=all_columns,
            key="missing_columns"
        )

        if st.button(
            "Remove incomplete rows",
            use_container_width=True,
            disabled=not missing_columns
        ):
            save_history()

            st.session_state.cleaned_data = remove_missing(
                st.session_state.cleaned_data,
                missing_columns
            )

            st.session_state.edit_version += 1
            st.rerun()

    with col3:
        if st.button(
            "Undo",
            disabled=not st.session_state.history,
            use_container_width=True
        ):
            undo_history()
            st.rerun()

    with col4:
        if st.button(
            "Restore original data",
            use_container_width=True
        ):
            save_history()

            st.session_state.cleaned_data = data.copy(deep=True)
            st.session_state.edit_version += 1
            st.rerun()
