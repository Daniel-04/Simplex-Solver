import ctypes
import numpy as np
import os

libname = "simplex"
libpath = os.path.join(os.path.dirname(__file__), f'lib{libname}.so')
lib = ctypes.CDLL(libpath)

# void simplex(double *c, double **A, double *b, int m, int n);
lib.simplex.argtypes = [
    ctypes.POINTER(ctypes.c_double),            # c: double*
    ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),  # A: double**
    ctypes.POINTER(ctypes.c_double),            # b: double*
    ctypes.c_int,                               # m: int
    ctypes.c_int                                # n: int
]
lib.simplex.restype = None

def simplex(c, A, b):
    """
    Parameters:
      c : array-like, shape (n,)
          The coefficients of the objective function.
      A : array-like, shape (m, n)
          The coefficient matrix for the constraints.
      b : array-like, shape (m,)
          The right-hand side values of the constraints.
    """
    c_arr = np.ascontiguousarray(c, dtype=np.double)
    b_arr = np.ascontiguousarray(b, dtype=np.double)
    A_arr = np.ascontiguousarray(A, dtype=np.double)

    m = A_arr.shape[0]
    n = A_arr.shape[1]

    c_ptr = c_arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    b_ptr = b_arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

    # ctypes array (of length m) of POINTER(c_double).
    RowPtrArray = ctypes.POINTER(ctypes.c_double) * m
    a_ptrs = RowPtrArray()
    for i in range(m):
        a_ptrs[i] = A_arr[i].ctypes.data_as(ctypes.POINTER(ctypes.c_double))

    lib.simplex(c_ptr, a_ptrs, b_ptr, m, n)

# Example usage:
if __name__ == "__main__":
    # Example data:
    # Maximise z = 3x + 2y
    # Subject to:
    #    x + y <= 4
    #   2x + y <= 5
    #
    c = [3.0, 2.0]
    A = [
        [1.0, 1.0],
        [2.0, 1.0]
    ]
    b = [4.0, 5.0]

    simplex(c, A, b)
