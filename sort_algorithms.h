#ifndef SORT_ALGORITHMS_H
#define SORT_ALGORITHMS_H

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifdef _OPENMP
#include <omp.h>
#endif

// 错误代码定义
typedef enum {
    SORT_SUCCESS = 0,
    SORT_ERROR_NULL_POINTER = -1,
    SORT_ERROR_INVALID_SIZE = -2,
    SORT_ERROR_MEMORY_ALLOC = -3
} SortError;

// Pivot选择策略
typedef enum {
    PIVOT_FIRST,           // 第一个元素
    PIVOT_LAST,            // 最后一个元素  
    PIVOT_MIDDLE,          // 中间元素
    PIVOT_RANDOM,          // 随机元素
    PIVOT_MEDIAN_OF_THREE  // 三数取中
} PivotStrategy;

// 函数声明

// 快速排序函数
SortError quick_sort_recursive(int arr[], int low, int high, PivotStrategy strategy);
SortError quick_sort_iterative(int arr[], int low, int high, PivotStrategy strategy);

// 归并排序函数
SortError merge_sort_parallel(int arr[], int left, int right);

// 辅助函数
int is_sorted(int arr[], int n);
SortError copy_array(int dest[], int src[], int n);
void print_array(int arr[], int n);
const char* pivot_strategy_name(PivotStrategy strategy);

// 内部使用的辅助函数（不暴露给外部）
void swap_elements(int* a, int* b);
int select_pivot(int arr[], int low, int high, PivotStrategy strategy);
int partition_array(int arr[], int low, int high, PivotStrategy strategy);
void merge_arrays(int arr[], int left, int mid, int right);

#endif
