"""
Ansible expert agent for automation and configuration management.
"""

from typing import Dict, Any, List
from agents.openai_agent import OpenAIAgent
from utils.code_generator import CodeGenerator


class AnsibleAgent(OpenAIAgent):
    """Ansible专家Agent - 专门处理自动化配置管理和部署任务"""
    
    def __init__(self):
        """初始化Ansible专家Agent"""
        super().__init__("ansible")
        self.code_generator = CodeGenerator(self.logger)
        self.logger.info("Ansible专家Agent已初始化")
    
    def get_system_prompt(self) -> str:
        """获取Ansible专家的系统提示词"""
        return """你是一个专业的Ansible专家，具有以下专长：

1. Ansible基础架构和概念
   - Ansible架构和工作原理
   - Inventory文件配置和管理
   - Playbook编写和调试
   - Role设计和最佳实践
   - 变量管理和模板系统

2. 系统配置自动化
   - 服务器初始化配置
   - 软件包管理自动化
   - 用户和权限管理
   - 网络配置自动化
   - 安全配置加固

3. 应用部署自动化
   - Web应用部署（Nginx, Apache）
   - 数据库部署和配置
   - 中间件部署（Tomcat, JBoss）
   - 微服务部署
   - 容器化应用部署

4. 云平台集成
   - AWS EC2实例管理
   - Azure虚拟机管理
   - 阿里云服务器管理
   - 云平台服务配置
   - 多云环境管理

5. 监控和日志自动化
   - 监控Agent部署
   - 日志收集配置
   - 告警规则部署
   - 性能监控配置
   - 可观测性系统搭建

6. DevOps工具链集成
   - CI/CD流水线集成
   - 版本控制集成
   - 配置管理集成
   - 监控系统集成
   - 自动化测试集成

请提供专业、准确、实用的Ansible自动化方案。你的回答应该：
- 提供完整的、可执行的Ansible代码
- 遵循Ansible最佳实践和安全规范
- 包含详细的注释和使用说明
- 考虑不同环境的兼容性
- 提供完整的测试和验证步骤
- 包含错误处理和回滚方案

如果需要，可以提供完整的Playbook、Role、Inventory文件和执行脚本。"""
    
    def generate_ansible_playbook(self, task_type: str, target_os: str = "centos") -> str:
        """
        生成Ansible Playbook模板
        
        Args:
            task_type: 任务类型
            target_os: 目标操作系统
            
        Returns:
            Ansible Playbook代码
        """
        playbooks = {
            "web_server": f"""---
# Web服务器部署Playbook - {target_os}
- name: 部署Web服务器
  hosts: webservers
  become: yes
  vars:
    http_port: 80
    https_port: 443
    doc_root: /var/www/html
    server_name: example.com
    
  tasks:
    - name: 安装Web服务器
      package:
        name: "{{{{ 'httpd' if target_os == 'centos' else 'apache2' }}}}"
        state: present
      when: target_os in ['centos', 'ubuntu']
    
    - name: 启动并启用Web服务器
      service:
        name: "{{{{ 'httpd' if target_os == 'centos' else 'apache2' }}}}"
        state: started
        enabled: yes
    
    - name: 创建网站根目录
      file:
        path: "{{{{ doc_root }}}}"
        state: directory
        mode: '0755'
    
    - name: 创建默认页面
      copy:
        content: |
          <html>
          <head><title>欢迎来到 {{{{ server_name }}}}</title></head>
          <body><h1>服务器部署成功！</h1></body>
          </html>
        dest: "{{{{ doc_root }}}}/index.html"
    
    - name: 配置防火墙
      firewalld:
        port: "{{{{ http_port }}}}/tcp"
        permanent: yes
        state: enabled
      when: target_os == 'centos'
    
    - name: 重启防火墙
      service:
        name: firewalld
        state: restarted
      when: target_os == 'centos'
  
  handlers:
    - name: 重启Web服务器
      service:
        name: "{{{{ 'httpd' if target_os == 'centos' else 'apache2' }}}}"
        state: restarted""",
            
            "database_server": f"""---
# 数据库服务器部署Playbook - {target_os}
- name: 部署MySQL数据库服务器
  hosts: databases
  become: yes
  vars:
    mysql_root_password: "your_secure_password"
    mysql_database: "webapp_db"
    mysql_user: "webapp_user"
    mysql_user_password: "user_password"
    
  tasks:
    - name: 安装MySQL服务器
      package:
        name: "{{{{ 'mariadb-server' if target_os == 'centos' else 'mysql-server' }}}}"
        state: present
    
    - name: 启动MySQL服务
      service:
        name: "{{{{ 'mariadb' if target_os == 'centos' else 'mysql' }}}}"
        state: started
        enabled: yes
    
    - name: 安装MySQL客户端
      package:
        name: "{{{{ 'mariadb' if target_os == 'centos' else 'mysql-client' }}}}"
        state: present
    
    - name: 设置MySQL root密码
      mysql_user:
        name: root
        password: "{{{{ mysql_root_password }}}}"
        host: localhost
        check_implicit_admin: yes
    
    - name: 创建应用数据库
      mysql_db:
        name: "{{{{ mysql_database }}}}"
        state: present
    
    - name: 创建数据库用户
      mysql_user:
        name: "{{{{ mysql_user }}}}"
        password: "{{{{ mysql_user_password }}}}"
        priv: "{{{{ mysql_database }}}}.*:ALL"
        host: "%"
        state: present
    
    - name: 配置MySQL远程访问
      copy:
        content: |
          [mysqld]
          bind-address = 0.0.0.0
        dest: /etc/my.cnf.d/bind-address.cnf
      notify: 重启MySQL服务
  
  handlers:
    - name: 重启MySQL服务
      service:
        name: "{{{{ 'mariadb' if target_os == 'centos' else 'mysql' }}}}"
        state: restarted""",
            
            "docker_install": f"""---
# Docker安装Playbook - {target_os}
- name: 安装Docker
  hosts: all
  become: yes
  vars:
    docker_users:
      - "{{{{ ansible_user }}}}"
    
  tasks:
    - name: 安装必要的包
      package:
        name:
          - yum-utils
          - device-mapper-persistent-data
          - lvm2
        state: present
      when: target_os == 'centos'
    
    - name: 添加Docker仓库
      yum_repository:
        name: docker-ce-stable
        description: Docker CE Stable
        baseurl: https://download.docker.com/linux/centos/7/x86_64/stable/
        enabled: yes
        gpgcheck: yes
        gpgkey: https://download.docker.com/linux/centos/gpg
      when: target_os == 'centos'
    
    - name: 安装Docker
      package:
        name: docker-ce
        state: present
      when: target_os == 'centos'
    
    - name: 启动Docker服务
      service:
        name: docker
        state: started
        enabled: yes
    
    - name: 添加用户到docker组
      user:
        name: "{{{{ item }}}}"
        groups: docker
        append: yes
      loop: "{{{{ docker_users }}}}"
    
    - name: 安装Docker Compose
      get_url:
        url: https://github.com/docker/compose/releases/download/1.29.2/docker-compose-Linux-x86_64
        dest: /usr/local/bin/docker-compose
        mode: '0755'
    
    - name: 验证Docker安装
      command: docker --version
      register: docker_version
      changed_when: false
    
    - name: 显示Docker版本
      debug:
        msg: "Docker版本: {{{{ docker_version.stdout }}}}" """
        }
        
        return playbooks.get(task_type, "请指定有效的任务类型")
    
    def generate_ansible_role(self, role_name: str, role_type: str = "generic") -> str:
        """
        生成Ansible Role结构
        
        Args:
            role_name: Role名称
            role_type: Role类型
            
        Returns:
            Role结构和示例代码
        """
        return f"""# Ansible Role: {role_name}
# 角色: {role_type}

## 目录结构
```
{role_name}/
├── defaults/
│   └── main.yml          # 默认变量
├── files/                # 静态文件
├── handlers/
│   └── main.yml          # 处理器
├── meta/
│   └── main.yml          # 角色依赖
├── tasks/
│   └── main.yml          # 任务列表
├── templates/            # 模板文件
├── tests/
│   ├── inventory
│   └── test.yml          # 测试文件
└── vars/
    └── main.yml          # 变量定义
```

## defaults/main.yml
```yaml
---
# {role_name} 默认变量
{role_name}_version: "1.0.0"
{role_name}_config_file: "/etc/{role_name}/config.conf"
{role_name}_service_name: "{role_name}"
{role_name}_port: 8080
```

## tasks/main.yml
```yaml
---
# {role_name} 主要任务
- name: 包含变量文件
  include_vars: "../vars/main.yml"

- name: 安装{role_name}包
  package:
    name: "{{{role_name}_package_name}}"
    state: present

- name: 创建配置目录
  file:
    path: "/etc/{role_name}"
    state: directory
    mode: '0755'

- name: 部署配置文件
  template:
    src: config.conf.j2
    dest: "{{{{ {role_name}_config_file }}}}"
    mode: '0644'
  notify: 重启{role_name}服务

- name: 启动{role_name}服务
  service:
    name: "{{{{ {role_name}_service_name }}}}"
    state: started
    enabled: yes
```

## handlers/main.yml
```yaml
---
# {role_name} 处理器
- name: 重启{role_name}服务
  service:
    name: "{{{{ {role_name}_service_name }}}}"
    state: restarted
```

## templates/config.conf.j2
```ini
# {role_name} 配置文件
# 自动生成，请勿手动修改

[general]
version = {{{{ {role_name}_version }}}}
port = {{{{ {role_name}_port }}}}

[logging]
level = INFO
file = /var/log/{role_name}/{role_name}.log
```

## vars/main.yml
```yaml
---
# {role_name} 变量定义
{role_name}_package_name: "{role_name}"
{role_name}_user: "{role_name}"
{role_name}_group: "{role_name}"
```

## meta/main.yml
```yaml
---
galaxy_info:
  author: Your Name
  description: {role_name} role for {role_type}
  company: Your Company
  license: MIT
  min_ansible_version: 2.9
  platforms:
    - name: EL
      versions:
        - 7
        - 8
    - name: Ubuntu
      versions:
        - 18.04
        - 20.04
  galaxy_tags:
    - {role_type}
    - {role_name}
dependencies: []
```

## 使用方法
```yaml
- name: 使用{role_name}角色
  hosts: all
  become: yes
  roles:
    - {role_name}
```"""
    
    def generate_inventory_file(self, environment: str = "production") -> str:
        """
        生成Inventory文件
        
        Args:
            environment: 环境类型
            
        Returns:
            Inventory文件内容
        """
        return f"""# Ansible Inventory文件 - {environment}环境

# Web服务器组
[webservers]
web01.example.com ansible_user=ubuntu ansible_port=22
web02.example.com ansible_user=ubuntu ansible_port=22

# 数据库服务器组
[databases]
db01.example.com ansible_user=centos ansible_port=22
db02.example.com ansible_user=centos ansible_port=22

# 应用服务器组
[appservers]
app01.example.com ansible_user=ubuntu ansible_port=22
app02.example.com ansible_user=ubuntu ansible_port=22

# 监控服务器组
[monitoring]
mon01.example.com ansible_user=centos ansible_port=22

# 负载均衡器组
[loadbalancers]
lb01.example.com ansible_user=ubuntu ansible_port=22

# 组合组
[webservers:vars]
ansible_python_interpreter=/usr/bin/python3
nginx_version=1.18.0

[databases:vars]
ansible_python_interpreter=/usr/bin/python3
mysql_version=8.0

[appservers:vars]
ansible_python_interpreter=/usr/bin/python3
java_version=11

# 环境变量
[{environment}:children]
webservers
databases
appservers
monitoring
loadbalancers

[{environment}:vars]
env={environment}
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
"""
    
    def get_ansible_best_practices(self) -> str:
        """获取Ansible最佳实践"""
        return """Ansible最佳实践指南：

## 1. Playbook编写规范
- 使用YAML格式，遵循2空格缩进
- 为每个Playbook添加描述性注释
- 使用有意义的name字段
- 将相关的任务组织在一起
- 使用handlers进行服务重启

## 2. 变量管理
- 使用变量文件管理配置
- 遵循变量命名规范
- 使用默认变量覆盖机制
- 避免在Playbook中硬编码值
- 使用vault加密敏感信息

## 3. Role设计
- 单一职责原则
- 模块化设计
- 可重用性
- 版本控制
- 文档完整

## 4. 错误处理
- 使用failed_when控制失败条件
- 使用ignore_errors忽略预期错误
- 添加适当的错误检查
- 实现回滚机制

## 5. 性能优化
- 使用async进行长时间运行任务
合理使用fact缓存
- 优化SSH连接
- 减少不必要的任务

## 6. 安全性
- 使用become进行权限提升
- 限制敏感信息访问
- 使用SSH密钥认证
- 定期更新依赖包

## 7. 测试策略
- 使用Molecule进行测试
- 实现持续集成
- 进行语法检查
- 执行dry-run测试

## 8. 文档规范
- 为每个Role添加README
- 记录变量和参数
- 提供使用示例
- 维护变更日志"""
    
    def troubleshoot_common_issues(self, issue_type: str) -> str:
        """
        提供Ansible常见问题排查指南
        
        Args:
            issue_type: 问题类型
            
        Returns:
            排查指南
        """
        troubleshooting = {
            "connection_failed": """Ansible连接失败排查：

1. 检查SSH连接
   ```bash
   ssh -i /path/to/key user@hostname
   ```

2. 验证Inventory配置
   - 确认主机名正确
   - 检查端口设置
   - 验证用户名和密码

3. 检查SSH密钥
   - 确保密钥文件存在
   - 验证密钥权限
   - 检查known_hosts文件

4. 网络连通性
   ```bash
   ping hostname
   telnet hostname 22
   ```

5. 防火墙设置
   - 检查本地防火墙
   - 验证目标主机防火墙
   - 确认SSH端口开放

6. 权限问题
   - 检查用户权限
   - 验证sudo配置
   - 确认become权限""",
            
            "module_not_found": """模块未找到问题排查：

1. 检查模块名称
   - 确认模块拼写正确
   - 查看模块文档
   - 验证模块版本兼容性

2. 安装缺失的模块
   ```bash
   pip install module_name
   ansible-galaxy collection install collection_name
   ```

3. 检查Python环境
   ```bash
   python --version
   pip list
   ```

4. 验证Ansible版本
   ```bash
   ansible --version
   ```

5. 检查模块路径
   ```bash
   python -c "import module_name"
   ```""",
            
            "permission_denied": """权限拒绝问题排查：

1. 检查文件权限
   ```bash
   ls -la /path/to/file
   ```

2. 验证用户权限
   ```bash
   whoami
   id
   ```

3. 检查sudo配置
   ```bash
   sudo -l
   ```

4. 使用become参数
   ```yaml
   - name: 任务示例
     command: /usr/bin/command
     become: yes
     become_user: root
   ```

5. 检查SELinux
   ```bash
   getenforce
   sestatus
   ```

6. 验证文件系统权限
   ```bash
   mount | grep ' / '
   df -h
   ```"""
        }
        
        return troubleshooting.get(issue_type, "请联系Ansible专家获取帮助")
    
    def validate_ansible_code(self, code: str, code_type: str = "yaml") -> tuple:
        """
        验证Ansible代码
        
        Args:
            code: Ansible代码内容
            code_type: 代码类型
            
        Returns:
            (是否有效, 错误信息)
        """
        if code_type == "yaml":
            return self.code_generator.validate_code(code, "yaml")
        elif code_type == "ini":
            # Inventory文件验证
            lines = code.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('['):
                    if '=' not in line:
                        return False, f"Inventory文件格式错误: {line}"
            return True, "Inventory文件格式正确"
        else:
            return True, "代码类型验证暂未实现"
    
    def generate_ansible_documentation(self, configs: Dict[str, str], title: str) -> str:
        """
        生成Ansible文档
        
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
                    "description": "Ansible配置文件",
                    "language": "yaml",
                    "code": content
                })
            elif filename.endswith('.ini'):
                code_examples.append({
                    "title": filename,
                    "description": "Ansible Inventory文件",
                    "language": "ini",
                    "code": content
                })
        
        return self.code_generator.generate_markdown_documentation(
            title,
            "这是一个完整的Ansible自动化部署方案，包含了Playbook、Role、Inventory等所有必要组件。",
            code_examples
        )
    
    def generate_ansible_project_structure(self, project_name: str, project_type: str = "web") -> Dict[str, str]:
        """
        生成Ansible项目结构
        
        Args:
            project_name: 项目名称
            project_type: 项目类型
            
        Returns:
            项目文件结构字典
        """
        project_structures = {
            "web": {
                f"{project_name}/": None,
                f"{project_name}/site.yml": f"""---
