# wdecoster

import mappy as mp
import argparse
import sys
from nanolyse.version import __version__
from os import path


def main():
    args = getArgs()
    ind = getIndex()
    align(ind, sys.stdin)


def getArgs():
    parser = argparse.ArgumentParser(
        description="Remove reads mapping to the lambda genome, \
                     reads from stdin and writes to stdout.")
    parser.add_argument("-v", "--version",
                        help="Print version and exit.",
                        action="version",
                        version='NanoLyse {}'.format(__version__))
    return parser.parse_args()


def getIndex():
    '''
    Find the reference folder using the location of the script file
    Create the index, test if successful
    '''
    parent_directory = path.dir(path.dir(path.abspath(path.dirname(__file__))))
    reffas = path.join(parent_directory, "reference/lambda.fasta.gz")
    if not path.isfile(reffas):
        sys.exit("Could not find reference fasta for lambda genome.")
    ind = mp.Aligner(reffas)  # build index
    if not ind:
        raise Exception("ERROR: failed to load/build index")
    return ind


def align(index, reads):
    '''
    Test if reads can get aligned to the lambda genome,
    if not: write to stdout
    '''
    for name, seq, qual in mp.fastx_read(reads):  # read a fasta/q sequence
        for hit in index.map(seq):  # traverse alignments
            print("{}\t{}\t{}\t{}".format(hit.ctg, hit.r_st, hit.r_en, hit.cigar_str))


if __name__ == '__main__':
    main()
