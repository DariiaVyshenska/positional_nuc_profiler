import logging
from collections import Counter

def get_combo_fr_count(reads):
  tally_complete = Counter(
    repr(read) for read in reads.values() if read.complete()
    )
  total_reads = sum(tally_complete.values())

  logging.info("Number of reads used for final frequency estimation: " 
               f"{total_reads}\n")
  if total_reads == 0:
    return []
  
  combo_fr_count = [
    (combo, round(count/total_reads, 4), count) 
    for combo, count in tally_complete.items()
    ]

  all_read_counts = Counter(repr(read) for read in reads.values()).items()
  logging.info(f"All detected nucleotide combinations & their depths are:\n%s\n",
               "\n".join(f"{nt}: {count}" for nt, count in all_read_counts))
  
  return combo_fr_count