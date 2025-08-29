"""
开发助手Agent系统测试案例
"""

import pytest
import os
import sys
import tempfile
import shutil
from unittest.mock import Mock, patch

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.operations_agent import OperationsAgent
from agents.go_agent import GoAgent
from agents.monitoring_agent import MonitoringAgent
from agents.ansible_agent import AnsibleAgent
from agents.multi_ai_agent import MultiAIAgent
from utils.code_generator import CodeGenerator
from utils.helpers import setup_logging, validate_agent_input, sanitize_response
from config.settings import get_config


class TestBaseFunctionality:
    """基础功能测试类"""
    
    def setup_method(self):
        """测试前设置"""
        self.temp_dir = tempfile.mkdtemp()
        self.logger = setup_logging()
        
    def teardown_method(self):
        """测试后清理"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_setup_logging(self):
        """测试日志设置功能"""
        logger = setup_logging("DEBUG")
        assert logger is not None
        assert logger.level == 10  # DEBUG level
        
    def test_validate_agent_input_valid(self):
        """测试有效的用户输入验证"""
        valid_input = "请帮我创建一个Docker容器"
        assert validate_agent_input(valid_input) == True
        
    def test_validate_agent_input_empty(self):
        """测试空输入验证"""
        empty_input = ""
        assert validate_agent_input(empty_input) == False
        
    def test_validate_agent_input_too_long(self):
        """测试过长输入验证"""
        long_input = "x" * 3000
        assert validate_agent_input(long_input) == False
        
    def test_sanitize_response_normal(self):
        """测试正常响应清理"""
        response = "这是正常的响应内容\n\n多行文本"
        sanitized = sanitize_response(response)
        assert "这是正常的响应内容" in sanitized
        assert "多行文本" in sanitized
        
    def test_sanitize_response_empty(self):
        """测试空响应清理"""
        empty_response = ""
        sanitized = sanitize_response(empty_response)
        assert "抱歉，无法生成响应" in sanitized
        
    def test_config_loading(self):
        """测试配置加载"""
        config = get_config()
        assert config is not None
        assert hasattr(config, 'model_name')
        assert hasattr(config, 'temperature')


class TestMultiAIAgent:
    """MultiAI Agent测试类"""
    
    def setup_method(self):
        """测试前设置"""
        self.agent = MultiAIAgent("test", "openai")
        
    def test_agent_initialization(self):
        """测试Agent初始化"""
        assert self.agent.agent_type == "test"
        assert self.agent.provider == "openai"
        assert self.agent.conversation_history == []
        
    def test_provider_config_loading(self):
        """测试AI提供商配置加载"""
        config = self.agent.config
        assert "api_key" in config
        assert "base_url" in config
        assert "model" in config
        assert "temperature" in config
        
    @patch('agents.multi_ai_agent.OpenAI')
    def test_openai_client_initialization(self, mock_openai):
        """测试OpenAI客户端初始化"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        agent = MultiAIAgent("test", "openai")
        assert agent.client is not None
        
    def test_system_prompt_loading(self):
        """测试系统提示词加载"""
        prompt = self.agent.get_system_prompt()
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        
    def test_conversation_history(self):
        """测试对话历史管理"""
        # 添加对话历史
        self.agent.add_to_history("user", "测试输入")
        self.agent.add_to_history("assistant", "测试输出")
        
        assert len(self.agent.conversation_history) == 2
        assert self.agent.conversation_history[0]["role"] == "user"
        assert self.agent.conversation_history[1]["role"] == "assistant"
        
    def test_conversation_context(self):
        """测试对话上下文获取"""
        # 添加一些历史
        self.agent.add_to_history("user", "用户问题")
        self.agent.add_to_history("assistant", "助手回答")
        
        context = self.agent.get_conversation_context()
        assert "用户问题" in context
        assert "助手回答" in context
        
    def test_clear_history(self):
        """测试清空对话历史"""
        self.agent.add_to_history("user", "测试")
        assert len(self.agent.conversation_history) == 1
        
        self.agent.clear_history()
        assert len(self.agent.conversation_history) == 0