# Ansible主站点文件 - {project_name}
- name: 部署{project_name}应用
  hosts: webservers
  become: yes
  vars:
    app_name: {project_name}
    app_version: "1.0.0"
    app_port: 8080
  
  roles:
    - common
    - nginx
    - app
    - monitoring""",
                f"{project_name}/inventory": f"""# 主机清单文件 - {project_name}

[webservers]
web01.example.com ansible_user=ubuntu ansible_port=22
web02.example.com ansible_user=ubuntu ansible_port=22

[databases]
db01.example.com ansible_user=centos ansible_port=22

[webservers:vars]
ansible_python_interpreter=/usr/bin/python3
app_version=1.0.0

[databases:vars]
ansible_python_interpreter=/usr/bin/python2
mysql_version=8.0""",
                f"{project_name}/group_vars/": None,
                f"{project_name}/group_vars/webservers.yml": f"""---
# Web服务器组变量
app_port: 8080
app_user: "{{{{ app_name }}}}"
app_dir: "/opt/{{{{ app_name }}}}"
nginx_config: "/etc/nginx/sites-available/{{{{ app_name }}}}"
""",
                f"{project_name}/group_vars/all.yml": f"""---
# 全局变量
ansible_python_interpreter: /usr/bin/python3
ntp_server: pool.ntp.org
timezone: Asia/Shanghai
""",
                f"{project_name}/roles/": None,
                f"{project_name}/roles/common/": None,
                f"{project_name}/roles/common/tasks/main.yml": f"""---
