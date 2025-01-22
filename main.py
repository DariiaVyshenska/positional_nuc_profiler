#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 09:47:33 2024

@author: Dariia Vyshenska
"""
import argparse
from parsers import extract_codon_frequencies
from io_utils import codon_stats_to_csv

def main(bam_file_path, output_file_path, nucleotide_positions):
  codon_frequencies = extract_codon_frequencies(bam_file_path, nucleotide_positions)
  codon_stats_to_csv(codon_frequencies, output_file_path, bam_file_path, nucleotide_positions) # this function was not yet changed to work with a list of requested nucleotide positions

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Extracts frequencies of complex mutations from INDEXED .bam file.',
                                  usage='Usage: ./main.py <indexed_bam_path> <output_dir> <nucleotide_positions>')
  parser.add_argument('indexed_bam_path', type=str, help='Path to the INDEXED bam file')
  parser.add_argument('output_path', type=str, help='Path where the output CSV will be saved')
  parser.add_argument('nucleotide_positions', type=int, nargs='+', help='Two or more nucleotide positions in the reference. 1-based indexation.')
  
  args = parser.parse_args()
  
  if len(args.nucleotide_positions) < 2:
    parser.error("At least two integers must be provided for 'nucleotide_positions'.")
    
  # also need to check positions: it must be a list (yes, cause set is not ordered)
  # of unique values (can do without throwing error)
  
  # it must be in the range of 1 to X (not sure if I want to test out of bonds of the reference)
  # maybe test too large is by ensuring the output is empty and a message pops up that no columns match position X
  
  main(args.indexed_bam_path, args.output_path, sorted(args.nucleotide_positions))
