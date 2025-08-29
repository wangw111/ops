"""
Base agent framework for development assistants.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging
from datetime import datetime

from utils.helpers import setup_logging, format_timestamp, validate_agent_input, sanitize_response
from config.settings import get_agent_config


class BaseAgent(ABC):
    """基础Agent抽象类"""
    
    def __init__(self, agent_type: str):
        """
        初始化Agent
        
        Args:
            agent_type: Agent类型
        """
        self.agent_type = agent_type
        self.config = get_agent_config(agent_type)
        self.logger = setup_logging()
        self.conversation_history = []
        
        self.logger.info(f"初始化 {agent_type} Agent")
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        pass
    
    def validate_input(self, user_input: str) -> bool:
        """
        验证用户输入
        
        Args:
            user_input: 用户输入文本
            
        Returns:
            是否通过验证
        """
        return validate_agent_input(user_input)
    
    def add_to_history(self, role: str, content: str, timestamp: Optional[datetime] = None):
        """
        添加对话历史
        
        Args:
            role: 角色（user/assistant）
            content: 对话内容
            timestamp: 时间戳
        """
        if timestamp is None:
            timestamp = datetime.now()
            
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": format_timestamp(timestamp)
        })
        
        # 保持历史记录在合理范围内
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def get_conversation_context(self) -> str:
        """
        获取对话上下文
        
        Returns:
            格式化的对话上下文
        """
        if not self.conversation_history:
            return ""
        
        context = "之前的对话历史：\n"
        for entry in self.conversation_history[-10:]:  # 只保留最近10条
            context += f"{entry['role']}: {entry['content']}\n"
        
        return context
    
    def process_request(self, user_input: str) -> str:
        """
        处理用户请求
        
        Args:
            user_input: 用户输入文本
            
        Returns:
            Agent响应
        """
        try:
            # 验证输入
            if not self.validate_input(user_input):
                return "输入无效，请提供有效的问题或请求。"
            
            # 记录用户输入
            self.add_to_history("user", user_input)
            
            # 生成响应
            response = self._generate_response(user_input)
            
            # 清理响应
            response = sanitize_response(response)
            
            # 记录响应
            self.add_to_history("assistant", response)
            
            return response
            
        except Exception as e:
            self.logger.error(f"处理请求时发生错误: {str(e)}")
            return f"抱歉，处理您的请求时发生了错误：{str(e)}"
    
    @abstractmethod
    def _generate_response(self, user_input: str) -> str:
        """生成响应的具体实现"""
        pass
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history.clear()
        self.logger.info("对话历史已清空")
    
    def get_agent_info(self) -> Dict[str, Any]:
        """
        获取Agent信息
        
        Returns:
            Agent信息字典
        """
        return {
            "type": self.agent_type,
            "system_prompt": self.get_system_prompt(),
            "config": self.config,
            "history_count": len(self.conversation_history)
        }