class TestOperationsAgent:
    """运维专家Agent测试类"""
    
    def setup_method(self):
        """测试前设置"""
        self.agent = OperationsAgent("openai")
        
    def test_agent_initialization(self):
        """测试运维Agent初始化"""
        assert self.agent.agent_type == "operations"
        assert self.agent.provider == "openai"
        assert hasattr(self.agent, 'code_generator')
        
    def test_system_prompt_content(self):
        """测试运维专家系统提示词内容"""
        prompt = self.agent.get_system_prompt()
        assert "运维专家" in prompt
        assert "Docker" in prompt
        assert "Kubernetes" in prompt
        assert "CI/CD" in prompt
        
    def test_expertise_areas(self):
        """测试专业领域列表"""
        areas = self.agent.get_expertise_areas()
        assert isinstance(areas, list)
        assert len(areas) > 0
        assert "服务器部署和配置" in areas
        
    def test_best_practices_docker(self):
        """测试Docker最佳实践"""
        practices = self.agent.provide_best_practices("docker")
        assert "Docker" in practices
        assert "最佳实践" in practices
        
    def test_best_practices_unknown(self):
        """测试未知主题最佳实践"""
        practices = self.agent.provide_best_practices("unknown")
        assert "正在整理中" in practices
        
    def test_troubleshooting_high_cpu(self):
        """测试高CPU使用率排查"""
        guide = self.agent.troubleshoot_common_issues("high_cpu")
        assert "高CPU使用率" in guide
        assert "top" in guide
        
    def test_troubleshooting_unknown(self):
        """测试未知问题排查"""
        guide = self.agent.troubleshoot_common_issues("unknown")
        assert "正在整理中" in guide
        
    def test_deployment_script_generation_web(self):
        """测试Web服务部署脚本生成"""
        scripts = self.agent.generate_runnable_deployment_script("test-service", "web")
        assert isinstance(scripts, dict)
        assert "deploy_test-service.sh" in scripts
        assert "README.md" in scripts
        
    def test_deployment_script_generation_docker(self):
        """测试Docker部署脚本生成"""
        scripts = self.agent.generate_runnable_deployment_script("test-service", "docker")
        assert isinstance(scripts, dict)
        assert "docker-compose.yml" in scripts
        assert "Dockerfile" in scripts
        
    def test_shell_script_validation(self):
        """测试Shell脚本验证"""
        valid_script = "#!/bin/bash\necho 'Hello World'"
        is_valid, error = self.agent.validate_shell_script(valid_script)
        assert is_valid == True
        assert error is None or len(error) == 0


class TestGoAgent:
    """Go语言专家Agent测试类"""
    
    def setup_method(self):
        """测试前设置"""
        self.agent = GoAgent("openai")
        
    def test_agent_initialization(self):
        """测试Go Agent初始化"""
        assert self.agent.agent_type == "go"
        assert self.agent.provider == "openai"
        assert hasattr(self.agent, 'code_generator')
        
    def test_system_prompt_content(self):
        """测试Go专家系统提示词内容"""
        prompt = self.agent.get_system_prompt()
        assert "Go语言" in prompt
        assert "并发编程" in prompt
        assert "goroutine" in prompt
        
    def test_go_best_practices(self):
        """测试Go语言最佳实践"""
        practices = self.agent.get_go_best_practices()
        assert "Go语言" in practices
        assert "最佳实践" in practices
        assert "错误处理" in practices
        
    def test_code_template_http_server(self):
        """测试HTTP服务器模板"""
        template = self.agent.generate_code_template("http_server")
        assert "package main" in template
        assert "net/http" in template
        assert "ListenAndServe" in template
        
    def test_code_template_grpc_service(self):
        """测试gRPC服务模板"""
        template = self.agent.generate_code_template("grpc_service")
        assert "package main" in template
        assert "grpc" in template
        assert "RegisterYourServiceServer" in template
        
    def test_code_template_concurrent_worker(self):
        """测试并发工作池模板"""
        template = self.agent.generate_code_template("concurrent_worker")
        assert "package main" in template
        assert "sync.WaitGroup" in template
        assert "goroutine" in template
        
    def test_code_template_unknown(self):
        """测试未知模板类型"""
        template = self.agent.generate_code_template("unknown")
        assert "不存在" in template
        
    def test_go_code_analysis(self):
        """测试Go代码分析"""
        code = "package main\n\nfunc main() {\n    println(\"Hello\")\n}"
        analysis = self.agent.analyze_go_code(code)
        assert "代码分析结果" in analysis
        assert "Go语言规范" in analysis
        
    def test_go_project_generation_web(self):
        """测试Go Web项目生成"""
        project = self.agent.generate_runnable_go_project("myapp", "web")
        assert isinstance(project, dict)
        assert "myapp/main.go" in project
        assert "myapp/go.mod" in project
        assert "myapp/handlers/" in project
        
    def test_go_code_validation(self):
        """测试Go代码验证"""
        valid_code = "package main\n\nfunc main() {}"
        is_valid, error = self.agent.validate_go_code(valid_code)
        assert is_valid == True


