#include "solver.h"
#include <stdlib.h>

int main() {
  // 3 constrains, 2 variables
  int m = 3, n = 2;
  // Objective function: Maximise 3x + 5y
  double c[] = {3, 5};
  // Constrains:
  double **A = malloc(m * sizeof(double *));
  for (int i = 0; i < m; i++)
    A[i] = malloc(n * sizeof(double));
  // x <= 4
  A[0][0] = 1;
  A[0][1] = 0;
  // 2y <= 12
  A[1][0] = 0;
  A[1][1] = 2;
  // 3x + 2y <= 18
  A[2][0] = 3;
  A[2][1] = 2;
  double b[] = {4, 12, 18};

  simplex(c, A, b, m, n);

  for (int i = 0; i < m; i++)
    free(A[i]);
  free(A);
  return 0;
}

// TODO: parser for lp files
