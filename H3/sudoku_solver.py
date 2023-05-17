from csp import Constraint, CSP

def filehelper(filename: str):
    with open(filename) as sudoku_file:
        all_lines = sudoku_file.readlines()
    return [[int(i) if i != '-' else None for i in line.strip().split(' ')] for line in all_lines]


class SudokuConstraint(Constraint[tuple[int, int], list[tuple[int, int]]]):
    def __init__(self, cell: tuple[int, int], restricting_cells: list[tuple[int, int]]) -> None:
        super().__init__([cell] + restricting_cells)

    def satisfied(self, assignment: dict[tuple[int, int], int]) -> bool:
        r, v = self.variables[0]
        value_assigned = assignment[self.variables[0]]
        for cell in self.variables[1:]:
            if assignment[cell] == value_assigned:
                return False    # value conflict!
        return True             # fall through: no conflict


class Sudoku:
    sudoku: list[list[int]]
    __dim: int
    __csp: CSP
    __variables: list[tuple[int, int]]
    __domains: dict[tuple[int, int], list[int]]

    def __init__(self, cells: list[list[int]]) -> None:
        assert len(cells) > 0, "No list provided for setting up initial sudoku"
        for i in range(len(cells)):
            assert len(cells) == len(cells[i]), f"Row {i} has length {len(cells[i])} - expected {len(cells)}"
        self.sudoku = cells
        self.__dim = len(cells)

    def __str__(self):
        s = [''.join([str(c) if c is not None else "-" for c in r]) for r in self.sudoku]
        return '\n'.join(s)

    def generate_variables(self) -> None:
        self.__variables =  [(r, c) for r in range(self.__dim) for c in range(self.__dim)]

    def generate_restricting_cells(self, cell: tuple[int, int]) -> list[tuple[int, int]]:
        """Generate the list of tuples (row,col) that restrict the value of a restricted location (r, c);
           excluding the cell itself
        """
        row, col = cell
        block_row, block_col = row // 3, col // 3  # row, column of the 3x3 block the cell belongs to
        restricting_cells = \
            [(row, c) for c in range(self.__dim) if c != col] + \
            [(r, col) for r in range(self.__dim) if r != row] + \
            [(3 * block_row + i, 3 * block_col+ j)
             for i in range(0, 3)
             for j in range(0, 3) if 3 * block_row + i != row and 3 * block_col + j != col]
        return list(set(restricting_cells))

    def generate_domains(self) -> None:
        domains = {}
        all_options = set(range(1, 10))
        for var in self.__variables:
            row, col = var  # row, column of the cell
            if self.sudoku[row][col] is None:               # not specified in setup
                used_values = list(set([self.sudoku[cell[0]][cell[1]] for cell in self.generate_restricting_cells(var) if self.sudoku[cell[0]][cell[1]] is not None]))
                domains[var] = list(all_options - set(used_values) - {None})
            else:                                           # specified in setup: must restrict to this value only
                domains[var] = self.sudoku[row][col]
        self.__domains = domains

    def setup_csp(self):
        self.generate_variables()
        self.generate_domains()
        self.__csp = CSP(self.__variables, self.__domains)
        for cell in self.__domains.keys():
            row, col = cell
            restrictions = sorted(self.generate_restricting_cells(cell))
            self.__csp.add_constraint(SudokuConstraint(cell, restrictions))


if __name__ == "__main__":
    lines: list[tuple[int, int]] = filehelper("test_sudoku.txt")
    sudoku: Sudoku = Sudoku(lines)
    sudoku.setup_csp()
    print(sudoku)
