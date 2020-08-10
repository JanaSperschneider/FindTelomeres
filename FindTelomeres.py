"""
    A python script for finding telomeric repeats (TTAGGG/CCCTAA) in FASTA files
    Copyright (C) 2019-2020 Jana Sperschneider  
    This program is free software; you can redistribute it and/or modify  
    it under the terms of the GNU General Public License as published by  
    the Free Software Foundation; either version 3 of the License, or     
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    Contact: jana.sperschneider@csiro.au
"""
import os
import sys
from Bio import SeqIO
import re
import argparse
#--------------------------------------------
#--------------------------------------------
#--------------------------------------------
# Canonical motif is TTAGGG/CCCTAA, but one might see variation
TELOMERES = ["C{2,4}T{1,2}A{1,3}", "T{1,3}A{1,2}G{2,4}"]
#--------------------------------------------
#--------------------------------------------
#--------------------------------------------
def findTelomere(sequence):
    '''
    This function takes a nucleotide sequence and checks if the 
    start and/or end of the sequence contain telomeric repeats.
    '''
    telomere_at_start, telomere_at_end = False, False
    tel_forward, tel_reverse = TELOMERES[0], TELOMERES[1]

    for index, position in enumerate(sequence.upper()):
        if position != 'N':
            start_of_sequence_withoutNs = index
            break

    for index, position in enumerate(reversed(sequence.upper())):
        if position != 'N':
            end_of_sequence_withoutNs = index
            break
    end_of_sequence_withoutNs = len(sequence) - end_of_sequence_withoutNs

    # Look for telomeric repeats at the start of the sequence
    telomeric_repeats = re.findall(tel_forward, sequence.upper()[start_of_sequence_withoutNs:start_of_sequence_withoutNs+WINDOW])
    # Calculate the % of nucleotides that are part of telomeric repeats
    percent_telomeric_repeats_start = 100.0*sum([len(repeat) for repeat in telomeric_repeats])/float(WINDOW)

    # Look for telomeric repeats at the end of the sequence
    telomeric_repeats = re.findall(tel_reverse, sequence.upper()[(end_of_sequence_withoutNs-WINDOW):end_of_sequence_withoutNs])
    # Calculate the % of nucleotides that are part of telomeric repeats    
    percent_telomeric_repeats_end = 100.0*sum([len(repeat) for repeat in telomeric_repeats])/float(WINDOW) 

    # If more than half of nucleotides at the start/end are telomeric repeats
    if percent_telomeric_repeats_start >= REPEAT_CUTOFF:
        telomere_at_start = True
    if percent_telomeric_repeats_end >= REPEAT_CUTOFF:
        telomere_at_end = True
        
    return telomere_at_start, telomere_at_end, start_of_sequence_withoutNs, end_of_sequence_withoutNs
#--------------------------------------------
#--------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("FASTA_FILE", help="Supply a FASTA sequence file.")
parser.add_argument("-w", "--window", type=int, help="This defines the number of first and last nucleotides that will get scanned for telomeric repeats (default: 50).")
parser.add_argument("-c", "--cutoff", type=float, help='''A telomere is detected if >= c%% of the first (last) nucleotides are telomeric repeats (default: 50%%).''')
args = parser.parse_args()
#--------------------------------------------
if args.cutoff == None:
    REPEAT_CUTOFF = 50.0
else:
    REPEAT_CUTOFF = args.cutoff

if args.window == None:
    WINDOW = 50
else:
    WINDOW = args.window
#--------------------------------------------
FASTA_FILE = args.FASTA_FILE
#--------------------------------------------
sequences = [(str(record.description), str(record.seq).strip()) for record in SeqIO.parse(FASTA_FILE, "fasta")]

number_forward, number_reverse = 0, 0
print('##########')
print(len(sequences), 'sequences to analyze for telomeric repeats (TTAGGG/CCCTAA) in file', FASTA_FILE)
print('##########')
print()
#--------------------------------------------
for header, sequence in sequences:
    if sequence.count('N') == len(sequence):
        pass
    else:
        forward, reverse, start_of_sequence_withoutNs, end_of_sequence_withoutNs = findTelomere(sequence)

        if forward == True:
            print(header, '\t', 'Forward (start of sequence)', '\t', sequence[start_of_sequence_withoutNs:start_of_sequence_withoutNs+WINDOW])
            number_forward += 1
        if reverse == True:        
            print(header, '\t', 'Reverse (end of sequence)', '\t', sequence[(end_of_sequence_withoutNs-WINDOW):end_of_sequence_withoutNs])
            number_reverse += 1

print(("\nTelomeres found: {} ({} forward, {} reverse)".format(str(number_forward+number_reverse),number_forward,number_reverse)))
#--------------------------------------------
