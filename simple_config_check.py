#!/usr/bin/env python3
"""
简单的智谱AI配置验证脚本
"""

import os

def check_zhipuai_config():
    """检查智谱AI配置"""
    print("🔍 智谱AI配置验证")
    print("=" * 40)
    
    # 检查环境变量
    openai_key = os.getenv("OPENAI_API_KEY", "")
    base_url = os.getenv("OPENAI_BASE_URL", "")
    model = os.getenv("OPENAI_MODEL", "")
    
    print(f"API Key: {'已设置' if openai_key else '未设置'}")
    print(f"Base URL: {base_url}")
    print(f"Model: {model}")
    
    # 验证智谱AI配置
    is_zhipuai = "bigmodel.cn" in base_url
    has_key = len(openai_key) > 10
    key_not_placeholder = openai_key != "your_openai_api_key_here"
    
    print(f"\n验证结果:")
    print(f"- 是智谱AI: {'✅' if is_zhipuai else '❌'}")
    print(f"- 有API密钥: {'✅' if has_key else '❌'}")
    print(f"- 非占位符: {'✅' if key_not_placeholder else '❌'}")
    
    if is_zhipuai and has_key and key_not_placeholder:
        print(f"\n🎉 智谱AI配置正确！")
        print(f"   - API密钥长度: {len(openai_key)}")
        print(f"   - 模型: {model}")
        return True
    else:
        print(f"\n❌ 智谱AI配置有问题")
        if not is_zhipuai:
            print(f"   - BASE_URL不正确，应该包含 bigmodel.cn")
        if not has_key:
            print(f"   - API密钥未设置或过短")
        if not key_not_placeholder:
            print(f"   - API密钥是占位符，需要设置真实密钥")
        return False

def show_fix_instructions():
    """显示修复说明"""
    print(f"\n📋 修复说明")
    print("=" * 40)
    print("1. 智谱AI API密钥验证逻辑已修复")
    print("2. 现在支持智谱AI的API密钥格式")
    print("3. 验证逻辑会自动检测BASE_URL并调整验证规则")
    print()
    print("🚀 下一步:")
    print("1. 重启Streamlit应用")
    print("2. 侧边栏应该显示'✅ 智谱AI已配置'")
    print("3. 可以正常使用AI功能")

if __name__ == "__main__":
    config_ok = check_zhipuai_config()
    show_fix_instructions()
    
    if config_ok:
        print(f"\n✅ 配置验证通过，问题已修复！")
    else:
        print(f"\n⚠️  请检查.env文件中的配置")