from csv import DictReader


def get_rna(s):
    """Get the header and the RNA from a String
    Argument: A String that contains info about the genome
    Return: An Id-value tuple
    """
    lines = s.split('\n')
    header, genome = lines[0], ''.join(lines[1:])
    genome_id = header.split('|')[0].strip()
    return genome_id, genome


def read_fasta(filepath):
    """Reads a fasta file and returns a Map where the key are the accessions
    and the values are the RNA sequences
    """
    data = dict()
    with open(filepath, 'r') as fasta:
        sequences = filter(None, fasta.read().split('>'))
        for seq in sequences:
            rna_id, rna = get_rna(seq)
            data[rna_id] = rna
    return data


def read_csv(filepath):
    """Reads a csv file and returns a list of Ordered Maps
    """
    with open(filepath, 'r') as csv_file:
        reader = DictReader(csv_file, delimiter=',')
        return list(reader)
