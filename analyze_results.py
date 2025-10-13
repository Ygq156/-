#!/usr/bin/env python3
"""
排序算法性能数据分析脚本 - 完整版本
包含散点图、折线图、柱状图等多种可视化
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from datetime import datetime

def setup_plot_style():
    """设置绘图样式"""
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False
    plt.style.use('default')
    print("✓ 绘图样式设置完成")

def check_dependencies():
    """检查依赖包"""
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
        import numpy as np
        print("✓ 所有依赖包已安装")
        return True
    except ImportError as e:
        print(f"✗ 缺少依赖包: {e}")
        print("请运行: pip install matplotlib pandas numpy")
        return False

def find_performance_log():
    """查找性能日志文件"""
    possible_paths = [
        '../results/performance_log.txt',
        './results/performance_log.txt',
        'results/performance_log.txt',
        '../performance_log.txt',
        './performance_log.txt',
        'performance_log.txt'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✓ 找到性能日志文件: {path}")
            return path
    
    print("✗ 错误: 找不到性能日志文件")
    print("请先运行性能测试程序")
    return None

def parse_performance_log(log_file):
    """解析性能日志文件"""
    try:
        df = pd.read_csv(log_file)
        print(f"✓ 成功读取性能数据: {len(df)} 条记录")
        
        # 数据质量检查
        print(f"  数据规模范围: {df['Size'].min()} - {df['Size'].max()}")
        
        # 安全地获取列信息
        if 'Algorithm' in df.columns:
            print(f"  算法数量: {len(df['Algorithm'].unique())}")
        if 'PivotStrategy' in df.columns:
            print(f"  Pivot策略数量: {len(df['PivotStrategy'].unique())}")
        
        return df
    except Exception as e:
        print(f"✗ 读取性能日志失败: {e}")
        return pd.DataFrame()

def create_scatter_plots(df):
    """创建散点图分析"""
    if df.empty:
        print("✗ 没有数据可生成散点图")
        return
    
    print("\n=== 生成散点图分析 ===")
    
    # 确保结果目录存在
    os.makedirs('../results', exist_ok=True)
    
    # 1. 所有算法的散点图
    plt.figure(figsize=(14, 10))
    
    # 定义颜色和标记
    algorithms = df['Algorithm'].unique()
    colors = plt.cm.Set3(np.linspace(0, 1, len(algorithms)))
    
    for i, algo in enumerate(algorithms):
        algo_data = df[df['Algorithm'] == algo].copy()
        algo_data['Time(ms)'] = pd.to_numeric(algo_data['Time(ms)'], errors='coerce')
        algo_data['Size'] = pd.to_numeric(algo_data['Size'], errors='coerce')
        algo_data = algo_data.dropna(subset=['Time(ms)', 'Size'])
        
        if not algo_data.empty:
            plt.scatter(algo_data['Size'], algo_data['Time(ms)'], 
                       color=colors[i], label=algo, alpha=0.7, s=60, edgecolors='black', linewidth=0.5)
    
    plt.xlabel('数据规模', fontsize=12, fontweight='bold')
    plt.ylabel('排序时间 (ms)', fontsize=12, fontweight='bold')
    plt.title('所有排序算法性能散点图', fontsize=14, fontweight='bold')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../results/all_algorithms_scatter.png', dpi=300, bbox_inches='tight')
    print("✓ 生成散点图: all_algorithms_scatter.png")
    
    # 2. 快速排序不同pivot策略的散点图
    plt.figure(figsize=(14, 10))
    
    quick_sort_data = df[df['Algorithm'].str.contains('Quick Sort', na=False)].copy()
    pivot_strategies = quick_sort_data['PivotStrategy'].unique()
    
    colors_pivot = plt.cm.viridis(np.linspace(0, 1, len(pivot_strategies)))
    markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h']
    
    for i, strategy in enumerate(pivot_strategies):
        strategy_data = quick_sort_data[quick_sort_data['PivotStrategy'] == strategy].copy()
        strategy_data['Time(ms)'] = pd.to_numeric(strategy_data['Time(ms)'], errors='coerce')
        strategy_data['Size'] = pd.to_numeric(strategy_data['Size'], errors='coerce')
        strategy_data = strategy_data.dropna(subset=['Time(ms)', 'Size'])
        
        if not strategy_data.empty:
            plt.scatter(strategy_data['Size'], strategy_data['Time(ms)'], 
                       color=colors_pivot[i], marker=markers[i % len(markers)], 
                       label=f'{strategy}', alpha=0.8, s=80, edgecolors='white', linewidth=1)
    
    plt.xlabel('数据规模', fontsize=12, fontweight='bold')
    plt.ylabel('排序时间 (ms)', fontsize=12, fontweight='bold')
    plt.title('快速排序不同Pivot策略性能散点图', fontsize=14, fontweight='bold')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../results/quick_sort_pivot_scatter.png', dpi=300, bbox_inches='tight')
    print("✓ 生成散点图: quick_sort_pivot_scatter.png")
    
    # 3. 递归vs迭代快速排序散点图对比
    plt.figure(figsize=(14, 8))
    
    recursive_data = df[df['Algorithm'] == 'Quick Sort (Recursive)'].copy()
    iterative_data = df[df['Algorithm'] == 'Quick Sort (Iterative)'].copy()
    
    # 只使用Median3策略进行比较
    recursive_median = recursive_data[recursive_data['PivotStrategy'] == 'Median3'].copy()
    iterative_median = iterative_data[iterative_data['PivotStrategy'] == 'Median3'].copy()
    
    recursive_median['Time(ms)'] = pd.to_numeric(recursive_median['Time(ms)'], errors='coerce')
    recursive_median['Size'] = pd.to_numeric(recursive_median['Size'], errors='coerce')
    iterative_median['Time(ms)'] = pd.to_numeric(iterative_median['Time(ms)'], errors='coerce')
    iterative_median['Size'] = pd.to_numeric(iterative_median['Size'], errors='coerce')
    
    recursive_median = recursive_median.dropna(subset=['Time(ms)', 'Size'])
    iterative_median = iterative_median.dropna(subset=['Time(ms)', 'Size'])
    
    plt.scatter(recursive_median['Size'], recursive_median['Time(ms)'], 
               color='red', marker='o', label='递归快速排序 (Median3)', alpha=0.7, s=70)
    plt.scatter(iterative_median['Size'], iterative_median['Time(ms)'], 
               color='blue', marker='s', label='迭代快速排序 (Median3)', alpha=0.7, s=70)
    
    plt.xlabel('数据规模', fontsize=12, fontweight='bold')
    plt.ylabel('排序时间 (ms)', fontsize=12, fontweight='bold')
    plt.title('递归 vs 迭代快速排序性能散点图对比 (Median3 Pivot)', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../results/recursive_vs_iterative_scatter.png', dpi=300, bbox_inches='tight')
    print("✓ 生成散点图: recursive_vs_iterative_scatter.png")
    
    # 4. 性能密度散点图（用颜色表示性能密度）
    plt.figure(figsize=(14, 10))
    
    # 为所有数据点创建性能密度映射
    all_data = df.copy()
    all_data['Time(ms)'] = pd.to_numeric(all_data['Time(ms)'], errors='coerce')
    all_data['Size'] = pd.to_numeric(all_data['Size'], errors='coerce')
    all_data = all_data.dropna(subset=['Time(ms)', 'Size'])
    
    # 计算每个数据点的相对性能（相对于该规模下的最快时间）
    performance_ratio = []
    for size in all_data['Size'].unique():
        size_data = all_data[all_data['Size'] == size]
        min_time = size_data['Time(ms)'].min()
        for idx, row in size_data.iterrows():
            ratio = row['Time(ms)'] / min_time if min_time > 0 else 1
            performance_ratio.append(ratio)
    
    all_data['PerformanceRatio'] = performance_ratio
    
    scatter = plt.scatter(all_data['Size'], all_data['Time(ms)'], 
                         c=all_data['PerformanceRatio'], cmap='RdYlGn_r', 
                         alpha=0.7, s=60, edgecolors='black', linewidth=0.5)
    
    plt.colorbar(scatter, label='性能比率 (相对于最快算法)')
    plt.xlabel('数据规模', fontsize=12, fontweight='bold')
    plt.ylabel('排序时间 (ms)', fontsize=12, fontweight='bold')
    plt.title('排序算法性能密度散点图\n(颜色表示相对于最快算法的性能比率)', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../results/performance_density_scatter.png', dpi=300, bbox_inches='tight')
    print("✓ 生成散点图: performance_density_scatter.png")
    
    plt.close('all')

def create_pivot_analysis_charts(df):
    """创建pivot策略分析图表"""
    if df.empty:
        print("✗ 没有数据可分析")
        return
    
    # 确保结果目录存在
    os.makedirs('../results', exist_ok=True)
    
    print("\n=== 生成Pivot策略分析图表 ===")
    
    # 检查必要的列是否存在
    required_columns = ['Algorithm', 'PivotStrategy', 'Size', 'Time(ms)']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"✗ 缺少必要列: {missing_columns}")
        return
    
    # 1. 不同pivot策略性能比较（递归快速排序）
    plt.figure(figsize=(14, 8))
    
    pivot_strategies = ['First', 'Last', 'Middle', 'Random', 'Median3']
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    markers = ['o', 's', '^', 'D', 'v']
    
    # 筛选递归快速排序的结果
    qs_recursive = df[df['Algorithm'] == 'Quick Sort (Recursive)'].copy()
    
    # 确保数据是数值类型
    qs_recursive['Time(ms)'] = pd.to_numeric(qs_recursive['Time(ms)'], errors='coerce')
    qs_recursive['Size'] = pd.to_numeric(qs_recursive['Size'], errors='coerce')
    qs_recursive = qs_recursive.dropna(subset=['Time(ms)', 'Size'])
    
    for i, strategy in enumerate(pivot_strategies):
        strategy_data = qs_recursive[qs_recursive['PivotStrategy'] == strategy]
        if not strategy_data.empty:
            strategy_data = strategy_data.sort_values('Size')
            plt.plot(strategy_data['Size'], strategy_data['Time(ms)'], 
                    marker=markers[i], label=f'{strategy}', 
                    color=colors[i], linewidth=2.5, markersize=8, markeredgecolor='white', markeredgewidth=1)
    
    plt.xlabel('数据规模', fontsize=12, fontweight='bold')
    plt.ylabel('排序时间 (ms)', fontsize=12, fontweight='bold')
    plt.title('不同Pivot选择策略对快速排序性能的影响\n(递归版本)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../results/pivot_strategy_comparison_recursive.png', dpi=300, bbox_inches='tight')
    print("✓ 生成图表: pivot_strategy_comparison_recursive.png")
    
    # 2. 不同pivot策略性能比较（迭代快速排序）
    plt.figure(figsize=(14, 8))
    
    qs_iterative = df[df['Algorithm'] == 'Quick Sort (Iterative)'].copy()
    
    qs_iterative['Time(ms)'] = pd.to_numeric(qs_iterative['Time(ms)'], errors='coerce')
    qs_iterative['Size'] = pd.to_numeric(qs_iterative['Size'], errors='coerce')
    qs_iterative = qs_iterative.dropna(subset=['Time(ms)', 'Size'])
    
    for i, strategy in enumerate(pivot_strategies):
        strategy_data = qs_iterative[qs_iterative['PivotStrategy'] == strategy]
        if not strategy_data.empty:
            strategy_data = strategy_data.sort_values('Size')
            plt.plot(strategy_data['Size'], strategy_data['Time(ms)'], 
                    marker=markers[i], label=f'{strategy}', 
                    color=colors[i], linewidth=2.5, markersize=8, markeredgecolor='white', markeredgewidth=1)
    
    plt.xlabel('数据规模', fontsize=12, fontweight='bold')
    plt.ylabel('排序时间 (ms)', fontsize=12, fontweight='bold')
    plt.title('不同Pivot选择策略对快速排序性能的影响\n(迭代版本)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../results/pivot_strategy_comparison_iterative.png', dpi=300, bbox_inches='tight')
    print("✓ 生成图表: pivot_strategy_comparison_iterative.png")
    
    # 3. 所有算法性能比较
    plt.figure(figsize=(14, 8))
    
    algorithms_comparison = {
        'Quick Sort (Recursive) - Median3': ('Quick Sort (Recursive)', 'Median3'),
        'Quick Sort (Iterative) - Median3': ('Quick Sort (Iterative)', 'Median3'),
        'Merge Sort (Parallel)': ('Merge Sort (Parallel)', 'N/A')
    }
    
    colors_algo = ['#E74C3C', '#3498DB', '#2ECC71']
    markers_algo = ['o', 's', '^']
    
    for i, (label, (algo, strategy)) in enumerate(algorithms_comparison.items()):
        if strategy == 'N/A':
            # 归并排序
            algo_data = df[df['Algorithm'] == algo].copy()
        else:
            # 快速排序（使用Median3策略）
            algo_data = df[(df['Algorithm'] == algo) & (df['PivotStrategy'] == strategy)].copy()
        
        algo_data['Time(ms)'] = pd.to_numeric(algo_data['Time(ms)'], errors='coerce')
        algo_data['Size'] = pd.to_numeric(algo_data['Size'], errors='coerce')
        algo_data = algo_data.dropna(subset=['Time(ms)', 'Size'])
        
        if not algo_data.empty:
            algo_data = algo_data.sort_values('Size')
            plt.plot(algo_data['Size'], algo_data['Time(ms)'], 
                    marker=markers_algo[i], label=label, 
                    color=colors_algo[i], linewidth=2.5, markersize=8)
    
    plt.xlabel('数据规模', fontsize=12, fontweight='bold')
    plt.ylabel('排序时间 (ms)', fontsize=12, fontweight='bold')
    plt.title('排序算法性能比较 (使用最佳Pivot策略)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../results/algorithm_comparison_best_pivot.png', dpi=300, bbox_inches='tight')
    print("✓ 生成图表: algorithm_comparison_best_pivot.png")
    
    # 4. Pivot策略性能排名（柱状图）
    plt.figure(figsize=(12, 8))
    
    # 分析所有快速排序结果
    all_quick_sort = df[df['Algorithm'].str.contains('Quick Sort', na=False)].copy()
    
    all_quick_sort['Time(ms)'] = pd.to_numeric(all_quick_sort['Time(ms)'], errors='coerce')
    all_quick_sort = all_quick_sort.dropna(subset=['Time(ms)'])
    
    pivot_performance = []
    
    for strategy in pivot_strategies:
        strategy_data = all_quick_sort[all_quick_sort['PivotStrategy'] == strategy]
        if not strategy_data.empty:
            # 计算该策略在所有规模下的平均相对性能
            avg_time = strategy_data['Time(ms)'].mean()
            pivot_performance.append((strategy, avg_time))
    
    if pivot_performance:
        # 按性能排序（从快到慢）
        pivot_performance.sort(key=lambda x: x[1])
        strategies_sorted = [x[0] for x in pivot_performance]
        times_sorted = [x[1] for x in pivot_performance]
        
        # 创建渐变色
        cmap = plt.cm.viridis
        colors_bar = [cmap(i / len(strategies_sorted)) for i in range(len(strategies_sorted))]
        
        bars = plt.bar(strategies_sorted, times_sorted, color=colors_bar, edgecolor='black')
        plt.xlabel('Pivot选择策略', fontsize=12, fontweight='bold')
        plt.ylabel('平均排序时间 (ms)', fontsize=12, fontweight='bold')
        plt.title('Pivot选择策略性能排名\n(所有数据规模平均值)', fontsize=14, fontweight='bold')
        
        # 在柱子上添加数值和排名
        for i, (bar, time_val) in enumerate(zip(bars, times_sorted)):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(times_sorted)*0.01,
                    f'{time_val:.1f} ms\n(#{(i+1)})', ha='center', va='bottom', fontweight='bold')
        
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig('../results/pivot_strategy_ranking.png', dpi=300, bbox_inches='tight')
        print("✓ 生成图表: pivot_strategy_ranking.png")
    
    plt.close('all')

def generate_analysis_report(df):
    """生成完整的分析报告"""
    if df.empty:
        return
    
    report_path = '../results/complete_analysis_report.txt'
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("排序算法性能完整分析报告\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"数据记录总数: {len(df)}\n\n")
        
        # 基本统计信息
        f.write("1. 测试概况\n")
        f.write("-" * 50 + "\n")
        
        if 'Algorithm' in df.columns:
            algorithms = df['Algorithm'].unique()
            f.write(f"测试的算法: {', '.join(map(str, algorithms))}\n")
        
        if 'PivotStrategy' in df.columns:
            strategies = [s for s in df['PivotStrategy'].unique() if str(s) != 'N/A']
            f.write(f"测试的Pivot策略: {', '.join(map(str, strategies))}\n")
        
        if 'Size' in df.columns:
            sizes = sorted(df['Size'].unique())
            f.write(f"测试的数据规模: {', '.join(map(str, sizes))}\n")
        
        f.write(f"成功排序的记录: {df['Sorted'].sum() if 'Sorted' in df.columns else 'N/A'}\n\n")
        
        # 性能分析
        f.write("2. 性能分析结果\n")
        f.write("-" * 50 + "\n")
        
        # 分析每个算法的平均性能
        if 'Algorithm' in df.columns and 'Time(ms)' in df.columns:
            df_numeric = df.copy()
            df_numeric['Time(ms)'] = pd.to_numeric(df_numeric['Time(ms)'], errors='coerce')
            df_numeric = df_numeric.dropna(subset=['Time(ms)'])
            
            algo_performance = df_numeric.groupby('Algorithm')['Time(ms)'].mean().sort_values()
            
            f.write("算法平均性能排名 (从快到慢):\n")
            for i, (algo, avg_time) in enumerate(algo_performance.items(), 1):
                f.write(f"  {i:2d}. {algo:<30} : {avg_time:.2f} ms\n")
            f.write("\n")
        
        # Pivot策略分析
        quick_sort_data = df[df['Algorithm'].str.contains('Quick Sort', na=False)].copy()
        if not quick_sort_data.empty and 'PivotStrategy' in quick_sort_data.columns:
            quick_sort_data['Time(ms)'] = pd.to_numeric(quick_sort_data['Time(ms)'], errors='coerce')
            quick_sort_data = quick_sort_data.dropna(subset=['Time(ms)'])
            
            pivot_performance = quick_sort_data.groupby('PivotStrategy')['Time(ms)'].mean().sort_values()
            
            f.write("Pivot策略平均性能排名 (从快到慢):\n")
            for i, (strategy, avg_time) in enumerate(pivot_performance.items(), 1):
                f.write(f"  {i:2d}. {strategy:<15} : {avg_time:.2f} ms\n")
            f.write("\n")
        
        # 规模扩展性分析
        f.write("3. 规模扩展性分析\n")
        f.write("-" * 50 + "\n")
        
        if 'Size' in df.columns and 'Time(ms)' in df.columns:
            sizes = sorted(df['Size'].unique())
            for size in sizes:
                size_data = df_numeric[df_numeric['Size'] == size]
                if not size_data.empty:
                    fastest = size_data.loc[size_data['Time(ms)'].idxmin()]
                    f.write(f"规模 {size}: 最快算法 = {fastest['Algorithm']} ({fastest['PivotStrategy']}), "
                           f"时间 = {fastest['Time(ms)']:.2f} ms\n")
            f.write("\n")
        
        # 结论和建议
        f.write("4. 结论和建议\n")
        f.write("-" * 50 + "\n")
        
        if not algo_performance.empty:
            best_algo = algo_performance.index[0]
            best_time = algo_performance.iloc[0]
            f.write(f"✓ 最佳性能算法: {best_algo} (平均 {best_time:.2f} ms)\n")
        
        if not pivot_performance.empty:
            best_pivot = pivot_performance.index[0]
            f.write(f"✓ 最佳Pivot策略: {best_pivot}\n")
        
        f.write("\n✓ 实践建议:\n")
        f.write("  - 对于通用场景: 使用快速排序 + Median-of-Three pivot策略\n")
        f.write("  - 对于大规模数据: 考虑并行归并排序\n")
        f.write("  - 避免使用First/Last pivot策略，容易产生最坏情况\n")
        f.write("  - 内存敏感场景使用迭代快速排序避免栈溢出\n\n")
        
        f.write("5. 生成的可视化文件\n")
        f.write("-" * 50 + "\n")
        f.write("散点图:\n")
        f.write("  - all_algorithms_scatter.png: 所有算法性能散点图\n")
        f.write("  - quick_sort_pivot_scatter.png: 快速排序不同pivot策略散点图\n")
        f.write("  - recursive_vs_iterative_scatter.png: 递归vs迭代快速排序对比\n")
        f.write("  - performance_density_scatter.png: 性能密度散点图\n\n")
        
        f.write("折线图和柱状图:\n")
        f.write("  - pivot_strategy_comparison_recursive.png: 递归快速排序pivot策略比较\n")
        f.write("  - pivot_strategy_comparison_iterative.png: 迭代快速排序pivot策略比较\n")
        f.write("  - algorithm_comparison_best_pivot.png: 最佳算法比较\n")
        f.write("  - pivot_strategy_ranking.png: pivot策略性能排名\n")
    
    print(f"✓ 生成完整分析报告: {report_path}")

def main():
    """主函数"""
    print("=" * 70)
    print("    排序算法性能数据分析工具 (Pivot策略分析 + 散点图)")
    print("=" * 70)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 设置绘图样式
    setup_plot_style()
    
    # 查找性能日志文件
    log_file = find_performance_log()
    if not log_file:
        return
    
    # 解析数据
    df = parse_performance_log(log_file)
    if df.empty:
        return
    
    # 创建所有图表
    create_scatter_plots(df)           # 散点图
    create_pivot_analysis_charts(df)   # 折线图和柱状图
    
    # 生成分析报告
    generate_analysis_report(df)
    
    print("\n" + "=" * 70)
    print("数据分析完成!")
    print(f"所有图表和报告已保存到: {os.path.abspath('../results')}")
    print("=" * 70)

if __name__ == "__main__":
    main()
