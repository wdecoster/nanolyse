# wdecoster

import mappy as mp
a = mp.Aligner("test/MT-human.fa")  # load or build index
if not a:
    raise Exception("ERROR: failed to load/build index")
for name, seq, qual in mp.fastx_read("test/MT-orang.fa"):  # read a fasta/q sequence
    for hit in a.map(seq):  # traverse alignments
        print("{}\t{}\t{}\t{}".format(hit.ctg, hit.r_st, hit.r_en, hit.cigar_str))
