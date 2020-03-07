"""Various tools to working with binary linear codes."""

from blincodes import matrix


def hadamard_product(generator_a, generator_b):
    """Evaluate the generator matrix of Hadamard product code.

    :param: Matrix generator_a -  the generator matrix of the first code;
    :param: Matrix generator_b -  the generator matrix of the second code.
    :return: Matrix generator - the generator matrix of Hadamard product of
                                the first and the second codes.
    """
    hadamard_dict = {}  # {index of the fist 1 in the row: row}
    hadamard = []
    for row_a in generator_a:
        for row_b in generator_b:
            row = row_a * row_b
            test_row = row.copy()
            for i, row_h in hadamard_dict.items():
                if test_row[i]:
                    test_row += row_h
            if test_row.value:
                hadamard_dict[test_row.support[0]] = test_row
                hadamard.append(row)
    return matrix.from_vectors(hadamard)
