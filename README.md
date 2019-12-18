#### What does this script do?

This is a tool for finding telomeric repeats (TTAGGG/CCCTAA) in FASTA files.

#### How does it do that?
It takes a FASTA file as input and goes through the sequences in it one by one. It ignores N's (unknown bases) at the start and the end of each sequence.

For each sequence, it will look at the first (last) 50 nts (-w/--window) and assess how much of this sequence is covered by telomeric repeats (-c/--cutoff). There is a bit of an allowance for sequencing errors/variation of telomeric motif/length of telomeres. More specifically, if >= 50% (-c/--cutoff) of the first (last) 50 nts of the region (-w/--window) is covered by telomeric repeats it will call a telomere.  

The default settings of 50% for -c/--cutoff and 50 nts for -w/--window seem to work well for most use cases.

The telomeric motifs that are used in the search are: 

```C{2,4}T{1,2}A{1,3} and T{1,3}A{1,2}G{2,4}```

#### Installation and usage
It is written in Python 3 and requires BioPython.

Just run the script as follows:

```
usage: FindTelomeres.py FASTA_FILE
```

For example:
```
python FindTelomeres.py test.fasta
```
This will output:

```
##########
2 sequences to analyze for telomeric repeats (TTAGGG/CCCTAA) in file test.fasta
##########

tig00000045 (contig with one telomere)           Forward (start of sequence)     acCTAACCTAACCTAACCTAACCCTAACCTAACCCTAACTAACCTAACCT
tig00001011 (contig with two telomeres)          Forward (start of sequence)     cctaacctaaccctaaacctaaacccaaccccCTAACCCTAACCAACCTA
tig00001011 (contig with two telomeres)          Reverse (end of sequence)       TTAGGGTTAGGTGGTTTAGGTTAGGGTTAGAGTAGTGAGGTTaggttagg
```
