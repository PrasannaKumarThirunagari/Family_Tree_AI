import streamlit as st
from ui.tree_tab import show_tree_tab
from ui.grid_tab import show_grid_tab
from ui.ask_ai_tab import show_ask_ai_tab
from ui.free_text_tab import extract_data_from_text

st.set_page_config(page_title="Family Tree AI", layout="wide")

tab1, tab2, tab3, tab4 = st.tabs(["🌳 Family Tree", "🧾 Person List", "🤖 Ask AI","📝 Add Person (Free Text)"])
with tab1:
    show_tree_tab()
with tab2:
    show_grid_tab()
with tab3:
    show_ask_ai_tab()
with tab4:
    extract_data_from_text()
