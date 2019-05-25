from tree import build_tree
from file import File, random_file

F = random_file(100, 10)

tree = build_tree(F)

print(tree)