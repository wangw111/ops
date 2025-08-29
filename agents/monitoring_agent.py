"""
Monitoring expert agent for system monitoring and performance analysis.
"""

from typing import Dict, Any, List
from agents.multi_ai_agent import MultiAIAgent
from utils.code_generator import CodeGenerator


class MonitoringAgent(MultiAIAgent):
    """监控专家Agent - 专门处理系统监控、性能分析和告警配置"""
    
    def __init__(self, provider: str = "openai"):
        """
        初始化监控专家Agent
        
        Args:
            provider: AI提供商 (openai, claude, qwen)
        """
        super().__init__("monitoring", provider)
        self.code_generator = CodeGenerator(self.logger)
        self.logger.info("监控专家Agent已初始化")
    
    def get_system_prompt(self) -> str:
        """获取监控专家的系统提示词"""
        return """你是一个专业的监控专家，具有以下专长：

1. 系统监控架构设计
   - 监控系统整体架构规划
   - 数据采集和存储策略
   - 监控指标定义和分类
   - 监控系统可扩展性设计
   - 多环境监控方案

2. 指标收集和存储
   - Prometheus配置和使用
   - Grafana仪表板设计
   - 时序数据库优化
   - 指标采集代理部署
   - 数据持久化和备份

3. 日志管理和分析
   - 日志收集架构设计
   - ELK Stack配置
   - 日志格式标准化
   - 日志查询和分析
   - 日志告警和可视化

4. 告警规则配置
   - 告警策略设计
   - 告警规则编写
   - 告警通知渠道配置
   - 告警降噪和聚合
   - 告警升级机制

5. 性能瓶颈分析
   - 应用性能监控（APM）
   - 数据库性能分析
   - 网络性能监控
   - 系统资源分析
   - 性能基准测试

6. 监控系统集成
   - 第三方系统集成
   - API监控和测试
   - 业务监控指标
   - 用户体验监控
   - 监控自动化运维

请提供全面、实用的监控方案和优化建议。你的回答应该：
- 基于业界最佳实践和标准
- 提供具体的配置示例和实现方案
- 考虑系统的可扩展性和可维护性
- 包含必要的监控指标和阈值设置
- 提供故障排查和优化建议
- 考虑成本效益和资源投入

如果需要，可以提供配置文件、脚本代码和架构图。"""
    
    def get_monitoring_stack_recommendation(self, system_type: str) -> str:
        """
        获取监控系统栈推荐
        
        Args:
            system_type: 系统类型
            
        Returns:
            监控系统栈推荐
        """
        stacks = {
            "microservices": """微服务监控栈推荐：

1. 指标收集
   - Prometheus + Node Exporter
   - 应用集成Prometheus Client
   - Service Mesh监控（Istio）

2. 日志管理
   - ELK Stack（Elasticsearch + Logstash + Kibana）
   - Fluentd作为日志收集器
   - 结构化日志格式

3. 追踪系统
   - Jaeger分布式追踪
   - OpenTelemetry集成
   - 链路分析仪表板

4. 告警系统
   - Alertmanager告警管理
   - 多渠道通知（邮件、短信、钉钉）
   - 告警聚合和降噪

5. 可视化
   - Grafana仪表板
   - 自定义监控面板
   - 业务指标展示""",
            "web_application": """Web应用监控栈推荐：

1. 前端监控
   - 页面性能监控
   - JavaScript错误收集
   - 用户体验分析
   - Real User Monitoring (RUM)

2. 后端监控
   - APM工具集成
   - 数据库性能监控
   - API响应时间监控
   - 错误率统计

3. 基础设施监控
   - 服务器资源使用率
   - 网络连接状态
   - 负载均衡器监控
   - CDN性能监控

4. 业务监控
   - 用户行为分析
   - 转化率统计
   - 业务流程监控
   - 收入指标监控""",
            "kubernetes": """Kubernetes监控栈推荐：

1. 集群监控
   - Kubernetes Metrics Server
   - Prometheus Operator
   - Grafana Operator
   - Kubernetes Events监控

2. 应用监控
   - Pod资源使用监控
   - Service健康检查
   - Ingress流量监控
   - ConfigMap/Secret监控

3. 日志收集
   - Fluentd/Fluent Bit
   - EFK Stack（Elasticsearch + Fluentd + Kibana）
   - Loki日志系统
   - 多租户日志隔离

4. 告警配置
   - Pod OOMKilled告警
   - 节点NotReady告警
   - PVC空间不足告警
   - 服务不可用告警"""
        }
        
        return stacks.get(system_type, "请联系监控专家定制监控方案")
    
    def generate_prometheus_config(self, service_name: str) -> str:
        """
        生成Prometheus配置示例
        
        Args:
            service_name: 服务名称
            
        Returns:
            Prometheus配置示例
        """
        return f"""# Prometheus配置示例 - {service_name}监控

global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  # {service_name}服务监控
  - job_name: '{service_name}'
    static_configs:
      - targets: ['{service_name}:8080']
    metrics_path: '/metrics'
    scrape_interval: 10s
    scrape_timeout: 5s
    
  # Node Exporter监控
  - job_name: 'node_exporter'
    static_configs:
      - targets: ['node-exporter:9100']
    
  # Docker监控
  - job_name: 'docker'
    static_configs:
      - targets: ['cadvisor:8080']

# 告警规则示例
alert_rules.yml:
  groups:
    - name: {service_name}_alerts
      rules:
        - alert: HighErrorRate
          expr: rate(http_requests_total{{status=~"5..", service="{service_name}"}}[5m]) > 0.1
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "High error rate detected for {service_name}"
            description: "Error rate is {{ $value }} errors per second"
        
        - alert: HighResponseTime
          expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{{service="{service_name}"}}[5m])) > 1
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "High response time for {service_name}"
            description: "95th percentile response time is {{ $value }} seconds"
        
        - alert: ServiceDown
          expr: up{{service="{service_name}"}} == 0
          for: 1m
          labels:
            severity: critical
          annotations:
            summary: "Service {service_name} is down"
            description: "Service {service_name} has been down for more than 1 minute" """
    
    def generate_grafana_dashboard(self, dashboard_type: str) -> str:
        """
        生成Grafana仪表板配置
        
        Args:
            dashboard_type: 仪表板类型
            
        Returns:
            Grafana仪表板配置
        """
        if dashboard_type == "web_service":
            return """{
  "dashboard": {
    "id": null,
    "title": "Web Service Dashboard",
    "tags": ["web", "service"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "HTTP Requests Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{status}}"
          }
        ],
        "yaxes": [{"format": "short"}]
      },
      {
        "id": 2,
        "title": "Response Time (95th percentile)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "{{endpoint}}"
          }
        ],
        "yaxes": [{"format": "s"}]
      },
      {
        "id": 3,
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m]) / rate(http_requests_total[5m])",
            "legendFormat": "Error Rate"
          }
        ],
        "yaxes": [{"format": "percentunit"}]
      }
    ],
    "time": {
      "from": "now-1h",
      "to": "now"
    }
  }
}"""
        
        return "请指定具体的仪表板类型"
    
    def get_monitoring_best_practices(self) -> str:
        """获取监控最佳实践"""
        return """监控最佳实践：

1. 监控指标设计
   - 关注业务指标而非技术指标
   - 建立分层监控体系
   - 定义明确的SLA/SLO
   - 保持指标的原子性和不可变性

2. 告警策略
   - 设置合理的告警阈值
   - 实现告警聚合和降噪
   - 建立告警升级机制
   - 定期审查告警规则

3. 数据存储
   - 选择合适的存储策略
   - 实现数据分层存储
   - 定期清理过期数据
   - 建立数据备份机制

4. 可视化设计
   - 设计直观的仪表板
   - 使用合适的图表类型
   - 保持界面简洁清晰
   - 支持下钻分析

5. 性能优化
   - 监控系统自身性能
   - 优化数据采集频率
   - 使用合理的采样率
   - 实现水平扩展"""
    
    def generate_monitoring_stack(self, service_name: str, stack_type: str = "prometheus") -> Dict[str, str]:
        """
        生成监控系统栈配置
        
        Args:
            service_name: 服务名称
            stack_type: 监控栈类型
            
        Returns:
            监控配置文件字典
        """
        monitoring_templates = {
            "prometheus": {
                f"prometheus.yml": f"""global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  # {service_name}服务监控
  - job_name: '{service_name}'
    static_configs:
      - targets: ['{service_name}:8080']
    metrics_path: '/metrics'
    scrape_interval: 10s
    
  # Node Exporter监控
  - job_name: 'node_exporter'
    static_configs:
      - targets: ['node-exporter:9100']
    
  # Docker监控
  - job_name: 'docker'
    static_configs:
      - targets: ['cadvisor:8080']
""",
                f"alert_rules.yml": f"""groups:
  - name: {service_name}_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{{status=~"5..", service="{service_name}"}}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected for {service_name}"
          description: "Error rate is {{ $value }} errors per second"
      
      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{{service="{service_name}"}}[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High response time for {service_name}"
          description: "95th percentile response time is {{ $value }} seconds"
      
      - alert: ServiceDown
        expr: up{{service="{service_name}"}} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {service_name} is down"
          description: "Service {service_name} has been down for more than 1 minute"
""",
                f"grafana-dashboard.json": f"""{{
  "dashboard": {{
    "id": null,
    "title": "{service_name} Dashboard",
    "tags": ["{service_name}", "monitoring"],
    "timezone": "browser",
    "panels": [
      {{
        "id": 1,
        "title": "HTTP Requests Rate",
        "type": "graph",
        "targets": [
          {{
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{status}}"
          }}
        ],
        "yaxes": [{{"format": "short"}}]
      }},
      {{
        "id": 2,
        "title": "Response Time (95th percentile)",
        "type": "graph",
        "targets": [
          {{
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "{{endpoint}}"
          }}
        ],
        "yaxes": [{{"format": "s"}}]
      }},
      {{
        "id": 3,
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {{
            "expr": "rate(http_requests_total{{status=~\"5..\"}}[5m]) / rate(http_requests_total[5m])",
            "legendFormat": "Error Rate"
          }}
        ],
        "yaxes": [{{"format": "percentunit"}}]
      }}
    ],
    "time": {{
      "from": "now-1h",
      "to": "now"
    }}
  }}
}}""",
                f"docker-compose.yml": f"""version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./alert_rules.yml:/etc/prometheus/alert_rules.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana-dashboard.json:/etc/grafana/provisioning/dashboards/dashboard.json
    restart: unless-stopped

  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
      - alertmanager_data:/alertmanager
    restart: unless-stopped

  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.rootfs=/rootfs'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    restart: unless-stopped

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
    restart: unless-stopped

volumes:
  prometheus_data:
  grafana_data:
  alertmanager_data:
""",
                f"setup_monitoring.sh": self.code_generator.generate_executable_script(
                    f"""#!/bin/bash
# {service_name} 监控系统部署脚本

set -e

SERVICE_NAME="{service_name}"
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

# 检查Docker
check_docker() {{
    if ! command -v docker &> /dev/null; then
        log_error "Docker未安装"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        log_error "Docker服务未运行"
        exit 1
    fi
    
    log_info "Docker环境检查通过"
}}

# 创建目录
setup_directories() {{
    log_info "创建监控目录..."
    mkdir -p monitoring_data/{{
        prometheus_data,grafana_data,alertmanager_data
    }}
    log_info "目录创建完成"
}}

# 启动监控栈
start_monitoring() {{
    log_info "启动监控栈..."
    docker-compose up -d
    log_info "监控栈启动完成"
}}

# 验证服务
verify_services() {{
    log_info "验证监控服务..."
    
    services=(
        "prometheus:9090"
        "grafana:3000"
        "alertmanager:9093"
        "node-exporter:9100"
        "cadvisor:8080"
    )
    
    for service in "${{services[@]}}"; do
        name="${{service%%:*}}"
        port="${{service##*:}}"
        
        if curl -s http://localhost:$port > /dev/null 2>&1; then
            log_info "$name 服务正常 (端口: $port)"
        else
            log_warn "$name 服务可能未启动 (端口: $port)"
        fi
    done
}}

# 显示访问信息
show_access_info() {{
    log_info "监控系统访问信息:"
    echo "  Prometheus: http://localhost:9090"
    echo "  Grafana: http://localhost:3000 (admin/admin)"
    echo "  Alertmanager: http://localhost:9093"
    echo "  Node Exporter: http://localhost:9100"
    echo "  cAdvisor: http://localhost:8080"
}}

# 主函数
main() {{
    log_info "开始部署 $SERVICE_NAME 监控系统..."
    
    check_docker
    setup_directories
    start_monitoring
    verify_services
    show_access_info
    
    log_info "监控系统部署完成！"
}}

main "$@"
""", "shell", "setup_monitoring.sh"
                ),
                f"README.md": self.code_generator.generate_markdown_documentation(
                    f"{service_name} - 监控系统",
                    "这是一个基于Prometheus + Grafana的完整监控系统。",
                    [
                        {
                            "title": "启动监控系统",
                            "description": "部署完整的监控栈",
                            "language": "bash",
                            "code": f"chmod +x setup_monitoring.sh\n./setup_monitoring.sh"
                        },
                        {
                            "title": "访问监控界面",
                            "description": "访问各个监控组件",
                            "language": "bash",
                            "code": "# Prometheus: http://localhost:9090\n# Grafana: http://localhost:3000 (admin/admin)\n# Alertmanager: http://localhost:9093"
                        }
                    ]
                )
            }
        }
        
        return monitoring_templates.get(stack_type, {})
    
    def validate_monitoring_config(self, config: str, config_type: str) -> tuple:
        """
        验证监控配置
        
        Args:
            config: 配置内容
            config_type: 配置类型
            
        Returns:
            (是否有效, 错误信息)
        """
        if config_type == "yaml":
            return self.code_generator.validate_code(config, "yaml")
        elif config_type == "json":
            try:
                import json
                json.loads(config)
                return True, "JSON格式正确"
            except Exception as e:
                return False, f"JSON格式错误: {str(e)}"
        else:
            return True, "配置类型验证暂未实现"
    
    def generate_monitoring_documentation(self, configs: Dict[str, str], title: str) -> str:
        """
        生成监控文档
        
        Args:
            configs: 配置文件字典
            title: 文档标题
            
        Returns:
            Markdown文档
        """
        code_examples = []
        for filename, content in configs.items():
            if filename.endswith('.yml') or filename.endswith('.yaml'):
                code_examples.append({
                    "title": filename,
                    "description": "监控配置文件",
                    "language": "yaml",
                    "code": content
                })
            elif filename.endswith('.sh'):
                code_examples.append({
                    "title": filename,
                    "description": "部署脚本",
                    "language": "bash",
                    "code": content
                })
        
        return self.code_generator.generate_markdown_documentation(
            title,
            "这是一个完整的监控系统部署方案，包含了数据收集、存储、可视化和告警等所有必要组件。",
            code_examples
        )