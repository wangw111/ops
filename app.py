"""
Development Assistant Agents - Streamlit Web Interface
"""

import streamlit as st
import os
import sys
from typing import Dict, Any
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.operations_agent import OperationsAgent
from agents.go_agent import GoAgent
from agents.monitoring_agent import MonitoringAgent
from utils.helpers import get_agent_info, setup_logging, format_timestamp
from config.settings import get_config


class StreamlitInterface:
    """Streamlit界面管理类"""
    
    def __init__(self):
        """初始化Streamlit界面"""
        self.agents = {
            "operations": OperationsAgent(),
            "go": GoAgent(),
            "monitoring": MonitoringAgent()
        }
        self.logger = setup_logging()
        self.config = get_config()
        
        # 初始化session state
        self._init_session_state()
    
    def _init_session_state(self):
        """初始化session state"""
        if 'current_agent' not in st.session_state:
            st.session_state.current_agent = "operations"
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = {}
        if 'conversation_count' not in st.session_state:
            st.session_state.conversation_count = 0
    
    def render_sidebar(self):
        """渲染侧边栏"""
        st.sidebar.title("🤖 开发助手Agent")
        st.sidebar.markdown("---")
        
        # Agent选择
        st.sidebar.subheader("选择专家")
        all_agent_info = get_agent_info()  # 获取所有agent信息
        
        for agent_type, info in all_agent_info.items():
            if agent_type in self.agents:
                col1, col2 = st.sidebar.columns([1, 4])
                with col1:
                    st.markdown(f"<h2 style='margin:0; text-align:center'>{info['icon']}</h2>", unsafe_allow_html=True)
                with col2:
                    if st.button(
                        info['name'],
                        key=f"agent_{agent_type}",
                        help=info['description'],
                        use_container_width=True
                    ):
                        st.session_state.current_agent = agent_type
                        st.rerun()
        
        st.sidebar.markdown("---")
        
        # 当前Agent信息
        current_info = get_agent_info(st.session_state.current_agent)
        st.sidebar.subheader(f"当前专家: {current_info['name']}")
        st.sidebar.markdown(f"**描述**: {current_info['description']}")
        
        # 操作按钮
        st.sidebar.markdown("---")
        if st.sidebar.button("🗑️ 清空对话", key="clear_chat"):
            self.agents[st.session_state.current_agent].clear_history()
            st.session_state.chat_history[st.session_state.current_agent] = []
            st.rerun()
        
        # 配置信息
        st.sidebar.markdown("---")
        st.sidebar.subheader("配置信息")
        st.sidebar.markdown(f"**模型**: {self.config.model_name}")
        st.sidebar.markdown(f"**温度**: {self.config.temperature}")
        st.sidebar.markdown(f"**最大令牌**: {self.config.max_tokens}")
    
    def render_chat_interface(self):
        """渲染聊天界面"""
        current_agent = self.agents[st.session_state.current_agent]
        agent_info = get_agent_info(st.session_state.current_agent)
        
        # 标题
        st.title(f"{agent_info['icon']} {agent_info['name']}")
        st.markdown(f"*{agent_info['description']}*")
        
        # 初始化聊天历史
        if st.session_state.current_agent not in st.session_state.chat_history:
            st.session_state.chat_history[st.session_state.current_agent] = []
        
        # 显示聊天历史
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_history[st.session_state.current_agent]:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                    if message["timestamp"]:
                        st.caption(f"📅 {message['timestamp']}")
        
        # 用户输入
        user_input = st.chat_input(f"向{agent_info['name']}提问...")
        
        if user_input:
            # 处理用户输入
            with st.chat_message("user"):
                st.markdown(user_input)
                st.caption(f"📅 {format_timestamp(datetime.now())}")
            
            # 添加到聊天历史
            st.session_state.chat_history[st.session_state.current_agent].append({
                "role": "user",
                "content": user_input,
                "timestamp": format_timestamp(datetime.now())
            })
            
            # 获取Agent响应
            with st.chat_message("assistant"):
                with st.spinner("思考中..."):
                    response = current_agent.process_request(user_input)
                    st.markdown(response)
                    st.caption(f"📅 {format_timestamp(datetime.now())}")
            
            # 添加响应到聊天历史
            st.session_state.chat_history[st.session_state.current_agent].append({
                "role": "assistant",
                "content": response,
                "timestamp": format_timestamp(datetime.now())
            })
    
    def render_agent_features(self):
        """渲染Agent特色功能"""
        current_agent = self.agents[st.session_state.current_agent]
        agent_info = get_agent_info(st.session_state.current_agent)
        
        st.markdown("---")
        st.subheader(f"{agent_info['name']} 特色功能")
        
        # 根据不同Agent类型显示不同功能
        if st.session_state.current_agent == "operations":
            self._render_operations_features()
        elif st.session_state.current_agent == "go":
            self._render_go_features()
        elif st.session_state.current_agent == "monitoring":
            self._render_monitoring_features()
    
    def _render_operations_features(self):
        """渲染运维专家特色功能"""
        ops_agent = self.agents["operations"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📚 专业领域")
            for area in ops_agent.get_expertise_areas():
                st.markdown(f"- {area}")
        
        with col2:
            st.markdown("#### 🔧 快速帮助")
            if st.button("Docker最佳实践", key="docker_best_practices"):
                st.info(ops_agent.provide_best_practices("docker"))
            
            if st.button("Kubernetes最佳实践", key="k8s_best_practices"):
                st.info(ops_agent.provide_best_practices("kubernetes"))
    
    def _render_go_features(self):
        """渲染Go专家特色功能"""
        go_agent = self.agents["go"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📖 Go最佳实践")
            if st.button("显示Go最佳实践", key="go_best_practices"):
                st.info(go_agent.get_go_best_practices())
        
        with col2:
            st.markdown("#### 📝 代码模板")
            template_type = st.selectbox(
                "选择模板类型",
                ["http_server", "grpc_service", "concurrent_worker"],
                key="template_select"
            )
            
            if st.button("生成代码模板", key="generate_template"):
                st.code(go_agent.generate_code_template(template_type), language="go")
    
    def _render_monitoring_features(self):
        """渲染监控专家特色功能"""
        monitor_agent = self.agents["monitoring"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 监控栈推荐")
            system_type = st.selectbox(
                "选择系统类型",
                ["microservices", "web_application", "kubernetes"],
                key="system_type_select"
            )
            
            if st.button("获取监控方案", key="get_monitoring_stack"):
                st.info(monitor_agent.get_monitoring_stack_recommendation(system_type))
        
        with col2:
            st.markdown("#### ⚙️ 配置生成")
            service_name = st.text_input("服务名称", value="my-service", key="service_name_input")
            
            if st.button("生成Prometheus配置", key="generate_prometheus"):
                st.code(monitor_agent.generate_prometheus_config(service_name), language="yaml")
    
    def render_statistics(self):
        """渲染统计信息"""
        st.markdown("---")
        st.subheader("📈 使用统计")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_conversations = sum(len(history) for history in st.session_state.chat_history.values())
            st.metric("总对话数", total_conversations)
        
        with col2:
            current_history = len(st.session_state.chat_history.get(st.session_state.current_agent, []))
            st.metric("当前对话数", current_history)
        
        with col3:
            st.metric("可用Agent", len(self.agents))
    
    def run(self):
        """运行Streamlit应用"""
        # 页面配置
        st.set_page_config(
            page_title="开发助手Agent",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # 自定义CSS
        st.markdown("""
        <style>
            .stChatMessage {
                padding: 1rem;
                border-radius: 0.5rem;
                margin-bottom: 1rem;
            }
            .stChatMessage.user {
                background-color: #f0f2f6;
            }
            .stChatMessage.assistant {
                background-color: #e8f4f8;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # 渲染界面
        self.render_sidebar()
        self.render_chat_interface()
        self.render_agent_features()
        self.render_statistics()
        
        # 页脚
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; color: #666;'>"
            "🤖 开发助手Agent - 基于Streamlit和OpenAI构建"
            "</div>",
            unsafe_allow_html=True
        )


def main():
    """主函数"""
    try:
        app = StreamlitInterface()
        app.run()
    except Exception as e:
        st.error(f"应用启动失败: {str(e)}")
        st.error("请检查配置文件和环境变量设置")


if __name__ == "__main__":
    main()