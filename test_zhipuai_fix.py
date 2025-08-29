#!/usr/bin/env python3
"""
测试智谱AI API密钥验证修复
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_zhipuai_validation():
    """测试智谱AI验证逻辑"""
    print("🧪 测试智谱AI API密钥验证修复")
    print("=" * 50)
    
    try:
        from agents.multi_ai_agent import MultiAIAgent
        
        # 测试智谱AI配置
        print("1. 创建智谱AI Agent...")
        agent = MultiAIAgent("test", "openai")
        
        print("2. 检查配置...")
        print(f"   - Provider: {agent.provider}")
        print(f"   - Base URL: {agent.config.get('base_url', 'N/A')}")
        print(f"   - API Key: {agent.config.get('api_key', 'N/A')[:20]}...")
        
        print("3. 验证配置...")
        is_valid, message = agent.validate_provider_config()
        
        print(f"   - 验证结果: {is_valid}")
        print(f"   - 验证消息: {message}")
        
        if is_valid:
            print("✅ 智谱AI API密钥验证修复成功！")
            return True
        else:
            print("❌ 智谱AI API密钥验证仍然失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_environment_check():
    """检查环境配置"""
    print("\n🔍 检查环境配置")
    print("=" * 50)
    
    openai_key = os.getenv("OPENAI_API_KEY", "")
    base_url = os.getenv("OPENAI_BASE_URL", "")
    
    print(f"OpenAI API Key: {'已设置' if openai_key else '未设置'}")
    print(f"Base URL: {base_url}")
    print(f"是否为智谱AI: {'是' if 'bigmodel.cn' in base_url else '否'}")
    
    if 'bigmodel.cn' in base_url and openai_key:
        print("✅ 智谱AI配置正确")
        return True
    else:
        print("⚠️  配置可能有问题")
        return False

if __name__ == "__main__":
    env_ok = test_environment_check()
    test_ok = test_zhipuai_validation()
    
    print("\n" + "=" * 50)
    if env_ok and test_ok:
        print("🎉 所有测试通过！智谱AI API密钥验证已修复")
    else:
        print("⚠️  仍有问题需要解决")
    
    print("\n💡 如果问题仍然存在，请尝试重启Streamlit应用")
    print("   运行: streamlit run app.py")