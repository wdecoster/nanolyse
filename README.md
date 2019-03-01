# NanoLyse
Remove reads mapping to the lambda phage genome from a fastq file.  
This script uses Heng Li's [minimap2](https://github.com/lh3/minimap2) and his [mappy](https://pypi.python.org/pypi/mappy) Python binding.

[![Twitter URL](https://img.shields.io/twitter/url/https/twitter.com/wouter_decoster.svg?style=social&label=Follow%20%40wouter_decoster)](https://twitter.com/wouter_decoster)
[![Build Status](https://travis-ci.org/wdecoster/nanolyse.svg?branch=master)](https://travis-ci.org/wdecoster/nanolyse)
[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat-square)](http://bioconda.github.io/recipes/nanolyse/README.html)


### INSTALLATION
`pip install NanoLyse`

### USAGE
```
Reads fastq from stdin and writes to stdout.  

NanoLyse [-h] [-v] [-r REFERENCE]

                    Remove reads mapping to the lambda genome.
                    Reads fastq from stdin and writes to stdout.

                    Example usage:
                    zcat reads.fastq.gz | NanoLyse | gzip > reads_without_lambda.fastq.gz


optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Print version and exit.
  -r REFERENCE, --reference REFERENCE
                        Specify a reference fasta file against which to filter.
```


### WARNING
If (some of) the reads of your genome of interest are sufficiently similar to the lambda genome those reads will be lost.

### EXAMPLES
`gunzip -c reads.fastq.gz | NanoLyse | gzip > reads_without_lambda.fastq.gz`  
In combination with [NanoFilt](https://github.com/wdecoster/nanofilt):  
`gunzip -c reads.fastq.gz | NanoLyse | NanoFilt -q 12 | gzip > filtered_reads_without_lambda.fastq.gz`  
Using a different genome to filter on (rather than lambda phage):  
`gunzip -c reads.fastq.gz | NanoLyse --reference mygenome.fa.gz | gzip > reads_without_mygenome.fastq.gz`  









I welcome all suggestions, bug reports, feature requests and contributions. Please leave an [issue](https://github.com/wdecoster/nanolyse/issues) or open a pull request. I will usually respond within a day, or rarely within a few days.


## CITATION
If you use this tool, please consider citing our [publication](https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/bty149/4934939).
