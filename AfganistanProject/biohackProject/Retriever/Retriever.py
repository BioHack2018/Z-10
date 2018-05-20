from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio import Entrez
from Bio import SeqIO

import os


class Retriever:

    @staticmethod
    def retrieve_blast_data(gi=["27527613"], filename="example.fasta", n=5):
        #os.chdir(os.getcwd())
        #print(os.getcwd())
        # 27527613; 1373737504; 34333388

        Entrez.email = "A.N.Other@example.com"
        with Entrez.efetch(db="nucleotide", rettype="fasta", retmode="text", id="27527613") as handle:
            seq_record = SeqIO.read(handle, "fasta")
        excluded = " ".join(seq_record.description.split(" ")[1:3])
        seqs_names = list()
        seqs_seqs = list()
        for gi_num in gi:
            if not os.path.isfile("my_blast.xml"):
                print("Running BLAST")
                GI = gi_num
                print(GI)
                print(excluded)
                tmp = excluded.split()
                ent_que = "{0}[Organism] NOT {1}[Organism]".format(tmp[0], excluded)
                print(ent_que)
                #result_handle_pre = NCBIWWW.qblast("blastn", "nr", "27527613", hitlist_size=n)
                result_handle_pre = NCBIWWW.qblast("blastn", "nr", GI, hitlist_size=n, entrez_query=ent_que)
                with open("my_blast.xml", "w") as out_handle:
                    out_handle.write(result_handle_pre.read())
            result_handle = open("my_blast.xml")

            blast_res = NCBIXML.parse(result_handle)
            blast_list = list(blast_res)[0]
            result_handle.close()

            aligned_seqs_names = list()
            aligned_seqs_seqs = list()
            for alignment in blast_list.alignments:
                for hsp in alignment.hsps:
                    name_pre = alignment.title.split('|')[4].strip(' ').split(" ")[0:2]
                    name = name_pre[0][0] + "_" + name_pre[1][0:8]
                    if hsp.expect < 0.04 and name not in aligned_seqs_names:
                        print('name: ', alignment.title)
                        #print('identities: ', hsp.identities)
                        #print('strand: ', hsp.strand)
                        #print('frame: ', hsp.frame)
                        #print('query: ', hsp.query)
                        print('subject: ', hsp.sbjct)
                        #aligned_seqs[alignment.title] = hsp.sbjct
                        aligned_seqs_names.append(name)
                        aligned_seqs_seqs.append(hsp.sbjct)
            excluded_name = excluded.strip(' ').split(" ")[0:2]
            aligned_seqs_names.append(excluded_name[0][0] + "_" + excluded_name[1][0:8])
            aligned_seqs_seqs.append(blast_list.alignments[4].hsps[0].query)
            seqs_names.append(aligned_seqs_names)
            seqs_seqs.append(aligned_seqs_seqs)
            print('aligned_seqs_seqs', len(aligned_seqs_seqs))
            os.remove("my_blast.xml")
        print('seqs_seqs', len(seqs_seqs))

        #MERGE THEM ALL
        seqs_ls = list()
        result = list(set(seqs_names[0]).intersection(*seqs_names))
        for i in range(len(seqs_names)):
            names_idx = [seqs_names[0].index(name) for name in result]
            seqs = [seqs_seqs[i][idx] for idx in names_idx]
            seqs_ls.append(seqs)
        cat_seqs = list()
        for i in range(len(seqs_ls[0])):
            cat_seqs.append("".join([s[i] for s in seqs_ls]))

        with open(filename, "w") as ofile:
            for i in range(len(cat_seqs)):
                #print(aligned_seqs_names[i])
                ofile.write(">" + result[i] + "\n" + cat_seqs[i] + "\n")
        ofile.close()

        seq_dict = dict(zip(result, cat_seqs))
        return seq_dict

    @staticmethod
    def intersect(*d):
        sets = iter(map(set, d))
        result = sets.next()
        for s in sets:
            result = result.intersection(s)
        return result


