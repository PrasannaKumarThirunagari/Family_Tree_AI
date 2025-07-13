import streamlit as st
import json
import ollama

def show_free_text_tab():
    st.header("📝 Add Person (Free Text)")
    st.markdown("Write natural language family details. AI will extract person and relationship information.")

    user_input = st.text_area("✍️ Enter family information here", height=200, placeholder="E.g., Rama and Sita are married. They have two sons Luv and Kush.")

    if st.button("🧠 Extract Data (Preview Only)"):
        if not user_input.strip():
            st.warning("Please enter some family details.")
        else:
            with st.spinner("Extracting family data using AI..."):
                extracted = extract_from_ollama(user_input)
                if extracted:
                    st.success("✅ Data extracted successfully!")

                    st.subheader("👤 People")
                    st.json(extracted.get("people", []))

                    st.subheader("🔗 Relationships")
                    relationships = extracted.get("relationships", [])
                    st.json(relationships)

                    # --- Remove duplicates: only show relationships not already in the file ---
                    import os
                    rel_path = os.path.join("data", "relationships_only.json")
                    try:
                        with open(rel_path, "r", encoding="utf-8") as f:
                            existing_relationships = json.load(f)
                    except Exception:
                        existing_relationships = []
                    # Create a set of tuples for uniqueness check
                    def rel_key(rel):
                        if rel.get("type") == "spouse":
                            # Spouse: order-insensitive
                            return (rel["type"], tuple(sorted([rel["person1"], rel["person2"]])))
                        elif rel.get("type") == "parent":
                            return (rel["type"], rel["parent"], rel["child"])
                        return tuple(sorted(rel.items()))
                    existing_keys = set(rel_key(r) for r in existing_relationships)
                    unique_relationships = [r for r in relationships if rel_key(r) not in existing_keys]
                    st.subheader("🔗 Relationships (Unique, Not Already in File)")
                    st.json(unique_relationships)
                    if unique_relationships:
                        if st.button("💾 Save Unique Relationships"):
                            # Append and save only unique
                            all_relationships = existing_relationships + unique_relationships
                            with open(rel_path, "w", encoding="utf-8") as f:
                                json.dump(all_relationships, f, ensure_ascii=False, indent=2)
                            st.success(f"Saved {len(unique_relationships)} new relationships to relationships_only.json!")

                    # --- Filter out invalid marriage_years (e.g., 'Sita') ---
                    filtered_people = []
                    for person in extracted.get("people", []):
                        myear = person.get("marriage_year", "")
                        # Keep if marriage_year is empty or a 4-digit year
                        if not myear or (isinstance(myear, str) and myear.isdigit() and len(myear) == 4):
                            filtered_people.append(person)
                        else:
                            # Optionally, clear the invalid value
                            person["marriage_year"] = ""
                            filtered_people.append(person)
                    if len(filtered_people) != len(extracted.get("people", [])):
                        st.info("Some people had invalid marriage_year values, which were cleared.")
                    # --- Remove duplicates: only show people not already in the database ---
                    from utils.helpers import load_people
                    existing_df, _ = load_people()
                    existing_names = set(
                        (str(row.get("firstname", "")).strip().lower(), str(row.get("lastname", "")).strip().lower())
                        for _, row in existing_df.iterrows()
                    )
                    unique_people = []
                    for person in filtered_people:
                        fname = str(person.get("firstname", "")).strip().lower()
                        lname = str(person.get("lastname", "")).strip().lower()
                        if (fname, lname) not in existing_names:
                            unique_people.append(person)
                    st.subheader("👤 People (Unique, Not Already in Database)")
                    st.json(unique_people)

                    if unique_people:
                        if st.button("💾 Add All Unique People to Database"):
                            import pandas as pd
                            from utils.helpers import save_people, generate_unique_id, load_people
                            df, relationships = load_people()
                            next_id = max([int(i) for i in df["id"] if str(i).isdigit()] + [0]) + 1 if not df.empty else 1
                            new_rows = []
                            for person in unique_people:
                                person_id = str(next_id)
                                next_id += 1
                                new_row = {
                                    "id": person_id,
                                    "firstname": person.get("firstname", ""),
                                    "surname": person.get("surname", ""),
                                    "gender": person.get("gender", ""),
                                    "birth_year": person.get("birth_year", ""),
                                    "death_year": person.get("death_year", ""),
                                    "marriage_year": person.get("marriage_year", "")
                                }
                                new_rows.append(new_row)
                            df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
                            save_people(df, relationships)

                            # Save unique_people to people_only.json
                            with open("data/people_only.json", "w", encoding="utf-8") as f:
                                json.dump(unique_people, f, ensure_ascii=False, indent=2)

                            st.success(f"Added {len(new_rows)} new people to the database!")
                            st.balloons()


# ---- Function to send text to Ollama and parse JSON ----
def extract_from_ollama(text):
    system_prompt = """
You are an information extractor that converts family information from natural language into structured JSON data.

Output JSON format:
{
  "people": [
    { "firstname": "Name", "surname": "", "gender": "Male/Female", 
    "birth_year": "", "death_year": "", 
    "marriage_year": "" }
  ],
  "relationships": [
    { "type": "spouse", "person1": "Name1", "person2": "Name2" },
    { "type": "parent", "parent": "Name1", "child": "Name2" }
  ]
}
Only return valid JSON.
"""

    prompt = f"{system_prompt}\n\nText:\n{text}"

    try:
        response = ollama.chat(
            model="llama2",  # or your local model name
            messages=[{"role": "user", "content": prompt}]
        )
        content = response['message']['content']
        return json.loads(content)
    except Exception as e:
        st.error("⚠️ Failed to parse AI output.")
        st.code(content if 'content' in locals() else str(e), language="text")
        return None

# For backward compatibility with main app file
extract_data_from_text = show_free_text_tab
