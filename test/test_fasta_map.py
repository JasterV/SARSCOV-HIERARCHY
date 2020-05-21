from unittest import TestCase

import libs.seqalign as sq


class TestFastaMap(TestCase):

    def test_sequence_align(self):
        """
            Use https://n9.cl/2qcq to
            check the distance.
        """
        seq1 = "AATCG"
        seq2 = "AACG"
        expected = 2
        self.assertEqual(expected, sq.compare_samples(seq1, seq2))

        seq1 = "JDSLFA"
        seq2 = "JALFDSA"
        expected = 6
        self.assertEqual(expected, sq.compare_samples(seq1, seq2))
        
        seq1 = "DSAJKJFHJAKHDIOUZVJCXMVCZIOIUOWUQRIEUWQIPIDSFSDKZXV"
        seq2 = "FKSJAFKJIOTIGHLKJVMCXXZCMVLJASIRUWQOIUTPQWURIIPOQ"
        expected = 46
        self.assertEqual(expected, sq.compare_samples(seq1, seq2))
        
        seq1 = "KFDSKAJFJPOTIPWQUIMXZMVMZXBVM"
        seq2 = "FKDSPOIQTUITYSKZMV"
        expected = 31
        self.assertEqual(expected, sq.compare_samples(seq1, seq2))

