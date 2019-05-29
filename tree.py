import numpy as np
import matplotlib.pyplot as plt

b = 5


class Node:
    def __init__(self, d, p, left, right):
        self.d = d
        self.p = p
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.left) + ' + ' + str(self.right)

    def plot(self, x_l=0, x_u=1, y_l=0, y_u=1):

        if self.d == 0:
            plt.plot([self.p, self.p], [y_l, y_u], 'b--')

            self.left.plot(x_l, self.p, y_l, y_u)
            self.right.plot(self.p, x_u, y_l, y_u)

        else:
            plt.plot([x_l, x_u], [self.p, self.p], 'b--')

            self.left.plot(x_l, x_u, y_l, self.p)
            self.right.plot(x_l, x_u, self.p, y_u)

class Leaf:
    def __init__(self, file):
        self.file = file

    def __str__(self):
        return str(self.file)

    def plot(self, x_l, x_u, y_l, y_u):
        plt.plot(self.file.data.T[0], self.file.data.T[1], 'yo')

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
