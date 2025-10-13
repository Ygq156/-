#include "sort_algorithms.h"

// ============================================================================
// 基础辅助函数
// ============================================================================

// 交换两个元素
void swap_elements(int* a, int* b) {
    if (a == NULL || b == NULL) return;
    int temp = *a;
    *a = *b;
    *b = temp;
}

// 验证数组是否已排序
int is_sorted(int arr[], int n) {
    if (arr == NULL || n <= 0) return 0;
    
    for (int i = 1; i < n; i++) {
        if (arr[i] < arr[i - 1]) {
            return 0;
        }
    }
    return 1;
}

// 复制数组
SortError copy_array(int dest[], int src[], int n) {
    if (dest == NULL || src == NULL) return SORT_ERROR_NULL_POINTER;
    if (n <= 0) return SORT_ERROR_INVALID_SIZE;
    
    for (int i = 0; i < n; i++) {
        dest[i] = src[i];
    }
    return SORT_SUCCESS;
}

// 打印数组（调试用）
void print_array(int arr[], int n) {
    if (arr == NULL || n <= 0) return;
    
    printf("[");
    for (int i = 0; i < n && i < 10; i++) {
        printf("%d", arr[i]);
        if (i < n - 1 && i < 9) printf(", ");
    }
    if (n > 10) printf(", ...");
    printf("]\n");
}

// 获取pivot策略名称
const char* pivot_strategy_name(PivotStrategy strategy) {
    switch(strategy) {
        case PIVOT_FIRST: return "First";
        case PIVOT_LAST: return "Last";
        case PIVOT_MIDDLE: return "Middle";
        case PIVOT_RANDOM: return "Random";
        case PIVOT_MEDIAN_OF_THREE: return "Median3";
        default: return "Unknown";
    }
}

// ============================================================================
// Pivot选择函数
// ============================================================================

// 选择pivot元素
int select_pivot(int arr[], int low, int high, PivotStrategy strategy) {
    if (low > high) return low;
    
    switch(strategy) {
        case PIVOT_FIRST:
            return low;
            
        case PIVOT_LAST:
            return high;
            
        case PIVOT_MIDDLE:
            return low + (high - low) / 2;
            
        case PIVOT_RANDOM:
            // 使用简单的伪随机数生成（不依赖stdlib的rand）
            static unsigned int seed = 123456789;
            seed = (seed * 1103515245 + 12345) & 0x7fffffff;
            return low + (seed % (high - low + 1));
            
        case PIVOT_MEDIAN_OF_THREE:
            {
                int mid = low + (high - low) / 2;
                
                // 对三个元素进行排序，取中值
                if (arr[low] > arr[mid]) 
                    swap_elements(&arr[low], &arr[mid]);
                if (arr[low] > arr[high]) 
                    swap_elements(&arr[low], &arr[high]);
                if (arr[mid] > arr[high]) 
                    swap_elements(&arr[mid], &arr[high]);
                
                return mid;
            }
            
        default:
            return low;
    }
}

// ============================================================================
// 快速排序分区函数
// ============================================================================

// 分区函数
int partition_array(int arr[], int low, int high, PivotStrategy strategy) {
    if (low >= high) return low;
    
    // 选择pivot
    int pivot_index = select_pivot(arr, low, high, strategy);
    int pivot_value = arr[pivot_index];
    
    // 将pivot移到末尾
    swap_elements(&arr[pivot_index], &arr[high]);
    
    int i = low - 1;
    
    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot_value) {
            i++;
            swap_elements(&arr[i], &arr[j]);
        }
    }
    
    // 将pivot放到正确位置
    swap_elements(&arr[i + 1], &arr[high]);
    return i + 1;
}

// ============================================================================
// 快速排序实现
// ============================================================================

// 递归快速排序
SortError quick_sort_recursive(int arr[], int low, int high, PivotStrategy strategy) {
    if (arr == NULL) return SORT_ERROR_NULL_POINTER;
    if (low < 0 || high < 0 || low > high) return SORT_ERROR_INVALID_SIZE;
    
    if (low < high) {
        int pivot_index = partition_array(arr, low, high, strategy);
        
        // 递归排序左半部分
        SortError left_error = quick_sort_recursive(arr, low, pivot_index - 1, strategy);
        if (left_error != SORT_SUCCESS) return left_error;
        
        // 递归排序右半部分
        SortError right_error = quick_sort_recursive(arr, pivot_index + 1, high, strategy);
        if (right_error != SORT_SUCCESS) return right_error;
    }
    
    return SORT_SUCCESS;
}

// 非递归快速排序（使用栈）
typedef struct {
    int low;
    int high;
} StackItem;