class TestMonitoringAgent:
    """监控专家Agent测试类"""
    
    def setup_method(self):
        """测试前设置"""
        self.agent = MonitoringAgent("openai")
        
    def test_agent_initialization(self):
        """测试监控Agent初始化"""
        assert self.agent.agent_type == "monitoring"
        assert self.agent.provider == "openai"
        assert hasattr(self.agent, 'code_generator')
        
    def test_system_prompt_content(self):
        """测试监控专家系统提示词内容"""
        prompt = self.agent.get_system_prompt()
        assert "监控专家" in prompt
        assert "Prometheus" in prompt
        assert "Grafana" in prompt
        
    def test_monitoring_best_practices(self):
        """测试监控最佳实践"""
        practices = self.agent.get_monitoring_best_practices()
        assert "监控" in practices
        assert "最佳实践" in practices
        assert "Prometheus" in practices
        
    def test_prometheus_config_generation(self):
        """测试Prometheus配置生成"""
        config = self.agent.generate_prometheus_config("myapp")
        assert isinstance(config, dict)
        assert "prometheus.yml" in config
        assert "alert_rules.yml" in config
        
    def test_grafana_dashboard_generation(self):
        """测试Grafana仪表板生成"""
        dashboard = self.agent.generate_grafana_dashboard("myapp", "web")
        assert isinstance(dashboard, dict)
        assert "dashboard.json" in dashboard
        assert "datasource.yml" in dashboard
        
    def test_monitoring_stack_generation(self):
        """测试监控栈生成"""
        stack = self.agent.generate_monitoring_stack("docker", "prometheus")
        assert isinstance(stack, dict)
        assert "docker-compose.yml" in stack
        assert "prometheus.yml" in stack


class TestAnsibleAgent:
    """Ansible专家Agent测试类"""
    
    def setup_method(self):
        """测试前设置"""
        self.agent = AnsibleAgent("openai")
        
    def test_agent_initialization(self):
        """测试Ansible Agent初始化"""
        assert self.agent.agent_type == "ansible"
        assert self.agent.provider == "openai"
        assert hasattr(self.agent, 'code_generator')
        
    def test_system_prompt_content(self):
        """测试Ansible专家系统提示词内容"""
        prompt = self.agent.get_system_prompt()
        assert "Ansible" in prompt
        assert "自动化" in prompt
        assert "Playbook" in prompt
        
    def test_ansible_best_practices(self):
        """测试Ansible最佳实践"""
        practices = self.agent.get_ansible_best_practices()
        assert "Ansible" in practices
        assert "最佳实践" in practices
        assert "Playbook" in practices
        
    def test_playbook_generation_web_deploy(self):
        """测试Web部署Playbook生成"""
        playbook = self.agent.generate_playbook("web-deploy", "nginx")
        assert isinstance(playbook, dict)
        assert "site.yml" in playbook
        assert "roles/" in playbook
        
    def test_role_structure_generation(self):
        """测试Role结构生成"""
        role = self.agent.generate_role_structure("webserver")
        assert isinstance(role, dict)
        assert "tasks/main.yml" in role
        assert "handlers/main.yml" in role
        assert "templates/" in role
        
    def test_inventory_config_generation(self):
        """测试Inventory配置生成"""
        inventory = self.agent.generate_inventory_config("production")
        assert isinstance(inventory, dict)
        assert "inventory.ini" in inventory
        assert "group_vars/" in inventory


