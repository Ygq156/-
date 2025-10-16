# ============================================================================
# 排序算法性能分析项目 Makefile
# ============================================================================

# 编译器设置
CC = gcc                                                       // 指定使用 GCC 编译器
CFLAGS = -Wall -Wextra -g -I./src                              //CFLAGS指代包含，-Wall指启用所有警告，-Wextra指启用额外警告，-g指生成调试信息，-I./src指添加头文件搜索路径
TARGET = sort_analysis                                         //TARGET= + 运动程序
SOURCES = src/main.c src/test_data.c src/sort_algorithms.c     //SOURCES= + 要执行的程序

# OpenMP支持（如果可用）
ifeq ($(shell which gcc >/dev/null 2>&1 && gcc -fopenmp -E - < /dev/null > /dev/null 2>&1 && echo 1),1)   //
    CFLAGS += -fopenmp
    OPENMP_SUPPORT = yes
else
    OPENMP_SUPPORT = no
endif

# 优化级别
OPTIMIZATIONS = -O0 -O1 -O2 -O3

# 小规模测试标志
SMALL_SCALE_FLAG = -DSMALL_SCALE

# 默认目标
.PHONY: all clean test small_test optimizations performance_test analyze

# 默认编译（使用O2优化）
all: $(TARGET)

$(TARGET): $(SOURCES)
	@echo "编译主程序 (O2优化)..."
	@echo "OpenMP支持: $(OPENMP_SUPPORT)"
	$(CC) $(CFLAGS) -O2 -o $(TARGET) $(SOURCES)
	@echo "✓ 编译完成: $(TARGET)"

# 小规模测试版本
small_test: $(SOURCES)
	@echo "编译小规模测试版本..."
	$(CC) $(CFLAGS) -O0 $(SMALL_SCALE_FLAG) -o $(TARGET)_small $(SOURCES)
	@echo "✓ 编译完成: $(TARGET)_small"
	@echo "=== 运行小规模测试 ==="
	./$(TARGET)_small

# 不同优化级别编译
optimizations: $(SOURCES)
	@echo "编译不同优化级别的版本..."
	@for opt in $(OPTIMIZATIONS); do \
		echo "编译优化级别: $$opt..."; \
		$(CC) $(CFLAGS) $$opt -o $(TARGET)_$$opt $(SOURCES); \
	done
	@echo "✓ 所有优化级别编译完成"

# 性能测试
performance_test: optimizations
	@echo "=== 运行性能测试 (包含Pivot策略比较) ==="
	@for opt in $(OPTIMIZATIONS); do \
		echo "--- 优化级别: $$opt ---"; \
		./$(TARGET)_$$opt 2>/dev/null | grep -E "(测试|Quick Sort|Merge Sort|时间|成功|失败)"; \
		echo ""; \
	done
	@echo "=== 性能测试完成 ==="

# Python数据分析
analyze:
	@echo "=== 运行数据分析 (Pivot策略分析) ==="
	cd scripts && python3 analyze_results.py && cd ..
	@echo "=== 数据分析完成 ==="

# 完整测试流程
all_tests: clean small_test performance_test analyze
	@echo "=== 完整测试流程完成 ==="

# 清理
clean:
	@echo "清理构建文件..."
	rm -f $(TARGET) $(TARGET)_* 
	rm -rf data/*.txt results/*.png results/*.txt results/*.csv
	@echo "✓ 清理完成"

# 运行测试
test: $(TARGET)
	@echo "=== 运行测试 ==="
	./$(TARGET)

# 专门测试pivot策略
pivot_test: $(TARGET)
	@echo "=== 专门测试Pivot策略 ==="
	./$(TARGET) | grep -E "(测试|Quick Sort.*First|Quick Sort.*Last|Quick Sort.*Middle|Quick Sort.*Random|Quick Sort.*Median3)"

# 显示项目信息
info:
	@echo "=== 项目信息 ==="
	@echo "项目名称: 排序算法性能分析"
	@echo "OpenMP支持: $(OPENMP_SUPPORT)"
	@echo "支持的排序算法:"
	@echo "  - 快速排序 (递归 + 非递归)"
	@echo "  - 归并排序 (并行版本)"
	@echo "Pivot选择策略:"
	@echo "  - First, Last, Middle, Random, Median3"
	@echo "编译目标:"
	@echo "  - make all: 编译主程序"
	@echo "  - make test: 运行测试"
	@echo "  - make analyze: 分析结果"
	@echo "  - make clean: 清理文件"
