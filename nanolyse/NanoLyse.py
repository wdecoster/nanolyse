# wdecoster

from __future__ import print_function
import mappy as mp
from argparse import HelpFormatter, ArgumentParser
import sys
from nanolyse.version import __version__
from os import path
from Bio import SeqIO
import logging
import textwrap as _textwrap


class CustomHelpFormatter(HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)
        return ', '.join(action.option_strings) + ' ' + args_string

    def _fill_text(self, text, width, indent):
        return ''.join(indent + line for line in text.splitlines(keepends=True))

    def _split_lines(self, text, width):
        text = self._whitespace_matcher.sub(' ', text).strip()
        return _textwrap.wrap(text, 80)


def custom_formatter(prog):
    return CustomHelpFormatter(prog)


def main():
    args = get_args()
    try:
        logging.basicConfig(
            format='%(asctime)s %(message)s',
            filename=args.logfile,
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
    epilog = """EXAMPLES:
    gunzip -c reads.fastq.gz | NanoLyse | gzip > reads_without_lambda.fastq.gz
    gunzip -c reads.fastq.gz | NanoLyse | NanoFilt -q 12 | gzip > filtered_reads_without_lambda.fastq.gz
    gunzip -c reads.fastq.gz | NanoLyse --reference mygenome.fa.gz | gzip > reads_without_mygenome.fastq.gz
    """
    parser = ArgumentParser(
        description="Remove reads mapping to the lambda genome. Reads fastq from stdin and writes to stdout.",
        epilog=epilog,
        formatter_class=custom_formatter,
        add_help=False)
    general = parser.add_argument_group(
        title='General options')
    general.add_argument("-h", "--help",
                         action="help",
                         help="show the help and exit")
    general.add_argument("-v", "--version",
                         help="Print version and exit.",
                         action="version",
                         version='NanoLyse {}'.format(__version__))
    parser.add_argument("-r", "--reference",
                        help="Specify a reference fasta file against which to filter.")
    parser.add_argument("--logfile",
                        help="Specify the path and filename for the log file.",
                        default="NanoLyse.log")
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
        reffas = path.join(parent_directory, "reference/DNA_CS.fasta")
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
    i = 0
    for record in SeqIO.parse(reads, "fastq"):
        try:
            next(aligner.map(str(record.seq)))
            i += 1
        except StopIteration:
            print(record.format("fastq"), end='')
    sys.stderr.write("NanoLyse: removed {} reads.\n".format(i))
    logging.info("NanoLyse: removed {} reads.\n".format(i))


if __name__ == '__main__':
    main()
