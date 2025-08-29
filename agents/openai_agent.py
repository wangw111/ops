"""
OpenAI Agent implementation for development assistants.
"""

from openai import OpenAI
from typing import Dict, Any
from agents.base_agent import BaseAgent


class OpenAIAgent(BaseAgent):
    """基于OpenAI的Agent实现"""
    
    def __init__(self, agent_type: str):
        """
        初始化OpenAI Agent
        
        Args:
            agent_type: Agent类型
        """
        super().__init__(agent_type)
        
        # 初始化OpenAI客户端
        self.client = OpenAI(
            api_key=self.config["api_key"]
        )
        
        self.logger.info(f"初始化OpenAI {agent_type} Agent")
    
    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return self.config["system_prompt"]
    
    def _generate_response(self, user_input: str) -> str:
        """
        使用OpenAI API生成响应
        
        Args:
            user_input: 用户输入文本
            
        Returns:
            AI生成的响应
        """
        try:
            # 构建对话上下文
            messages = [
                {"role": "system", "content": self.get_system_prompt()}
            ]
            
            # 添加历史对话上下文
            context = self.get_conversation_context()
            if context:
                messages.append({"role": "system", "content": context})
            
            # 添加用户输入
            messages.append({"role": "user", "content": user_input})
            
            # 调用OpenAI API
            response = self.client.chat.completions.create(
                model=self.config["model_name"],
                messages=messages,  # type: ignore
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"],
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            # 提取响应内容
            assistant_response = response.choices[0].message.content
            if assistant_response is None:
                assistant_response = "抱歉，无法生成响应。"
            
            self.logger.info(f"成功生成响应，使用模型: {self.config['model_name']}")
            return assistant_response
            
        except Exception as e:
            self.logger.error(f"调用OpenAI API时发生错误: {str(e)}")
            raise e
    
    def update_config(self, new_config: Dict[str, Any]):
        """
        更新Agent配置
        
        Args:
            new_config: 新的配置字典
        """
        self.config.update(new_config)
        if "api_key" in new_config:
            self.client.api_key = new_config["api_key"]
        self.logger.info("Agent配置已更新")