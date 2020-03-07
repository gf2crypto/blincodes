"""Various tools to working with binary linear codes."""

from blincodes import matrix, vector


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


def intersection(generator_a, generator_b, parity_check=False):
    """Return generator matrix of intersection of two codes."""
    if parity_check:
        concat_matrix = matrix.concatenate(
            generator_a, generator_b, by_rows=True)
        return matrix.Matrix(
            (row.value for row in concat_matrix if row.value),
            concat_matrix.ncolumns)
    return matrix.concatenate(
        generator_a, generator_b, by_rows=True).orthogonal


def puncture(generator, columns=None, remove_zeroes=False):
    """Return generator matrix of punctured code.

    Punctured code is code obtaining by set the positions
    with indexes from `ncolumns` of every codeword to zero.
    """
    if not columns:
        columns = []
    mask = vector.from_support(columns, generator.ncolumns)
    puncture_matrix = matrix.Matrix(
        ((row + mask).value for row in generator),
        generator.ncolumns).diagonal_form
    if remove_zeroes:
        return matrix.Matrix(
            (row.value for row in puncture_matrix if row.value),
            generator.ncolumns).submatrix(
                columns=(i for i in range(generator.ncolumns)
                         if i not in columns))
    return matrix.Matrix(
        (row.value for row in puncture_matrix if row.value),
        generator.ncolumns)
