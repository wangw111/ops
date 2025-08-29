# 开发助手 Agent 系统

基于 Streamlit 和 OpenAI 构建的专业开发助手 Agent 系统，包含运维专家、Go 语言专家和监控专家三个专业 Agent。

## 功能特性

- 🔧 **运维专家 Agent**: 提供服务器运维、容器化、CI/CD 和系统监控专业指导
- 💻 **Go 语言专家 Agent**: 提供 Go 语言开发、并发编程和微服务架构专业建议
- 📊 **监控专家 Agent**: 提供系统监控、性能分析和告警配置专业方案

## 技术特点

- **完整的代码注释**: 所有代码都有详细的中文注释，符合 Python 语言规范
- **逻辑清晰**: 采用模块化设计，代码结构清晰易懂
- **可运行代码**: 所有生成的代码都经过测试，可以直接运行
- **Markdown 文档**: 支持生成规范的 Markdown 文档
- **多模型支持**: 可对接 OpenAI、Claude、Qwen 等多种大模型

## 系统架构

```
├── agents/                 # Agent 实现模块
│   ├── base_agent.py      # 基础 Agent 抽象类
│   ├── openai_agent.py    # OpenAI API 集成
│   ├── operations_agent.py # 运维专家 Agent
│   ├── go_agent.py        # Go 语言专家 Agent
│   └── monitoring_agent.py # 监控专家 Agent
├── config/                # 配置管理
│   └── settings.py        # 系统配置
├── utils/                 # 工具函数
│   └── helpers.py         # 辅助函数
├── app.py                 # Streamlit 主应用
└── requirements.txt       # 依赖列表
```

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd xx

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置设置

```bash
# 复制配置文件模板
cp .env.example .env

# 编辑配置文件，添加你的 OpenAI API Key
vim .env
```

在 `.env` 文件中配置：

```env
# OpenAI API 配置
OPENAI_API_KEY=your_openai_api_key_here

# 模型配置
MODEL_NAME=gpt-3.5-turbo
TEMPERATURE=0.7
MAX_TOKENS=1000

# Streamlit 配置
STREAMLIT_PORT=8501
STREAMLIT_HOST=0.0.0.0
```

### 3. 启动应用

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动 Streamlit 应用
streamlit run app.py
```

应用将在 http://localhost:8501 启动。

## 使用指南

### 选择专家

在左侧边栏选择你需要的专家：

- 🔧 **运维专家**: 适用于服务器部署、容器化、CI/CD 等运维相关问题
- 💻 **Go 语言专家**: 适用于 Go 语言开发、性能优化、架构设计等问题
- 📊 **监控专家**: 适用于系统监控、告警配置、性能分析等问题

### 对话交互

1. 在聊天框中输入你的问题或需求
2. Agent 会根据其专业领域提供详细的解答和代码示例
3. 支持连续对话，Agent 会记住上下文

### 特色功能

每个 Agent 都提供专业的快速功能：

- **运维专家**: Docker/Kubernetes 最佳实践、故障排查指南
- **Go 语言专家**: 代码模板生成、最佳实践指导
- **监控专家**: 监控方案推荐、配置文件生成

## 扩展开发

### 添加新的 Agent

1. 继承 `BaseAgent` 或 `OpenAIAgent` 类
2. 实现 `get_system_prompt()` 方法
3. 在 `app.py` 中注册新的 Agent
4. 在 `utils/helpers.py` 中添加 Agent 信息

### 支持其他大模型

1. 创建新的 Agent 基类（如 `ClaudeAgent`、`QwenAgent`）
2. 实现对应的 API 调用逻辑
3. 更新配置文件支持新的模型参数

## 开发规范

- **代码注释**: 所有函数和类都需要详细的中文注释
- **类型提示**: 使用 Python 类型提示增强代码可读性
- **错误处理**: 完善的异常处理和日志记录
- **模块化设计**: 保持代码的模块化和可维护性

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

如有问题或建议，请创建 Issue 或联系维护者。