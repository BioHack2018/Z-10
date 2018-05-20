#!/usr/bin/python3
import os
from Bio import Entrez
from Bio import SeqIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML

Entrez.email = "217321@student.pwr.edu.pl"
filename = "NP_000523.fasta"
#Check if sequence was downloaded and download if not (using method from Biopython tutorial)
if not os.path.isfile(filename):
    net_handle = Entrez.efetch(db="protein", id="NP_000523", rettype="fasta", retmode="text")
    out_handle = open(filename, "w")
    out_handle.write(net_handle.read())
    out_handle.close()
    net_handle.close()
    print("Saved")

record = SeqIO.read(filename, "fasta")
print(record)

sequence = open(filename).read()

#Check if there is a file with blast results and make query if not
blast_file = "blastp_results.xml"

if not os.path.isfile(blast_file):
	print("Running BLAST...")
	blast=open(blast_file, "w")
	results = NCBIWWW.qblast("blastp", "nr", sequence)
	blast.write(results.read())
	print("Results saved")

result_handle = open(blast_file)
blast_record = NCBIXML.read(result_handle)


for alignment in blast_record.alignments:
	for hsp in alignment.hsps:
		print('sequence:', alignment.title)
		print('length:', alignment.length)
		print('e value:', hsp.expect)
		print('score:', hsp.score)
		
		

