# Positional Nucleotide Profiler

## Introduction
**Positional Nucleotide Profiler** analyzes nucleotide co-occurrence within sequencing reads to determine linkage between distant positions. It is particularly useful for detecting whether specific mutations (SNVs) occur on the same strand. While primarily designed for viral genome analysis, it can be used with any BAM file that contains a single reference genome.

_Example:_ A researcher must know if two SNVs within the sequencing read length distance appear on the same or different strand. They have 1x100bp sequencing data, and the two SNVs of interest are at reference genome positions 20 and 100.


## Installation

### Installation with `pip` from GitHub
To avoid conflicts, we recommend installing **positional_nuc_profiler** using a conda environment or a similar approach.

#### Installation
```
pip install git+https://github.com/DariiaVyshenska/positional_nuc_profiler.git
```
#### Updating to the latest version
```
pip install --no-deps --force-reinstall git+https://github.com/DariiaVyshenska/positional_nuc_profiler.git
```

#### Uninstall
```
pip uninstall positional_nuc_profiler
```


## Usage

> [!IMPORTANT]
>	- The tool only supports BAM files mapped to a single contiguous reference genome (e.g., a viral genome). It does not support multi-chromosome or fragmented genome assemblies.
> 	- Paired-end reads are not explicitly supported or tested.
```
positional_nuc_profiler <indexed_bam_path> <output_dir> <nucleotide_positions> [options]
```
#### Arguments:
***indexed_bam_path*** - Path to the <ins>indexed</ins> BAM file.\
***output_path*** - Path to a directory where the output CSV will be saved.\
***nucleotide_positions*** - Two or more unique reference genome positions (1-based indexing) specifying nucleotide sites of interest. These positions must be within the read length distance to be analyzed together.

#### Optional Parameters:
***--min_base_qual*** - Minimum base quality. Bases below this threshold are ignored. Default: 13.\
***--min_mapping_qual*** - Minimum mapping quality. Reads below this value are ignored. Default: 0.\
***--max_depth*** - Maximum read depth permitted. Default: 8000.

> [!NOTE]
> This program automatically excludes the following reads:
>	- Unmapped reads (BAM_FUNMAP, 0x4)
>	- Secondary alignments (BAM_FSECONDARY, 0x100)
>	- Reads failing quality checks (BAM_FQCFAIL, 0x200)
>	- PCR duplicates (BAM_FDUP, 0x400)
> 
> No adjustment of the mapping quality of reads during pileup generation is done.

#### Usage example

```
python positional_nuc_profiler/main.py ./my_file.bam ./out_dir/ 9646 9654 1000 --min_base_qual 0
```

*Expected Standard Output:*

```
2025-02-08 14:21:12 - INFO - Starting data extraction...
2025-02-08 14:21:12 - INFO - Processing reference position: 9651
2025-02-08 14:21:12 - INFO - Processing reference position: 9652
2025-02-08 14:21:12 - INFO - Processing reference position: 9653
2025-02-08 14:21:12 - INFO - Processing all nt positions within the given region is complete.

2025-02-08 14:21:12 - INFO - Total number of reads processed across all reference positions: 11

2025-02-08 14:21:12 - INFO - Number of reads used for final frequency estimation: 7

2025-02-08 14:21:12 - INFO - All detected nucleotide combinations & their depths are:
AAC: 7
AAN: 3
ANN: 1

2025-02-08 14:21:12 - INFO - Selected nucleotide combinations (final results):
NUCLEOTIDE_COMBOS  FREQUENCY  DEPTH
              AAC        1.0      7

2025-02-08 14:21:12 - INFO - Processing complete.
Results saved to: ./out_dir/my_file_9651-9652-9653_freqs.csv
```
Output file example (`./out_dir/my_file_9651-9652-9653_freqs.csv`):
| NUCLEOTIDE_COMBOS  | FREQUENCY  | DEPTH |
| ------------- | ------------- | ------------- |
| AAC  | 1  | 7  |

## Running Tests

Test data files are not included in the repository due to size constraints. Please reach out to the repository owner to request access.

#### Run All Tests
```
python -m unittest discover -s tests -v
```
#### Run a Single Test
```
python -m unittest tests.test_io_utils
```
## License

This project is licensed under the MIT License.

## Need Help?

For questions or issues, open an issue on GitHub.