class TestCodeGenerator:
    """代码生成器测试类"""
    
    def setup_method(self):
        """测试前设置"""
        self.generator = CodeGenerator()
        
    def test_code_generator_initialization(self):
        """测试代码生成器初始化"""
        assert self.generator is not None
        assert hasattr(self.generator, 'logger')
        
    def test_executable_script_generation(self):
        """测试可执行脚本生成"""
        script_content = "#!/bin/bash\necho 'Hello World'"
        script = self.generator.generate_executable_script(script_content, "shell", "test.sh")
        assert "#!/bin/bash" in script
        assert "Hello World" in script
        
    def test_markdown_documentation_generation(self):
        """测试Markdown文档生成"""
        code_examples = [
            {
                "title": "测试代码",
                "description": "这是一个测试",
                "language": "python",
                "code": "print('Hello')"
            }
        ]
        doc = self.generator.generate_markdown_documentation(
            "测试文档", "这是描述", code_examples
        )
        assert "# 测试文档" in doc
        assert "```python" in doc
        assert "print('Hello')" in doc
        
    def test_code_validation_python(self):
        """测试Python代码验证"""
        valid_python = "print('Hello World')"
        is_valid, error = self.generator.validate_code(valid_python, "python")
        assert is_valid == True
        
    def test_code_validation_invalid_python(self):
        """测试无效Python代码验证"""
        invalid_python = "print('Hello World'"
        is_valid, error = self.generator.validate_code(invalid_python, "python")
        assert is_valid == False
        
    def test_code_validation_go(self):
        """测试Go代码验证"""
        valid_go = "package main\n\nfunc main() {}"
        is_valid, error = self.generator.validate_code(valid_go, "go")
        assert is_valid == True


class TestIntegration:
    """集成测试类"""
    
    def setup_method(self):
        """测试前设置"""
        self.operations_agent = OperationsAgent("openai")
        self.go_agent = GoAgent("openai")
        self.monitoring_agent = MonitoringAgent("openai")
        self.ansible_agent = AnsibleAgent("openai")
        
    def test_all_agents_initialization(self):
        """测试所有Agent初始化"""
        assert self.operations_agent.agent_type == "operations"
        assert self.go_agent.agent_type == "go"
        assert self.monitoring_agent.agent_type == "monitoring"
        assert self.ansible_agent.agent_type == "ansible"
        
    def test_agent_switching(self):
        """测试Agent切换功能"""
        agents = {
            "operations": self.operations_agent,
            "go": self.go_agent,
            "monitoring": self.monitoring_agent,
            "ansible": self.ansible_agent
        }
        
        for agent_type, agent in agents.items():
            assert agent.agent_type == agent_type
            assert hasattr(agent, 'get_system_prompt')
            assert hasattr(agent, 'process_request')
            
    def test_cross_agent_functionality(self):
        """测试跨Agent功能协作"""
        # 运维Agent生成部署脚本
        deploy_scripts = self.operations_agent.generate_runnable_deployment_script("test-app", "web")
        
        # Go Agent生成Go代码
        go_code = self.go_agent.generate_code_template("http_server")
        
        # 监控Agent生成监控配置
        monitoring_config = self.monitoring_agent.generate_prometheus_config("test-app")
        
        # Ansible Agent生成自动化配置
        ansible_config = self.ansible_agent.generate_playbook("deploy", "web")
        
        # 验证所有输出都是字典格式
        assert isinstance(deploy_scripts, dict)
        assert isinstance(go_code, str)
        assert isinstance(monitoring_config, dict)
        assert isinstance(ansible_config, dict)


class TestErrorHandling:
    """错误处理测试类"""
    
    def test_invalid_provider(self):
        """测试无效AI提供商"""
        with pytest.raises(ValueError):
            MultiAIAgent("test", "invalid_provider")
            
    def test_empty_api_key(self):
        """测试空API密钥"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            agent = MultiAIAgent("test", "openai")
            # 应该能够处理空API密钥情况
            assert agent is not None
            
    def test_network_error_handling(self):
        """测试网络错误处理"""
        agent = MultiAIAgent("test", "openai")
        
        # 模拟网络错误
        with patch.object(agent, 'client', None):
            # 应该能够处理客户端为None的情况
            assert agent.client is None
            
    def test_invalid_input_handling(self):
        """测试无效输入处理"""
        agent = OperationsAgent("openai")
        
        # 测试空输入
        result = agent.validate_shell_script("")
        assert result[0] == False  # 应该返回无效
        
        # 测试None输入
        result = agent.validate_shell_script(None)
        assert result[0] == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])