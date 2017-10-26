# wdecoster

from __future__ import print_function
import mappy as mp
import argparse
import sys
from nanolyse.version import __version__
from os import path
from Bio import SeqIO
import logging


def main():
    args = get_args()
    try:
        logging.basicConfig(
            format='%(asctime)s %(message)s',
            filename="NanoLyse.log",
            level=logging.INFO)
    except PermissionError:
        pass  # indicates that user has no write permission in this directory. No logs then
    try:
        logging.info('NanoLyse {} started with arguments {}'.format(__version__, args))
        aligner = getIndex(args.reference)
        align(aligner, sys.stdin)
        logging.info('NanoLyse finished.')
    except Exception as e:
        logging.error(e, exc_info=True)
        raise


def get_args():
    parser = argparse.ArgumentParser(
        description="""
                    Remove reads mapping to the lambda genome.
                    Reads fastq from stdin and writes to stdout.\n
                    Example usage:
                    zcat reads.fastq.gz | NanoLyse | gzip > reads_without_lambda.fastq.gz
                    """,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-v", "--version",
                        help="Print version and exit.",
                        action="version",
                        version='NanoLyse {}'.format(__version__))
    parser.add_argument("-r", "--reference",
                        help="Specify a reference fasta file against which to filter.")
    return parser.parse_args()


def getIndex(reference):
    '''
    Find the reference folder using the location of the script file
    Create the index, test if successful
    '''
    if reference:
        reffas = reference
    else:
        parent_directory = path.dirname(path.abspath(path.dirname(__file__)))
        reffas = path.join(parent_directory, "reference/lambda.fasta.gz")
    if not path.isfile(reffas):
        logging.error("Could not find reference fasta for lambda genome.")
        sys.exit("Could not find reference fasta for lambda genome.")
    aligner = mp.Aligner(reffas, preset="map-ont")  # build index
    if not aligner:
        logging.error("Failed to load/build index")
        raise Exception("ERROR: failed to load/build index")
    return aligner


def align(aligner, reads):
    '''
    Test if reads can get aligned to the lambda genome,
    if not: write to stdout
    '''
    for record in SeqIO.parse(reads, "fastq"):
        try:
            next(aligner.map(str(record.seq)))
        except StopIteration:
            print(record.format("fastq"), end='')


if __name__ == '__main__':
    main()
