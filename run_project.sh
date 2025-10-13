#!/bin/bash

echo "===================================================================="
echo "   排序算法性能分析项目 (Pivot策略比较 + 并行归并)"
echo "===================================================================="
echo "项目目录: $(pwd)"
echo "开始时间: $(date)"
echo ""

# 1. 检查环境
echo "步骤1: 检查环境..."
gcc --version > /dev/null 2>&1 && echo "✓ GCC 编译器" || echo "✗ GCC 编译器未安装"
python3 --version > /dev/null 2>&1 && echo "✓ Python3" || echo "✗ Python3 未安装"

# 检查OpenMP支持
if gcc -fopenmp -E - < /dev/null > /dev/null 2>&1; then
    echo "✓ OpenMP 支持已启用"
else
    echo "⚠ OpenMP 不支持（并行归并排序将使用串行版本）"
fi

# 2. 清理和编译
echo ""
echo "步骤2: 编译程序..."
make clean
make all

# 3. 运行小规模测试
echo ""
echo "步骤3: 运行小规模测试..."
make small_test

# 4. 运行性能测试
echo ""
echo "步骤4: 运行性能测试 (包含Pivot策略比较)..."
make performance_test

# 5. 运行数据分析
echo ""
echo "步骤5: 运行数据分析 (Pivot策略分析)..."
if python3 --version > /dev/null 2>&1; then
    make analyze
else
    echo "跳过数据分析 (Python3未安装)"
fi

echo ""
echo "===================================================================="
echo "   项目运行完成"
echo "===================================================================="
echo "完成时间: $(date)"
echo ""
echo "📊 生成的结果文件:"
find results/ -type f 2>/dev/null | while read file; do
    echo "  - $file"
done

echo ""
echo "💡 项目特色:"
echo "  • 快速排序: 递归 + 非递归版本，5种pivot选择策略"
echo "  • 归并排序: 并行版本（使用OpenMP）"
echo "  • 不依赖标准库排序函数"
echo "  • 完整的性能分析和可视化"
echo ""
echo "🚀 下一步:"
echo "  查看 results/pivot_analysis_report.txt 获取详细分析结论"
echo "  查看 results/ 目录中的图表文件可视化分析结果"
