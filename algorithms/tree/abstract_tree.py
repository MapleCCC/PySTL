from ..queue import Queue


class Node:
    def __init__(self, data):
        self.data = data
        self.children = []

    __slots__ = ["data", "children"]

    def __str__(self):
        return "Node(data={})".format(self.data)

    def __repr__(self):
        return self.__str__()

    def copy(self):
        """Return a shallow copy"""
        # Warning: use `self.__class__` instead of `Node` or `__class__`, to avoid mistake in subclassing.
        new = self.__class__(self.data)
        new.children = self.children
        return new


class Tree:
    def __init__(self):
        self._root = None
        self._size = 0

    __slots__ = ["_root", "_size"]

    def clear(self):
        # A more memory efficient way is to deallocate all nodes. Reduce burden on gc. But it also yields overhead.
        # Unlike writing C, idiomatic writing style in Python would be to leave the task to gabbage collector.
        self._root = None
        self._size = 0
        return self

    @property
    def root(self):
        if self._root is None:
            raise KeyError("No root in an empty tree")
        return self._root.data

    @property
    def size(self):
        return self._size

    def isEmpty(self):
        return self.size == 0

    def __len__(self):
        return self.size

    @property
    def height(self):
        return self.recur_height(self._root)

    def recur_height(self, node):
        if node is None:
            return -1
        return 1 + max(self.recur_height(node.left), self.recur_height(node.right))

    def __str__(self):
        return self._recursive_str(self._root)

    def _recursive_str(self, node):
        if node is None:
            return 'An empty Tree'
        if len(node.children) == 0:
            return "Node(data={})".format(node.data)
        else:
            return "Node(data={}, children=[{}])".format(node.data, ', '.join(self._recursive_str(child) for child in node.children if child is not None))

    def __repr__(self):
        return str(self)

    def copy(self):
        """
            Return a new Tree storing copying data
            Note that data itself possibly requires further deep copy.
            This method only guarantees deep copy to the level of node.
        """
        def recur_copy(node):
            if node is None:
                return None, 0
            new_node = node.copy()
            new_size = 1
            for child in new_node.children:
                child, size = recur_copy(child)
                new_size += size
            return new_node, 1 + new_size

        new_root, new_size = recur_copy(self._root)
        # Warning: use `self.__class__` instead of `Tree` or `__class__`, to avoid mistake in subclassing.
        new_tree = self.__class__()
        new_tree._root = new_root
        new_tree._size = new_size
        return new_tree

    def __iter__(self):
        return self.traverse()

    # traversal returns an iterator, utilize power of lazy evaluation to save space and reduce overhead.
    def traverse(self, order=None):
        """
            'Generator Factory' pattern
            Calling this function will return a generator.
            Iterating over the generator will retrieve the tree node in given order.
            Note that the retrieval is real-time, which means altering the tree between two consecutive generator call may result in different results.
        """
        if order is None:
            # Use `self.__class__` instead of `__class__`, otherwise there will be errora behavior in subclassing.
            order = self.__class__.default_traversal_order

        for node in self._traverse(order):
            yield node.data

    default_traversal_order = "breadth_first_order"

    def _traverse(self, order):
        if not isinstance(order, str):
            raise ValueError("`order` should be string.")
        try:
            return getattr(self, order+"_traverse")()
        except AttributeError:
            raise ValueError("Wrong ordering chosen.")

    def pre_order_traverse(self):
        return self.recur_pre_order_traverse(self._root)

    def recur_pre_order_traverse(self, node):
        if node is None:
            return
        yield node
        for child in node.children:
            yield from self.recur_pre_order_traverse(child)

    def post_order_traverse(self):
        return self.recur_post_order_traverse(self._root)

    def recur_post_order_traverse(self, node):
        if node is None:
            return
        for child in node.children:
            yield from self.recur_post_order_traverse(child)
        yield node

    def breadth_first_order_traverse(self):
        q = Queue()
        q.enqueue(self._root)
        while not q.isEmpty():
            node = q.dequeue()
            if node is not None:
                yield node
                for child in node.children:
                    q.enqueue(child)

    # def visualize(self):
    #     q = Queue()

    #     def log(node):
    #         q.enqueue(node.key)
    #     self.traverse(log, order="pre_order")

    #     h = self.height

    #     node_num_of_full_tree = 2 ** h - 1
    #     res = node_num_of_full_tree - q.size
    #     for _ in range(res):
    #         q.enqueue(' ')
    #     print("\n")
    #     for n in range(h):
    #         margin = ' ' * (3 * h - 3 * n - 2)
    #         interval = ' ' * 5
    #         s = margin
    #         for _ in range(2 ** n):
    #             s += str(q.dequeue()) + interval
    #         s = s[:-5]
    #         s += margin
    #         print(s)
    #     print("\n")


if __name__ == '__main__':
    tree1 = Tree()
    tree1._root = Node(0)
    tree1._root.children = [Node(1), Node(2), Node(3)]
    tree1._root.children[0].children = [Node(4), Node(2), Node(3)]

    tree2 = Tree()
    tree2._root = Node(0)
    tree2._root.children = [Node(4), Node(2), Node(3)]

    print(list(tree1.pre_order_traverse()))
    print(tree1)
    print(tree2)
