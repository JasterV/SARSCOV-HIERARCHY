from typing import Tuple, Dict


def get_rna(genome_info_str: str) -> Tuple[str, str]:
    """Get the header and the RNA from a String
    Argument: A String that contains info about the genome
    Return: An Id-value tuple
    """
    lines = genome_info_str.split('\n')
    header, genome = lines[0], ''.join(lines[1:])
    genome_id = header.split('|')[0].strip()
    return genome_id, genome


def read_fasta(file_path: str) -> Dict[str, str]:
    """Reads a fasta file and returns a dict where the keys are the accessions
    and the values are the RNA sequences
    """
    data = dict()
    with open(file_path, 'r') as fasta:
        sequences = filter(None, fasta.read().split('>'))
        for seq in sequences:
            rna_id, rna = get_rna(seq)
            data[rna_id] = rna
    return data
