#!/bin/bash

# 开发助手 Agent 启动脚本

echo "🤖 启动开发助手 Agent 系统..."

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，正在创建..."
    python3 -m venv venv
    echo "✅ 虚拟环境创建完成"
fi

# 激活虚拟环境
echo "🔄 激活虚拟环境..."
source venv/bin/activate

# 检查依赖
echo "📦 检查依赖包..."
pip install -r requirements.txt > /dev/null 2>&1

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "⚠️  .env 文件不存在，请先配置 OpenAI API Key"
    echo "📝 复制 .env.example 到 .env 并填入你的 API Key:"
    echo "   cp .env.example .env"
    echo "   vim .env"
    exit 1
fi

# 启动应用
echo "🚀 启动 Streamlit 应用..."
echo "📱 应用将在 http://localhost:8501 运行"
echo "⏹️  按 Ctrl+C 停止应用"
echo ""

streamlit run app.py