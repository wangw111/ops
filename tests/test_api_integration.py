"""
API集成测试案例
"""

import pytest
import os
import sys
import json
import time
from unittest.mock import Mock, patch, MagicMock
import requests

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.multi_ai_agent import MultiAIAgent
from agents.operations_agent import OperationsAgent
from agents.go_agent import GoAgent
from agents.monitoring_agent import MonitoringAgent
from agents.ansible_agent import AnsibleAgent


class TestAPIIntegration:
    """API集成测试类"""
    
    def setup_method(self):
        """测试前设置"""
        # 设置测试环境变量
        os.environ['OPENAI_API_KEY'] = 'test-key-for-testing'
        os.environ['OPENAI_BASE_URL'] = 'https://api.openai.com/v1'
        os.environ['OPENAI_MODEL'] = 'gpt-3.5-turbo'
        os.environ['OPENAI_TEMPERATURE'] = '0.7'
        os.environ['OPENAI_MAX_TOKENS'] = '1000'
        
    def test_openai_api_integration(self):
        """测试OpenAI API集成"""
        print("\n=== OpenAI API集成测试 ===")
        
        # 模拟OpenAI响应
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="测试响应内容"))]
        
        with patch('agents.multi_ai_agent.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client
            
            # 创建Agent并测试
            agent = MultiAIAgent("test", "openai")
            
            # 测试API调用
            response = agent.process_request("测试输入")
            assert response == "测试响应内容"
            
            # 验证API调用参数
            mock_client.chat.completions.create.assert_called_once()
            call_args = mock_client.chat.completions.create.call_args
            
            assert call_args.kwargs['model'] == 'gpt-3.5-turbo'
            assert call_args.kwargs['temperature'] == 0.7
            assert call_args.kwargs['max_tokens'] == 1000
            assert len(call_args.kwargs['messages']) > 0
            
            print("✅ OpenAI API集成测试通过")
            
    def test_claude_api_integration(self):
        """测试Claude API集成"""
        print("\n=== Claude API集成测试 ===")
        
        # 设置Claude环境变量
        os.environ['ANTHROPIC_AUTH_TOKEN'] = 'test-claude-key'
        os.environ['CLAUDE_MODEL'] = 'claude-3-sonnet-20240229'
        
        # 模拟Claude响应
        mock_response = Mock()
        mock_response.content = [Mock(text="Claude测试响应")]
        
        with patch('agents.multi_ai_agent.anthropic') as mock_anthropic:
            mock_client = Mock()
            mock_client.messages.create.return_value = mock_response
            mock_anthropic.Anthropic.return_value = mock_client
            
            # 创建Agent并测试
            agent = MultiAIAgent("test", "claude")
            
            # 测试API调用
            response = agent.process_request("测试输入")
            assert response == "Claude测试响应"
            
            # 验证API调用参数
            mock_client.messages.create.assert_called_once()
            call_args = mock_client.messages.create.call_args
            
            assert call_args.kwargs['model'] == 'claude-3-sonnet-20240229'
            assert call_args.kwargs['max_tokens'] == 1000
            assert call_args.kwargs['temperature'] == 0.7
            
            print("✅ Claude API集成测试通过")
            
    def test_qwen_api_integration(self):
        """测试Qwen API集成"""
        print("\n=== Qwen API集成测试 ===")
        
        # 设置Qwen环境变量
        os.environ['QWEN_API_KEY'] = 'test-qwen-key'
        os.environ['QWEN_MODEL'] = 'qwen-turbo'
        
        # 模拟Qwen响应
        mock_response = {
            'output': {
                'text': 'Qwen测试响应'
            }
        }
        
        with patch('agents.multi_ai_agent.Generation') as mock_generation:
            mock_generation.call.return_value = mock_response
            
            # 创建Agent并测试
            agent = MultiAIAgent("test", "qwen")
            
            # 测试API调用
            response = agent.process_request("测试输入")
            assert response == "Qwen测试响应"
            
            # 验证API调用参数
            mock_generation.call.assert_called_once()
            
            print("✅ Qwen API集成测试通过")
            
    def test_zhipu_ai_integration(self):
        """测试智谱AI集成"""
        print("\n=== 智谱AI集成测试 ===")
        
        # 设置智谱AI环境变量
        os.environ['OPENAI_API_KEY'] = '66fa8bd3f4984c5d969e444cd0d5805d.FuGSLsJ40iE8f3zn'
        os.environ['OPENAI_BASE_URL'] = 'https://open.bigmodel.cn/api/paas/v4'
        os.environ['OPENAI_MODEL'] = 'glm-4.5'
        
        # 模拟智谱AI响应
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="智谱AI测试响应"))]
        
        with patch('agents.multi_ai_agent.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client
            
            # 创建Agent并测试
            agent = MultiAIAgent("test", "openai")
            
            # 验证智谱AI配置被正确识别
            assert "bigmodel.cn" in agent.config["base_url"]
            
            # 测试API调用
            response = agent.process_request("测试输入")
            assert response == "智谱AI测试响应"
            
            # 验证API调用参数
            mock_client.chat.completions.create.assert_called_once()
            call_args = mock_client.chat.completions.create.call_args
            
            assert call_args.kwargs['model'] == 'glm-4.5'
            assert call_args.kwargs['base_url'] == 'https://open.bigmodel.cn/api/paas/v4'
            
            print("✅ 智谱AI集成测试通过")
            
    def test_api_error_handling(self):
        """测试API错误处理"""
        print("\n=== API错误处理测试 ===")
        
        # 测试网络错误
        with patch('agents.multi_ai_agent.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_client.chat.completions.create.side_effect = Exception("网络错误")
            mock_openai.return_value = mock_client
            
            agent = MultiAIAgent("test", "openai")
            
            # 测试错误处理
            response = agent.process_request("测试输入")
            assert "抱歉" in response or "错误" in response
            
            print("✅ API错误处理测试通过")
            
    def test_api_timeout_handling(self):
        """测试API超时处理"""
        print("\n=== API超时处理测试 ===")
        
        # 模拟超时错误
        with patch('agents.multi_ai_agent.OpenAI') as mock_openai:
            import requests
            mock_client = Mock()
            mock_client.chat.completions.create.side_effect = requests.Timeout("请求超时")
            mock_openai.return_value = mock_client
            
            agent = MultiAIAgent("test", "openai")
            
            # 测试超时处理
            response = agent.process_request("测试输入")
            assert "抱歉" in response or "超时" in response
            
            print("✅ API超时处理测试通过")
            
    def test_api_rate_limit_handling(self):
        """测试API速率限制处理"""
        print("\n=== API速率限制处理测试 ===")
        
        # 模拟速率限制错误
        with patch('agents.multi_ai_agent.OpenAI') as mock_openai:
            mock_client = Mock()
            
            # 模拟速率限制异常
            rate_limit_error = Exception("Rate limit exceeded")
            rate_limit_error.status_code = 429
            mock_client.chat.completions.create.side_effect = rate_limit_error
            
            mock_openai.return_value = mock_client
            
            agent = MultiAIAgent("test", "openai")
            
            # 测试速率限制处理
            response = agent.process_request("测试输入")
            assert "抱歉" in response or "限制" in response
            
            print("✅ API速率限制处理测试通过")
            
    def test_provider_switching(self):
        """测试AI提供商切换"""
        print("\n=== AI提供商切换测试 ===")
        
        # 模拟不同提供商的响应
        mock_openai_response = Mock()
        mock_openai_response.choices = [Mock(message=Mock(content="OpenAI响应"))]
        
        mock_claude_response = Mock()
        mock_claude_response.content = [Mock(text="Claude响应")]
        
        with patch('agents.multi_ai_agent.OpenAI') as mock_openai, \
             patch('agents.multi_ai_agent.anthropic') as mock_anthropic:
            
            # 设置模拟
            mock_openai_client = Mock()
            mock_openai_client.chat.completions.create.return_value = mock_openai_response
            mock_openai.return_value = mock_openai_client
            
            mock_anthropic_client = Mock()
            mock_anthropic_client.messages.create.return_value = mock_claude_response
            mock_anthropic.Anthropic.return_value = mock_anthropic_client
            
            # 创建Agent并测试切换
            agent = MultiAIAgent("test", "openai")
            response1 = agent.process_request("测试输入")
            assert response1 == "OpenAI响应"
            
            # 切换到Claude
            agent.switch_provider("claude")
            response2 = agent.process_request("测试输入")
            assert response2 == "Claude响应"
            
            print("✅ AI提供商切换测试通过")
            
    def test_concurrent_api_calls(self):
        """测试并发API调用"""
        print("\n=== 并发API调用测试 ===")
        
        import threading
        import concurrent.futures
        
        # 模拟响应
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content=f"并发响应{threading.current_thread().ident}"))]
        
        with patch('agents.multi_ai_agent.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client
            
            agent = MultiAIAgent("test", "openai")
            
            # 并发调用测试
            def api_call(thread_id):
                response = agent.process_request(f"并发测试{thread_id}")
                return response
                
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                futures = [executor.submit(api_call, i) for i in range(3)]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]
                
            # 验证所有调用都成功
            assert len(results) == 3
            for result in results:
                assert "并发响应" in result
                
            print("✅ 并发API调用测试通过")
            
    def test_api_response_validation(self):
        """测试API响应验证"""
        print("\n=== API响应验证测试 ===")
        
        # 测试正常响应
        mock_normal_response = Mock()
        mock_normal_response.choices = [Mock(message=Mock(content="正常响应"))]
        
        with patch('agents.multi_ai_agent.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_client.chat.completions.create.return_value = mock_normal_response
            mock_openai.return_value = mock_client
            
            agent = MultiAIAgent("test", "openai")
            response = agent.process_request("测试输入")
            assert response == "正常响应"
            
            # 测试空响应
            mock_empty_response = Mock()
            mock_empty_response.choices = [Mock(message=Mock(content=""))]
            mock_client.chat.completions.create.return_value = mock_empty_response
            
            response = agent.process_request("测试输入")
            assert response == ""  # 空响应应该被保留
            
            # 测试None响应
            mock_none_response = Mock()
            mock_none_response.choices = [Mock(message=Mock(content=None))]
            mock_client.chat.completions.create.return_value = mock_none_response
            
            response = agent.process_request("测试输入")
            assert response == ""  # None响应应该转换为空字符串
            
            print("✅ API响应验证测试通过")
            
    def test_api_request_formatting(self):
        """测试API请求格式化"""
        print("\n=== API请求格式化测试 ===")
        
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="格式化测试"))]
        
        with patch('agents.multi_ai_agent.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client
            
            agent = MultiAIAgent("test", "openai")
            
            # 添加一些对话历史
            agent.add_to_history("user", "历史问题1")
            agent.add_to_history("assistant", "历史回答1")
            agent.add_to_history("user", "当前问题")
            
            # 发送请求
            agent.process_request("当前问题")
            
            # 验证请求格式
            call_args = mock_client.chat.completions.create.call_args
            messages = call_args.kwargs['messages']
            
            # 应该包含系统提示词和对话历史
            assert len(messages) >= 3
            assert messages[0]['role'] == 'system'
            assert messages[-1]['role'] == 'user'
            assert messages[-1]['content'] == '当前问题'
            
            print("✅ API请求格式化测试通过")


class TestRealAPITest:
    """真实API测试类（仅在需要时运行）"""
    
    @pytest.mark.skipif(
        not os.getenv('RUN_REAL_API_TESTS'),
        reason="需要设置RUN_REAL_API_TESTS环境变量来运行真实API测试"
    )
    def test_real_openai_api(self):
        """测试真实OpenAI API"""
        print("\n=== 真实OpenAI API测试 ===")
        
        if not os.getenv('OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY') == 'your_openai_api_key_here':
            pytest.skip("需要有效的OpenAI API密钥")
            
        agent = MultiAIAgent("test", "openai")
        
        if agent.client is None:
            pytest.skip("OpenAI客户端初始化失败")
            
        response = agent.process_request("请简单介绍一下Python")
        assert len(response) > 0
        assert "Python" in response
        
        print("✅ 真实OpenAI API测试通过")
        
    @pytest.mark.skipif(
        not os.getenv('RUN_REAL_API_TESTS'),
        reason="需要设置RUN_REAL_API_TESTS环境变量来运行真实API测试"
    )
    def test_real_claude_api(self):
        """测试真实Claude API"""
        print("\n=== 真实Claude API测试 ===")
        
        if not os.getenv('ANTHROPIC_AUTH_TOKEN') or os.getenv('ANTHROPIC_AUTH_TOKEN') == 'your_claude_api_key_here':
            pytest.skip("需要有效的Claude API密钥")
            
        agent = MultiAIAgent("test", "claude")
        
        if agent.client is None:
            pytest.skip("Claude客户端初始化失败")
            
        response = agent.process_request("请简单介绍一下Go语言")
        assert len(response) > 0
        assert "Go" in response
        
        print("✅ 真实Claude API测试通过")
        
    @pytest.mark.skipif(
        not os.getenv('RUN_REAL_API_TESTS'),
        reason="需要设置RUN_REAL_API_TESTS环境变量来运行真实API测试"
    )
    def test_real_zhipu_api(self):
        """测试真实智谱AI API"""
        print("\n=== 真实智谱AI API测试 ===")
        
        if not os.getenv('OPENAI_API_KEY') or "bigmodel" not in os.getenv('OPENAI_BASE_URL', ''):
            pytest.skip("需要有效的智谱AI配置")
            
        agent = MultiAIAgent("test", "openai")
        
        if agent.client is None:
            pytest.skip("智谱AI客户端初始化失败")
            
        response = agent.process_request("请简单介绍一下机器学习")
        assert len(response) > 0
        assert "机器学习" in response or "机器" in response
        
        print("✅ 真实智谱AI API测试通过")


class TestAPIPerformance:
    """API性能测试类"""
    
    def test_api_response_time(self):
        """测试API响应时间"""
        print("\n=== API响应时间测试 ===")
        
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="性能测试响应"))]
        
        with patch('agents.multi_ai_agent.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client
            
            agent = MultiAIAgent("test", "openai")
            
            # 测试响应时间
            start_time = time.time()
            response = agent.process_request("性能测试")
            end_time = time.time()
            
            response_time = end_time - start_time
            print(f"   - 响应时间: {response_time:.3f}秒")
            
            # 响应时间应该在合理范围内（模拟情况下应该很快）
            assert response_time < 1.0  # 模拟响应应该小于1秒
            assert response == "性能测试响应"
            
            print("✅ API响应时间测试通过")
            
    def test_multiple_requests_performance(self):
        """测试多次请求性能"""
        print("\n=== 多次请求性能测试 ===")
        
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="多次请求测试"))]
        
        with patch('agents.multi_ai_agent.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client
            
            agent = MultiAIAgent("test", "openai")
            
            # 发送多个请求
            num_requests = 10
            start_time = time.time()
            
            for i in range(num_requests):
                response = agent.process_request(f"请求{i}")
                assert response == "多次请求测试"
                
            end_time = time.time()
            total_time = end_time - start_time
            avg_time = total_time / num_requests
            
            print(f"   - 总时间: {total_time:.3f}秒")
            print(f"   - 平均时间: {avg_time:.3f}秒")
            print(f"   - 请求数量: {num_requests}")
            
            # 平均响应时间应该合理
            assert avg_time < 0.5  # 模拟情况下应该很快
            
            print("✅ 多次请求性能测试通过")


def run_api_integration_tests():
    """运行API集成测试"""
    print("🚀 开始API集成测试")
    print("=" * 60)
    
    # 创建测试实例
    api_test = TestAPIIntegration()
    performance_test = TestAPIPerformance()
    
    # 设置测试环境
    api_test.setup_method()
    
    try:
        # 运行API集成测试
        api_test.test_openai_api_integration()
        api_test.test_claude_api_integration()
        api_test.test_qwen_api_integration()
        api_test.test_zhipu_ai_integration()
        api_test.test_api_error_handling()
        api_test.test_api_timeout_handling()
        api_test.test_api_rate_limit_handling()
        api_test.test_provider_switching()
        api_test.test_concurrent_api_calls()
        api_test.test_api_response_validation()
        api_test.test_api_request_formatting()
        
        # 运行性能测试
        performance_test.test_api_response_time()
        performance_test.test_multiple_requests_performance()
        
        print("\n" + "=" * 60)
        print("🎉 API集成测试完成！")
        print("✅ 所有API集成功能正常工作")
        
    finally:
        # 清理测试环境
        pass


if __name__ == "__main__":
    run_api_integration_tests()