SortError quick_sort_iterative(int arr[], int low, int high, PivotStrategy strategy) {
    if (arr == NULL) return SORT_ERROR_NULL_POINTER;
    if (low < 0 || high < 0 || low > high) return SORT_ERROR_INVALID_SIZE;
    
    // 创建栈
    int stack_size = high - low + 1;
    StackItem* stack = (StackItem*)malloc(stack_size * sizeof(StackItem));
    if (stack == NULL) return SORT_ERROR_MEMORY_ALLOC;
    
    int top = -1;
    
    // 初始区间入栈
    stack[++top].low = low;
    stack[top].high = high;
    
    while (top >= 0) {
        // 弹出区间
        int current_low = stack[top].low;
        int current_high = stack[top--].high;
        
        if (current_low < current_high) {
            int pivot_index = partition_array(arr, current_low, current_high, strategy);
            
            // 将左区间入栈
            if (pivot_index - 1 > current_low) {
                stack[++top].low = current_low;
                stack[top].high = pivot_index - 1;
            }
            
            // 将右区间入栈
            if (pivot_index + 1 < current_high) {
                stack[++top].low = pivot_index + 1;
                stack[top].high = current_high;
            }
        }
    }
    
    free(stack);
    return SORT_SUCCESS;
}

// ============================================================================
// 归并排序实现
// ============================================================================

// 合并两个有序数组
void merge_arrays(int arr[], int left, int mid, int right) {
    int left_size = mid - left + 1;
    int right_size = right - mid;
    
    // 创建临时数组
    int* left_arr = (int*)malloc(left_size * sizeof(int));
    int* right_arr = (int*)malloc(right_size * sizeof(int));
    
    if (left_arr == NULL || right_arr == NULL) {
        if (left_arr) free(left_arr);
        if (right_arr) free(right_arr);
        return;
    }
    
    // 复制数据到临时数组
    for (int i = 0; i < left_size; i++)
        left_arr[i] = arr[left + i];
    for (int j = 0; j < right_size; j++)
        right_arr[j] = arr[mid + 1 + j];
    
    // 合并临时数组回原数组
    int i = 0, j = 0, k = left;
    while (i < left_size && j < right_size) {
        if (left_arr[i] <= right_arr[j]) {
            arr[k] = left_arr[i];
            i++;
        } else {
            arr[k] = right_arr[j];
            j++;
        }
        k++;
    }
    
    // 复制剩余元素
    while (i < left_size) {
        arr[k] = left_arr[i];
        i++;
        k++;
    }
    
    while (j < right_size) {
        arr[k] = right_arr[j];
        j++;
        k++;
    }
    
    free(left_arr);
    free(right_arr);
}

// 串行归并排序（内部使用）
static SortError merge_sort_serial(int arr[], int left, int right) {
    if (arr == NULL) return SORT_ERROR_NULL_POINTER;
    if (left < 0 || right < 0 || left > right) return SORT_ERROR_INVALID_SIZE;
    
    if (left < right) {
        int mid = left + (right - left) / 2;
        
        // 递归排序左半部分
        SortError left_error = merge_sort_serial(arr, left, mid);
        if (left_error != SORT_SUCCESS) return left_error;
        
        // 递归排序右半部分
        SortError right_error = merge_sort_serial(arr, mid + 1, right);
        if (right_error != SORT_SUCCESS) return right_error;
        
        // 合并两个有序部分
        merge_arrays(arr, left, mid, right);
    }
    
    return SORT_SUCCESS;
}

// 并行归并排序
SortError merge_sort_parallel(int arr[], int left, int right) {
    if (arr == NULL) return SORT_ERROR_NULL_POINTER;
    if (left < 0 || right < 0 || left > right) return SORT_ERROR_INVALID_SIZE;
    
    // 设置阈值，小数组使用串行版本
    const int PARALLEL_THRESHOLD = 1000;
    
    if (right - left < PARALLEL_THRESHOLD) {
        return merge_sort_serial(arr, left, right);
    }
    
    if (left < right) {
        int mid = left + (right - left) / 2;
        
        #ifdef _OPENMP
        // 使用OpenMP并行处理两个子数组
        #pragma omp parallel sections
        {
            #pragma omp section
            {
                merge_sort_parallel(arr, left, mid);
            }
            
            #pragma omp section
            {
                merge_sort_parallel(arr, mid + 1, right);
            }
        }
        #else
        // 如果没有OpenMP支持，使用串行版本
        merge_sort_parallel(arr, left, mid);
        merge_sort_parallel(arr, mid + 1, right);
        #endif
        
        // 合并结果
        merge_arrays(arr, left, mid, right);
    }
    
    return SORT_SUCCESS;
}
