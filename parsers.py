import pysam
import sys
from stats import get_combo_fr_count
from collections import defaultdict
from io_utils import open_and_validate_bam
from models import Read
from exceptions import RefError

def process_pileup(bam, nucleotide_positions, min_base_qual, min_mapping_qual, max_depth):
  sorted_nt_pos = sorted(nucleotide_positions)
  updated_nt_pos = [pos - 1 for pos in sorted_nt_pos]
  pileup_start = updated_nt_pos[0]
  pileup_end = nucleotide_positions[-1]
  if pileup_end > bam.lengths[0]:
    raise RefError('RefError: one or more nucleotide_positions exceed the length of the reference sequence.')
  
  reads = defaultdict(lambda: Read(updated_nt_pos))
  ref_name = bam.references[0]

  for pileup_column in bam.pileup(reference=ref_name, 
                                  start=pileup_start, 
                                  stop=pileup_end, 
                                  min_base_quality=min_base_qual,
                                  min_mapping_quality=min_mapping_qual,
                                  max_depth=max_depth, 
                                  truncate=True):
    ref_pos = pileup_column.reference_pos
    if ref_pos not in updated_nt_pos:
      continue

    print("Processing reference position: ", ref_pos + 1)

    for pileup_read in pileup_column.pileups:
      read_pos = pileup_read.query_position
      if read_pos is None:
        continue
      
      read_id = pileup_read.alignment.query_name
      read_seq = pileup_read.alignment.query_sequence
      reads[read_id].nucleotides[ref_pos] = read_seq[read_pos]

  return reads


def extract_nt_combo_frequencies(bam_file, nt_args):
  with open_and_validate_bam(bam_file) as bam:
    return get_combo_fr_count(process_pileup(bam, **nt_args))