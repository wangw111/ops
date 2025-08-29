"""
Multi-AI provider agent implementation supporting OpenAI, Claude, and Qwen.
"""

import os
from typing import Dict, Any, Optional
from agents.base_agent import BaseAgent


class MultiAIAgent(BaseAgent):
    """多AI提供商Agent - 支持OpenAI、Claude和Qwen"""
    
    def __init__(self, agent_type: str, provider: str = "openai"):
        """
        初始化多AI提供商Agent
        
        Args:
            agent_type: Agent类型
            provider: AI提供商 (openai, claude, qwen)
        """
        super().__init__(agent_type)
        self.provider = provider
        self.config = self._get_provider_config()
        self.client = self._initialize_client()
        self.logger.info(f"初始化 {provider} {agent_type} Agent")
    
    def _get_provider_config(self) -> Dict[str, Any]:
        """获取提供商配置"""
        base_config = get_agent_config(self.agent_type)
        
        provider_configs = {
            "openai": {
                "api_key": os.getenv("OPENAI_API_KEY", ""),
                "base_url": "https://api.openai.com/v1",
                "model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                "max_tokens": int(os.getenv("OPENAI_MAX_TOKENS", "1000")),
                "temperature": float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
            },
            "claude": {
                "api_key": os.getenv("CLAUDE_API_KEY", ""),
                "base_url": "https://api.anthropic.com",
                "model": os.getenv("CLAUDE_MODEL", "claude-3-sonnet-20240229"),
                "max_tokens": int(os.getenv("CLAUDE_MAX_TOKENS", "1000")),
                "temperature": float(os.getenv("CLAUDE_TEMPERATURE", "0.7"))
            },
            "qwen": {
                "api_key": os.getenv("QWEN_API_KEY", ""),
                "base_url": "https://dashscope.aliyuncs.com/api/v1",
                "model": os.getenv("QWEN_MODEL", "qwen-turbo"),
                "max_tokens": int(os.getenv("QWEN_MAX_TOKENS", "1000")),
                "temperature": float(os.getenv("QWEN_TEMPERATURE", "0.7"))
            }
        }
        
        config = provider_configs.get(self.provider, provider_configs["openai"])
        config.update({
            "system_prompt": base_config["system_prompt"]
        })
        
        return config
    
    def _initialize_client(self):
        """初始化AI客户端"""
        if self.provider == "openai":
            from openai import OpenAI
            return OpenAI(api_key=self.config["api_key"])
        elif self.provider == "claude":
            import anthropic
            return anthropic.Anthropic(api_key=self.config["api_key"])
        elif self.provider == "qwen":
            # Qwen使用DashScope SDK
            try:
                from dashscope import Generation
                return Generation
            except ImportError:
                self.logger.warning("DashScope SDK未安装，请运行: pip install dashscope")
                return None
        else:
            raise ValueError(f"不支持的AI提供商: {self.provider}")
    
    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return self.config["system_prompt"]
    
    def _generate_response(self, user_input: str) -> str:
        """生成响应"""
        try:
            if self.provider == "openai":
                return self._generate_openai_response(user_input)
            elif self.provider == "claude":
                return self._generate_claude_response(user_input)
            elif self.provider == "qwen":
                return self._generate_qwen_response(user_input)
            else:
                raise ValueError(f"不支持的AI提供商: {self.provider}")
                
        except Exception as e:
            self.logger.error(f"调用{self.provider} API时发生错误: {str(e)}")
            return f"抱歉，处理您的请求时发生了错误：{str(e)}"
    
    def _generate_openai_response(self, user_input: str) -> str:
        """生成OpenAI响应"""
        messages = [
            {"role": "system", "content": self.get_system_prompt()}
        ]
        
        # 添加历史对话上下文
        context = self.get_conversation_context()
        if context:
            messages.append({"role": "system", "content": context})
        
        messages.append({"role": "user", "content": user_input})
        
        response = self.client.chat.completions.create(
            model=self.config["model"],
            messages=messages,
            temperature=self.config["temperature"],
            max_tokens=self.config["max_tokens"],
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        
        assistant_response = response.choices[0].message.content
        return assistant_response if assistant_response else "抱歉，无法生成响应。"
    
    def _generate_claude_response(self, user_input: str) -> str:
        """生成Claude响应"""
        system_prompt = self.get_system_prompt()
        
        # 添加历史对话上下文
        context = self.get_conversation_context()
        if context:
            system_prompt += f"\n\n{context}"
        
        response = self.client.messages.create(
            model=self.config["model"],
            max_tokens=self.config["max_tokens"],
            temperature=self.config["temperature"],
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        
        assistant_response = response.content[0].text
        return assistant_response if assistant_response else "抱歉，无法生成响应。"
    
    def _generate_qwen_response(self, user_input: str) -> str:
        """生成Qwen响应"""
        if not self.client:
            return "Qwen SDK未正确安装，请检查配置。"
        
        system_prompt = self.get_system_prompt()
        
        # 添加历史对话上下文
        context = self.get_conversation_context()
        if context:
            user_input = f"{context}\n\n用户: {user_input}"
        
        try:
            response = self.client.call(
                model=self.config["model"],
                input={
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ]
                },
                parameters={
                    "temperature": self.config["temperature"],
                    "max_tokens": self.config["max_tokens"]
                }
            )
            
            if response and response.output and response.output.text:
                return response.output.text
            else:
                return "抱歉，无法生成响应。"
                
        except Exception as e:
            self.logger.error(f"调用Qwen API时发生错误: {str(e)}")
            return f"抱歉，处理您的请求时发生了错误：{str(e)}"
    
    def switch_provider(self, new_provider: str):
        """切换AI提供商"""
        if new_provider not in ["openai", "claude", "qwen"]:
            raise ValueError(f"不支持的AI提供商: {new_provider}")
        
        self.provider = new_provider
        self.config = self._get_provider_config()
        self.client = self._initialize_client()
        self.logger.info(f"已切换到 {new_provider} 提供商")
    
    def get_provider_info(self) -> Dict[str, Any]:
        """获取当前提供商信息"""
        return {
            "provider": self.provider,
            "model": self.config["model"],
            "max_tokens": self.config["max_tokens"],
            "temperature": self.config["temperature"],
            "api_key_status": "已设置" if self.config["api_key"] else "未设置"
        }
    
    def validate_provider_config(self) -> tuple:
        """验证提供商配置"""
        if not self.config["api_key"]:
            return False, f"{self.provider} API密钥未设置"
        
        if self.provider == "openai":
            try:
                # 简单的API密钥格式验证
                if not self.config["api_key"].startswith("sk-"):
                    return False, "OpenAI API密钥格式不正确"
            except Exception as e:
                return False, f"OpenAI配置验证失败: {str(e)}"
        
        elif self.provider == "claude":
            try:
                if not self.config["api_key"].startswith("sk-ant-"):
                    return False, "Claude API密钥格式不正确"
            except Exception as e:
                return False, f"Claude配置验证失败: {str(e)}"
        
        elif self.provider == "qwen":
            try:
                if len(self.config["api_key"]) < 10:
                    return False, "Qwen API密钥格式不正确"
            except Exception as e:
                return False, f"Qwen配置验证失败: {str(e)}"
        
        return True, "配置验证通过"


# 为了避免循环导入，在这里导入get_agent_config
from config.settings import get_agent_config