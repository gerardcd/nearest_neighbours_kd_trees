import math

import numpy as np
import heapq

from tree import build_tree, Leaf
from file import File, random_file

N = 3
k = 2
m = 2

# Build the Data File and store it in a new kd-tree
F = File([[0,0], [1,1], [0,3]])
tree = build_tree(F)

class Done(Exception):
    pass


# Global variables

Xq = [0,2]                                          # Query record
PQD = [math.inf for _ in range(m)]                  # Priority queue of the m closest distances encountered at any phase of the search
PQR = [None for _ in range(m)]                      # Priority queue of the record numbers of the corresponding m best matches encountered at any phase of the search
Bu = [math.inf for _ in range(k)]                   # Coordinate upper bounds
Bl = [-math.inf for _ in range(k)]                  # Coordinate lower bounds

# Search method
def search(node):
    if isinstance(node, Leaf):
        search_in_leaf(node)
        if ball_within_bounds():
            raise Done()
        else:
            return

    d = node.d; p = node.p

    # Recursive call on closer son
    if Xq[d] <= p:
        temp = Bu[d]; Bu[d] = p
        search(node.left); Bu[d] = temp
    else:
        temp = Bl[d]; Bl[d] = p
        search(node.right); Bl[d] = temp

    # Recursive call on farther son, if necessary
    if Xq[d] <= p:
        temp = Bl[d]; Bl[d] = p
        if bounds_overlap_ball():
            search(node.right)
        Bl[d] = temp
    else:
        temp = Bu[d]; Bu[d] = p
        if bounds_overlap_ball():
            search(node.left)
        Bu[d] = temp

    # See if we should return or terminate
    if ball_within_bounds():
        raise Done()
    else:
        return

def search_in_leaf(node):
    data = node.file.data

    for x in data:
        distance = 0

        for d in range(k):
            distance += coordinate_distance(d, Xq[d], x[d])

        distance = dissim(distance)

        i = 0
        while i < m and distance < PQD[i]:
            if i > 0:
                PQD[i-1] = PQD[i]
                PQR[i-1] = PQR[i]

            i += 1

        i -= 1
        if i >= 0:
            PQD[i] = distance
            PQR[i] = x


def ball_within_bounds():
    for d in range(k):
        if coordinate_distance(d, Xq[d], Bl[d]) <= PQD[1] or coordinate_distance(d, Xq[d], Bl[d]) <= PQD[1]:
            return False

    return True


def bounds_overlap_ball():
    sum = 0
    for d in range(k):

        # Lower than low boundary
        if Xq[d] < Bl[d]:
            sum += coordinate_distance(d, Xq[d], Bl[d])
            if dissim(sum) > PQD[1]:
                return True

        # Higher than high boundary
        elif Xq[d] > Bu[d]:
            sum += coordinate_distance(d, Xq[d], Bu[d])
            if dissim(sum) > PQD[1]:
                return True

    return False

def coordinate_distance(d, x_d, y_d):
    return math.fabs(x_d - y_d) ** 2


def dissim(x):
    return x ** (1/2)

try:
    search(tree)
except Done as d:
    print('Done')
    print(PQR)