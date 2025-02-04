#include <float.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

void print_tableau(double **tableau, int m, int n) {
  int rows = m + 1;
  int cols = n + m + 1;
  for (int i = 0; i < m; i++) {
    for (int j = 0; j < n; j++) {
      printf("%lf ", tableau[i][j]);
    }
    printf("\n");
  }
  printf("\n");
}

void print_solution(double **tableau, int m, int n) {
  int rows = m + 1;
  int cols = n + m + 1;
  double *solution = malloc(sizeof(double) * cols);
  for (int i = 0; i < m; i++) {
    int basic_var = -1;
    for (int j = 0; j < cols - 1; j++) {
      if (tableau[i][j] == 1) {
        bool is_basic = true;
        for (int k = 0; k < m; k++) {
          if (k != i && tableau[k][j] != 0) {
            is_basic = false;
            break;
          }
        }
        if (is_basic) {
          basic_var = j;
          break;
        }
      }
    }
    if (basic_var != -1) {
      solution[basic_var] = tableau[i][cols - 1];
    }
  }

  printf("Optimal Solution:\n");
  for (int j = 0; j < n; j++) {
    printf("x[%d] = %lf\n", j + 1, solution[j]);
  }
  printf("Optimal Value: %lf\n", tableau[m][cols - 1]);
  free(solution);
}

void simplex(double *c, double **A, double *b, int m, int n) {
  int rows = m + 1;
  int cols = n + m + 1;
  double **tableau = malloc(sizeof(double *) * rows);
  if (tableau)
    for (int i = 0; i < rows; i++)
      tableau[i] = malloc(sizeof(double) * cols);

  // initial tableau
  for (int i = 0; i < m; i++) {
    for (int j = 0; j < n; j++) {
      tableau[i][j] = A[i][j];
    }
    tableau[i][n + i] = 1.0; // slack variables
    tableau[i][cols - 1] = b[i];
  }

  for (int j = 0; j < n; j++) {
    tableau[m][j] = -c[j];
  }

  while (1) {
    // optimal?
    int pivot_col = -1;
    for (int j = 0; j < cols - 1; j++) {
      if (tableau[m][j] < 0) {
        pivot_col = j;
        break;
      }
    }
    if (pivot_col == -1)
      break; // optimum found

    // minimum ratio test
    int pivot_row = -1;
    double min_ratio = DBL_MAX;
    for (int i = 0; i < m; i++) {
      if (tableau[i][pivot_col] > 0) {
        double ratio = tableau[i][cols - 1] / tableau[i][pivot_col];
        if (ratio < min_ratio) {
          min_ratio = ratio;
          pivot_row = i;
        }
      }
    }
    if (pivot_row == -1) {
      printf("Unbounded solution\n");
      goto finish;
    }

    // pivot operation
    double pivot_value = tableau[pivot_row][pivot_col];
    for (int j = 0; j < cols; j++) {
      tableau[pivot_row][j] /= pivot_value;
    }
    for (int i = 0; i <= m; i++) {
      if (i != pivot_row) {
        double factor = tableau[i][pivot_col];
        for (int j = 0; j < cols; j++) {
          tableau[i][j] -= factor * tableau[pivot_row][j];
        }
      }
    }
  }

  print_solution(tableau, m, n);

finish:
  for (int i = 0; i < rows; i++)
    free(tableau[i]);
  free(tableau);
}
