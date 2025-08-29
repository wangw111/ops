# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a new project for creating development assistant agents using Streamlit and Agno. The goal is to build specialized agents for different domains including operations, Go development, and monitoring.

## Current State

The project is in early planning stage with only a plan.txt file outlining the initial requirements:
- Create development assistant agents using Streamlit and Agno
- Build specialized agents for operations, Go development, and monitoring
- Ensure complete code comments, language specification compliance, and clear logic

## Development Environment

This appears to be a Python-based project that will require:
- Streamlit for the web interface
- Agno for agent functionality
- Python 3.8+ (recommended for Streamlit compatibility)

## Getting Started

### 环境配置
1. 复制环境变量配置文件：
   ```bash
   cp .env.example .env
   ```
2. 编辑 `.env` 文件，设置 OpenAI API 密钥和其他配置

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行应用
```bash
streamlit run app.py
```

应用将在 `http://localhost:8501` 启动

## 项目结构

```
xx/
├── app.py                    # Streamlit主应用
├── requirements.txt          # Python依赖
├── .env.example            # 环境变量配置示例
├── agents/                  # Agent实现
│   ├── __init__.py
│   ├── base_agent.py       # 基础Agent类
│   ├── openai_agent.py     # OpenAI Agent实现
│   ├── operations_agent.py # 运维专家Agent
│   ├── go_agent.py         # Go语言专家Agent
│   └── monitoring_agent.py # 监控专家Agent
├── config/                  # 配置管理
│   ├── __init__.py
│   └── settings.py         # 配置设置
├── utils/                   # 工具函数
│   ├── __init__.py
│   └── helpers.py          # 辅助函数
└── CLAUDE.md               # 项目文档
```

## Agent类型

### 1. 运维专家 (Operations Agent)
- 服务器部署和配置管理
- 容器化技术（Docker, Kubernetes）
- CI/CD 流水线搭建和维护
- 系统监控和性能优化
- 故障排查和应急响应

### 2. Go语言专家 (Go Agent)
- Go语言语法和最佳实践
- 并发编程和goroutine管理
- 微服务架构设计
- 性能优化和内存管理
- 测试驱动开发

### 3. 监控专家 (Monitoring Agent)
- 系统监控架构设计
- 指标收集和存储（Prometheus, Grafana）
- 日志管理和分析
- 告警规则配置
- 性能瓶颈分析

## 开发规范

### 代码规范
- 所有代码必须包含完整的中文注释
- 遵循PEP 8 Python代码规范
- 使用类型注解提高代码可读性
- 错误处理要完善，提供友好的错误信息

### 文档规范
- 所有函数和类都需要docstring文档
- 使用中文编写注释和文档
- 文档要包含参数说明、返回值说明和使用示例

### 测试规范
- 为所有核心功能编写单元测试
- 测试覆盖率要达到80%以上
- 使用pytest进行测试

## 架构设计

### 模块化设计
- 使用基础Agent类提供通用功能
- 各专业Agent继承基础类并实现特定功能
- 配置管理统一在config模块
- 工具函数集中在utils模块

### 扩展性设计
- 可以轻松添加新的Agent类型
- 支持不同的AI模型提供商
- 配置化管理便于部署和维护

### 用户界面
- 基于Streamlit的Web界面
- 支持多种Agent切换
- 实时对话和历史记录
- 特色功能快速访问