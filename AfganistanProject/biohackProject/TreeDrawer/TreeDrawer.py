import os
from subprocess import Popen, PIPE
from Bio import SeqIO
from Bio.Align.Applications import ClustalOmegaCommandline
from Bio import Phylo
from io import StringIO
# from ete3 import Tree, TreeStyle
import pylab


class TreeDrawer:

    def __init__(self, sequences=None):
        self.sequences = sequences

    def make_alignment(self, method):
        ### Mulltiple Sequence Alignment ###
        path = os.getcwd()
        in_file = "example.fasta"
        out_file = "alignment.aln"

        if os.path.isfile("alignment.aln"):
            os.remove("alignment.aln")
        clustalomega_cline = ClustalOmegaCommandline(infile=in_file, outfile=out_file, verbose=True, iterations=1,
                                                     max_guidetree_iterations=1, max_hmm_iterations=1, dealign=True,
                                                     outfmt="clu")

        print(clustalomega_cline)
        stdout, stderr = clustalomega_cline()
        ### Convert to phylip format ###
        SeqIO.convert("alignment.aln", "clustal", "alignment.phy", "phylip")
        ### Phylogentetic analysis ###
        # Choose method proml, dnaml
        # Maximum likelihood analysis #
        # Run Phylip Proml program
        instructions = bytes("alignment.phy\ny\n", 'utf-8')
        proml = Popen("phylip " + method, stdin=PIPE, shell=True)
        (out, err) = proml.communicate(instructions)
        # Change output files names
        files = Popen("mv outfile " + method + ".out", stdin=PIPE, shell=True)
        (out, err) = files.communicate()
        files = Popen("mv outtree " + method + ".tree", stdin=PIPE, shell=True)
        (out, err) = files.communicate()

    def draw_tree(self, filename):
        # instructions = bytes("dnaml.tree\nl\na\ny\n", 'utf-8')
        # dnaml = Popen("phylip drawtree", stdin=PIPE, shell=True)
        # (out, err) = dnaml.communicate(instructions)
        tree_file = open('dnaml.tree')
        x = tree_file.read()
        # t = Tree()
        # ts = TreeStyle()
        # ts.show_leaf_name = True
        # ts.branch_vertical_margin = 10  # 10 pixels between adjacent branches
        # t.show(tree_style=ts)
        tree = Phylo.read(StringIO(x[:-2]), "newick")
        Phylo.draw(tree, do_show=False)
        pylab.savefig('biohackProject/static/images/'+filename+'.png', dpi=300)
