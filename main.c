#include "sort_algorithms.h"
#include "test_data.h"
#include <sys/time.h>
#include <string.h>

// 获取当前时间（微秒）
double get_current_time() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (double)tv.tv_sec * 1000000 + (double)tv.tv_usec;
}

// 排序算法测试函数
void test_sort_algorithm(const char* name, 
                        SortError (*sort_func)(int[], int, int, PivotStrategy), 
                        int arr[], int n, int* original, 
                        PivotStrategy strategy) {
    if (arr == NULL || original == NULL || name == NULL) {
        printf("错误: 测试参数为空指针\n");
        return;
    }
    
    // 复制原始数据
    int* test_arr = (int*)malloc(n * sizeof(int));
    if (test_arr == NULL) {
        printf("错误: 无法为测试数组分配内存\n");
        return;
    }
    
    SortError copy_error = copy_array(test_arr, original, n);
    if (copy_error != SORT_SUCCESS) {
        printf("错误: 复制数组失败\n");
        free(test_arr);
        return;
    }
    
    // 测量排序时间
    double start_time = get_current_time();
    SortError sort_error = sort_func(test_arr, 0, n - 1, strategy);
    double end_time = get_current_time();
    
    double elapsed_time = (end_time - start_time) / 1000.0; // 转换为毫秒
    
    // 验证排序结果
    int sorted = (sort_error == SORT_SUCCESS) ? is_sorted(test_arr, n) : 0;
    
    // 获取pivot策略名称
    const char* strategy_name = pivot_strategy_name(strategy);
    
    // 输出结果
    if (sort_error != SORT_SUCCESS) {
        printf("%-25s (%-8s): 错误代码 %d\n", name, strategy_name, sort_error);
    } else {
        printf("%-25s (%-8s): 时间 = %8.3f ms, 排序 %s\n", 
               name, strategy_name, elapsed_time, sorted ? "成功" : "失败");
    }
    
    // 记录到性能日志文件
    FILE* log_file = fopen("results/performance_log.txt", "a");
    if (log_file) {
        fprintf(log_file, "%s,%s,%d,%.3f,%d\n", 
                name, strategy_name, n, elapsed_time, sorted);
        fclose(log_file);
    }
    
    free(test_arr);
}

// 测试归并排序的包装函数（不需要pivot策略）
void test_merge_sort(const char* name, 
                    SortError (*sort_func)(int[], int, int), 
                    int arr[], int n, int* original) {
    if (arr == NULL || original == NULL || name == NULL) {
        printf("错误: 测试参数为空指针\n");
        return;
    }
    
    // 复制原始数据
    int* test_arr = (int*)malloc(n * sizeof(int));
    if (test_arr == NULL) {
        printf("错误: 无法为测试数组分配内存\n");
        return;
    }
    
    SortError copy_error = copy_array(test_arr, original, n);
    if (copy_error != SORT_SUCCESS) {
        printf("错误: 复制数组失败\n");
        free(test_arr);
        return;
    }
    
    // 测量排序时间
    double start_time = get_current_time();
    SortError sort_error = sort_func(test_arr, 0, n - 1);
    double end_time = get_current_time();
    
    double elapsed_time = (end_time - start_time) / 1000.0; // 转换为毫秒
    
    // 验证排序结果
    int sorted = (sort_error == SORT_SUCCESS) ? is_sorted(test_arr, n) : 0;
    
    // 输出结果
    if (sort_error != SORT_SUCCESS) {
        printf("%-25s (%-8s): 错误代码 %d\n", name, "N/A", sort_error);
    } else {
        printf("%-25s (%-8s): 时间 = %8.3f ms, 排序 %s\n", 
               name, "N/A", elapsed_time, sorted ? "成功" : "失败");
    }
    
    // 记录到性能日志文件
    FILE* log_file = fopen("results/performance_log.txt", "a");
    if (log_file) {
        fprintf(log_file, "%s,%s,%d,%.3f,%d\n", 
                name, "N/A", n, elapsed_time, sorted);
        fclose(log_file);
    }
    
    free(test_arr);
}

