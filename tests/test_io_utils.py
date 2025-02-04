import unittest
import sys
import os
from exceptions import RefError
from io_utils import open_and_validate_bam

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestIOUtils(unittest.TestCase):
    def setUp(self):
        self.nonexisting_bam_file = './test_data/tmp_cdv/cdv_wt-i860m1.fastq.gz.bam'
        self.unindexed_bam_file = './test_data/tmp_cdv/cdv_wt-i860m.fastq.gz.bam'

    def test_open_and_validate_bam_file_not_found(self):
        with self.assertRaises(RefError) as context:
            with open_and_validate_bam(self.nonexisting_bam_file):
                pass
        self.assertIn("Failed to open BAM file", str(context.exception))
        
    def test_open_and_validate_bam_file_no_index(self):
        with self.assertRaises(RefError) as context:
            with open_and_validate_bam(self.unindexed_bam_file):
                pass
        self.assertIn("No index file found", str(context.exception))