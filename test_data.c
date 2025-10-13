#include "test_data.h"

// 简单的伪随机数生成器（不依赖stdlib的rand）
static unsigned int random_seed = 123456789;

static int simple_rand() {
    random_seed = (random_seed * 1103515245 + 12345) & 0x7fffffff;
    return (int)(random_seed >> 16) & 0x7fff;
}

// 生成测试数据
DataError generate_test_data(const char* filename, int size) {
    if (filename == NULL) return DATA_ERROR_FILE;
    if (size <= 0) return DATA_ERROR_INVALID_SIZE;
    
    FILE* file = fopen(filename, "w");
    if (!file) {
        return DATA_ERROR_FILE;
    }
    
    // 重置随机种子
    random_seed = 123456789;
    
    for (int i = 0; i < size; i++) {
        int value = simple_rand() % 1000000;
        if (fprintf(file, "%d\n", value) < 0) {
            fclose(file);
            return DATA_ERROR_FILE;
        }
    }
    
    fclose(file);
    return DATA_SUCCESS;
}

// 读取测试数据
int* read_test_data(const char* filename, int* size, DataError* error) {
    if (filename == NULL || size == NULL) {
        if (error) *error = DATA_ERROR_FILE;
        return NULL;
    }
    
    FILE* file = fopen(filename, "r");
    if (!file) {
        if (error) *error = DATA_ERROR_FILE;
        return NULL;
    }
    
    // 第一遍：计算数据量
    *size = 0;
    int temp;
    while (fscanf(file, "%d", &temp) == 1) {
        (*size)++;
    }
    
    if (*size <= 0) {
        fclose(file);
        if (error) *error = DATA_ERROR_INVALID_SIZE;
        return NULL;
    }
    
    // 第二遍：读取数据
    rewind(file);
    int* data = (int*)malloc(*size * sizeof(int));
    if (data == NULL) {
        fclose(file);
        if (error) *error = DATA_ERROR_MEMORY;
        return NULL;
    }
    
    for (int i = 0; i < *size; i++) {
        if (fscanf(file, "%d", &data[i]) != 1) {
            free(data);
            fclose(file);
            if (error) *error = DATA_ERROR_FILE;
            return NULL;
        }
    }
    
    fclose(file);
    if (error) *error = DATA_SUCCESS;
    
    return data;
}

// 释放测试数据
void free_test_data(int* data) {
    if (data) {
        free(data);
    }
}
