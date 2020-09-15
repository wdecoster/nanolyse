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
        if args.summary_in:
            import tempfile
            tmp = tempfile.TemporaryFile()
            filter_reads(aligner, sys.stdin, tmp=tmp)
            logging.info('Filtering the summary file.')
            filter_summary(args.summary_in, args.summary_out, tmp)
        else:
            filter_reads(aligner, sys.stdin)
        logging.info('NanoLyse finished.')
    except Exception as e:
        logging.error(e, exc_info=True)
        raise


def get_args():
    epilog = """EXAMPLES:
    gunzip -c reads.fastq.gz | NanoLyse | gzip > reads_without_lambda.fastq.gz
    gunzip -c reads.fastq.gz | NanoLyse | NanoFilt -q 12 | gzip > filt_reads_without_lambda.fastq.gz
    gunzip -c reads.fastq.gz | NanoLyse --reference mydb.fa.gz | gzip > reads_without_mydb.fastq.gz
    """
    parser = ArgumentParser(
        description="Remove reads mapping to DNA CS. Reads fastq on stdin and writes to stdout.",
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
    parser.add_argument("--summary_in", help="Summary file to filter")
    parser.add_argument("--summary_out", help="with --summary_in: name of output file.")
    parser.add_argument("-r", "--reference",
                        help="Specify a fasta file against which to filter. Standard is DNA CS.")
    parser.add_argument("--logfile",
                        help="Specify the path and filename for the log file.",
                        default="NanoLyse.log")
    args = parser.parse_args()
    if bool(args.summary_in) != bool(args.summary_out):
        sys.exit("ERROR: With --summary_in also --summary_out is required and vice versa!")
    return args


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


def filter_reads(aligner, reads, tmp=None):
    '''
    Test if reads can get aligned to the lambda genome,
    if not: write to stdout

    if tmp is not None, then write lambda read identifiers to this file
    To filter the summary file on later
    '''
    i = 0
    for record in SeqIO.parse(reads, "fastq"):
        try:
            next(aligner.map(str(record.seq)))
            i += 1
            if tmp:
                tmp.write(record.id.encode('utf-8') + b"\n")
        except StopIteration:
            print(record.format("fastq"), end='')
    sys.stderr.write("NanoLyse: removed {} reads.\n".format(i))
    logging.info("NanoLyse: removed {} reads.".format(i))


def filter_summary(summary_file, output, read_ids_file):
    '''
    Optional function to filter entries from a sequencing_summary file
    using a read_ids_file (tmp) to which the identifiers have been written
    '''
    read_ids_file.seek(0)
    lambda_identifiers = [line.rstrip() for line in read_ids_file]
    sys.stderr.write(f"{len(lambda_identifiers)} lambda reads to remove from the summary\n")
    i = 0
    j = 0
    with open(output, 'wb') as summary_out, open(summary_file, 'rb') as summary_in:
        header = next(summary_in)
        summary_out.write(header)
        try:
            index = header.split(b'\t').index(b'read_id')
        except ValueError:
            sys.stderr.write("ERROR: Filtering your FASTQ went okay.\n")
            sys.stderr.write("But something unexpected happened with the summary file.\n")
            sys.stderr.write("Header which NanoLyse was trying to parse: {}\n".format(header))
            raise
        for line in summary_in:
            i += 1
            if not line.split(b'\t')[index] in lambda_identifiers:
                summary_out.write(line)
                j += 1
    sys.stderr.write(f"summary had {i} lines, of which {j} got kept\n")


if __name__ == '__main__':
    main()
