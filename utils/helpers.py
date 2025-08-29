"""
Utility functions for the development assistant agents.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime


def setup_logging(level: str = "INFO") -> logging.Logger:
    """
    设置日志配置
    
    Args:
        level: 日志级别
        
    Returns:
        配置好的日志记录器
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('agent.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def format_timestamp(timestamp: Optional[datetime] = None) -> str:
    """
    格式化时间戳
    
    Args:
        timestamp: 时间戳对象，默认为当前时间
        
    Returns:
        格式化的时间字符串
    """
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def validate_agent_input(user_input: str, max_length: int = 2000) -> bool:
    """
    验证用户输入
    
    Args:
        user_input: 用户输入文本
        max_length: 最大允许长度
        
    Returns:
        是否通过验证
    """
    if not user_input or not user_input.strip():
        return False
    
    if len(user_input) > max_length:
        return False
    
    return True


def sanitize_response(response: str) -> str:
    """
    清理和格式化响应内容
    
    Args:
        response: 原始响应文本
        
    Returns:
        清理后的响应文本
    """
    if not response:
        return "抱歉，无法生成响应。"
    
    # 移除多余的空行
    lines = [line.strip() for line in response.split('\n') if line.strip()]
    return '\n'.join(lines)


def get_agent_info(agent_type: Optional[str] = None) -> Dict[str, Any]:
    """
    获取Agent信息
    
    Args:
        agent_type: Agent类型，如果为None则返回所有agent信息
        
    Returns:
        Agent信息字典
    """
    agent_info = {
        "operations": {
            "name": "运维专家",
            "description": "专业的服务器运维、容器化、CI/CD和系统监控专家",
            "icon": "🔧",
            "color": "#FF6B6B"
        },
        "go": {
            "name": "Go语言专家", 
            "description": "专业的Go语言开发、并发编程和微服务架构专家",
            "icon": "💻",
            "color": "#4ECDC4"
        },
        "monitoring": {
            "name": "监控专家",
            "description": "专业的系统监控、性能分析和告警配置专家", 
            "icon": "📊",
            "color": "#45B7D1"
        },
        "ansible": {
            "name": "Ansible专家",
            "description": "专业的自动化配置管理、部署和DevOps工具链专家",
            "icon": "🎭",
            "color": "#9B59B6"
        }
    }
    
    if agent_type is None:
        return agent_info
    
    return agent_info.get(agent_type, agent_info["operations"])