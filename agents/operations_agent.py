"""
Operations expert agent for DevOps and system administration.
"""

from typing import Dict, Any, List
from agents.openai_agent import OpenAIAgent
from utils.code_generator import CodeGenerator


class OperationsAgent(OpenAIAgent):
    """运维专家Agent - 专门处理服务器运维、容器化、CI/CD等任务"""
    
    def __init__(self):
        """初始化运维专家Agent"""
        super().__init__("operations")
        self.code_generator = CodeGenerator(self.logger)
        self.logger.info("运维专家Agent已初始化")
    
    def get_system_prompt(self) -> str:
        """获取运维专家的系统提示词"""
        return """你是一个专业的运维专家，具有以下专长：

1. 服务器部署和配置管理
   - Linux/Windows服务器配置
   - 网络配置和优化
   - 安全配置和防护
   - 性能调优和资源管理

2. 容器化技术
   - Docker容器化部署
   - Kubernetes集群管理
   - 容器编排和自动化
   - 微服务架构部署

3. CI/CD 流水线
   - Jenkins/GitLab CI配置
   - 自动化构建和部署
   - 代码质量检查
   - 发布流程管理

4. 系统监控和性能优化
   - 系统资源监控
   - 应用性能分析
   - 日志管理和分析
   - 故障诊断和排查

5. 故障排查和应急响应
   - 系统故障诊断
   - 网络问题排查
   - 性能瓶颈分析
   - 应急响应方案

6. 自动化脚本开发
   - Shell脚本编写
   - Python自动化工具
   - 配置管理工具（Ansible, Puppet）
   - 监控脚本开发

请提供专业、准确、实用的运维建议和解决方案。你的回答应该：
- 技术准确，符合最佳实践
- 提供具体的实施步骤
- 考虑安全性和可维护性
- 适合生产环境使用
- 包含必要的注意事项和风险提示

如果需要，可以提供代码示例和配置文件模板。"""
    
    def get_expertise_areas(self) -> list:
        """获取专业领域列表"""
        return [
            "服务器部署和配置",
            "容器化技术（Docker/Kubernetes）",
            "CI/CD流水线搭建",
            "系统监控和性能优化",
            "故障排查和应急响应",
            "自动化脚本开发",
            "网络安全和防护",
            "备份和恢复策略"
        ]
    
    def provide_best_practices(self, topic: str) -> str:
        """
        提供特定主题的最佳实践
        
        Args:
            topic: 主题名称
            
        Returns:
            最佳实践建议
        """
        best_practices = {
            "docker": "Docker最佳实践：\n1. 使用官方基础镜像\n2. 最小化镜像层数\n3. 使用多阶段构建\n4. 设置适当的资源限制\n5. 定期更新镜像\n6. 使用健康检查",
            "kubernetes": "Kubernetes最佳实践：\n1. 使用命名空间隔离环境\n2. 配置资源请求和限制\n3. 使用ConfigMap和Secret管理配置\n4. 实现健康检查和就绪探针\n5. 使用HPA进行自动扩缩容\n6. 定期备份集群配置",
            "monitoring": "监控最佳实践：\n1. 建立完整的监控体系\n2. 设置合理的告警阈值\n3. 实现多维度监控\n4. 建立告警升级机制\n5. 定期审查监控策略\n6. 实现自动化故障处理"
        }
        
        return best_practices.get(topic.lower(), f"关于{topic}的最佳实践正在整理中...")
    
    def troubleshoot_common_issues(self, issue_type: str) -> str:
        """
        提供常见问题的排查指南
        
        Args:
            issue_type: 问题类型
            
        Returns:
            排查指南
        """
        troubleshooting_guides = {
            "high_cpu": "高CPU使用率排查：\n1. 使用top/htop查看进程占用\n2. 使用ps aux按CPU排序\n3. 检查异常进程和服务\n4. 分析应用日志\n5. 检查系统负载和进程数\n6. 考虑优化配置或扩容",
            "memory_leak": "内存泄漏排查：\n1. 使用free -h查看内存使用\n2. 使用top按内存排序\n3. 检查应用日志\n4. 使用valgrind等工具分析\n5. 重启问题服务临时解决\n6. 代码层面优化内存使用",
            "disk_full": "磁盘空间不足排查：\n1. 使用df -h查看分区使用\n2. 使用du -sh查看目录大小\n3. 清理临时文件和日志\n4. 检查大文件和重复文件\n5. 设置日志轮转策略\n6. 考虑扩容或清理策略"
        }
        
        return troubleshooting_guides.get(issue_type.lower(), f"关于{issue_type}的排查指南正在整理中...")
    
    def generate_runnable_deployment_script(self, service_name: str, service_type: str = "web") -> Dict[str, str]:
        """
        生成可运行的部署脚本
        
        Args:
            service_name: 服务名称
            service_type: 服务类型
            
        Returns:
            部署脚本文件字典
        """
        deployment_templates = {
            "web": {
                f"deploy_{service_name}.sh": self.code_generator.generate_executable_script(
                    f"""#!/bin/bash
# {service_name} Web服务部署脚本
# 自动生成的部署脚本

set -e  # 遇到错误时退出

# 配置变量
SERVICE_NAME="{service_name}"
SERVICE_USER="webuser"
SERVICE_PORT=8080
DEPLOY_DIR="/opt/$SERVICE_NAME"
LOG_DIR="/var/log/$SERVICE_NAME"
BACKUP_DIR="/backup/$SERVICE_NAME"

# 颜色定义
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

# 日志函数
log_info() {{
    echo -e "${{GREEN}}[INFO]${{NC}} $1"
}}

log_warn() {{
    echo -e "${{YELLOW}}[WARN]${{NC}} $1"
}}

log_error() {{
    echo -e "${{RED}}[ERROR]${{NC}} $1"
}}

# 检查权限
check_permissions() {{
    if [[ $EUID -ne 0 ]]; then
        log_error "此脚本需要root权限运行"
        exit 1
    fi
}}

# 创建用户和目录
setup_environment() {{
    log_info "设置部署环境..."
    
    # 创建用户
    if ! id "$SERVICE_USER" &>/dev/null; then
        useradd -r -s /bin/false -d /opt/$SERVICE_NAME $SERVICE_USER
        log_info "创建用户: $SERVICE_USER"
    fi
    
    # 创建目录
    mkdir -p $DEPLOY_DIR $LOG_DIR $BACKUP_DIR
    chown -R $SERVICE_USER:$SERVICE_USER $DEPLOY_DIR $LOG_DIR
    chmod 755 $DEPLOY_DIR
    chmod 755 $LOG_DIR
    
    log_info "目录创建完成"
}}

# 安装依赖
install_dependencies() {{
    log_info "安装系统依赖..."
    
    # 更新系统
    apt-get update
    apt-get upgrade -y
    
    # 安装基础软件
    apt-get install -y \\
        nginx \\
        supervisor \\
        python3 \\
        python3-pip \\
        git \\
        curl \\
        wget
    
    log_info "依赖安装完成"
}}

# 部署应用
deploy_application() {{
    log_info "部署应用..."
    
    # 备份现有部署
    if [ -d "$DEPLOY_DIR/current" ]; then
        backup_name="$SERVICE_NAME-$(date +%Y%m%d_%H%M%S)"
        cp -r $DEPLOY_DIR/current $BACKUP_DIR/$backup_name
        log_info "备份完成: $backup_name"
    fi
    
    # 创建应用目录
    mkdir -p $DEPLOY_DIR/releases/$(date +%Y%m%d_%H%M%S)
    ln -sfn $DEPLOY_DIR/releases/$(date +%Y%m%d_%H%M%S) $DEPLOY_DIR/current
    
    # 创建示例应用
    cat > $DEPLOY_DIR/current/app.py << 'EOF'
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {{
            'message': 'Hello from {service_name}!',
            'timestamp': time.time(),
            'status': 'running'
        }}
        
        self.wfile.write(json.dumps(response).encode())

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', {SERVICE_PORT}))
    print(f'Server running on port {{server.server_port}}')
    server.serve_forever()
EOF
    
    # 创建requirements.txt
    cat > $DEPLOY_DIR/current/requirements.txt << 'EOF'
flask>=2.0.0
gunicorn>=20.0.0
EOF
    
    # 安装Python依赖
    cd $DEPLOY_DIR/current
    pip3 install -r requirements.txt
    
    # 设置权限
    chown -R $SERVICE_USER:$SERVICE_USER $DEPLOY_DIR/current
    
    log_info "应用部署完成"
}}

# 配置nginx
configure_nginx() {{
    log_info "配置Nginx..."
    
    cat > /etc/nginx/sites-available/$SERVICE_NAME << EOF
server {{
    listen 80;
    server_name _;
    
    location / {{
        proxy_pass http://127.0.0.1:$SERVICE_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }}
}}
EOF
    
    ln -sf /etc/nginx/sites-available/$SERVICE_NAME /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default
    
    nginx -t
    systemctl restart nginx
    
    log_info "Nginx配置完成"
}}

# 配置supervisor
configure_supervisor() {{
    log_info "配置Supervisor..."
    
    cat > /etc/supervisor/conf.d/$SERVICE_NAME.conf << EOF
[program:$SERVICE_NAME]
command=/usr/bin/python3 $DEPLOY_DIR/current/app.py
directory=$DEPLOY_DIR/current
user=$SERVICE_USER
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=$LOG_DIR/$SERVICE_NAME.log
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=10
environment=PYTHONPATH=$DEPLOY_DIR/current
EOF
    
    supervisorctl reread
    supervisorctl update
    supervisorctl start $SERVICE_NAME
    
    log_info "Supervisor配置完成"
}}

# 健康检查
health_check() {{
    log_info "执行健康检查..."
    
    # 检查服务状态
    if supervisorctl status $SERVICE_NAME | grep -q "RUNNING"; then
        log_info "服务运行正常"
    else
        log_error "服务未运行"
        return 1
    fi
    
    # 检查端口
    if netstat -tlnp | grep -q ":$SERVICE_PORT"; then
        log_info "端口监听正常"
    else
        log_error "端口未监听"
        return 1
    fi
    
    # 检查HTTP响应
    if curl -s http://localhost:$SERVICE_PORT | grep -q "Hello"; then
        log_info "HTTP响应正常"
    else
        log_error "HTTP响应异常"
        return 1
    fi
    
    log_info "健康检查通过"
}}

# 主函数
main() {{
    log_info "开始部署 $SERVICE_NAME..."
    
    check_permissions
    setup_environment
    install_dependencies
    deploy_application
    configure_nginx
    configure_supervisor
    health_check
    
    log_info "部署完成！"
    log_info "服务访问地址: http://localhost:$SERVICE_PORT"
    log_info "日志文件: $LOG_DIR/$SERVICE_NAME.log"
}}

# 执行主函数
main "$@"
""", "shell", f"deploy_{service_name}.sh"
                ),
                f"README.md": self.code_generator.generate_markdown_documentation(
                    f"{service_name} - Web服务部署",
                    "这是一个完整的Web服务自动化部署方案。",
                    [
                        {
                            "title": "运行部署脚本",
                            "description": "执行自动化部署",
                            "language": "bash",
                            "code": f"chmod +x deploy_{service_name}.sh\nsudo ./deploy_{service_name}.sh"
                        },
                        {
                            "title": "检查服务状态",
                            "description": "验证服务运行状态",
                            "language": "bash",
                            "code": f"supervisorctl status {service_name}\ncurl http://localhost:8080"
                        }
                    ]
                )
            },
            "docker": {
                f"docker-compose.yml": f"""version: '3.8'

services:
  {service_name}:
    build: .
    ports:
      - "8080:8080"
    environment:
      - NODE_ENV=production
      - PORT=8080
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - {service_name}
    restart: unless-stopped

volumes:
  logs:
    driver: local
""",
                f"Dockerfile": f"""FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# 复制应用代码
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 创建非root用户
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8080/health || exit 1

# 启动应用
CMD ["python", "app.py"]
""",
                f"deploy_docker.sh": self.code_generator.generate_executable_script(
                    f"""#!/bin/bash
# {service_name} Docker部署脚本

set -e

# 配置变量
SERVICE_NAME="{service_name}"
IMAGE_NAME="$SERVICE_NAME:latest"
CONTAINER_NAME="$SERVICE_NAME"

# 颜色定义
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m'

log_info() {{
    echo -e "${{GREEN}}[INFO]${{NC}} $1"
}}

log_warn() {{
    echo -e "${{YELLOW}}[WARN]${{NC}} $1"
}}

log_error() {{
    echo -e "${{RED}}[ERROR]${{NC}} $1"
}}

# 构建镜像
build_image() {{
    log_info "构建Docker镜像..."
    docker build -t $IMAGE_NAME .
    log_info "镜像构建完成: $IMAGE_NAME"
}}

# 停止并删除旧容器
stop_container() {{
    if docker ps -a --format 'table {{{{.Names}}}}' | grep -q "^$CONTAINER_NAME$"; then
        log_info "停止旧容器..."
        docker stop $CONTAINER_NAME
        docker rm $CONTAINER_NAME
    fi
}}

# 启动新容器
start_container() {{
    log_info "启动新容器..."
    docker run -d \\
        --name $CONTAINER_NAME \\
        --restart unless-stopped \\
        -p 8080:8080 \\
        -v $(pwd)/logs:/app/logs \\
        $IMAGE_NAME
    
    log_info "容器启动完成"
}}

# 检查容器状态
check_container() {{
    log_info "检查容器状态..."
    
    if docker ps | grep -q "$CONTAINER_NAME"; then
        log_info "容器运行正常"
        
        # 健康检查
        if docker exec $CONTAINER_NAME curl -f http://localhost:8080/health > /dev/null 2>&1; then
            log_info "健康检查通过"
        else
            log_warn "健康检查失败"
        fi
    else
        log_error "容器未运行"
        return 1
    fi
}}

# 清理旧镜像
cleanup_images() {{
    log_info "清理旧镜像..."
    docker image prune -f
    log_info "清理完成"
}}

# 主函数
main() {{
    log_info "开始Docker部署 $SERVICE_NAME..."
    
    build_image
    stop_container
    start_container
    check_container
    cleanup_images
    
    log_info "部署完成！"
    log_info "服务访问地址: http://localhost:8080"
    log_info "查看日志: docker logs -f $CONTAINER_NAME"
}}

main "$@"
""", "shell", "deploy_docker.sh"
                )
            }
        }
        
        return deployment_templates.get(service_type, {})
    
    def validate_shell_script(self, script: str) -> tuple:
        """
        验证Shell脚本
        
        Args:
            script: Shell脚本内容
            
        Returns:
            (是否有效, 错误信息)
        """
        return self.code_generator.validate_code(script, "shell")
    
    def generate_operations_documentation(self, scripts: Dict[str, str], title: str) -> str:
        """
        生成运维文档
        
        Args:
            scripts: 脚本文件字典
            title: 文档标题
            
        Returns:
            Markdown文档
        """
        code_examples = []
        for filename, content in scripts.items():
            if filename.endswith('.sh'):
                code_examples.append({
                    "title": filename.replace('.sh', ''),
                    "description": "部署脚本",
                    "language": "bash",
                    "code": content
                })
        
        return self.code_generator.generate_markdown_documentation(
            title,
            "这是一个完整的运维自动化部署方案，包含了环境配置、依赖安装、应用部署和监控等所有必要步骤。",
            code_examples
        )