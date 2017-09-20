# NanoLyse
Remove reads mapping to the lambda phage genome from a fastq file.  
This script uses Heng Li's [minimap2](https://github.com/lh3/minimap2) and his [mappy](https://pypi.python.org/pypi/mappy) Python binding.


### INSTALLATION
`pip install NanoLyse`

### USAGE
Reads fastq from stdin and writes to stdout.  
Simple example:  
`gunzip -c reads.fastq.gz | NanoLyse | gzip > reads_without_lambda.fastq.gz`  
In combination with [NanoFilt](https://github.com/wdecoster/nanofilt):  
`gunzip -c reads.fastq.gz | NanoLyse | NanoFilt -q 12 |gzip > filtered_reads_without_lambda.fastq.gz`  

### WARNING
If (some of) the reads of your genome of interest are sufficiently similar to the lambda genome those reads will be lost.

### STATUS
[![Build Status](https://travis-ci.org/wdecoster/nanolyse.svg?branch=master)](https://travis-ci.org/wdecoster/nanolyse) [![Code Health](https://landscape.io/github/wdecoster/nanolyse/master/landscape.svg?style=flat)](https://landscape.io/github/wdecoster/nanolyse/master)

[![Twitter URL](https://img.shields.io/twitter/url/https/twitter.com/wouter_decoster.svg?style=social&label=Follow%20%40wouter_decoster)](https://twitter.com/wouter_decoster)