# 通用任务 - {project_name}
- name: 更新系统包
  apt:
    update_cache: yes
    upgrade: dist
  when: ansible_os_family == "Debian"

- name: 安装基础软件包
  package:
    name:
      - curl
      - wget
      - git
      - vim
      - htop
    state: present

- name: 设置时区
  timezone:
    name: "{{{{ timezone }}}}"

- name: 配置NTP
  template:
    src: ntp.conf.j2
    dest: /etc/ntp.conf
  notify: 重启NTP服务

- name: 创建应用用户
  user:
    name: "{{{{ app_user }}}}"
    shell: /bin/bash
    create_home: yes
    state: present""",
                f"{project_name}/roles/nginx/": None,
                f"{project_name}/roles/nginx/tasks/main.yml": f"""---
# Nginx安装和配置 - {project_name}
- name: 安装Nginx
  package:
    name: nginx
    state: present

- name: 创建Nginx配置目录
  file:
    path: /etc/nginx/sites-available
    state: directory
    mode: '0755'

- name: 部署Nginx配置
  template:
    src: nginx.conf.j2
    dest: "{{{{ nginx_config }}}}"
  notify: 重启Nginx

- name: 启用站点
  file:
    src: "{{{{ nginx_config }}}}"
    dest: "/etc/nginx/sites-enabled/{{{{ app_name }}}}"
    state: link
  notify: 重启Nginx

