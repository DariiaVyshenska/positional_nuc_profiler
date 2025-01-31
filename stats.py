from collections import Counter

def get_combo_fr_count(reads):
  tally_complete = Counter(
    repr(read) for read in reads.values() if read.complete()
    )
  total_reads = sum(tally_complete.values())
  
  if total_reads == 0:
    return []
  
  combo_fr_count = [
    (combo, round(count/total_reads, 4), count) 
    for combo, count in tally_complete.items()
    ]

  all_read_counts = Counter(repr(read) for read in reads.values()).items()
  print(f"\nTotal number of reads processed across all reference positions:\n{len(reads)}\n")
  print('All detected nucleotide combinations & their depths are:')
  for nts, count in all_read_counts:
    print(f'{nts}: {count}')
  
  return combo_fr_count