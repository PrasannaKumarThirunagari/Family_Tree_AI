import json
import pandas as pd
import os
import networkx as nx

# ---------- Load and Save People Data ----------


def load_people():
    people_path = "data/people_only.json"
    relationships_path = "data/relationships_only.json"
    if not os.path.exists(people_path):
        return pd.DataFrame(columns=["id", "firstname", "gender"]), []
    try:
        with open(people_path, "r") as f:
            people = json.load(f)
        with open(relationships_path, "r") as f:
            relationships = json.load(f)
        df = pd.DataFrame(people)
        for col in ["id", "firstname", "gender"]:
            if col not in df.columns:
                df[col] = ""
        return df, relationships
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame(columns=["id", "firstname", "gender"]), []

def save_people(df, relationships):
    with open("data/people_only.json", "w") as f:
        json.dump(df.to_dict(orient="records"), f, indent=4)
    with open("data/relationships_only.json", "w") as f:
        json.dump(relationships, f, indent=4)

def generate_unique_id(df):
    existing_ids = set(df["id"].astype(str).tolist()) if "id" in df.columns else set()
    new_id = str(max([int(i) for i in existing_ids if i.isdigit()], default=0) + 1)
    return new_id

def generate_unique_id(df):
    existing_ids = set(df["id"].astype(str).tolist()) if "id" in df.columns else set()
    new_id = str(max([int(i) for i in existing_ids if i.isdigit()], default=0) + 1)
    return new_id


# ---------- Dropdown Values for Forms ----------

def get_dropdowns():
    gender_options = ["Male", "Female", "Other"]
    relationship_options = [
        "Father", "Mother", "Son", "Daughter", "Brother", "Sister", "Spouse",
        "Uncle", "Aunt", "Grandfather", "Grandmother", "Cousin"
    ]
    return gender_options, relationship_options


# ---------- Build Graph for Family Tree ----------

def build_graph():
    df, relationships = load_people()
    people = {row['id']: row for _, row in df.iterrows()}
    G = nx.DiGraph()

    # Group spouses into couple nodes
    spouse_pairs = set()
    spouse_to_node = {}
    for rel in relationships:
        if rel['type'] == 'spouse':
            pair = tuple(sorted([rel['person1_id'], rel['person2_id']]))
            spouse_pairs.add(pair)
    # Add spouse nodes
    for pair in spouse_pairs:
        p1, p2 = people[pair[0]], people[pair[1]]
        node_id = f"{pair[0]}_{pair[1]}"
        marriage_year = p1.get('marriage_year') or p2.get('marriage_year') or ""
        label = f"""
        <div style='white-space:normal;text-align:center;'>
            <b>{p1.get('firstname','')} {p1.get('surname','')}</b><br>
            {p1.get('birth_year','')} - {p1.get('death_year','')}<br>
            <b>{p2.get('firstname','')} {p2.get('surname','')}</b><br>
            {p2.get('birth_year','')} - {p2.get('death_year','')}<br>
            <span style='color:#1976d2;'>Married {marriage_year}</span>
        </div>
        """
        G.add_node(node_id, label=label, p1=p1, p2=p2, shape="box")
        spouse_to_node[pair[0]] = node_id
        spouse_to_node[pair[1]] = node_id
    # Add single (non-spouse) people as nodes
    for pid, p in people.items():
        if pid not in spouse_to_node:
            label = f"""
            <div style='white-space:normal;text-align:center;'>
                <b>{p.get('firstname','')} {p.get('surname','')}</b><br>
                {p.get('birth_year','')} - {p.get('death_year','')}
            </div>
            """
            G.add_node(pid, label=label, **p, shape="box")
    # Add parent-child edges: from spouse node (if exists) or person to child/couple
    for rel in relationships:
        if rel['type'] == 'parent':
            parent_id = rel['parent_id']
            child_id = rel['child_id']
            from_node = spouse_to_node.get(parent_id, parent_id)
            to_node = spouse_to_node.get(child_id, child_id)
            G.add_edge(from_node, to_node, relation='parent')
    return G
