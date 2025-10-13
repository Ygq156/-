#ifndef TEST_DATA_H
#define TEST_DATA_H

#include <stdio.h>
#include <stdlib.h>

typedef enum {
    DATA_SUCCESS = 0,
    DATA_ERROR_FILE = -1,
    DATA_ERROR_MEMORY = -2,
    DATA_ERROR_INVALID_SIZE = -3
} DataError;

// 函数声明
DataError generate_test_data(const char* filename, int size);
int* read_test_data(const char* filename, int* size, DataError* error);
void free_test_data(int* data);

#endif
