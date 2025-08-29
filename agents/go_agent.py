"""
Go language expert agent for Go development assistance.
"""

from agents.openai_agent import OpenAIAgent


class GoAgent(OpenAIAgent):
    """Go语言专家Agent - 专门处理Go语言开发相关任务"""
    
    def __init__(self):
        """初始化Go语言专家Agent"""
        super().__init__("go")
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