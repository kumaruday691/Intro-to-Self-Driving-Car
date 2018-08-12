import math
from math import sqrt
import numbers


def zeroes(height, width):
    """
    Creates a matrix of zeroes.
    """
    g = [[0.0 for _ in range(width)] for __ in range(height)]
    return Matrix(g)


def identity(n):
    """
    Creates a n x n identity matrix.
    """
    I = zeroes(n, n)
    for i in range(n):
        I.g[i][i] = 1.0
    return I


class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################

    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise (ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise (NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")

        # TODO - your code here
        if self.h == 1 and self.w == 1:
            return self.g[0][0]

        if len(self.g) == 2:
            return (self.g[0][0] * self.g[1][1]) - (self.g[0][1] * self.g[1][0])

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise (ValueError, "Cannot calculate the trace of a non-square matrix.")

        # TODO - your code here
        trace = 0
        for i in range(self.h):
            trace += self.g[i][i]

        return trace

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise (ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise (NotImplementedError, "inversion not implemented for matrices larger than 2x2.")

        # TODO - your code here
        determinant = self.determinant()
        if self.h == 1 and self.w == 1:
            grid = []
            grid.append([determinant])
            return Matrix(grid)

        grid = [[self.g[1][1], -1*self.g[0][1]], [-1*self.g[1][0], self.g[0][0]]]
        invInitMatrix = Matrix(grid)

        oneByDet = 1 / float(determinant)
        return invInitMatrix.__rmul__(oneByDet)

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        # TODO - your code here
        newHeight = self.w
        newWidth = self.h

        initMatrixGrid = [[0] * newWidth for x in range(newHeight)]

        initMatrix = Matrix(initMatrixGrid)
        initMatrix.g = [list(element) for element in zip(*self.g)]

        return initMatrix

    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self, idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self, other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise (ValueError, "Matrices can only be added if the dimensions are the same")
            #
        # TODO - your code here
        #
        # guard clause
        if not isinstance(other, Matrix):
            raise (ValueError, "Paramter must be an instance of matrix")

        newMatrixInitGrid = [[0] * self.w for x in range(self.h)]
        resultMatrix = Matrix(newMatrixInitGrid)

        row = 0
        col = 0
        for row1 in range(self.h):
            for element in zip(self.g[row1], other[row1]):
                resultMatrix[row][col] = element[0] + element[1]
                col += 1

            row += 1
            col = 0

        return resultMatrix

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        #
        # TODO - your code here
        #
        return self.__rmul__(-1)

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        #
        # TODO - your code here
        #
        # guard clause
        if not isinstance(other, Matrix):
            raise (ValueError, "Paramter must be an instance of matrix")

        newMatrixInitGrid = [[0] * self.w for x in range(self.h)]
        resultMatrix = Matrix(newMatrixInitGrid)

        row = 0
        col = 0
        for row1 in range(self.h):
            for element in zip(self.g[row1], other[row1]):
                resultMatrix[row][col] = element[0] - element[1]
                col += 1

            row += 1
            col = 0

        return resultMatrix

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        #
        # TODO - your code here
        #

        # guard clause
        if not isinstance(other, Matrix):
            raise (ValueError, "Paramter must be an instance of matrix")

        newHeight = self.h
        newWidth = other.w

        newMatrixInitGrid = [[0] * newWidth for x in range(newHeight)]
        resultMatrix = Matrix(newMatrixInitGrid)
        transMatrix = other.T()

        for row1 in range(self.h):
            for col2 in range(transMatrix.h):
                for element in zip(self.g[row1], transMatrix[col2]):
                    newMatrixInitGrid[row1][col2] += element[0] * element[1]

        return resultMatrix

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if not isinstance(other, numbers.Number):
            raise (ValueError, "Paramter must be a number")

        newMatrixInitGrid = [[0] * self.w for x in range(self.h)]
        resultMatrix = Matrix(newMatrixInitGrid)

        row = 0
        col = 0
        for row1 in range(self.h):
            for element in self.g[row1]:
                resultMatrix[row][col] = other * element
                col += 1

            row += 1
            col = 0

        return resultMatrix
