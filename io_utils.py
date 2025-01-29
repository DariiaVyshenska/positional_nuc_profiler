import pysam
import pandas as pd
import os
import sys
from exceptions import RefError

def get_output_file_path(output_file_path, bam_file_path, nt_positions):
  try:
    os.makedirs(output_file_path, exist_ok=True)
  except OSError as e:
    raise ValueError(f"Failed to create output directory: {output_file_path}. Error: {e}")
  
  bam_file_basename = os.path.basename(bam_file_path)
  smpl_id = bam_file_basename.removesuffix('.fastq.gz.bam').removesuffix('.bam')
  positions_str = '-'.join([str(pos) for pos in nt_positions])
  return f"{output_file_path}/{smpl_id}_{positions_str}_complex_freqs.csv"

def codon_stats_to_csv(codon_stats, output_path):
  df = pd.DataFrame(codon_stats, columns=['CODON', 'FREQUENCY', 'DEPTH'])
  df = df.sort_values(by='FREQUENCY', ascending=False)
  print("\nSelected nucleotide combinations (final results):")
  print(df)
  df.to_csv(output_path, index=False)

def validate_bam_index(bam_file):
    bai_file = bam_file + ".bai"
    csi_file = bam_file + ".csi"
    if not any(os.path.exists(file) for file in [bai_file, csi_file]):
      raise RefError(f'RefError: No index file found for {bam_file!r}. Please index the BAM file before proceeding.')
    
def open_and_validate_bam(bam_file):
  bam = pysam.AlignmentFile(bam_file, "rb")
  validate_bam_index(bam_file)
  if len(bam.references) != 1:
    bam.close()
    raise RefError('RefError: input .bam must contain one and only one reference (chromosome)')
  return bam