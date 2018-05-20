#!/usr/bin/python3
import os
from Bio import Entrez
from Bio import SeqIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML

Entrez.email = "217321@student.pwr.edu.pl"
# Open list of species
gene = 'hsp65'
organism = 'Mycobacterium tuberculosis'
accession = 'JF491311'

query = '(' + organism + '[Organism]) AND' + gene  + '[Gene Name]'
results = NCBIWWW.qblast("blastn", "nt", accession,  entrez_query = query)
blast_res = NCBIXML.parse(results)
blast_list = list(blast_res)[0]

for alignment in blast_list.alignments:


