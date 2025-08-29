"""
Configuration management for the development assistant agents.
"""

import os
from typing import Dict, Any, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class AgentConfig(BaseSettings):
    """Configuration settings for agent system."""
    
    # OpenAI Configuration
    openai_api_key: str = Field(env="OPENAI_API_KEY", default="")
    openai_model: str = Field(env="OPENAI_MODEL", default="gpt-3.5-turbo")
    openai_temperature: float = Field(env="OPENAI_TEMPERATURE", default=0.7)
    openai_max_tokens: int = Field(env="OPENAI_MAX_TOKENS", default=1000)
    
    # Claude Configuration
    claude_api_key: str = Field(env="CLAUDE_API_KEY", default="")
    claude_model: str = Field(env="CLAUDE_MODEL", default="claude-3-sonnet-20240229")
    claude_temperature: float = Field(env="CLAUDE_TEMPERATURE", default=0.7)
    claude_max_tokens: int = Field(env="CLAUDE_MAX_TOKENS", default=1000)
    
    # Qwen Configuration
    qwen_api_key: str = Field(env="QWEN_API_KEY", default="")
    qwen_model: str = Field(env="QWEN_MODEL", default="qwen-turbo")
    qwen_temperature: float = Field(env="QWEN_TEMPERATURE", default=0.7)
    qwen_max_tokens: int = Field(env="QWEN_MAX_TOKENS", default=1000)
    
    # Default Configuration
    default_ai_provider: str = Field(env="DEFAULT_AI_PROVIDER", default="openai")
    model_name: str = Field(env="MODEL_NAME", default="gpt-3.5-turbo")
    temperature: float = Field(env="TEMPERATURE", default=0.7)
    max_tokens: int = Field(env="MAX_TOKENS", default=1000)
    
    # Streamlit Configuration
    streamlit_port: int = Field(env="STREAMLIT_PORT", default=8501)
    streamlit_host: str = Field(env="STREAMLIT_HOST", default="0.0.0.0")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_config() -> AgentConfig:
    """Get configuration instance."""
    return AgentConfig()


def get_agent_config(agent_type: str) -> Dict[str, Any]:
    """Get specific agent configuration."""
    base_config = get_config()
    
    agent_configs = {
        "operations": {
            "system_prompt": """你是一个专业的运维专家，具有以下专长：
1. 服务器部署和配置管理
2. 容器化技术（Docker, Kubernetes）
3. CI/CD 流水线搭建和维护
4. 系统监控和性能优化
5. 故障排查和应急响应
6. 自动化脚本开发

请提供专业、准确、实用的运维建议和解决方案。""",
            "temperature": 0.3,
        },
        "go": {
            "system_prompt": """你是一个专业的Go语言开发专家，具有以下专长：
1. Go语言语法和最佳实践
2. 并发编程和goroutine管理
3. 微服务架构设计
4. 性能优化和内存管理
5. 测试驱动开发
6. 标准库和第三方库使用

请提供符合Go语言规范的高质量代码建议和解决方案。""",
            "temperature": 0.2,
        },
        "monitoring": {
            "system_prompt": """你是一个专业的监控专家，具有以下专长：
1. 系统监控架构设计
2. 指标收集和存储（Prometheus, Grafana）
3. 日志管理和分析
4. 告警规则配置
5. 性能瓶颈分析
6. 监控系统集成

请提供全面、实用的监控方案和优化建议。""",
            "temperature": 0.4,
        },
        "ansible": {
            "system_prompt": """你是一个专业的Ansible专家，具有以下专长：
1. Ansible基础架构和概念
2. 系统配置自动化
3. 应用部署自动化
4. 云平台集成
5. 监控和日志自动化
6. DevOps工具链集成

请提供专业、准确、实用的Ansible自动化方案。""",
            "temperature": 0.3,
        }
    }
    
    config = agent_configs.get(agent_type, agent_configs["operations"])
    return {
        "model_name": base_config.model_name,
        "temperature": config["temperature"],
        "max_tokens": base_config.max_tokens,
        "system_prompt": config["system_prompt"],
        "api_key": base_config.openai_api_key,
    }