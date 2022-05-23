#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#define H 6.0
#define W 8.0
#define h 2.0
#define w 4.0
#define T_LIQUID 100.0
#define T_PIPE 10
#define TIME_RUNNING 25
#define A 1
#define PATH_PLT "t.plt"

void get_index(int index, int ny, int* ix, int* iy) {
    *iy = index % ny;
    *ix = index / ny;
}

void write_to_file(double** T, FILE* fds1, int ny, int nx) {
    FILE *fd;
    if ((fd = fopen(PATH_PLT,"w")) == NULL) {
        printf("Cannot open file!\n");
        exit(0);
    }

    fprintf(fd, "set terminal png size 2000, 1000\n");
    fprintf(fd, "set output 'screen.png'\n");
    fprintf(fd, "set palette defined (0 \"black\", 1\"blue\", 2 \"red\", 3 \"yellow\")\n");
    fprintf(fd, "set xrange[0:25]\n");
    fprintf(fd, "set yrange[0:19]\n");
    fprintf(fd, "set cbrange[0:100]\n");
    fprintf(fd, "plot '-' using 1:2:3 with image notitle\n");

    for (int k = 0; k < ny * nx; k++) {
        int i, j;
        get_index(k, ny,&i, &j);
        fprintf(fd, "%d %d %lf\n",i, j, T[i][j]);
        fprintf(fds1,"%d %d %3lf\n", i, j, T[i][j]);
    }

    fprintf(fd, "e\n");
    fprintf(fds1, "\n\n");

    fclose(fd);
}

void initial_pipe(double **T, double **T_next, int N, int li, int bj, int tj, int ri, int ny) {
    for (int k = 0; k < N; k++) {
        int i, j;
        get_index(k, ny, &i, &j);
        if (i == li && j >= bj && j <= tj) {
            T_next[i][j] = T_LIQUID;
            T[i][j] = T_LIQUID;
            continue;
        }
        // Правая
        if (i == ri && j >= bj && j <= tj) {
            T_next[i][j] = T_LIQUID;
            T[i][j] = T_LIQUID;
            continue;
        }
        // Верхняя
        if (j == tj && i >= li && i <= ri) {
            T_next[i][j] = T_LIQUID;
            T[i][j] = T_LIQUID;
            continue;
        }
        // Нижняя
        if (j == bj && i >= li && i <= ri) {
            T_next[i][j] = T_LIQUID;
            T[i][j] = T_LIQUID;
            continue;
        }

        if (i > li && i < ri && j > bj && j < tj) {
            T_next[i][j] = T_LIQUID;
            T[i][j] = T_LIQUID;
            continue;
        } else {
            T[i][j] = T_PIPE;
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        printf("Use %s nx ny file_name\n", argv[0]);
        exit(1);
    }

    FILE *file;
    char *file_name;

    int nx = atoi(argv[1]);
    int ny = atoi(argv[2]);
    file_name = argv[3];

    if ((file = fopen(file_name,"w")) == NULL) {
        printf("Cannot open file!\n");
        exit(0);
    }

    int N = nx * ny;

    double l = (W - w) / 2.0;
    double b = (H - h) / 2.0;

    double hx = W / (nx - 1);
    double hy = H / (ny - 1);

    int li = (int)(l / hx);
    int ri = (int)((l + w) / hx);
    int bj = (int)(b / hy);
    int tj = (int)((b + h) / hy);

    double **T = (double **)malloc(sizeof(double *) * nx);
    double **T_next = (double **)malloc(sizeof(double *) * nx);

    for (int k = 0; k < nx; k++) {
        T[k] = (double *) malloc(sizeof(double) * ny);
        T_next[k] = (double *) malloc(sizeof(double) * ny);
    }

    initial_pipe(T, T_next, N, li, bj, tj, ri, ny);

    int i, j;
    for (int g = 0; g < TIME_RUNNING; g++) {
        double ht = 0;
        for (int k = 0; k < N; k++) {
            get_index(k, ny, &i, &j);
            // Внутренние границы
            // Левая
            if (i == li && j >= bj && j <= tj) {
                T_next[i][j] = T_LIQUID;
                T[i][j] = T_LIQUID;
                continue;
            }
            // Правая
            if (i == ri && j >= bj && j <= tj) {
                T_next[i][j] = T_LIQUID;
                T[i][j] = T_LIQUID;
                continue;
            }
            // Верхняя
            if (j == tj && i >= li && i <= ri) {
                T_next[i][j] = T_LIQUID;
                T[i][j] = T_LIQUID;
                continue;
            }
            // Нижняя
            if (j == bj && i >= li && i <= ri) {
                T_next[i][j] = T_LIQUID;
                T[i][j] = T_LIQUID;
                continue;
            }

            if (i > li && i < ri && j > bj && j < tj) {
                T_next[i][j] = T_LIQUID;
                continue;
            }
            // Внешние границы
            // Левая и правая
            if (i == 0) {
//                T_next[0][j] = (T[1][j]) / (1 + hx);
                continue;
            }

            if (i == nx - 1) {
//                T_next[i][j] = (T[i - 1][j]) / (1 + hx);
                continue;
            }
            //нижняя и верхняя
            if (j == 0) {
//                T_next[i][0] = (T[i][1]) / (1 + hy);
                continue;
            }

            if (j == ny - 1) {
//                T_next[i][j] = (T[i][j - 1]) / (1 + hy);
                continue;
            }

            T_next[i][j] = ((T[i + 1][j] - 2 * T[i][j] + T[i - 1][j]) / (hx * hx) +
                    (T[i][j + 1] - 2 * T[i][j] + T[i][j - 1]) / (hy * hy)) * A;

            if (ht < fabs(T_next[i][j])) {
                ht = fabs(T_next[i][j]);
            }
        }

        for (int col = 0; col < nx; col++) {
            for (int row = 0; row < ny; row++) {
                if ((col == li && row >= bj && row <= tj) || (col == ri && row >= bj && row <= tj)
                    || (row == tj && col >= li && col <= ri) || (row == bj && col >= li && col <= ri)
                    || (col == 0) || (col == nx - 1) || (row == 0) || (row == ny - 1)
                    || (col > li && col < ri && row > bj && row < tj)) {
                    T[col][row] = T_next[col][row];
                } else {
                    T[col][row] = T_next[col][row] * (2 / ht) + T[col][row];
                }
            }
        }

        for (int k = 0; k < N; k++) {
            get_index(k, ny, &i, &j);
            if (i == 0) {
                T[0][j] = (T[1][j]) / (1 + hx);
                continue;
            }

            if (i == nx - 1) {
                T[i][j] = (T[i - 1][j]) / (1 + hx);
                continue;
            }
            //нижняя и верхняя
            if (j == 0) {
                T[i][0] = (T[i][1]) / (1 + hy);
                continue;
            }

            if (j == ny - 1) {
                T[i][j] = (T[i][j - 1]) / (1 + hy);
                continue;
            }
        }

        T[0][0] = (T[0][1]) / (1 + hx);
        T[0][ny - 1] = (T[0][ny - 2]) / (1 + hy);
    }

    for (j = ny - 1; j >= 0; j--) {
        for (i = 0; i < nx; i++) {
            printf("%8.3f", T[i][j]);
        }
        printf("\n");
    }
    printf("\nhx = %g\nhy = %g\n", hx, hy);

    write_to_file(T,file, ny, nx);

    fclose(file);
}