from typing import List, Dict


class Node:
    def __init__(self, item: Dict[str, str | int | None]):
        """
        Node class.
        Storing node children and node meta.

        Args:
            item: Node meta, with id, parent and type values.
        """

        self.item = item
        self.children = []


class TreeStore:

    def __init__(self, items_: List[Dict[str, str | int | None]]):
        """
        Tree-conductor class.

        Args:
            items_: List of dict-elements that will be translated into nodes.
        """

        self.nodes_map = {}
        self.root_node = None
        self.build_tree(items_)

    def build_tree(self, items_: List[Dict[str, str | int | None]]):
        """
        Tree creator. Converts elements to nodes.

        Args:
            items_: List of dict-elements that will be translated into nodes.
        """

        for item in items_:
            self.nodes_map[item['id']] = Node(item)

        for id_, node in self.nodes_map.items():
            if node.item.get('parent') == 'root':
                self.root_node = node
            else:
                parent_node = self.nodes_map.get(node.item.get('parent'))
                if parent_node:
                    parent_node.children.append(node)
        self.print_tree()
        print()

    def print_tree(self, node: Node | None = None, indent: int = 0):
        if self.nodes_map == {}:
            return None
        if node is None:
            node = self.root_node
        print(" " * indent + str(node.item.get('id')))
        for child in node.children:
            self.print_tree(child, indent + 4)

    def get_all(self) -> List[Dict[str, str | int | None]]:
        """
        Get full list of tree elements.
        (Python version depended. Since 3.7 dictionaries save elements sequence).

        Returns:
            list: ALl elements of the tree.
        """

        return [node.item for node in self.nodes_map.values()]

    def get_item(self, id_: int) -> Dict[str, str | int | None] | None:
        """
        Get tree element by its ID.
        Args:
            id_: Element ID.

        Returns:
            Element with ID.
        """

        return self.nodes_map.get(id_).item if id_ in self.nodes_map else {}

    def get_children(self, id_: int) -> List[Dict[str, str | int | None]] | list:
        """
        Get all children of the element with an ID.

        Args:
            id_: Parent element ID.

        Returns:
            list: Sequence of children or empty list.
        """

        node = self.nodes_map.get(id_)
        return [child.item for child in node.children] if node else []

    def get_all_parents(self, id_: int) -> List[Dict[str, str | int | None]]:
        """
        Get all parents of the element with an ID.

        Args:
            id_: Children element ID.

        Returns:
            list: Sequence of parents.
        """

        parents = []
        current_node = self.nodes_map.get(id_)
        while current_node:
            parents.append(current_node.item)
            parent_id = current_node.item['parent']
            current_node = self.nodes_map.get(parent_id)
        return parents


if __name__ == '__main__':
    # Target test values ---------------------------------------
    get_item_7 = {"id": 7, "parent": 4, "type": None}
    get_children_4 = [{"id": 7, "parent": 4, "type": None},
                      {"id": 8, "parent": 4, "type": None}]
    get_children_5 = []
    get_all_parents_7 = [{"id": 7, "parent": 4, "type": None},
                         {"id": 4, "parent": 2, "type": "test"},
                         {"id": 2, "parent": 1, "type": "test"},
                         {"id": 1, "parent": "root"}]
    # ----------------------------------------------------------

    items = [
        {"id": 1, "parent": "root"},
        {"id": 2, "parent": 1, "type": "test"},
        {"id": 3, "parent": 1, "type": "test"},
        {"id": 4, "parent": 2, "type": "test"},
        {"id": 5, "parent": 2, "type": "test"},
        {"id": 6, "parent": 2, "type": "test"},
        {"id": 7, "parent": 4, "type": None},
        {"id": 8, "parent": 4, "type": None}
    ]

    ts = TreeStore(items)
    print(ts.get_all() == items)
    print(ts.get_item(7) == get_item_7)
    print(ts.get_children(4) == get_children_4)
    print(ts.get_children(5) == get_children_5)
    print(ts.get_all_parents(7) == get_all_parents_7)
