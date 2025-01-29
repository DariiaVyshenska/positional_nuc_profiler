from collections import Counter

def get_combo_fr_count(reads):
  complete_nt_combos = [repr(read) for read in reads.values() if read.complete()]
  total_reads = len(complete_nt_combos)
  tally = Counter(complete_nt_combos)
  combo_fr_count = [ (combo, round(count/total_reads, 4), count) for combo, count in tally.items()]

  print(f"\nTotal number of reads processed across all reference positions:\n{len(reads)}\n")
  print('All detected nucleotide combinations & their depths are:')
  for nts, count in Counter(repr(read) for read in reads.values()).items():
    print(f'{nts}: {count}')
  
  return combo_fr_count