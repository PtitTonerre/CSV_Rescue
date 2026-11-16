import streamlit as st


def save_history():
    history = st.session_state.history

    history.append(
        st.session_state.cleaned_data.copy(deep=True)
    )

    if len(history) > 5:
        history.pop(0)


def undo_history():
    if not st.session_state.history:
        return

    st.session_state.cleaned_data = (
        st.session_state.history.pop()
    )

    st.session_state.edit_version += 1