- name: 移除默认站点
  file:
    path: /etc/nginx/sites-enabled/default
    state: absent
  notify: 重启Nginx""",
                f"{project_name}/roles/nginx/templates/nginx.conf.j2": f"""server {{
    listen {{{{ app_port }}}};
    server_name _;
    
    root {{{{ app_dir }}}}/public;
    index index.html index.htm;
    
    location / {{
        try_files $uri $uri/ =404;
    }}
    
    location /health {{
        access_log off;
        return 200 "healthy\\n";
        add_header Content-Type text/plain;
    }}
}}""",
                f"{project_name}/roles/app/": None,
                f"{project_name}/roles/app/tasks/main.yml": f"""---
# 应用部署 - {project_name}
- name: 创建应用目录
  file:
    path: "{{{{ app_dir }}}}"
    state: directory
    owner: "{{{{ app_user }}}}"
    group: "{{{{ app_user }}}}"
    mode: '0755'

- name: 部署应用文件
  copy:
    src: app/
    dest: "{{{{ app_dir }}}}"
    owner: "{{{{ app_user }}}}"
    group: "{{{{ app_user }}}}"
    mode: '0644'

- name: 设置应用权限
  file:
    path: "{{{{ app_dir }}}}"
    owner: "{{{{ app_user }}}}"
    group: "{{{{ app_user }}}}"
    recurse: yes

