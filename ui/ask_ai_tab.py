import streamlit as st
from agents.reasoning_agent import ingest_documents, query_family_question
from utils.helpers import load_people

def generate_facts():
    df = load_people()
    facts = []
    for _, row in df.iterrows():
        facts.append(f"{row['name']} is a {row['gender']} born on {row['dob']} living in {row['location']}.")
        facts.append(f"{row['name']} has a relationship as {row['relationship']}.")
    return facts

def show_ask_ai_tab():
    st.header("🤖 Ask AI about your Family Tree")

    if st.button("📥 Ingest Family Facts into Memory"):
        facts = generate_facts()
        ingest_documents(facts)
        st.success("Family facts ingested into vector memory!")

    query = st.text_input("💬 Ask a question (e.g., 'Who is Radha’s father?')")
    if query:
        with st.spinner("Thinking..."):
            answer = query_family_question(query)
            st.success("Answer:")
            st.write(answer)