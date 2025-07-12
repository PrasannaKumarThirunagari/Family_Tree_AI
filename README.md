# Family Tree AI

🌳 **Family Tree AI** is a modern, interactive web application for building, visualizing, and managing complex family trees. Designed for genealogists, families, and researchers, it combines a beautiful UI with powerful data management and visualization features.

---

## 🚀 Features

- **Add, Edit, and Delete People**: Manage detailed profiles with fields like surname, firstname, lastname, date of birth, date of death, gender, education, occupation, email, and phone number.
- **Relationship Management**: Link people as spouses, parents, and children. All relationships are normalized and stored separately for scalability.
- **Advanced Visualization**: View your family tree as an interactive, movable, and hierarchical graph. Spouses are grouped in a single box, and generations are clearly separated.
- **Modern UI**: Built with Streamlit for a fast, responsive, and user-friendly experience.
- **Data Integrity**: Robust error handling ensures all relationships reference valid people, and data is always consistent.

---

## 🛠️ Technologies Used

- **Python 3**
- **Streamlit** – UI framework for rapid web app development
- **Pandas** – Data manipulation and management
- **Pyvis** – Interactive network graph visualization
- **NetworkX** – Graph data structures and algorithms
- **HTML/CSS/JS** – Custom visualization and UI enhancements

---

## 📁 Project Structure

```
family_tree_ai/
│
├── main.py                  # Streamlit app entry point
├── requirements.txt         # Python dependencies
├── tree.html                # Generated family tree visualization
│
├── data/
│   ├── people_only.json         # All person records
│   └── relationships_only.json  # All relationship records
│
├── ui/
│   ├── ask_ai_tab.py        # AI Q&A tab (optional)
│   ├── grid_tab.py          # People/relationship management UI
│   └── tree_tab.py          # Family tree visualization UI
│
├── utils/
│   └── helpers.py           # Data loading, saving, and graph logic
│
└── lib/                     # Frontend libraries (JS/CSS)
```

---

## 📖 About the Project

Family Tree AI was created to make genealogy accessible, interactive, and visually engaging. Unlike traditional family tree tools, it uses a normalized data model (people and relationships stored separately) for maximum flexibility and scalability. The app is ideal for:

- Families wanting to preserve and explore their heritage
- Genealogists and researchers managing large, complex trees
- Anyone interested in visualizing and understanding family connections

**Key Innovations:**
- Spouses are grouped in a single node for clarity
- Generations are displayed level-wise, horizontally, with no overlap
- All data is easily exportable and maintainable

---

## 📦 Installation & Usage

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd family_tree_ai
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the app:**
   ```sh
   streamlit run main.py
   ```
4. **Open in your browser:**
   - Go to `http://localhost:8501`

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome! Please open an issue or submit a pull request.

---

## 📜 License

This project is licensed under the MIT License.

---

## 👤 Author

- Developed by [Your Name]
- [Your Contact or GitHub Profile]

---

Enjoy exploring your family history with **Family Tree AI**! 🌳
