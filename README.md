# AI Engineering Learning

这是我的 AI 应用开发学习与实践仓库。

我具备 Java 后端开发和深度学习科研背景，目前正在系统学习 Python、LLM、RAG、Agent 与 AI 应用工程化。本仓库用于记录学习过程、代码实验、项目实践和面试复盘。

## 学习目标

通过持续学习与实践，逐步掌握以下能力：

- Python AI 应用开发基础
- 大语言模型 API 接入
- Prompt Engineering
- 结构化输出
- Function Calling 与 Tool Calling
- FastAPI 与流式响应
- Embedding 与向量检索
- RAG 知识库构建与评测
- AI Agent 工作流
- MCP 协议
- AI 应用部署、稳定性与可观测性

## 当前进度

-  完成 Python 开发环境搭建
-  创建项目虚拟环境
-  配置 VS Code Python 解释器
-  初始化 GitHub 学习仓库
-  学习 AI 应用开发所需的 Python 基础
-  完成第一个 LLM API 调用
-  实现结构化输出
-  实现 Function Calling
-  构建基础 RAG 链路
-  构建 AI Agent
-  增加评测与工程化能力

## 技术栈

当前计划使用：

- Python 3.12
- OpenAI Compatible API
- Pydantic
- HTTPX
- FastAPI
- PostgreSQL
- pgvector
- Redis
- Docker

后续将根据学习进度逐步补充相关框架和工具。

## 项目结构

当前仓库结构：

```text
ai-engineering-learning/
├── .gitignore
├── requirements.txt
├── test_env.py
└── README.md
```

后续计划逐步扩展为：

```text
ai-engineering-learning/
├── 01-python-basics/
├── 02-llm-api/
├── 03-structured-output/
├── 04-function-calling/
├── 05-fastapi/
├── 06-embedding/
├── 07-rag-basic/
├── 08-rag-evaluation/
├── 09-agent/
├── 10-mcp/
├── notes/
├── experiments/
├── requirements.txt
└── README.md
```

## 环境说明

当前开发环境：

- 操作系统：Windows
- Python：3.12.6
- 编辑器：Visual Studio Code
- 虚拟环境：venv

## 本地运行

### 1. 克隆仓库

```bash
git clone https://github.com/tingfeng-work/ai-engineering-learning.git
```

进入项目目录：

```bash
cd ai-engineering-learning
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
```

### 3. 激活虚拟环境

Windows PowerShell：

```powershell
.venv\Scripts\Activate.ps1
```

Windows CMD：

```cmd
.venv\Scripts\activate.bat
```

### 4. 安装依赖

```bash
python -m pip install -r requirements.txt
```

### 5. 验证环境

```bash
python test_env.py
```

正确运行后，应输出当前 Python 版本和虚拟环境解释器路径。

## 学习方式

本仓库采用以下学习闭环：

```text
原理学习
→ 代码实现
→ 实验验证
→ 问题复盘
→ 面试表达
```

每个模块尽量包含：

- 核心原理
- 示例代码
- 实验结果
- 常见问题
- 面试题与个人表达
- Git 提交记录

## 学习计划

### 第一阶段：Python 与 LLM 基础

- Python 核心语法
- 模块与依赖管理
- 类型标注
- 异常处理
- Pydantic
- LLM API 调用
- Token 与采样参数
- Prompt 基础

### 第二阶段：AI 应用开发

- 结构化输出
- Function Calling
- FastAPI
- SSE 流式响应
- 异步调用
- 超时、重试与降级

### 第三阶段：RAG

- 文档解析与切分
- Embedding
- 向量数据库
- 混合检索
- Rerank
- RAG 评测

### 第四阶段：Agent

- Tool Calling
- ReAct
- Agent 状态管理
- Memory
- MCP
- Agent 评测

### 第五阶段：工程化

- Docker 部署
- Redis 状态管理
- 日志与链路追踪
- Token 与成本统计
- 限流、熔断与降级
- Prompt Injection 防护
- 自动化评测

## 说明

本仓库主要用于个人学习和求职准备。

代码会随着学习进度持续更新，部分内容可能处于实验或重构阶段。

## 联系方式

- GitHub：https://github.com/tingfeng-work
- 技术博客：[https://tingfeng-work.github.io](https://tingfeng-work.github.io/)