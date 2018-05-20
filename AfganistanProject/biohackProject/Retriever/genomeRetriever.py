from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio import Entrez
from Bio import SeqIO
import os


class genomeRetriever:

    @staticmethod
    def retrieve_blast_data(gi="1190661737", filename="example.fasta", n=10):

        Entrez.email = "asiakXX@wp.pl"
        search_term = "Mycobacterium Tuberculosis[orgn] AND complete genome[title]"
        handle = Entrez.esearch(db='nucleotide', term=search_term)
        result = Entrez.read(handle)
        handle.close()
        genome_id = result['IdList'][0]
        Entrez.email = "A.N.Other@example.com"

        if not os.path.isfile("my_blast.xml"):

            with Entrez.efetch(db="nucleotide", rettype="fasta", retmode="text", id=genome_id) as handle:
                seq_record = SeqIO.read(handle, "fasta")
            print("%s with %i features" % (seq_record.id, len(seq_record.features)))

        with open(filename, "w") as ofile:
            for i in range(len(aligned_seqs_seqs)):
                #print(aligned_seqs_names[i])
                ofile.write(">" + aligned_seqs_names[i] + "\n" + aligned_seqs_seqs[i] + "\n")
        ofile.close()

        seq_dict = dict(zip(aligned_seqs_names, aligned_seqs_seqs))
        return seq_dict