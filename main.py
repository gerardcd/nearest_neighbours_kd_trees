import math
import time
import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from tree import build_tree, Leaf
from file import File

N = int(sys.argv[1])
k = 10
m = 10

# Build the Data File and store it in a new kd-tree
data = np.random.normal(0.5, 0.1, (N, k)) # Normal distribution
#data = np.random.rand(N, k)    # Uniform distribution

F = File(data)
tree = build_tree(F)


# Global variables

Xq = np.random.rand(k)                              # Query record
PQD = [math.inf for _ in range(m)]                  # Priority queue of the m closest distances encountered at any phase of the search
PQR = [None for _ in range(m)]                      # Priority queue of the record numbers of the corresponding m best matches encountered at any phase of the search
Bu = [math.inf for _ in range(k)]                   # Coordinate upper bounds
Bl = [-math.inf for _ in range(k)]                  # Coordinate lower bounds

# Only works for the k == 2 case
if k == 2:
    tree.plot()
    plt.plot(Xq[0], Xq[1], 'bo')
    plt.show()

class Done(Exception):
    pass


def search(node):
    print_status()

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
        if coordinate_distance(d, Xq[d], Bl[d]) <= PQD[0] or coordinate_distance(d, Xq[d], Bu[d]) <= PQD[0]:
            return False

    return True


def bounds_overlap_ball():
    sum = 0
    for d in range(k):

        # Lower than low boundary
        if Xq[d] < Bl[d]:
            sum += coordinate_distance(d, Xq[d], Bl[d])
            if dissim(sum) < PQD[0]:
                return True

        # Higher than high boundary
        elif Xq[d] > Bu[d]:
            sum += coordinate_distance(d, Xq[d], Bu[d])
            if dissim(sum) < PQD[0]:
                return True

    return False


def coordinate_distance(d, x_d, y_d):
    return math.fabs(x_d - y_d) ** 2


def dissim(x):
    return x ** (1/2)


def print_status():
    # Only works for the k == 2 case
    if k != 2:
        return

    np_PQR = np.array([PQR[i] for i in range(m) if PQR[i] is not None])

    fig, ax = plt.subplots(1)

    x_l = min(max(Bl[0], 0), 1)
    x_u = min(max(Bu[0], 0), 1)

    y_l = min(max(Bl[1], 0), 1)
    y_u = min(max(Bu[1], 0), 1)

    rect = patches.Rectangle((x_l, y_l), x_u - x_l, y_u - y_l, linewidth=1, edgecolor='r', facecolor='none')

    circle = plt.Circle((Xq[0], Xq[1]), PQD[0], color='b', fill=False)

    tree.plot()
    plt.plot(Xq[0], Xq[1], 'bo')

    if len(np_PQR) > 0:
        plt.plot(np_PQR.T[0], np_PQR.T[1], 'go')

    ax.add_patch(rect)
    ax.add_artist(circle)

    plt.show()

    time.sleep(0.5)

start = time.time()
try:
    search(tree)
except Done as d:
    print('Done')
    end = time.time()
    elapsed = end - start
    print(str(elapsed) + " s")
    print(PQR)
    print_status()

