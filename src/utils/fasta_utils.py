from typing import Tuple, Dict


class Fasta:
    def __init__(self, file_path):
        self.__data = self._read_fasta(file_path)

    def get_rna(self, rna_id):
        return self.__data[rna_id]

    def compare_rna(self, id1, id2):
        rna1, rna2 = self.get_rna(id1), self.get_rna(id2)
        len1, len2 = len(rna1), len(rna2)
        matches = 0
        for i in range(min(len1, len2)):
            symbol1, symbol2 = rna1[i], rna2[i]
            if symbol1 == symbol2 or symbol1 == 'N' or symbol2 == 'N':
                matches += 1
        return matches / max(len1, len2)

    def _read_fasta(self, file_path: str) -> Dict[str, str]:
        """Reads a fasta file and returns a dict where the keys are the accessions
        and the values are the RNA sequences
        """
        data = dict()
        with open(file_path, 'r') as fasta:
            sequences = filter(None, fasta.read().split('>'))
            for seq in sequences:
                rna_id, rna = self._get_rna(seq)
                data[rna_id] = rna
        return data

    @staticmethod
    def _get_rna(genome_info_str: str) -> Tuple[str, str]:
        """Get the header and the RNA from a String
        Argument: A String that contains info about the genome
        Return: An Id-value tuple
        """
        lines = genome_info_str.split('\n')
        header, genome = lines[0], ''.join(lines[1:])
        genome_id = header.split('|')[0].strip()
        return genome_id, genome
