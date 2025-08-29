#!/usr/bin/env python3
"""
测试运行器 - 不依赖pytest的简单测试框架
"""

import sys
import os
import traceback
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_test_method(test_class, method_name):
    """运行单个测试方法"""
    print(f"  运行 {method_name}...", end=" ")
    
    try:
        # 创建测试实例
        test_instance = test_class()
        
        # 运行setup方法
        if hasattr(test_instance, 'setup_method'):
            test_instance.setup_method()
        
        # 运行测试方法
        method = getattr(test_instance, method_name)
        method()
        
        # 运行teardown方法
        if hasattr(test_instance, 'teardown_method'):
            test_instance.teardown_method()
        
        print("✅ 通过")
        return True
        
    except Exception as e:
        print(f"❌ 失败: {str(e)}")
        traceback.print_exc()
        return False

def run_test_class(test_class, class_name):
    """运行测试类的所有方法"""
    print(f"\n=== {class_name} ===")
    
    methods = [method for method in dir(test_class) if method.startswith('test_')]
    passed = 0
    failed = 0
    
    for method in methods:
        if run_test_method(test_class, method):
            passed += 1
        else:
            failed += 1
    
    print(f"\n{class_name} 结果: {passed} 通过, {failed} 失败")
    return passed, failed

def run_all_tests():
    """运行所有测试"""
    print("🚀 开始运行测试套件")
    print("=" * 60)
    
    # 导入测试模块
    try:
        from tests.test_agents import (
            TestBaseFunctionality, TestMultiAIAgent, TestOperationsAgent,
            TestGoAgent, TestMonitoringAgent, TestAnsibleAgent,
            TestCodeGenerator, TestIntegration, TestErrorHandling
        )
    except ImportError as e:
        print(f"❌ 导入测试模块失败: {e}")
        return
    
    # 定义要运行的测试类
    test_classes = [
        (TestBaseFunctionality, "基础功能测试"),
        (TestMultiAIAgent, "MultiAI Agent测试"),
        (TestOperationsAgent, "运维专家Agent测试"),
        (TestGoAgent, "Go语言专家Agent测试"),
        (TestMonitoringAgent, "监控专家Agent测试"),
        (TestAnsibleAgent, "Ansible专家Agent测试"),
        (TestCodeGenerator, "代码生成器测试"),
        (TestIntegration, "集成测试"),
    ]
    
    total_passed = 0
    total_failed = 0
    
    # 运行所有测试类
    for test_class, class_name in test_classes:
        passed, failed = run_test_class(test_class, class_name)
        total_passed += passed
        total_failed += failed
    
    # 输出总结
    print("\n" + "=" * 60)
    print("🎉 测试运行完成！")
    print(f"总计: {total_passed} 通过, {total_failed} 失败")
    
    if total_failed == 0:
        print("✅ 所有测试通过！系统功能正常。")
    else:
        print(f"⚠️  有 {total_failed} 个测试失败，请检查相关功能。")
    
    return total_failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)