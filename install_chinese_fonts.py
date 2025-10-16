#!/usr/bin/env python3
"""
中文字体安装辅助脚本
帮助解决matplotlib中文显示问题
"""

import matplotlib
import matplotlib.font_manager as fm
import os
import sys

def check_current_fonts():
    """检查当前可用的字体"""
    print("=== 检查当前字体 ===")
    
    # 获取所有字体
    fonts = [f.name for f in fm.fontManager.ttflist]
    print(f"系统中可用的字体数量: {len(fonts)}")
    
    # 查找中文字体
    chinese_keywords = ['SimHei', 'Microsoft', 'YaHei', 'Kai', 'Song', 'Hei', 'Fang', 'Li', 'YouYuan', 'SimSun']
    chinese_fonts = []
    
    for font in fonts:
        for keyword in chinese_keywords:
            if keyword.lower() in font.lower():
                chinese_fonts.append(font)
                break
    
    if chinese_fonts:
        print("✓ 发现以下中文字体:")
        for font in sorted(set(chinese_fonts))[:10]:  # 显示前10个
            print(f"  - {font}")
    else:
        print("✗ 未发现中文字体")
    
    return chinese_fonts

def test_chinese_display():
    """测试中文显示"""
    import matplotlib.pyplot as plt
    import numpy as np
    
    print("\n=== 测试中文显示 ===")
    
    # 测试数据
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    # 创建测试图表
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', linewidth=2)
    plt.title('中文标题测试 Chinese Title Test', fontsize=16)
    plt.xlabel('X轴标签 X-axis Label', fontsize=12)
    plt.ylabel('Y轴标签 Y-axis Label', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # 尝试保存
    try:
        plt.savefig('../results/chinese_font_test.png', dpi=150, bbox_inches='tight')
        print("✓ 中文测试图表已保存: results/chinese_font_test.png")
    except Exception as e:
        print(f"✗ 保存中文测试图表失败: {e}")
    
    plt.close()

def suggest_solutions():
    """提供解决方案建议"""
    print("\n=== 中文显示问题解决方案 ===")
    print("1. 安装中文字体:")
    print("   Ubuntu/Debian: sudo apt install fonts-wqy-microhei fonts-wqy-zenhei")
    print("   CentOS/RHEL: sudo yum install wqy-microhei-fonts wqy-zenhei-fonts")
    print("")
    print("2. 手动下载字体:")
    print("   下载 SimHei.ttf 或 Microsoft YaHei 字体文件")
    print("   复制到 ~/.local/share/fonts/ 或 /usr/share/fonts/")
    print("   运行: fc-cache -fv")
    print("")
    print("3. 使用英文标签 (当前方案):")
    print("   分析脚本已自动使用英文标签，避免中文显示问题")

if __name__ == "__main__":
    print("中文字体检查工具")
    print("=" * 50)
    
    # 检查字体
    chinese_fonts = check_current_fonts()
    
    # 测试显示
    test_chinese_display()
    
    # 提供解决方案
    if not chinese_fonts:
        suggest_solutions()
    else:
        print("\n✓ 系统中已安装中文字体，但matplotlib可能未正确配置")
        print("  可以尝试在代码中明确指定字体:")
        print("  plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']")
