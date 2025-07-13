
import streamlit as st
import pandas as pd
from utils.helpers import load_people, save_people, generate_unique_id

def show_grid_tab():
    st.header("🧾 Person & Relationship Manager")

    # Load or initialize session state
    if 'people_df' not in st.session_state or 'relationships' not in st.session_state:
        df, relationships = load_people()
        st.session_state['people_df'] = df
        st.session_state['relationships'] = relationships
    else:
        df = st.session_state['people_df']
        relationships = st.session_state['relationships']

    # Show people table
    st.subheader("👤 People List")
    st.dataframe(df)

    # Add new person
    st.subheader("➕ Add New Person")
    with st.form("add_person_form", clear_on_submit=True):
        firstname = st.text_input("First Name")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        submitted = st.form_submit_button("Add Person")
        if submitted:
            new_id = generate_unique_id(df)
            new_row = {"id": new_id, "firstname": firstname, "gender": gender}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            st.session_state['people_df'] = df
            st.success(f"✅ Added {firstname} (ID: {new_id})")
            st.rerun()

    # Add spouse relationship
    st.subheader("💍 Add Spouse Relationship")
    people_options = df["firstname"].tolist()
    person1 = st.selectbox("Person 1", people_options, key="spouse1")
    person2 = st.selectbox("Person 2", people_options, key="spouse2")
    if st.button("Link as Spouses"):
        if person1 != person2 and not any(r for r in relationships if r["type"]=="spouse" and set([r["person1"], r["person2"]])==set([person1, person2])):
            relationships.append({"type": "spouse", "person1": person1, "person2": person2})
            st.session_state['relationships'] = relationships
            st.success(f"Linked {person1} and {person2} as spouses.")
            st.rerun()

    # Add parent-child relationship
    st.subheader("👨‍👩‍👧 Add Parent-Child Relationship")
    parent = st.selectbox("Parent", people_options, key="parent")
    child = st.selectbox("Child", people_options, key="child")
    if st.button("Link as Parent-Child"):
        if parent != child and not any(r for r in relationships if r["type"]=="parent" and r["parent"]==parent and r["child"]==child):
            relationships.append({"type": "parent", "parent": parent, "child": child})
            st.session_state['relationships'] = relationships
            st.success(f"Linked {parent} as parent of {child}.")
            st.rerun()

    # Show relationships table with names instead of IDs
    st.subheader("🔗 Relationships")
    rel_display = []
    for r in relationships:
        if r['type'] == 'spouse':
            rel_display.append({
                'type': 'spouse',
                'person1': r['person1'],
                'person2': r['person2']
            })
        elif r['type'] == 'parent':
            rel_display.append({
                'type': 'parent',
                'parent': r['parent'],
                'child': r['child']
            })
    st.dataframe(pd.DataFrame(rel_display))

    # Save all changes
    if st.button("💾 Save All Changes"):
        save_people(st.session_state['people_df'], st.session_state['relationships'])
        st.success("✅ All changes saved.")
