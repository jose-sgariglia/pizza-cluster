import json

def view_nb(path):
    with open(path, "r") as f:
        nb = json.load(f)
    for i, cell in enumerate(nb.get("cells", [])):
        src_str = "".join(cell.get("source", []))
        if "overlapping" in src_str.lower() or "centroid" in src_str.lower():
            print(f"--- CELL {i} ({cell['cell_type']}) ---")
            print(src_str)

view_nb("src/notebooks/clustering_umap_hdbscan.ipynb")
