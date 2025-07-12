
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
    people_options = df["id"].astype(str) + ": " + df["firstname"]
    person1 = st.selectbox("Person 1", people_options, key="spouse1")
    person2 = st.selectbox("Person 2", people_options, key="spouse2")
    if st.button("Link as Spouses"):
        id1 = person1.split(":")[0]
        id2 = person2.split(":")[0]
        if id1 != id2 and not any(r for r in relationships if r["type"]=="spouse" and set([r["person1_id"], r["person2_id"]])==set([id1, id2])):
            relationships.append({"type": "spouse", "person1_id": id1, "person2_id": id2})
            st.session_state['relationships'] = relationships
            st.success(f"Linked {person1} and {person2} as spouses.")
            st.rerun()

    # Add parent-child relationship
    st.subheader("👨‍👩‍� Add Parent-Child Relationship")
    parent = st.selectbox("Parent", people_options, key="parent")
    child = st.selectbox("Child", people_options, key="child")
    if st.button("Link as Parent-Child"):
        parent_id = parent.split(":")[0]
        child_id = child.split(":")[0]
        if parent_id != child_id and not any(r for r in relationships if r["type"]=="parent" and r["parent_id"]==parent_id and r["child_id"]==child_id):
            relationships.append({"type": "parent", "parent_id": parent_id, "child_id": child_id})
            st.session_state['relationships'] = relationships
            st.success(f"Linked {parent} as parent of {child}.")
            st.rerun()

    # Show relationships table with names instead of IDs
    st.subheader("🔗 Relationships")
    rel_display = []
    people_dict = {row['id']: row['firstname'] for _, row in df.iterrows()}
    for r in relationships:
        if r['type'] == 'spouse':
            rel_display.append({
                'type': 'spouse',
                'person1': people_dict.get(r['person1_id'], r['person1_id']),
                'person2': people_dict.get(r['person2_id'], r['person2_id'])
            })
        elif r['type'] == 'parent':
            rel_display.append({
                'type': 'parent',
                'parent': people_dict.get(r['parent_id'], r['parent_id']),
                'child': people_dict.get(r['child_id'], r['child_id'])
            })
    st.dataframe(pd.DataFrame(rel_display))

    # Save all changes
    if st.button("💾 Save All Changes"):
        save_people(st.session_state['people_df'], st.session_state['relationships'])
        st.success("✅ All changes saved.")
