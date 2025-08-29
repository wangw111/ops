#!/usr/bin/env python3
"""
系统状态检查脚本
"""

import os
import sys
import importlib.util
from pathlib import Path

def check_file_exists(filepath, description):
    """检查文件是否存在"""
    exists = Path(filepath).exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filepath}")
    return exists

def check_module_exists(module_name, description):
    """检查模块是否可以导入"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {description}: {module_name}")
        return True
    except ImportError:
        print(f"❌ {description}: {module_name} (未安装)")
        return False

def check_environment_var(var_name, description):
    """检查环境变量"""
    value = os.getenv(var_name, "")
    if value and value != f"your_{var_name.lower()}":
        print(f"✅ {description}: {var_name}")
        return True
    else:
        print(f"❌ {description}: {var_name} (未配置)")
        return False

def check_system_structure():
    """检查系统文件结构"""
    print("\n=== 系统文件结构检查 ===")
    
    structure_checks = [
        ("app.py", "主应用文件"),
        ("requirements.txt", "依赖配置文件"),
        (".env", "环境变量文件"),
        ("agents/__init__.py", "Agent模块初始化"),
        ("agents/base_agent.py", "基础Agent类"),
        ("agents/multi_ai_agent.py", "多AI Agent"),
        ("agents/operations_agent.py", "运维专家Agent"),
        ("agents/go_agent.py", "Go语言专家Agent"),
        ("agents/monitoring_agent.py", "监控专家Agent"),
        ("agents/ansible_agent.py", "Ansible专家Agent"),
        ("config/__init__.py", "配置模块初始化"),
        ("config/settings.py", "配置设置"),
        ("utils/__init__.py", "工具模块初始化"),
        ("utils/helpers.py", "辅助函数"),
        ("utils/code_generator.py", "代码生成器"),
        ("tests/", "测试目录"),
        ("tests/test_agents.py", "Agent测试"),
        ("tests/test_demos.py", "演示测试"),
        ("tests/test_api_integration.py", "API集成测试"),
        ("tests/test_code_generation.py", "代码生成测试"),
        ("tests/test_error_handling.py", "错误处理测试"),
        ("tests/simple_tests.py", "简化测试"),
        ("run_tests.py", "测试运行器"),
    ]
    
    passed = 0
    total = len(structure_checks)
    
    for filepath, description in structure_checks:
        if check_file_exists(filepath, description):
            passed += 1
    
    print(f"\n文件结构检查: {passed}/{total} 通过")
    return passed == total

def check_dependencies():
    """检查依赖包"""
    print("\n=== 依赖包检查 ===")
    
    dependencies = [
        ("streamlit", "Streamlit Web框架"),
        ("openai", "OpenAI API客户端"),
        ("anthropic", "Anthropic Claude客户端"),
        ("dashscope", "阿里云Qwen客户端"),
        ("dotenv", "环境变量管理"),
        ("pydantic", "数据验证"),
        ("pydantic_settings", "配置管理"),
        ("yaml", "YAML解析"),
        ("pytest", "测试框架"),
    ]
    
    passed = 0
    total = len(dependencies)
    
    for module, description in dependencies:
        if check_module_exists(module, description):
            passed += 1
    
    print(f"\n依赖包检查: {passed}/{total} 通过")
    return passed >= total * 0.8  # 80%通过即可

def check_environment():
    """检查环境配置"""
    print("\n=== 环境配置检查 ===")
    
    env_vars = [
        ("OPENAI_API_KEY", "OpenAI API密钥"),
        ("OPENAI_BASE_URL", "OpenAI基础URL"),
        ("OPENAI_MODEL", "OpenAI模型"),
        ("CLAUDE_API_KEY", "Claude API密钥"),
        ("QWEN_API_KEY", "Qwen API密钥"),
    ]
    
    passed = 0
    total = len(env_vars)
    
    for var, description in env_vars:
        if check_environment_var(var, description):
            passed += 1
    
    print(f"\n环境配置检查: {passed}/{total} 通过")
    return passed >= 2  # 至少2个配置即可

def check_test_files():
    """检查测试文件内容"""
    print("\n=== 测试文件检查 ===")
    
    test_files = [
        "tests/test_agents.py",
        "tests/test_demos.py", 
        "tests/test_api_integration.py",
        "tests/test_code_generation.py",
        "tests/test_error_handling.py",
        "tests/simple_tests.py"
    ]
    
    passed = 0
    total = len(test_files)
    
    for test_file in test_files:
        if Path(test_file).exists():
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content) > 100:  # 文件应该有内容
                    print(f"✅ 测试文件: {test_file}")
                    passed += 1
                else:
                    print(f"❌ 测试文件内容过少: {test_file}")
        else:
            print(f"❌ 测试文件不存在: {test_file}")
    
    print(f"\n测试文件检查: {passed}/{total} 通过")
    return passed == total

def generate_system_report():
    """生成系统报告"""
    print("\n" + "=" * 60)
    print("🎯 开发助手Agent系统验证报告")
    print("=" * 60)
    
    # 运行各项检查
    structure_ok = check_system_structure()
    dependencies_ok = check_dependencies()
    environment_ok = check_environment()
    test_files_ok = check_test_files()
    
    print("\n" + "=" * 60)
    print("📊 总结报告")
    print("=" * 60)
    
    print(f"📁 文件结构: {'✅ 完整' if structure_ok else '❌ 不完整'}")
    print(f"📦 依赖包: {'✅ 基本满足' if dependencies_ok else '❌ 缺少较多'}")
    print(f"⚙️  环境配置: {'✅ 已配置' if environment_ok else '❌ 需要配置'}")
    print(f"🧪 测试文件: {'✅ 完整' if test_files_ok else '❌ 不完整'}")
    
    # 计算总体状态
    checks = [structure_ok, dependencies_ok, environment_ok, test_files_ok]
    passed_checks = sum(checks)
    total_checks = len(checks)
    
    print(f"\n🎯 总体状态: {passed_checks}/{total_checks} 项通过")
    
    if passed_checks == total_checks:
        print("🎉 系统状态良好，可以正常运行！")
        print("💡 建议安装缺失的依赖包后运行测试")
    elif passed_checks >= total_checks * 0.75:
        print("✅ 系统基本完整，需要少量配置")
        print("💡 建议安装依赖包并配置环境变量")
    else:
        print("⚠️  系统需要完善配置")
        print("💡 请检查文件结构和依赖安装")
    
    # 生成建议
    print("\n💡 下一步建议:")
    if not dependencies_ok:
        print("1. 安装依赖: pip3 install -r requirements.txt")
    if not environment_ok:
        print("2. 配置环境变量，参考.env.example文件")
    if structure_ok and dependencies_ok:
        print("3. 运行测试: python3 tests/simple_tests.py")
    if structure_ok:
        print("4. 启动应用: streamlit run app.py")
    
    return passed_checks >= total_checks * 0.75

if __name__ == "__main__":
    success = generate_system_report()
    sys.exit(0 if success else 1)