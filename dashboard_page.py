import streamlit as st

st.title("Budget Buddy v1")
st.header("_By TheGalacticProg_")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Budget", "temp")

with col2:
    st.metric("Total Spent", "temp")

with col3:
    st.metric("Remaining", "temp")