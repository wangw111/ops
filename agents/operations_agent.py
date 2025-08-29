"""
Operations expert agent for DevOps and system administration.
"""

from agents.openai_agent import OpenAIAgent


class OperationsAgent(OpenAIAgent):
    """运维专家Agent - 专门处理服务器运维、容器化、CI/CD等任务"""
    
    def __init__(self):
        """初始化运维专家Agent"""
        super().__init__("operations")
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