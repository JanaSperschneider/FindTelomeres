#### What does this script do?

This is a tool for finding telomeric repeats (TTAGGG/CCCTAA) in FASTA files.

#### What does this script NOT do?

It will only look for telomeres at the start and end of the sequences. It only looks for variations of the TTAGGG/CCCTAA repeats.

#### How does it do that?
It takes a FASTA file as input and goes through the sequences in it one by one. It ignores N's (unknown bases) at the start and the end of each sequence.

For each sequence, it will look at the first (last) 50 nts and assess how much of this sequence is covered by telomeric repeats. This is deliberately flexible to allow for sequencing errors and sequence/length variation of telomeric motifs. More specifically, if >= 50% of the first (last) 50 nts are covered by telomeric repeats, it will call a telomere.  

The default settings of 50% (-c/--cutoff) and 50 nts (-w/--window) seem to work well for most use cases. Some telomeres can be very short or vary from the canonical TTAGGG/CCCTAA motif. With these parameters they will likely be recovered. However, the parameters can be set differently.

The telomeric motifs that are used in the search are these regular expressions: C{2,4}T{1,2}A{1,3} and T{1,3}A{1,2}G{2,4}. They can be changed by editing one line in the script to suit other needs.

#### Installation and usage
The script is written in Python 3 and requires BioPython (https://biopython.org/wiki/Download).

After installing Python 3 and BioPython, run the script as follows:

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
