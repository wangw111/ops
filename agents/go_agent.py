"""
Go language expert agent for Go development assistance.
"""

from typing import Dict, Any, List
from agents.multi_ai_agent import MultiAIAgent
from utils.code_generator import CodeGenerator


class GoAgent(MultiAIAgent):
    """Go语言专家Agent - 专门处理Go语言开发相关任务"""
    
    def __init__(self, provider: str = "openai"):
        """
        初始化Go语言专家Agent
        
        Args:
            provider: AI提供商 (openai, claude, qwen)
        """
        super().__init__("go", provider)
        self.code_generator = CodeGenerator(self.logger)
        self.logger.info("Go语言专家Agent已初始化")
    
    def get_system_prompt(self) -> str:
        """获取Go语言专家的系统提示词"""
        return """你是一个专业的Go语言开发专家，具有以下专长：

1. Go语言语法和最佳实践
   - Go语言基础语法和特性
   - 代码风格和命名规范
   - 错误处理模式
   - 接口设计和实现
   - 包管理和依赖

2. 并发编程和goroutine管理
   - goroutine和channel使用
   - sync包工具应用
   - 并发模式和实践
   - 竞态条件检测
   - 性能优化技巧

3. 微服务架构设计
   - RESTful API设计
   - gRPC服务开发
   - 服务发现和注册
   - 负载均衡策略
   - 分布式系统设计

4. 性能优化和内存管理
   - 内存分配和回收
   - CPU性能分析
   - 垃圾回收调优
   - 并发性能优化
   - 资源使用监控

5. 测试驱动开发
   - 单元测试编写
   - 集成测试设计
   - 基准测试分析
   - Mock和Stub技术
   - �覆盖率分析

6. 标准库和第三方库使用
   - 标准库深度应用
   - 流行第三方库推荐
   - 框架选择和评估
   - 库的最佳实践
   - 版本管理策略

请提供符合Go语言规范的高质量代码建议和解决方案。你的回答应该：
- 遵循Go语言官方规范和最佳实践
- 提供简洁、高效、可读性强的代码
- 考虑并发安全和性能优化
- 包含必要的错误处理
- 提供完整的使用示例
- 解释代码的设计思路和原理

如果需要，可以提供代码示例、配置文件和使用说明。"""
    
    def get_go_best_practices(self) -> str:
        """获取Go语言最佳实践"""
        return """Go语言开发最佳实践：

1. 代码组织
   - 使用有意义的包名
   - 遵循Go的命名约定
   - 保持函数简短和专注
   - 使用接口定义行为

2. 错误处理
   - 始终检查错误
   - 提供有意义的错误信息
   - 使用errors.New和fmt.Errorf
   - 考虑自定义错误类型

3. 并发编程
   - 优先使用channel而非共享内存
   - 使用sync包的工具
   - 避免goroutine泄漏
   - 使用context管理生命周期

4. 性能优化
   - 使用pprof进行性能分析
   - 避免不必要的内存分配
   - 使用strings.Builder处理字符串
   - 选择合适的数据结构

5. 测试
   - 编写全面的单元测试
   - 使用表驱动测试
   - 测试边界条件和错误情况
   - 保持测试的独立性"""
    
    def generate_code_template(self, template_type: str) -> str:
        """
        生成Go代码模板
        
        Args:
            template_type: 模板类型
            
        Returns:
            代码模板
        """
        templates = {
            "http_server": """package main

import (
    "encoding/json"
    "log"
    "net/http"
)

type Response struct {
    Message string `json:"message"`
    Status  int    `json:"status"`
}

func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        
        response := Response{
            Message: "Hello, World!",
            Status:  200,
        }
        
        if err := json.NewEncoder(w).Encode(response); err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }
    })
    
    log.Println("Server starting on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatal(err)
    }
}""",
            "grpc_service": """package main

import (
    "context"
    "log"
    "net"

    "google.golang.org/grpc"
    pb "your-package/protobuf"
)

type server struct {
    pb.UnimplementedYourServiceServer
}

func (s *server) YourMethod(ctx context.Context, req *pb.YourRequest) (*pb.YourResponse, error) {
    return &pb.YourResponse{
        Message: "Hello " + req.Name,
    }, nil
}

func main() {
    lis, err := net.Listen("tcp", ":50051")
    if err != nil {
        log.Fatalf("Failed to listen: %v", err)
    }
    
    s := grpc.NewServer()
    pb.RegisterYourServiceServer(s, &server{})
    
    log.Println("gRPC server starting on :50051")
    if err := s.Serve(lis); err != nil {
        log.Fatalf("Failed to serve: %v", err)
    }
}""",
            "concurrent_worker": """package main

import (
    "fmt"
    "sync"
    "time"
)

type Worker struct {
    id       int
    jobs     <-chan int
    results  chan<- int
    wg       *sync.WaitGroup
}

func NewWorker(id int, jobs <-chan int, results chan<- int, wg *sync.WaitGroup) *Worker {
    return &Worker{
        id:      id,
        jobs:    jobs,
        results: results,
        wg:      wg,
    }
}

func (w *Worker) Start() {
    go func() {
        defer w.wg.Done()
        
        for job := range w.jobs {
            result := w.process(job)
            w.results <- result
        }
    }()
}

func (w *Worker) process(job int) int {
    // 模拟工作
    time.Sleep(time.Millisecond * time.Duration(job))
    return job * 2
}

func main() {
    const numJobs = 10
    const numWorkers = 3
    
    jobs := make(chan int, numJobs)
    results := make(chan int, numJobs)
    
    var wg sync.WaitGroup
    
    // 创建工作池
    for i := 1; i <= numWorkers; i++ {
        wg.Add(1)
        worker := NewWorker(i, jobs, results, &wg)
        worker.Start()
    }
    
    // 发送任务
    for j := 1; j <= numJobs; j++ {
        jobs <- j
    }
    close(jobs)
    
    // 等待所有工作完成
    wg.Wait()
    close(results)
    
    // 收集结果
    for result := range results {
        fmt.Printf("Result: %d\\n", result)
    }
}"""
        }
        
        return templates.get(template_type, "模板类型不存在")
    
    def analyze_go_code(self, code: str) -> str:
        """
        分析Go代码并提供改进建议
        
        Args:
            code: Go代码
            
        Returns:
            分析结果和建议
        """
        # 这里可以实现更复杂的代码分析逻辑
        analysis_points = [
            "检查代码是否符合Go语言规范",
            "识别潜在的性能问题",
            "评估错误处理的完整性",
            "检查并发安全性",
            "评估代码的可读性和可维护性"
        ]
        
        return f"代码分析结果：\n" + "\n".join([f"✓ {point}" for point in analysis_points])
    
    def generate_runnable_go_project(self, project_name: str, project_type: str = "web") -> Dict[str, str]:
        """
        生成可运行的Go项目
        
        Args:
            project_name: 项目名称
            project_type: 项目类型
            
        Returns:
            项目文件结构字典
        """
        project_templates = {
            "web": {
                f"{project_name}/main.go": self.code_generator.generate_executable_script(
                    """package main

import (
    "encoding/json"
    "log"
    "net/http"
    "time"
)

type Response struct {
    Message    string    `json:"message"`
    Timestamp  time.Time `json:"timestamp"`
    Status     int       `json:"status"`
}

func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        
        response := Response{
            Message:   "Hello from Go Web Server!",
            Timestamp: time.Now(),
            Status:    200,
        }
        
        if err := json.NewEncoder(w).Encode(response); err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }
    })
    
    port := ":8080"
    log.Printf("Server starting on port %s", port)
    
    if err := http.ListenAndServe(port, nil); err != nil {
        log.Fatal(err)
    }
}""", "go", "main.go"
                ),
                f"{project_name}/go.mod": f"""module {project_name}

go 1.21

require (
)""",
                f"{project_name}/handlers/": None,
                f"{project_name}/handlers/handlers.go": """package handlers

import (
    "net/http"
)

// HealthHandler 健康检查处理器
func HealthHandler(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusOK)
    w.Write([]byte("OK"))
}

// APIHandler API处理器
func APIHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)
    w.Write([]byte(`{"message": "API endpoint"}`))
}
""",
                f"{project_name}/config/": None,
                f"{project_name}/config/config.go": """package config

import (
    "os"
    "strconv"
)

// Config 应用配置
type Config struct {
    Port         string
    LogLevel     string
    DatabaseURL  string
}

// LoadConfig 加载配置
func LoadConfig() *Config {
    return &Config{
        Port:         getEnv("PORT", "8080"),
        LogLevel:     getEnv("LOG_LEVEL", "info"),
        DatabaseURL:  getEnv("DATABASE_URL", ""),
    }
}

func getEnv(key, defaultValue string) string {
    if value := os.Getenv(key); value != "" {
        return value
    }
    return defaultValue
}
""",
                f"{project_name}/README.md": self.code_generator.generate_markdown_documentation(
                    f"{project_name} - Go Web项目",
                    "这是一个使用Go语言开发的Web应用项目。",
                    [
                        {
                            "title": "运行项目",
                            "description": "启动Go Web服务器",
                            "language": "bash",
                            "code": f"cd {project_name}\ngo run main.go"
                        },
                        {
                            "title": "构建项目",
                            "description": "编译Go项目",
                            "language": "bash",
                            "code": f"cd {project_name}\ngo build -o {project_name} main.go"
                        }
                    ]
                )
            },
            "cli": {
                f"{project_name}/main.go": self.code_generator.generate_executable_script(
                    """package main

import (
    "flag"
    "fmt"
    "log"
    "os"
)

func main() {
    // 定义命令行参数
    name := flag.String("name", "World", "指定名称")
    age := flag.Int("age", 0, "指定年龄")
    verbose := flag.Bool("verbose", false, "详细输出")
    
    flag.Parse()
    
    // 验证参数
    if *age < 0 {
        log.Fatal("年龄不能为负数")
    }
    
    // 输出结果
    if *verbose {
        fmt.Printf("详细信息：\\n")
        fmt.Printf("  名称: %s\\n", *name)
        fmt.Printf("  年龄: %d\\n", *age)
        fmt.Printf("  程序名: %s\\n", os.Args[0])
    } else {
        fmt.Printf("Hello, %s! ", *name)
        if *age > 0 {
            fmt.Printf("You are %d years old.\\n", *age)
        } else {
            fmt.Println("\\n")
        }
    }
}
""", "go", "main.go"
                ),
                f"{project_name}/go.mod": f"""module {project_name}

go 1.21

require (
)""",
                f"{project_name}/cmd/": None,
                f"{project_name}/cmd/version.go": """package cmd

import (
    "fmt"
    "os"
    "runtime"
)

// Version 版本信息
var Version = "1.0.0"
var BuildTime = "unknown"

// PrintVersion 打印版本信息
func PrintVersion() {
    fmt.Printf("%s version %s\\n", os.Args[0], Version)
    fmt.Printf("Build time: %s\\n", BuildTime)
    fmt.Printf("Go version: %s\\n", runtime.Version())
    fmt.Printf("OS/Arch: %s/%s\\n", runtime.GOOS, runtime.GOARCH)
}
""",
                f"{project_name}/README.md": self.code_generator.generate_markdown_documentation(
                    f"{project_name} - Go CLI工具",
                    "这是一个使用Go语言开发的命令行工具。",
                    [
                        {
                            "title": "基本使用",
                            "description": "运行CLI工具",
                            "language": "bash",
                            "code": f"cd {project_name}\ngo run main.go -name Alice -age 25"
                        },
                        {
                            "title": "详细输出",
                            "description": "启用详细模式",
                            "language": "bash",
                            "code": f"cd {project_name}\ngo run main.go -name Bob -age 30 -verbose"
                        }
                    ]
                )
            }
        }
        
        return project_templates.get(project_type, {})
    
    def validate_go_code(self, code: str) -> tuple:
        """
        验证Go代码
        
        Args:
            code: Go代码内容
            
        Returns:
            (是否有效, 错误信息)
        """
        return self.code_generator.validate_code(code, "go")
    
    def generate_go_documentation(self, code: str, title: str) -> str:
        """
        生成Go代码文档
        
        Args:
            code: Go代码
            title: 文档标题
            
        Returns:
            Markdown文档
        """
        return self.code_generator.generate_markdown_documentation(
            title,
            "这是一个Go语言代码示例，包含了完整的代码实现和使用说明。",
            [
                {
                    "title": "Go代码示例",
                    "description": "完整的Go代码实现",
                    "language": "go",
                    "code": code
                },
                {
                    "title": "运行代码",
                    "description": "如何运行Go代码",
                    "language": "bash",
                    "code": "go run main.go"
                },
                {
                    "title": "构建项目",
                    "description": "如何构建Go项目",
                    "language": "bash",
                    "code": "go build -o app main.go"
                }
            ]
        )