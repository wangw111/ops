"""
Code generation utilities for creating runnable code and markdown documentation.
"""

import os
import tempfile
import subprocess
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging


class CodeGenerator:
    """代码生成器基类"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """初始化代码生成器"""
        self.logger = logger or logging.getLogger(__name__)
    
    def validate_code(self, code: str, language: str) -> tuple:
        """
        验证代码是否可以运行
        
        Args:
            code: 代码内容
            language: 编程语言
            
        Returns:
            (是否有效, 错误信息)
        """
        try:
            if language == "python":
                return self._validate_python_code(code)
            elif language == "go":
                return self._validate_go_code(code)
            elif language == "yaml":
                return self._validate_yaml_code(code)
            elif language == "shell":
                return self._validate_shell_code(code)
            elif language == "markdown":
                return self._validate_markdown(code)
            else:
                return True, "Language validation not implemented"
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def _validate_python_code(self, code: str) -> tuple:
        """验证Python代码"""
        try:
            # 基本语法检查
            compile(code, '<string>', 'exec')
            
            # 创建临时文件执行
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # 尝试执行语法检查
                result = subprocess.run(
                    ['python', '-m', 'py_compile', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    return True, "Python代码语法正确"
                else:
                    return False, result.stderr
                    
            finally:
                os.unlink(temp_file)
                
        except SyntaxError as e:
            return False, f"Python语法错误: {str(e)}"
        except Exception as e:
            return False, f"Python验证错误: {str(e)}"
    
    def _validate_go_code(self, code: str) -> tuple:
        """验证Go代码"""
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.go', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # 尝试编译检查
                result = subprocess.run(
                    ['go', 'build', '-o', '/dev/null', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    return True, "Go代码编译成功"
                else:
                    return False, result.stderr
                    
            finally:
                os.unlink(temp_file)
                
        except Exception as e:
            return False, f"Go验证错误: {str(e)}"
    
    def _validate_yaml_code(self, code: str) -> tuple:
        """验证YAML代码"""
        try:
            import yaml
            yaml.safe_load(code)
            return True, "YAML格式正确"
        except ImportError:
            return True, "YAML验证需要PyYAML库"
        except Exception as e:
            return False, f"YAML格式错误: {str(e)}"
    
    def _validate_shell_code(self, code: str) -> tuple:
        """验证Shell代码"""
        try:
            # 基本语法检查
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                result = subprocess.run(
                    ['bash', '-n', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    return True, "Shell脚本语法正确"
                else:
                    return False, result.stderr
                    
            finally:
                os.unlink(temp_file)
                
        except Exception as e:
            return False, f"Shell验证错误: {str(e)}"
    
    def _validate_markdown(self, code: str) -> tuple:
        """验证Markdown文档"""
        try:
            # 基本Markdown结构检查
            required_elements = ['#', '##']  # 至少有标题
            
            if not any(elem in code for elem in required_elements):
                return False, "Markdown文档缺少标题结构"
            
            # 检查代码块格式
            lines = code.split('\n')
            in_code_block = False
            code_block_count = 0
            
            for line in lines:
                if line.strip().startswith('```'):
                    in_code_block = not in_code_block
                    if not in_code_block:
                        code_block_count += 1
            
            if code_block_count == 0:
                return True, "Markdown文档格式正确（建议添加代码块）"
            
            return True, "Markdown文档格式正确"
            
        except Exception as e:
            return False, f"Markdown验证错误: {str(e)}"
    
    def generate_executable_script(self, code: str, language: str, filename: str) -> str:
        """
        生成可执行脚本
        
        Args:
            code: 代码内容
            language: 编程语言
            filename: 文件名
            
        Returns:
            完整的脚本内容
        """
        script_template = {
            "python": f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 自动生成的Python脚本
# 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# 文件名: {filename}

{code}

if __name__ == "__main__":
    print("脚本执行开始...")
    # 在这里添加主逻辑
    print("脚本执行完成")
""",
            "shell": f"""#!/bin/bash
# -*- coding: utf-8 -*-

# 自动生成的Shell脚本
# 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# 文件名: {filename}

set -e  # 遇到错误时退出

{code}

echo "脚本执行完成"
""",
            "go": f"""// 自动生成的Go程序
// 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
// 文件名: {filename}

package main

import (
	"fmt"
)

{code}

func main() {{
	fmt.Println("程序执行开始...")
	// 在这里添加主逻辑
	fmt.Println("程序执行完成")
}}
"""
        }
        
        return script_template.get(language, code)
    
    def generate_markdown_documentation(self, 
                                       title: str, 
                                       content: str, 
                                       code_examples: List[Dict[str, str]] = None,
                                       language: str = "zh") -> str:
        """
        生成Markdown文档
        
        Args:
            title: 文档标题
            content: 文档内容
            code_examples: 代码示例列表
            language: 文档语言
            
        Returns:
            Markdown文档内容
        """
        doc_template = f"""# {title}

> **说明**: 本文档由开发助手Agent自动生成  
> **生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 概述

{content}

"""

        if code_examples:
            doc_template += "## 代码示例\n\n"
            
            for i, example in enumerate(code_examples, 1):
                doc_template += f"""### 示例 {i}: {example.get('title', '未命名示例')}

{example.get('description', '无描述')}

```{example.get('language', 'text')}
{example.get('code', '')}
```

"""

        doc_template += f"""## 使用说明

### 前置条件

- 确保环境依赖已安装
- 检查配置文件是否正确
- 确保有必要的权限

### 执行步骤

1. 准备环境和依赖
2. 配置相关参数
3. 执行代码/脚本
4. 验证执行结果

### 注意事项

- 请在测试环境中先进行验证
- 根据实际环境调整配置
- 确保数据安全和备份

## 常见问题

### 问题1: 代码无法执行
**解决方案**: 检查环境依赖和权限设置

### 问题2: 配置错误
**解决方案**: 仔细阅读配置说明，确保参数正确

### 问题3: 权限不足
**解决方案**: 使用合适的用户权限执行

---

## 技术支持

如有问题，请联系技术支持团队。

"""
        
        return doc_template
    
    def create_file_with_permissions(self, content: str, filepath: str, permissions: int = 0o644) -> bool:
        """
        创建文件并设置权限
        
        Args:
            content: 文件内容
            filepath: 文件路径
            permissions: 文件权限
            
        Returns:
            是否创建成功
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 设置权限
            os.chmod(filepath, permissions)
            
            self.logger.info(f"文件创建成功: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"文件创建失败: {filepath}, 错误: {str(e)}")
            return False
    
    def generate_project_structure(self, project_type: str, project_name: str) -> Dict[str, str]:
        """
        生成项目结构
        
        Args:
            project_type: 项目类型
            project_name: 项目名称
            
        Returns:
            项目文件结构字典
        """
        structures = {
            "python": {
                f"{project_name}/": None,
                f"{project_name}/__init__.py": "",
                f"{project_name}/main.py": self.generate_executable_script(
                    "# Python主程序", "python", "main.py"
                ),
                f"{project_name}/requirements.txt": "streamlit>=1.28.0\npython-dotenv>=1.0.0",
                f"{project_name}/config.py": "# 配置文件",
                f"{project_name}/utils/": None,
                f"{project_name}/utils/__init__.py": "",
                f"{project_name}/utils/helpers.py": "# 工具函数",
                f"{project_name}/tests/": None,
                f"{project_name}/tests/__init__.py": "",
                f"{project_name}/tests/test_main.py": "# 测试文件",
                f"{project_name}/README.md": self.generate_markdown_documentation(
                    f"{project_name}项目", "这是一个Python项目"
                )
            },
            "go": {
                f"{project_name}/": None,
                f"{project_name}/main.go": self.generate_executable_script(
                    "// Go主程序", "go", "main.go"
                ),
                f"{project_name}/go.mod": f"module {project_name}\n\ngo 1.21\n",
                f"{project_name}/utils/": None,
                f"{project_name}/utils/utils.go": "package utils\n\n// 工具函数",
                f"{project_name}/internal/": None,
                f"{project_name}/internal/config/": None,
                f"{project_name}/internal/config/config.go": "package config\n\n// 配置管理",
                f"{project_name}/README.md": self.generate_markdown_documentation(
                    f"{project_name}项目", "这是一个Go项目"
                )
            },
            "ansible": {
                f"{project_name}/": None,
                f"{project_name}/site.yml": "---\n# Ansible主站点文件",
                f"{project_name}/inventory": "# 主机清单文件",
                f"{project_name}/roles/": None,
                f"{project_name}/roles/common/": None,
                f"{project_name}/roles/common/tasks/": None,
                f"{project_name}/roles/common/tasks/main.yml": "---\n# 通用任务",
                f"{project_name}/group_vars/": None,
                f"{project_name}/host_vars/": None,
                f"{project_name}/README.md": self.generate_markdown_documentation(
                    f"{project_name}项目", "这是一个Ansible项目"
                )
            }
        }
        
        return structures.get(project_type, {})
    
    def validate_project_structure(self, structure: Dict[str, str]) -> tuple:
        """
        验证项目结构
        
        Args:
            structure: 项目结构字典
            
        Returns:
            (是否有效, 错误信息列表)
        """
        errors = []
        
        for filepath, content in structure.items():
            if filepath.endswith('/'):
                # 目录检查
                continue
            elif filepath.endswith('.py'):
                valid, error = self._validate_python_code(content)
                if not valid:
                    errors.append(f"{filepath}: {error}")
            elif filepath.endswith('.go'):
                valid, error = self._validate_go_code(content)
                if not valid:
                    errors.append(f"{filepath}: {error}")
            elif filepath.endswith('.yml') or filepath.endswith('.yaml'):
                valid, error = self._validate_yaml_code(content)
                if not valid:
                    errors.append(f"{filepath}: {error}")
            elif filepath.endswith('.md'):
                valid, error = self._validate_markdown(content)
                if not valid:
                    errors.append(f"{filepath}: {error}")
        
        return len(errors) == 0, errors