- name: 创建日志目录
  file:
    path: "/var/log/{{{{ app_name }}}}"
    state: directory
    owner: "{{{{ app_user }}}}"
    group: "{{{{ app_user }}}}"
    mode: '0755'""",
                f"{project_name}/roles/monitoring/": None,
                f"{project_name}/roles/monitoring/tasks/main.yml": f"""---
# 监控配置 - {project_name}
- name: 安装监控Agent
  package:
    name:
      - prometheus-node-exporter
      - telegraf
    state: present

- name: 启动监控服务
  service:
    name: "{{{{ item }}}}"
    state: started
    enabled: yes
  loop:
    - prometheus-node-exporter
    - telegraf""",
                f"{project_name}/README.md": self.code_generator.generate_markdown_documentation(
                    f"{project_name} - Ansible自动化部署项目",
                    "这是一个完整的Ansible自动化部署项目，包含了Web应用部署、监控配置等所有必要组件。",
                    [
                        {
                            "title": "部署应用",
                            "description": "使用Ansible部署Web应用",
                            "language": "bash",
                            "code": f"cd {project_name}\nansible-playbook -i inventory site.yml"
                        },
                        {
                            "title": "检查语法",
                            "description": "验证Ansible Playbook语法",
                            "language": "bash",
                            "code": f"cd {project_name}\nansible-playbook -i inventory --syntax-check site.yml"
                        }
                    ]
                )
            }
        }
        
        return project_structures.get(project_type, {})