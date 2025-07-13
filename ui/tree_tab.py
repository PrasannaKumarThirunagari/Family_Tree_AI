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
    people = {p["firstname"]: p for p in people_list}

    # Group spouses into a single node
    spouse_pairs = set()
    spouse_to_node = {}
    G = nx.DiGraph()
    # Find all spouse pairs
    for rel in relationships:
        if rel["type"] == "spouse":
            pair = tuple(sorted([rel["person1"], rel["person2"]]))
            spouse_pairs.add(pair)
    # Add spouse nodes with HTML labels for wrapping
    for pair in spouse_pairs:
        p1, p2 = people.get(pair[0], {}), people.get(pair[1], {})
        node_id = f"{pair[0]}_{pair[1]}"
        label = f"{p1.get('firstname','')} & {p2.get('firstname','')}"
        G.add_node(node_id, label=label, p1=p1, p2=p2, shape="box")
        spouse_to_node[pair[0]] = node_id
        spouse_to_node[pair[1]] = node_id
    # Add single (non-spouse) people as nodes with HTML labels for wrapping
    for name, p in people.items():
        if name not in spouse_to_node:
            label = f"{p.get('firstname','')}" if p.get('firstname') else name
            G.add_node(name, label=label, **p, shape="box")
    # Add parent-child edges: from spouse node (if exists) or person to child/couple
    for rel in relationships:
        if rel["type"] == "parent":
            parent = rel["parent"]
            child = rel["child"]
            from_node = spouse_to_node.get(parent, parent)
            to_node = spouse_to_node.get(child, child)
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
        "zoomView": true,
        "multiselect": true,
        "navigationButtons": true,
        "keyboard": true,
        "tooltipDelay": 200,
        "hover": true,
        "selectConnectedEdges": true
      },
      "manipulation": {
        "enabled": false
      },
      "physics": {
        "enabled": false
      },
      "nodes": {
        "shape": "box",
        "color": {
          "background": "#ffffff",
          "border": "#1565c0",
          "highlight": {
            "background": "#e3f2fd",
            "border": "#0d47a1"
          }
        },
        "font": {
          "color": "#212121",
          "size": 22,
          "face": "Segoe UI, Arial, sans-serif"
        },
        "margin": 20
      },
      "edges": {
        "color": {
          "color": "#1976d2",
          "highlight": "#0d47a1"
        },
        "font": {
          "color": "#1976d2",
          "size": 18,
          "face": "Segoe UI, Arial, sans-serif",
          "align": "middle"
        },
        "arrows": {
          "to": {"enabled": true, "scaleFactor": 1.2}
        },
        "smooth": {
          "type": "cubicBezier"
        }
      },
      "configure": {
        "enabled": false
      }
    }
    ''')

    # Add nodes with labels and all details in the title (for popup)
    for node_id, data in G.nodes(data=True):
        if 'p1' in data and 'p2' in data:
            # Spouse node
            p1 = data['p1']
            p2 = data['p2']
            if p1.get('gender','').lower() == 'male' and p2.get('gender','').lower() == 'female':
                title = (
                    f"{p1.get('firstname','')} W/O {p2.get('firstname','')}"
                    f" Husband: {p1.get('firstname','')} ({p1.get('gender','')})"
                    f" Wife: {p2.get('firstname','')} ({p2.get('gender','')})"
                )
            elif p1.get('gender','').lower() == 'female' and p2.get('gender','').lower() == 'male':
                title = (
                    f"{p2.get('firstname','')} W/O {p1.get('firstname','')}"
                    f" Husband: {p2.get('firstname','')} ({p2.get('gender','')})"
                    f" Wife: {p1.get('firstname','')} ({p1.get('gender','')})"
                )
            else:
                # fallback for other gender combinations
                title = (
                    f"{p1.get('firstname','')} & {p2.get('firstname','')}"
                    f"{p1.get('firstname','')} ({p1.get('gender','')})"
                    f"{p2.get('firstname','')} ({p2.get('gender','')})"
                )
        else:
            # Single person node
            title = (
                f"{data.get('firstname','')}"
                f" Gender: {data.get('gender','')}"
            )
        net.add_node(node_id, label=data.get("label", str(node_id)), shape="box", title=title)

    # Add edges with relationship label
    for source, target, data in G.edges(data=True):
        relation = data.get("relation", "")
        if relation == "spouse":
            net.add_edge(source, target, label=relation, arrows="to", dashes=True, color="purple")
        else:
            net.add_edge(source, target, label=relation)


    net.save_graph("familytree.html")
    with open("familytree.html", "r", encoding="utf-8") as f:
        html = f.read()
    st.components.v1.html(html, height=650, scrolling=True)
