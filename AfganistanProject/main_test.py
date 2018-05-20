from biohackProject.Retriever.Retriever import Retriever
from biohackProject.TreeDrawer.TreeDrawer import TreeDrawer

import os

print(os.getcwd())

ret = Retriever()
#, "34333388"
gi1 = ["27527613", "1373737504", "34333388"]
gi2 = ["34333388"]
x = ret.retrieve_blast_data(gi=gi1, filename="example.fasta", n=50)
print(x.keys())

tree = TreeDrawer()
tree.make_alignment(method="dnaml")
tree.draw_tree("tree.png")




