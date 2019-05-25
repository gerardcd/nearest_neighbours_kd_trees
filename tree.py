import numpy as np

b = 10


class Node:
    def __init__(self, d, p, left, right):
        self.d = d
        self.p = p
        self.left = left
        self.right = right

    def __str__(self):
       return str(self.left) + ' + ' + str(self.right)


class Leaf:
    def __init__(self, file):
        self.file = file

    def __str__(self):
        return str(self.file)


def build_tree(file):
    if len(file.data) <= b:
        return Leaf(file)

    max_spread, d = spreadest(file)
    p = np.median(file.data, axis=0)[d]

    left_sub_file, right_sub_file = file.split(d, p)

    left_sub_tree = build_tree(left_sub_file)
    right_sub_tree = build_tree(right_sub_file)

    return Node(d, p, left_sub_tree, right_sub_tree)


def spreadest(file):
    vars = [np.var(coord_values) for coord_values in file.data.T]

    max_var = max(vars)
    max_var_coord = vars.index(max_var)

    return max_var, max_var_coord
