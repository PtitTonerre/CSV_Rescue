import pandas as pd
import streamlit as st

from core import split_missing
from state import save_history


def render_editor(data: pd.DataFrame) -> None:
    complete, incomplete = split_missing(
        st.session_state.cleaned_data
    )

    st.html("""
    <style>
    .stTabs [role="tablist"] {
        display: flex !important;
        width: 100% !important;
        gap: 0 !important;
    }

    .stTabs [role="tab"] {
        flex: 1 1 0 !important;
        min-width: 0;
        justify-content: center;
        text-align: center;
    }

    @media (max-width: 768px) {
        .stTabs [role="tab"] {
            flex: 0 0 auto !important;
            min-width: max-content;
            padding: 0 12px;
        }
    }
    </style>
    """)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Original data",
        "Final data",
        "Complete rows",
        "Incomplete rows"
    ])

    with tab1:
        st.subheader("Original data")
        st.dataframe(data, width="stretch")

    with tab2:
        st.subheader("Current data")

        edited_all = st.data_editor(
            st.session_state.cleaned_data,
            num_rows="fixed",
            width="stretch",
            key=f"all_{st.session_state.edit_version}"
        )

        if not edited_all.equals(
            st.session_state.cleaned_data
        ):
            if st.button("Save changes", key="save_all"):
                save_history()

                st.session_state.cleaned_data = (
                    edited_all.copy()
                )

                st.session_state.edit_version += 1
                st.rerun()

    with tab3:
        st.subheader("Complete rows")

        if complete.empty:
            st.success("No complete rows")

        else:
            edited_complete = st.data_editor(
                complete,
                num_rows="fixed",
                width="stretch",
                key=f"complete_{st.session_state.edit_version}"
            )

            if not edited_complete.equals(complete):
                if st.button("Save changes", key="save_complete"):
                    save_history()

                    st.session_state.cleaned_data.loc[
                        edited_complete.index,
                        edited_complete.columns
                    ] = edited_complete

                    st.session_state.edit_version += 1
                    st.rerun()

    with tab4:
        st.subheader("Incomplete rows")

        if incomplete.empty:
            st.success("No incomplete rows")

        else:
            edited_incomplete = st.data_editor(
                incomplete,
                num_rows="fixed",
                width="stretch",
                key=f"incomplete_{st.session_state.edit_version}"
            )

            if not edited_incomplete.equals(incomplete):
                if st.button(
                    "Save changes",
                    key="save_incomplete"
                ):
                    save_history()

                    st.session_state.cleaned_data.loc[
                        edited_incomplete.index,
                        edited_incomplete.columns
                    ] = edited_incomplete

                    st.session_state.edit_version += 1
                    st.rerun()
