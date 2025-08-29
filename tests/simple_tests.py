#!/usr/bin/env python3
"""
简化的测试案例 - 不依赖pytest
"""

import os
import sys
import tempfile
import shutil
from unittest.mock import Mock, patch

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.operations_agent import OperationsAgent
from agents.go_agent import GoAgent
from agents.monitoring_agent import MonitoringAgent
from agents.ansible_agent import AnsibleAgent
from agents.multi_ai_agent import MultiAIAgent
from utils.code_generator import CodeGenerator
from utils.helpers import setup_logging, validate_agent_input, sanitize_response
from config.settings import get_config

class TestRunner:
    """测试运行器"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.temp_dir = None
    
    def setup(self):
        """测试前设置"""
        self.temp_dir = tempfile.mkdtemp()
        self.logger = setup_logging()
    
    def teardown(self):
        """测试后清理"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def assert_true(self, condition, message=""):
        """断言条件为真"""
        if not condition:
            raise AssertionError(f"断言失败: {message}")
    
    def assert_equal(self, actual, expected, message=""):
        """断言相等"""
        if actual != expected:
            raise AssertionError(f"断言失败: {message} - 期望: {expected}, 实际: {actual}")
    
    def assert_in(self, item, container, message=""):
        """断言包含"""
        if item not in container:
            raise AssertionError(f"断言失败: {message} - '{item}' 不在 '{container}' 中")
    
    def run_test(self, test_func, test_name):
        """运行单个测试"""
        print(f"  运行 {test_name}...", end=" ")
        
        try:
            test_func()
            print("✅ 通过")
            self.passed += 1
            return True
        except Exception as e:
            print(f"❌ 失败: {str(e)}")
            self.failed += 1
            return False
    
    def test_basic_functionality(self):
        """测试基础功能"""
        print("\n=== 基础功能测试 ===")
        
        # 测试日志设置
        def test_logging():
            logger = setup_logging("DEBUG")
            self.assert_true(logger is not None, "日志器不应为None")
            self.assert_equal(logger.level, 10, "日志级别应为DEBUG")
        
        self.run_test(test_logging, "日志设置")
        
        # 测试输入验证
        def test_input_validation():
            valid_input = "请帮我创建一个Docker容器"
            self.assert_true(validate_agent_input(valid_input), "有效输入应通过验证")
            
            empty_input = ""
            self.assert_true(not validate_agent_input(empty_input), "空输入应被拒绝")
            
            long_input = "x" * 3000
            self.assert_true(not validate_agent_input(long_input), "过长输入应被拒绝")
        
        self.run_test(test_input_validation, "输入验证")
        
        # 测试响应清理
        def test_response_sanitization():
            response = "这是正常的响应内容\n\n多行文本"
            sanitized = sanitize_response(response)
            self.assert_in("这是正常的响应内容", sanitized, "正常内容应保留")
            self.assert_in("多行文本", sanitized, "多行文本应保留")
            
            empty_response = ""
            sanitized = sanitize_response(empty_response)
            self.assert_in("抱歉", sanitized, "空响应应返回默认消息")
        
        self.run_test(test_response_sanitization, "响应清理")
        
        # 测试配置加载
        def test_config_loading():
            config = get_config()
            self.assert_true(config is not None, "配置不应为None")
            self.assert_true(hasattr(config, 'model_name'), "配置应包含model_name")
            self.assert_true(hasattr(config, 'temperature'), "配置应包含temperature")
        
        self.run_test(test_config_loading, "配置加载")
    
    def test_multi_ai_agent(self):
        """测试MultiAI Agent"""
        print("\n=== MultiAI Agent测试 ===")
        
        def test_agent_initialization():
            agent = MultiAIAgent("test", "openai")
            self.assert_equal(agent.agent_type, "test", "Agent类型应正确")
            self.assert_equal(agent.provider, "openai", "提供商应正确")
            self.assert_equal(agent.conversation_history, [], "对话历史应为空")
        
        self.run_test(test_agent_initialization, "Agent初始化")
        
        def test_provider_config_loading():
            agent = MultiAIAgent("test", "openai")
            config = agent.config
            self.assert_in("api_key", config, "配置应包含api_key")
            self.assert_in("base_url", config, "配置应包含base_url")
            self.assert_in("model", config, "配置应包含model")
            self.assert_in("temperature", config, "配置应包含temperature")
        
        self.run_test(test_agent_config_loading, "提供商配置加载")
        
        def test_conversation_history(self):
            agent = MultiAIAgent("test", "openai")
            
            # 添加对话历史
            agent.add_to_history("user", "测试输入")
            agent.add_to_history("assistant", "测试输出")
            
            self.assert_equal(len(agent.conversation_history), 2, "对话历史长度应为2")
            self.assert_equal(agent.conversation_history[0]["role"], "user", "第一条应为用户消息")
            self.assert_equal(agent.conversation_history[1]["role"], "assistant", "第二条应为助手消息")
        
        self.run_test(test_conversation_history, "对话历史管理")
        
        def test_clear_history(self):
            agent = MultiAIAgent("test", "openai")
            agent.add_to_history("user", "测试")
            self.assert_equal(len(agent.conversation_history), 1, "添加后应有1条历史")
            
            agent.clear_history()
            self.assert_equal(len(agent.conversation_history), 0, "清空后历史应为空")
        
        self.run_test(test_clear_history, "清空对话历史")
    
    def test_operations_agent(self):
        """测试运维专家Agent"""
        print("\n=== 运维专家Agent测试 ===")
        
        def test_agent_initialization():
            agent = OperationsAgent("openai")
            self.assert_equal(agent.agent_type, "operations", "Agent类型应为operations")
            self.assert_equal(agent.provider, "openai", "提供商应为openai")
            self.assert_true(hasattr(agent, 'code_generator'), "应有code_generator属性")
        
        self.run_test(test_agent_initialization, "运维Agent初始化")
        
        def test_system_prompt_content():
            agent = OperationsAgent("openai")
            prompt = agent.get_system_prompt()
            self.assert_in("运维专家", prompt, "系统提示词应包含'运维专家'")
            self.assert_in("Docker", prompt, "系统提示词应包含'Docker'")
            self.assert_in("Kubernetes", prompt, "系统提示词应包含'Kubernetes'")
            self.assert_in("CI/CD", prompt, "系统提示词应包含'CI/CD'")
        
        self.run_test(test_system_prompt_content, "系统提示词内容")
        
        def test_expertise_areas():
            agent = OperationsAgent("openai")
            areas = agent.get_expertise_areas()
            self.assert_true(isinstance(areas, list), "专业领域应为列表")
            self.assert_true(len(areas) > 0, "专业领域列表不应为空")
            self.assert_in("服务器部署和配置", areas, "应包含服务器部署领域")
        
        self.run_test(test_expertise_areas, "专业领域列表")
        
        def test_deployment_script_generation(self):
            agent = OperationsAgent("openai")
            
            # 测试Web服务部署脚本生成
            scripts = agent.generate_runnable_deployment_script("test-service", "web")
            self.assert_true(isinstance(scripts, dict), "脚本应为字典格式")
            self.assert_in("deploy_test-service.sh", scripts, "应包含部署脚本")
            self.assert_in("README.md", scripts, "应包含README文档")
            
            # 测试Docker部署脚本生成
            scripts = agent.generate_runnable_deployment_script("test-service", "docker")
            self.assert_true(isinstance(scripts, dict), "脚本应为字典格式")
            self.assert_in("docker-compose.yml", scripts, "应包含docker-compose.yml")
            self.assert_in("Dockerfile", scripts, "应包含Dockerfile")
        
        self.run_test(test_deployment_script_generation, "部署脚本生成")
        
        def test_shell_script_validation(self):
            agent = OperationsAgent("openai")
            
            valid_script = "#!/bin/bash\necho 'Hello World'"
            is_valid, error = agent.validate_shell_script(valid_script)
            self.assert_true(is_valid, "有效脚本应通过验证")
            self.assert_true(error is None or len(error) == 0, "有效脚本不应有错误")
        
        self.run_test(test_shell_script_validation, "Shell脚本验证")
    
    def test_go_agent(self):
        """测试Go语言专家Agent"""
        print("\n=== Go语言专家Agent测试 ===")
        
        def test_agent_initialization():
            agent = GoAgent("openai")
            self.assert_equal(agent.agent_type, "go", "Agent类型应为go")
            self.assert_equal(agent.provider, "openai", "提供商应为openai")
            self.assert_true(hasattr(agent, 'code_generator'), "应有code_generator属性")
        
        self.run_test(test_agent_initialization, "Go Agent初始化")
        
        def test_system_prompt_content():
            agent = GoAgent("openai")
            prompt = agent.get_system_prompt()
            self.assert_in("Go语言", prompt, "系统提示词应包含'Go语言'")
            self.assert_in("并发编程", prompt, "系统提示词应包含'并发编程'")
            self.assert_in("goroutine", prompt, "系统提示词应包含'goroutine'")
        
        self.run_test(test_system_prompt_content, "系统提示词内容")
        
        def test_code_template_generation():
            agent = GoAgent("openai")
            
            # 测试HTTP服务器模板
            template = agent.generate_code_template("http_server")
            self.assert_in("package main", template, "HTTP模板应包含package main")
            self.assert_in("net/http", template, "HTTP模板应包含net/http")
            self.assert_in("ListenAndServe", template, "HTTP模板应包含ListenAndServe")
            
            # 测试gRPC服务模板
            template = agent.generate_code_template("grpc_service")
            self.assert_in("package main", template, "gRPC模板应包含package main")
            self.assert_in("grpc", template, "gRPC模板应包含grpc")
            self.assert_in("RegisterYourServiceServer", template, "gRPC模板应包含RegisterYourServiceServer")
            
            # 测试并发工作池模板
            template = agent.generate_code_template("concurrent_worker")
            self.assert_in("package main", template, "并发模板应包含package main")
            self.assert_in("sync.WaitGroup", template, "并发模板应包含sync.WaitGroup")
            self.assert_in("goroutine", template, "并发模板应包含goroutine")
        
        self.run_test(test_code_template_generation, "代码模板生成")
        
        def test_go_project_generation(self):
            agent = GoAgent("openai")
            
            project = agent.generate_runnable_go_project("myapp", "web")
            self.assert_true(isinstance(project, dict), "项目应为字典格式")
            self.assert_in("myapp/main.go", project, "应包含main.go")
            self.assert_in("myapp/go.mod", project, "应包含go.mod")
            self.assert_in("myapp/handlers/", project, "应包含handlers目录")
        
        self.run_test(test_go_project_generation, "Go项目生成")
    
    def test_monitoring_agent(self):
        """测试监控专家Agent"""
        print("\n=== 监控专家Agent测试 ===")
        
        def test_agent_initialization():
            agent = MonitoringAgent("openai")
            self.assert_equal(agent.agent_type, "monitoring", "Agent类型应为monitoring")
            self.assert_equal(agent.provider, "openai", "提供商应为openai")
            self.assert_true(hasattr(agent, 'code_generator'), "应有code_generator属性")
        
        self.run_test(test_agent_initialization, "监控Agent初始化")
        
        def test_system_prompt_content():
            agent = MonitoringAgent("openai")
            prompt = agent.get_system_prompt()
            self.assert_in("监控专家", prompt, "系统提示词应包含'监控专家'")
            self.assert_in("Prometheus", prompt, "系统提示词应包含'Prometheus'")
            self.assert_in("Grafana", prompt, "系统提示词应包含'Grafana'")
        
        self.run_test(test_system_prompt_content, "系统提示词内容")
        
        def test_prometheus_config_generation(self):
            agent = MonitoringAgent("openai")
            
            config = agent.generate_prometheus_config("myapp")
            self.assert_true(isinstance(config, dict), "配置应为字典格式")
            self.assert_in("prometheus.yml", config, "应包含prometheus.yml")
            self.assert_in("alert_rules.yml", config, "应包含alert_rules.yml")
        
        self.run_test(test_prometheus_config_generation, "Prometheus配置生成")
        
        def test_grafana_dashboard_generation(self):
            agent = MonitoringAgent("openai")
            
            dashboard = agent.generate_grafana_dashboard("myapp", "web")
            self.assert_true(isinstance(dashboard, dict), "仪表板应为字典格式")
            self.assert_in("dashboard.json", dashboard, "应包含dashboard.json")
            self.assert_in("datasource.yml", dashboard, "应包含datasource.yml")
        
        self.run_test(test_grafana_dashboard_generation, "Grafana仪表板生成")
    
    def test_ansible_agent(self):
        """测试Ansible专家Agent"""
        print("\n=== Ansible专家Agent测试 ===")
        
        def test_agent_initialization():
            agent = AnsibleAgent("openai")
            self.assert_equal(agent.agent_type, "ansible", "Agent类型应为ansible")
            self.assert_equal(agent.provider, "openai", "提供商应为openai")
            self.assert_true(hasattr(agent, 'code_generator'), "应有code_generator属性")
        
        self.run_test(test_agent_initialization, "Ansible Agent初始化")
        
        def test_system_prompt_content():
            agent = AnsibleAgent("openai")
            prompt = agent.get_system_prompt()
            self.assert_in("Ansible", prompt, "系统提示词应包含'Ansible'")
            self.assert_in("自动化", prompt, "系统提示词应包含'自动化'")
            self.assert_in("Playbook", prompt, "系统提示词应包含'Playbook'")
        
        self.run_test(test_system_prompt_content, "系统提示词内容")
        
        def test_playbook_generation(self):
            agent = AnsibleAgent("openai")
            
            playbook = agent.generate_playbook("web-deploy", "nginx")
            self.assert_true(isinstance(playbook, dict), "Playbook应为字典格式")
            self.assert_in("site.yml", playbook, "应包含site.yml")
            self.assert_in("roles/", playbook, "应包含roles目录")
        
        self.run_test(test_playbook_generation, "Playbook生成")
        
        def test_role_structure_generation(self):
            agent = AnsibleAgent("openai")
            
            role = agent.generate_role_structure("webserver")
            self.assert_true(isinstance(role, dict), "Role应为字典格式")
            self.assert_in("tasks/main.yml", role, "应包含tasks/main.yml")
            self.assert_in("handlers/main.yml", role, "应包含handlers/main.yml")
            self.assert_in("templates/", role, "应包含templates目录")
            self.assert_in("vars/", role, "应包含vars目录")
        
        self.run_test(test_role_structure_generation, "Role结构生成")
    
    def test_code_generator(self):
        """测试代码生成器"""
        print("\n=== 代码生成器测试 ===")
        
        def test_code_generator_initialization():
            generator = CodeGenerator()
            self.assert_true(generator is not None, "生成器不应为None")
            self.assert_true(hasattr(generator, 'logger'), "应有logger属性")
        
        self.run_test(test_code_generator_initialization, "代码生成器初始化")
        
        def test_executable_script_generation(self):
            generator = CodeGenerator()
            
            script_content = "#!/bin/bash\necho 'Hello World'"
            script = generator.generate_executable_script(script_content, "shell", "test.sh")
            self.assert_in("#!/bin/bash", script, "脚本应包含shebang")
            self.assert_in("Hello World", script, "脚本应包含原始内容")
        
        self.run_test(test_executable_script_generation, "可执行脚本生成")
        
        def test_markdown_documentation_generation(self):
            generator = CodeGenerator()
            
            code_examples = [
                {
                    "title": "测试代码",
                    "description": "这是一个测试",
                    "language": "python",
                    "code": "print('Hello')"
                }
            ]
            
            doc = generator.generate_markdown_documentation(
                "测试文档", "这是描述", code_examples
            )
            self.assert_in("# 测试文档", doc, "文档应包含标题")
            self.assert_in("```python", doc, "文档应包含代码块")
            self.assert_in("print('Hello')", doc, "文档应包含代码")
        
        self.run_test(test_markdown_documentation_generation, "Markdown文档生成")
        
        def test_code_validation(self):
            generator = CodeGenerator()
            
            # 测试Python代码验证
            valid_python = "print('Hello World')"
            is_valid, error = generator.validate_code(valid_python, "python")
            self.assert_true(is_valid, "有效Python代码应通过验证")
            
            # 测试无效Python代码
            invalid_python = "print('Hello World'"
            is_valid, error = generator.validate_code(invalid_python, "python")
            self.assert_true(not is_valid, "无效Python代码应被拒绝")
            
            # 测试Go代码验证
            valid_go = "package main\n\nfunc main() {}"
            is_valid, error = generator.validate_code(valid_go, "go")
            self.assert_true(is_valid, "有效Go代码应通过验证")
        
        self.run_test(test_code_validation, "代码验证")
    
    def test_integration(self):
        """测试集成功能"""
        print("\n=== 集成测试 ===")
        
        def test_all_agents_initialization():
            operations_agent = OperationsAgent("openai")
            go_agent = GoAgent("openai")
            monitoring_agent = MonitoringAgent("openai")
            ansible_agent = AnsibleAgent("openai")
            
            self.assert_equal(operations_agent.agent_type, "operations", "运维Agent类型正确")
            self.assert_equal(go_agent.agent_type, "go", "Go Agent类型正确")
            self.assert_equal(monitoring_agent.agent_type, "monitoring", "监控Agent类型正确")
            self.assert_equal(ansible_agent.agent_type, "ansible", "Ansible Agent类型正确")
        
        self.run_test(test_all_agents_initialization, "所有Agent初始化")
        
        def test_cross_agent_functionality(self):
            operations_agent = OperationsAgent("openai")
            go_agent = GoAgent("openai")
            monitoring_agent = MonitoringAgent("openai")
            ansible_agent = AnsibleAgent("openai")
            
            # 运维Agent生成部署脚本
            deploy_scripts = operations_agent.generate_runnable_deployment_script("test-app", "web")
            
            # Go Agent生成Go代码
            go_code = go_agent.generate_code_template("http_server")
            
            # 监控Agent生成监控配置
            monitoring_config = monitoring_agent.generate_prometheus_config("test-app")
            
            # Ansible Agent生成自动化配置
            ansible_config = ansible_agent.generate_playbook("deploy", "web")
            
            # 验证所有输出格式正确
            self.assert_true(isinstance(deploy_scripts, dict), "部署脚本应为字典")
            self.assert_true(isinstance(go_code, str), "Go代码应为字符串")
            self.assert_true(isinstance(monitoring_config, dict), "监控配置应为字典")
            self.assert_true(isinstance(ansible_config, dict), "Ansible配置应为字典")
        
        self.run_test(test_cross_agent_functionality, "跨Agent功能协作")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始运行简化测试套件")
        print("=" * 60)
        
        try:
            self.setup()
            
            # 运行所有测试
            self.test_basic_functionality()
            self.test_multi_ai_agent()
            self.test_operations_agent()
            self.test_go_agent()
            self.test_monitoring_agent()
            self.test_ansible_agent()
            self.test_code_generator()
            self.test_integration()
            
            # 输出总结
            print("\n" + "=" * 60)
            print("🎉 测试运行完成！")
            print(f"总计: {self.passed} 通过, {self.failed} 失败")
            
            if self.failed == 0:
                print("✅ 所有测试通过！系统功能正常。")
            else:
                print(f"⚠️  有 {self.failed} 个测试失败，请检查相关功能。")
            
            return self.failed == 0
            
        finally:
            self.teardown()

if __name__ == "__main__":
    runner = TestRunner()
    success = runner.run_all_tests()
    sys.exit(0 if success else 1)