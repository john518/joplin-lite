"""Utility and data transformation helpers for Joplin Lite.

This module provides pure helper functions for processing and shaping data
retrieved from the Joplin Data/API server (such as hierarchical notebook tree
sorting and depth-annotation) before it is passed across the bridge to the
frontend interface.
"""


def build_notebook_tree(raw_notebooks) -> list[dict]:
    """Transforms a raw flat list of Joplin notebook objects into a sorted, depth-annotated flat list.

        This method organizes the flat list of notebooks into a hierarchical tree based on
        their parent-child relationships, sorts the root nodes and child nodes alphanumerically
        by title (case-insensitive), and then flattens the tree structure while assigning a
        `depth` property to each notebook item for UI indentation rendering.

        Args:
            raw_notebooks (list of dict): A list of notebook dictionaries from the Joplin API,
                where each dictionary contains at least 'id', 'parent_id', and 'title'.

        Returns:
            list of dict: A flattened list of notebook dictionaries sorted hierarchically and
            alphanumerically, with an added 'depth' integer field indicating the nesting level.
    """
    # Create lookup table <id, notebook>
    notebook_map = {nb["id"]: {**nb, "children": []} for nb in raw_notebooks}
    roots = []

    for nb in raw_notebooks:
        parent_id = nb.get("parent_id")
        if parent_id and parent_id in notebook_map:
            notebook_map[parent_id]["children"].append(notebook_map[nb["id"]])
        else:
            roots.append(notebook_map[nb["id"]])

    # Sort root notebooks alphanumerically by title
    roots.sort(key=lambda x: x.get("title", "").lower())

    # Sort children for every node alphanumerically by title
    for node in notebook_map.values():
        if node["children"]:
            node["children"].sort(key=lambda x: x.get("title", "").lower())

    # Flatten into a depth-annotated list preserving the sorted hierarchy
    flattened = []

    def traverse(nodes, depth=0):
        for node in nodes:
            # Copy node without the nested children array for the flat list
            item = {k: v for k, v in node.items() if k != "children"}
            item["depth"] = depth
            flattened.append(item)
            if node["children"]:
                traverse(node["children"], depth + 1)

    traverse(roots)
    return flattened
