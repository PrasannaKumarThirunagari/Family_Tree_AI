import streamlit as st
from pyvis.network import Network
import networkx as nx
from utils.helpers import build_graph

def show_tree_tab():
    st.header("🌳 Family Tree Visualizer")

    # Load people and relationships from separate files
    import json
    with open("data/people_only.json", "r") as f:
        people_list = json.load(f)
    with open("data/relationships_only.json", "r") as f:
        relationships = json.load(f)
    people = {p["id"]: p for p in people_list}

    # Group spouses into a single node
    spouse_pairs = set()
    spouse_to_node = {}
    G = nx.DiGraph()
    # Find all spouse pairs
    for rel in relationships:
        if rel["type"] == "spouse":
            pair = tuple(sorted([rel["person1_id"], rel["person2_id"]]))
            spouse_pairs.add(pair)
    # Add spouse nodes with HTML labels for wrapping
    for pair in spouse_pairs:
        p1, p2 = people[pair[0]], people[pair[1]]
        node_id = f"{pair[0]}_{pair[1]}"
        label = f"{p1.get('firstname','')} & {p2.get('firstname','')}"
        G.add_node(node_id, label=label, p1=p1, p2=p2, shape="box")
        spouse_to_node[pair[0]] = node_id
        spouse_to_node[pair[1]] = node_id
    # Add single (non-spouse) people as nodes with HTML labels for wrapping
    for pid, p in people.items():
        if pid not in spouse_to_node:
            label = f"{p.get('firstname','')}" if p.get('firstname') else pid
            G.add_node(pid, label=label, **p, shape="box")
    # Add parent-child edges: from spouse node (if exists) or person to child/couple
    # Find all child spouse nodes
    child_spouse_nodes = {v: set(k) for k, v in spouse_to_node.items()}
    for rel in relationships:
        if rel["type"] == "parent":
            parent_id = rel["parent_id"]
            child_id = rel["child_id"]
            from_node = spouse_to_node.get(parent_id, parent_id)
            # If child is part of a spouse node, link to the couple node
            to_node = spouse_to_node.get(child_id, child_id)
            G.add_edge(from_node, to_node, relation="parent")

    net = Network(height='700px', width='100%', directed=True)
    # Hierarchical layout, fixed positions, no dragging
    net.barnes_hut(gravity=-80000, central_gravity=0, spring_length=95, spring_strength=0.01, damping=0.09, overlap=0)
    net.set_options('''
    {
      "layout": {
        "hierarchical": {
          "enabled": true,
          "direction": "UD",
          "sortMethod": "directed",
          "nodeSpacing": 250,
          "levelSeparation": 200
        }
      },
      "interaction": {
        "dragNodes": true,
        "dragView": true,
        "zoomView": true
      },
      "physics": {
        "enabled": false
      },
      "nodes": {
        "shape": "box",
        "color": {
          "background": "#e3f2fd",
          "border": "#1976d2",
          "highlight": {
            "background": "#bbdefb",
            "border": "#0d47a1"
          }
        },
        "font": {
          "color": "#0d47a1",
          "size": 18,
          "face": "Arial"
        }
      },
      "edges": {
        "color": {
          "color": "#1976d2",
          "highlight": "#0d47a1"
        },
        "font": {
          "color": "#1976d2",
          "size": 16,
          "face": "Arial",
          "align": "middle"
        },
        "arrows": {
          "to": {"enabled": true, "scaleFactor": 1.2}
        },
        "smooth": {
          "type": "cubicBezier"
        }
      }
    }
    ''')

    # Add nodes with labels and all details in the title (for popup)
    for node_id, data in G.nodes(data=True):
        title = f"""
        <b>{data.get('firstname','')}</b><br>
        Gender: {data.get('gender','')}<br>
        """
        net.add_node(node_id, label=data.get("label", str(node_id)), shape="box", title=title)

    # Add edges with relationship label
    for source, target, data in G.edges(data=True):
        relation = data.get("relation", "")
        if relation == "spouse":
            net.add_edge(source, target, label=relation, arrows="to", dashes=True, color="purple")
        else:
            net.add_edge(source, target, label=relation)


    net.save_graph("tree.html")
    with open("tree.html", "r", encoding="utf-8") as f:
        html = f.read()
    st.components.v1.html(html, height=650, scrolling=True)
