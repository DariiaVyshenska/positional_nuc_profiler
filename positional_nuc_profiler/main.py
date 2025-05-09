#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 09:47:33 2024

@author: Dariia Vyshenska
"""
import argparse
import sys
import logging
from positional_nuc_profiler.parsers import extract_nt_combo_frequencies
from positional_nuc_profiler.io_utils import nt_combo_stats_to_csv, get_output_file_path

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)]
)

def run_profiler(bam_file_path, output_file_path, nt_args):
  try:
    nt_combo_frequencies = extract_nt_combo_frequencies(bam_file_path, nt_args)
    
    if not nt_combo_frequencies:
      print("no data to support stats extraction. Exiting program... ")
      sys.exit(0)
    
    output_path = get_output_file_path(
      output_file_path, bam_file_path, nt_args["nucleotide_positions"]
      )
    nt_combo_stats_to_csv(nt_combo_frequencies, output_path)
    logging.info(
      "Processing complete.\n"
      f"Results saved to: {output_path}"
      )
  except Exception as e:
    logging.error(f"An error occured: {e}")
    sys.exit(1)

def main():
  parser = argparse.ArgumentParser(description='Extracts frequencies of complex mutations from INDEXED .bam file.',
                                usage='Usage: positional_nuc_profiler <indexed_bam_path> <output_dir> <nucleotide_positions> [--min_base_quality BASE_QUAL] [--min_mapping_quality MAP_QUAL] [--max_depth DEPTH]',
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('indexed_bam_path', type=str, help='Path to the INDEXED bam file')
  parser.add_argument('output_path', type=str, help='Path to a directory where the output CSV will be saved')
  parser.add_argument('nucleotide_positions', type=int, nargs='+', help='Two or more unique, positive nucleotide positions in the reference (1-based indexing).')
  parser.add_argument('--min_base_qual', type=int, default=13, metavar='', help='Minimum base quality. Bases below the minimum quality will not be counted in.')
  parser.add_argument('--min_mapping_qual', type=int, default=0, metavar='', help='Mininum mapping quality. Only use reads above a minimum mapping quality.')
  parser.add_argument('--max_depth', type=int, default=8000, metavar='', help='Maximum read depth permitted.')
  
  args = parser.parse_args()
  
  nucleotide_positions = sorted(list(set(args.nucleotide_positions)))
  if len(nucleotide_positions) < 2:
    parser.error("nucleotide_positions must include at least two unique positions (1-based index).")
  
  if nucleotide_positions[0] < 1:
    parser.error("nucleotide_positions must contain only positive integers (1-based index).")

  nt_args = {
      "nucleotide_positions": nucleotide_positions,
      "min_base_qual": args.min_base_qual,
      "min_mapping_qual": args.min_mapping_qual,
      "max_depth": args.max_depth,
  }
  
  run_profiler(args.indexed_bam_path, args.output_path, nt_args)

if __name__ == '__main__':
  main()