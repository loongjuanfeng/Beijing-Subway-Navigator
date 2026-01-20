from __future__ import annotations


class Matrix:
    data: list[list[float]]
    dim: tuple[int, int]
    init_value: float

    def __init__(
        self,
        data: list[list[float]] | None = None,
        dim: tuple[int, int] | None = None,
        init_value: float = 0,
    ) -> None:
        if data is None and dim is None:
            raise ValueError("1-1: Lack enough variables")

        if data is not None:
            if not isinstance(data, list):
                raise TypeError("1-2: The data should be a nested list")

            for i in range(len(data)):
                if i == 0:
                    if not isinstance(data[i], list):
                        raise TypeError("1-3: All the elements in 'data' should be a list")
                else:
                    if not isinstance(data[i], list) or len(data[i]) != len(data[i - 1]):
                        raise TypeError(
                            "1-4: All elements in 'data' should be a list and they must have"
                            " the same length to be a matrix"
                        )

            if len(data) == 0:
                self.data: list[list[float]] = []
                self.dim: tuple[int, int] = (0, 0)
            else:
                self.data = data
                row_num = len(data)
                col_num = len(data[0])
                self.dim = (row_num, col_num)
        else:
            if not isinstance(dim, tuple):
                raise TypeError("1-5: The variable 'dim' should be a tuple")
            if len(dim) != 2:
                raise ValueError("1-6: The tuple 'dim' should contains two elements")
            m, n = dim
            if not (isinstance(m, int) and isinstance(n, int)):
                raise TypeError("1-7: The elements in 'dim' should be integers")

            self.dim = dim
            self.data = [[init_value for _ in range(n)] for _ in range(m)]

        self.init_value = init_value

    def T(self) -> Matrix:
        if not isinstance(self, Matrix):
            raise TypeError("5-1: Only Matrix objects can be transposed")
        res: list[list[float]] = []
        for i in range(len(self.data[0])):
            new_row: list[float] = []
            for j in range(len(self.data)):
                new_row.append(self.data[j][i])
            res.append(new_row)
        return Matrix(res)

    def __pow__(self, n: int) -> Matrix:
        if not isinstance(n, int):
            raise TypeError("11-1: Exponent must be an integer")
        if not isinstance(self, Matrix):
            raise TypeError("11-2: Only Matrix objects can be exponentiated")
        if len(self.data) == 0 or len(self.data[0]) == 0:
            raise ValueError("11-3: We do not accept empty matrix and list")
        if len(self.data) != len(self.data[0]):
            raise ValueError("11-4: Only square matrix can be exponentiated")
        res = Matrix(data=self.data)
        for _ in range(n - 1):
            res = res * self
            res = Matrix(data=res.data)
        return res

    def __add__(self, other: Matrix) -> Matrix:
        if not isinstance(self, Matrix) or not isinstance(other, Matrix):
            raise TypeError("12-1: Only Matrix objects can be added")
        res: list[list[float]] = []
        for i in range(len(self.data)):
            row: list[float] = []
            for j in range(len(self.data[0])):
                row.append(self.data[i][j] + other.data[i][j])
            res.append(row)
        return Matrix(data=res)

    def __mul__(self, other: Matrix) -> Matrix:
        if not (isinstance(self, Matrix) and isinstance(other, Matrix)):
            raise TypeError("4-1: Self and other should be Matrix obects")
        new_self = self.data
        new_other = other.T().data
        width = len(new_self[0])
        res: list[list[float]] = []
        for i in range(len(new_self)):
            new_row: list[float] = []
            for j in range(len(new_other)):
                new_ele: float = 0
                for k in range(width):
                    new_ele += new_self[i][k] * new_other[j][k]
                new_row.append(new_ele)
            res.append(new_row)
        return Matrix(data=res)
