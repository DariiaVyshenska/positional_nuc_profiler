import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from parsers import extract_nt_combo_frequencies
from exceptions import RefError

class TestParsers(unittest.TestCase):
  def setUp(self):
    self.bam_file = './test_data/ibv_malaysia/ibv_malaysia_egg_ail.fastq.gz.bam'
    
  def test_extract_nt_combo_frequencies_easy_codon_default(self):
    curr_output = extract_nt_combo_frequencies(self.bam_file,   nt_args = {
      "nucleotide_positions": [9951, 9952, 9953],
      "min_base_qual": 13,
      "min_mapping_qual": 0,
      "max_depth": 8000,
  })
    self.assertEqual(curr_output[0][0], 'TCA')
    self.assertEqual(curr_output[0][1], 1.0)
    self.assertEqual(curr_output[0][2], 21)
    self.assertEqual(len(curr_output), 1)

  def test_extract_nt_combo_frequencies_easy_codon_qal_high(self):
    curr_output = extract_nt_combo_frequencies(self.bam_file,   nt_args = {
      "nucleotide_positions": [9951, 9952, 9953],
      "min_base_qual": 0,
      "min_mapping_qual": 0,
      "max_depth": 8000,
  })
    self.assertEqual(curr_output[0][0], 'TCA')
    self.assertEqual(curr_output[0][1], 1.0)
    self.assertEqual(curr_output[0][2], 22)
    self.assertEqual(len(curr_output), 1)
  
  def test_extract_nt_combo_frequencies_partial_align(self):
    curr_output = extract_nt_combo_frequencies(self.bam_file,   nt_args = {
      "nucleotide_positions": [9953, 9954, 9955],
      "min_base_qual": 0,
      "min_mapping_qual": 0,
      "max_depth": 8000,
  })
    self.assertEqual(curr_output[0][0], 'AAG')
    self.assertEqual(curr_output[0][1], 1.0)
    self.assertEqual(curr_output[0][2], 23)
    self.assertEqual(len(curr_output), 1)

  def test_extract_nt_combo_frequencies_secondary_alignm_excluded(self):
    curr_output = extract_nt_combo_frequencies(self.bam_file,   nt_args = {
      "nucleotide_positions": [2355, 2356, 2357],
      "min_base_qual": 0,
      "min_mapping_qual": 0,
      "max_depth": 8000,
  })
    self.assertEqual(curr_output[0][0], 'TGA')
    self.assertEqual(curr_output[0][1], 1.0)
    self.assertEqual(curr_output[0][2], 59)
    self.assertEqual(len(curr_output), 1)
    
  def test_extract_nt_combo_frequencies_two_pos_input(self):
    curr_output = extract_nt_combo_frequencies(self.bam_file,   nt_args = {
      "nucleotide_positions": [9646, 9654],
      "min_base_qual": 0,
      "min_mapping_qual": 0,
      "max_depth": 8000,
  })
    self.assertEqual(curr_output[0][0], 'CG')
    self.assertEqual(curr_output[0][1], 1.0)
    self.assertEqual(curr_output[0][2], 7)
    self.assertEqual(len(curr_output), 1)
  
  def test_extract_nt_combo_frequencies_four_nt_input(self):
    curr_output = extract_nt_combo_frequencies(self.bam_file,   nt_args = {
      "nucleotide_positions": [9951, 9952, 9953, 9954],
      "min_base_qual": 0,
      "min_mapping_qual": 0,
      "max_depth": 8000,
  })
    self.assertEqual(curr_output[0][0], 'TCAA')
    self.assertEqual(curr_output[0][1], 1.0)
    self.assertEqual(curr_output[0][2], 22)
    self.assertEqual(len(curr_output), 1)
  
  def test_extract_nt_combo_frequencies_nt_too_far_away(self):
    curr_output = extract_nt_combo_frequencies(self.bam_file,   nt_args = {
      "nucleotide_positions": [9646, 9654, 1000],
      "min_base_qual": 0,
      "min_mapping_qual": 0,
      "max_depth": 8000,
  })
    self.assertIsInstance(curr_output, list)
    self.assertEqual(len(curr_output), 0)
    
  def test_extract_nt_combo_frequencies_nt_position_exceeds_ref_length(self):
    nt_args = {
      "nucleotide_positions": [9999999],
      "min_base_qual": 0,
      "min_mapping_qual": 0,
      "max_depth": 8000,
    }
    
    with self.assertRaises(RefError) as context:
      extract_nt_combo_frequencies(self.bam_file, nt_args)

    self.assertIn("one or more nucleotide_positions exceed the length of the reference sequence", str(context.exception))
