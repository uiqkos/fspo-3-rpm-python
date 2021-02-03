from random import randint, sample, randrange
from copy import deepcopy


def swap_rows(matrix_):
    matrix = deepcopy(matrix_)
    block = randint(0, 2)
    row_indexes = sample(range(3), 2)

    line1, line2 = block * 3 + row_indexes[0], block * 3 + row_indexes[1]

    matrix[line1], matrix[line2] = matrix[line2], matrix[line1]

    return matrix


def swap_columns(matrix):
    return transpose(swap_rows(transpose(matrix)))


def transpose(matrix):
    return list(map(list, zip(*matrix)))


def generate_solved_sudoku():
    sudoku = [
        ['5', '3', '4', '6', '7', '8', '9', '1', '2'],
        ['6', '7', '2', '1', '9', '5', '3', '4', '8'],
        ['1', '9', '8', '3', '4', '2', '5', '6', '7'],
        ['8', '5', '9', '7', '6', '1', '4', '2', '3'],
        ['4', '2', '6', '8', '5', '3', '7', '9', '1'],
        ['7', '1', '3', '9', '2', '4', '8', '5', '6'],
        ['9', '6', '1', '5', '3', '7', '2', '8', '4'],
        ['2', '8', '7', '4', '1', '9', '6', '3', '5'],
        ['3', '4', '5', '2', '8', '6', '1', '7', '9']
    ]

    transformers = [
        transpose, swap_rows, swap_columns
    ]

    for i in range(randint(2, 20)):
        sudoku = transformers[randrange(0, len(transformers), 1)](sudoku)

    return sudoku


def generate_sudoku(n):
    solved = generate_solved_sudoku()
    indexes = sample(range(1, 82), 81-n)

    for index in indexes:
        solved[(index - 1) // 9][(index - 1) % 9] = '.'

    return solved