// 小规模测试（验证算法正确性）
void run_small_test() {
    printf("\n=== 小规模测试（验证算法正确性） ===\n");
    
    int test_data[] = {5, 2, 8, 1, 9, 3, 7, 4, 6, 0};
    int size = sizeof(test_data) / sizeof(test_data[0]);
    
    printf("原始数据: ");
    print_array(test_data, size);
    
    // 测试不同pivot策略的快速排序
    PivotStrategy strategies[] = {
        PIVOT_FIRST, PIVOT_LAST, PIVOT_MIDDLE, 
        PIVOT_RANDOM, PIVOT_MEDIAN_OF_THREE
    };
    const char* strategy_names[] = {
        "First", "Last", "Middle", "Random", "Median3"
    };
    int num_strategies = sizeof(strategies) / sizeof(strategies[0]);
    
    for (int i = 0; i < num_strategies; i++) {
        int* qs_data = (int*)malloc(size * sizeof(int));
        if (qs_data) {
            copy_array(qs_data, test_data, size);
            quick_sort_recursive(qs_data, 0, size - 1, strategies[i]);
            printf("快速排序(%-8s): ", strategy_names[i]);
            print_array(qs_data, size);
            printf("排序%s\n", is_sorted(qs_data, size) ? "成功" : "失败");
            free(qs_data);
        }
    }
    
    // 测试归并排序
    int* ms_data = (int*)malloc(size * sizeof(int));
    if (ms_data) {
        copy_array(ms_data, test_data, size);
        merge_sort_parallel(ms_data, 0, size - 1);
        printf("归并排序(并行):   ");
        print_array(ms_data, size);
        printf("排序%s\n", is_sorted(ms_data, size) ? "成功" : "失败");
        free(ms_data);
    }
    
    printf("=== 小规模测试完成 ===\n");
}

int main() {
    printf("=== 排序算法性能分析（Pivot策略比较 + 并行归并） ===\n");
    
    // 显示当前工作目录
    char cwd[1024];
    if (getcwd(cwd, sizeof(cwd)) != NULL) {
        printf("当前工作目录: %s\n", cwd);
    }
    
    // 创建必要的目录
    system("mkdir -p data results");
    printf("已创建 data 和 results 目录\n");
    
    // 先运行小规模测试
    run_small_test();
    
    // 定义测试规模
    const int sizes[] = {1000, 5000, 10000, 50000, 100000};
    const int num_sizes = sizeof(sizes) / sizeof(sizes[0]);
    
    // 清空性能日志
    FILE* log_file = fopen("results/performance_log.txt", "w");
    if (log_file) {
        fprintf(log_file, "Algorithm,PivotStrategy,Size,Time(ms),Sorted\n");
        fclose(log_file);
        printf("已初始化性能日志: results/performance_log.txt\n");
    } else {
        printf("错误: 无法初始化性能日志文件\n");
    }
    
    // 生成和测试不同规模的数据
    printf("\n生成测试数据...\n");
    for (int i = 0; i < num_sizes; i++) {
        char filename[256];
        snprintf(filename, sizeof(filename), "data/test_data_%d.txt", sizes[i]);
        
        DataError gen_error = generate_test_data(filename, sizes[i]);
        if (gen_error != DATA_SUCCESS) {
            printf("警告: 生成测试数据失败，跳过规模 %d\n", sizes[i]);
            continue;
        }
    }
    
    printf("\n测试排序算法...\n");
    
    // 定义所有pivot策略
    PivotStrategy all_strategies[] = {
        PIVOT_FIRST, PIVOT_LAST, PIVOT_MIDDLE, 
        PIVOT_RANDOM, PIVOT_MEDIAN_OF_THREE
    };
    int num_strategies = sizeof(all_strategies) / sizeof(all_strategies[0]);
    
    // 测试不同规模的数据
    for (int i = 0; i < num_sizes; i++) {
        char filename[256];
        snprintf(filename, sizeof(filename), "data/test_data_%d.txt", sizes[i]);
        
        int size;
        DataError read_error;
        int* data = read_test_data(filename, &size, &read_error);
        
        if (data == NULL) {
            printf("警告: 读取测试数据失败，跳过规模 %d\n", sizes[i]);
            continue;
        }
        
        printf("\n--- 测试规模: %d 个元素 ---\n", size);
        
        // 测试所有pivot策略的快速排序
        for (int s = 0; s < num_strategies; s++) {
            test_sort_algorithm("Quick Sort (Recursive)", quick_sort_recursive, 
                               data, size, data, all_strategies[s]);
            test_sort_algorithm("Quick Sort (Iterative)", quick_sort_iterative, 
                               data, size, data, all_strategies[s]);
        }
        
        // 测试并行归并排序
        test_merge_sort("Merge Sort (Parallel)", merge_sort_parallel, 
                       data, size, data);
        
        free_test_data(data);
    }
    
    printf("\n=== 性能测试完成 ===\n");
    printf("结果已保存到: results/performance_log.txt\n");
    
    // 验证文件确实存在
    printf("\n生成的文件清单:\n");
    system("find . -name \"*.txt\" -o -name \"*.csv\" 2>/dev/null | head -10");
    
    return 0;
}
