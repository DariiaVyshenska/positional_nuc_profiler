import pysam
import sys
from collections import defaultdict, Counter
from utils import calc_freq
from io_utils import open_and_validate_bam
from exceptions import RefError

class Read():
  def __init__(self, positions):
    self.nucleotides = {pos: None for pos in positions}
  
  def __repr__(self):
    return ''.join([nt if nt else 'N' for nt in self.nucleotides.values()])

  def complete(self):
    return all(list(self.nucleotides.values()))
  
def process_pileup(bam, nucleotide_positions, min_base_qual, min_mapping_qual, max_depth):    
  updated_nt_pos = [pos - 1 for pos in sorted(nucleotide_positions)]
  pileup_start = updated_nt_pos[0]
  pileup_end = nucleotide_positions[-1]
  if pileup_end > bam.lengths[0]:
    bam.close()
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
    
    print("Current position is: ", ref_pos) # tmp, for dev mode

    for pileup_read in pileup_column.pileups:

      read_pos = pileup_read.query_position
      read_id = pileup_read.alignment.query_name
      read_seq = pileup_read.alignment.query_sequence
        
      if read_pos is None:
        continue

      reads[read_id].nucleotides[ref_pos] = read_seq[read_pos]

  complete_nt_combos = [repr(read) for read in reads.values() if read.complete()]
  total_reads = len(complete_nt_combos)
  tally = Counter(complete_nt_combos)
  combo_fr_count = [ (combo, round(count/total_reads, 4), count) for combo, count in tally.items()]

  print("total length is: ", len(reads))  #temporary
  print("full tally")  #temporary
  print(Counter([repr(read) for read in reads.values()]))  #temporary
  
  return combo_fr_count

# collect nt positions and andy defaults into **kwarg (check the spelling here)
def extract_codon_frequencies(bam_file, nt_args):
  try:
    bam = open_and_validate_bam(bam_file)
    # codon_counts, total_reads = process_pileup(bam, codon_start_pos)  # check if this is still needed
    # return calc_freq(codon_counts, total_reads)

    return process_pileup(bam, **nt_args)
  except Exception as e:
    print(e)
    sys.exit(1)

