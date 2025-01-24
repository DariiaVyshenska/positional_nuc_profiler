import pysam
import pandas as pd
import os
import sys
from exceptions import RefError

def codon_stats_to_csv(codon_stats, output_file_path, bam_file_path, codon_start_pos):
  os.makedirs(output_file_path, exist_ok=True)
  df = pd.DataFrame(codon_stats, columns=['CODON', 'FREQUENCY', 'DEPTH'])
  df = df.sort_values(by='FREQUENCY', ascending=False)
  print(df)
  
  basename = os.path.basename(bam_file_path)
  smpl_id = basename.replace('.fastq.gz.bam', '')
  output_path = f"{output_file_path}/{smpl_id}_{'-'.join([str(pos) for pos in codon_start_pos])}_complex_freqs.csv"
  df.to_csv(output_path, index=False)

def validate_bam_index(bam_file):
    bai_file = bam_file + ".bai"
    csi_file = bam_file + ".csi"
    if not any(os.path.exists(file) for file in [bai_file, csi_file]):
      raise RefError(f'RefError: No index file found for {bam_file!r}. Please index the BAM file before proceeding.')
    
def open_and_validate_bam(bam_file):
  validate_bam_index(bam_file)
  bam = pysam.AlignmentFile(bam_file, "rb")
  if len(bam.references) != 1:
    bam.close()
    raise RefError('RefError: input .bam must contain one and only one reference (chromosome)')
  return bam