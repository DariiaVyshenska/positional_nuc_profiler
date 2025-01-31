import pysam
import pandas as pd
import os
from contextlib import contextmanager
from exceptions import RefError

def get_output_file_path(output_file_path, bam_file_path, nt_positions):
  try:
    os.makedirs(output_file_path, exist_ok=True)
  except OSError as e:
    raise ValueError(f"Failed to create output directory: {output_file_path}. Error: {e}")
  
  bam_file_basename = os.path.basename(bam_file_path)
  smpl_id = bam_file_basename.removesuffix('.fastq.gz.bam').removesuffix('.bam')
  positions_str = '-'.join(map(str, nt_positions))
  return f"{output_file_path}/{smpl_id}_{positions_str}_complex_freqs.csv"

def codon_stats_to_csv(codon_stats, output_path):
  df = pd.DataFrame(codon_stats, columns=['CODON', 'FREQUENCY', 'DEPTH'])
  df.sort_values(by='FREQUENCY', ascending=False, inplace=True)
  print("\nSelected nucleotide combinations (final results):")
  print(df)
  df.to_csv(output_path, index=False)
  
@contextmanager
def open_and_validate_bam(bam_file):
  try:
    with pysam.AlignmentFile(bam_file, "rb") as bam:
      try:
        bam.check_index()
      except ValueError as e:
        raise RefError(
          f"RefError: No index file found for {bam_file!r}. Please index the BAM file "
          f"before proceeding. Error: {e}"
        )
        
      if not bam.lengths or len(bam.references) != 1:
        raise RefError('RefError: input .bam must contain one and only one reference (chromosome)')
    
      yield bam

  except (FileNotFoundError, OSError, pysam.utils.SamtoolsError) as e:
    raise RefError(f'RefError: Failed to open BAM file: {bam_file!r}. Error: {e}')