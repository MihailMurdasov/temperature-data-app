from Node import Node

class RedBlackTree:
    def __init__(self):
        self.TNULL = Node(None)
        self.TNULL.color = "BLACK"
        self.root = self.TNULL
        self.min_key = float('inf')
        self.max_key = float('-inf')

    def insert(self, key):
        new_node = Node(key)
        new_node.left = self.TNULL
        new_node.right = self.TNULL
        parent = None
        current = self.root

        while current != self.TNULL:
            parent = current
            if key == current.key:
                current.count += 1
                return
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent
        if not parent:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        if (new_node.parent is None):
            new_node.color = "BLACK"
            return

        if (new_node.parent.parent == None):
            return

        self.min_key = min(self.min_key, key)
        self.max_key = max(self.max_key, key)

        self._fix_insert(new_node)

    def _fix_insert(self, node):
        while node != self.root and node.parent.color == "RED":
            if node.parent == node.parent.parent.right:
                uncle = node.parent.parent.left
                if uncle.color == "RED":
                    uncle.color = "BLACK"
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._left_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.right
                if uncle.color == "RED":
                    uncle.color = "BLACK"
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._right_rotate(node.parent.parent)
        self.root.color = "BLACK"

    def _left_rotate(self, node):
        y = node.right
        node.right = y.left
        if y.left != self.TNULL:
            y.left.parent = node
        y.parent = node.parent
        if not node.parent:
            self.root = y
        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y
        y.left = node
        node.parent = y

    def _right_rotate(self, node):
        y = node.left
        node.left = y.right
        if y.right != self.TNULL:
            y.right.parent = node
        y.parent = node.parent
        if not node.parent:
            self.root = y
        elif node == node.parent.right:
            node.parent.right = y
        else:
            node.parent.left = y
        y.right = node
        node.parent = y

    def inorder(self):
        nodes = []
        self._inorder_helper(self.root, nodes)
        return nodes

    def _inorder_helper(self, node, nodes):
        if node != self.TNULL:
            self._inorder_helper(node.left, nodes)
            nodes.append((node.key, node.count))
            self._inorder_helper(node.right, nodes)

    def find_count(self, key):
        current = self.root
        while current != self.TNULL:
            if key == current.key:
                return current.count
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return 0