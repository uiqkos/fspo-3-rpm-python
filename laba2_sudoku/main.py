import pathlib
import sudoku_generator
from pprint import pprint as pp


def group(values: list, n: int):
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[index:index + n] for index in range(0, len(values), n)]


def create_grid(puzzle: str):
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def read_sudoku(path):
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def display(grid) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def get_row(grid, pos):
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """

    return grid[pos[0]]


def get_col(grid, pos):
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """

    return [
        row[pos[1]] for row in grid
    ]


def get_block(grid, pos):
    """ Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """

    begin_row = (pos[0] // 3) * 3
    begin_column = (pos[1] // 3) * 3

    return [
        grid[i][j]
        for i in range(begin_row, begin_row + 3)
        for j in range(begin_column, begin_column + 3)
    ]


from itertools import filterfalse
from copy import deepcopy

def solve(grid):
    """ Поиск решения для указанного пазла.

    Как решать Судоку?
    1. Найти свободную позицию
    2. Найти все возможные значения, которые могут находиться на этой позиции
    3. Для каждого возможного значения:
        3.1. Поместить это значение на эту позицию
        3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """

    for i in range(9):
        for j in range(9):
            if grid[i][j] == '.':
                all_possible = get_row(grid, (i, j)) + get_col(grid, (i, j)) + get_block(grid, (i, j))

                for possible in filterfalse(all_possible.__contains__, '123456789'):
                    new_grid = deepcopy(grid)
                    new_grid[i][j] = possible

                    solution = solve(new_grid)

                    if solution is not None:
                        return solution
                return None
    return grid

"""
https://en.wikipedia.org/wiki/Backtracking
Мы будем решать Судоку методом перебора (поиска) с возвратом. Общая схема этого метода заключается в следующем:
def Перебор(Ситуация):
    if Ситуация конечная:
        Завершающая обработка
    else:
        for Действие in Множество всех возможных действий:
            Применить Действие к Ситуация
            Перебор(Ситуация)
            откатить Действие назад
"""


def without(full, to_remove) -> list:
    return list(filterfalse(to_remove.__contains__, full))


def generate_sudoku(N: int) -> list:
    """ Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """

    return sudoku_generator.generate_sudoku(N)


def check_i_j(grid, i, j) -> bool:
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    return \
        list(map(get_row(grid, (i, j)).count, numbers)) == \
        list(map(get_col(grid, (i, j)).count, numbers)) == \
        list(map(get_block(grid, (i, j)).count, numbers)) == [1] * 9


def check_solution(solution: list) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    for i in range(9):
        for j in range(9):
            if not check_i_j(solution, i, j):
                return False
    return True


# grid = read_sudoku('C:\\Users\\uiqko\\GoogleDrive\\code\\python\\fspo\\5semak\\laba2\\puzzle1.txt')
# grid_ = [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
# print(check_solution(grid_))
# print(list(map(get_row(grid, (0, 1)).count, ['1', '2', '3', '4', '5', '6', '7', '8', '9'])))
# display(solve(read_sudoku('C:\\Users\\uiqko\\GoogleDrive\\code\\python\\fspo\\5semak\\laba2\\puzzle1.txt')))
# display(grid)

for i in range(10):
    sudoku = generate_sudoku(2)
    # print('\n'.join(map(str, sudoku)))
    display(sudoku)
    sudoku = solve(sudoku)
    display(sudoku)
