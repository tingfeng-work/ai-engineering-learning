# Day 1 学习安排

## 一、今日目标

1. 搭建 Python 开发环境。
2. 掌握 LLM 调用所需的最小 Python 语法。
3. 创建 AI 学习 GitHub 仓库。
4. 独立跑通一次非流式 LLM API 调用。
5. 能解释完整调用流程。
6. 完成当天面试复盘和算法训练。

------

# 二、时间安排

## 09:00—10:30 Python 开发环境搭建

完成：

- 安装并确认 Python 3.11。
- 配置 VS Code、Python 插件和 Pylance。
- 创建项目目录：

```text
ai-engineering-learning
```

- 创建虚拟环境：

```bash
python -m venv .venv
```

- 激活虚拟环境：

```bash
.venv\Scripts\Activate.ps1
```

- 安装依赖：

```bash
pip install openai python-dotenv pydantic httpx
```

- 导出依赖：

```bash
pip freeze > requirements.txt
```

- 创建：

```text
.env
.env.example
.gitignore
```

`.gitignore` 至少包含：

```gitignore
.venv/
.env
__pycache__/
*.pyc
.vscode/
.idea/
```

验收：

- 虚拟环境可正常激活。
- 依赖安装成功。
- Python 文件可正常运行。
- `.env` 不会提交到 GitHub。

------

## 10:30—12:30 Python 最小语法学习

重点学习：

### 1. 文件与程序入口

```python
if __name__ == "__main__":
    ...
```

### 2. 常用数据结构

- `list`
- `dict`
- `tuple`
- `set`

重点理解：

- JSON 与 `dict`、`list` 的关系。
- `list` 可变。
- `tuple` 通常不可变。

### 3. 函数

```python
def call_model(question: str, temperature: float = 0.2) -> str:
    ...
```

掌握：

- 参数
- 默认参数
- 返回值
- 关键字参数

### 4. 类型标注

重点掌握：

```python
str
float
list[str]
dict[str, str]
str | None
```

### 5. 模块与导入

```python
from dotenv import load_dotenv
from openai import OpenAI
```

### 6. 环境变量

```python
import os

api_key = os.getenv("LLM_API_KEY")
```

### 7. 异常处理

```python
try:
    ...
except Exception as exc:
    ...
```

### 8. Pydantic 入门

```python
from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str
    temperature: float = 0.2
```

------

## 13:30—14:30 创建 GitHub 学习仓库

仓库名称：

```text
ai-engineering-learning
```

目录结构：

```text
ai-engineering-learning/
├── 01-python-basics/
│   ├── README.md
│   └── examples/
├── 02-llm-api/
│   ├── README.md
│   └── src/
├── notes/
│   └── day-01.md
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

完成：

- 创建仓库。
- 编写最小 README。
- 写明学习目标、目录结构和运行方式。
- 完成首次提交：

```bash
git add .
git commit -m "chore: initialize AI engineering learning repository"
```

------

## 14:30—15:30 Python 小练习

### 练习一：构造消息列表

实现：

```python
def build_messages(question: str) -> list[dict[str, str]]:
    ...
```

返回：

```python
[
    {
        "role": "system",
        "content": "你是一名 AI 应用开发助手"
    },
    {
        "role": "user",
        "content": question
    }
]
```

### 练习二：读取配置

从 `.env` 读取：

- API Key
- Base URL
- Model Name

缺失配置时主动报错。

### 练习三：Pydantic 校验

测试：

- 正常参数
- 缺少问题
- 错误类型
- 默认参数

------

## 15:30—18:00 第一次 LLM API 调用

### 1. 先理解调用流程

```text
用户输入
→ 构造 messages
→ 创建模型客户端
→ 发送 API 请求
→ 模型生成结果
→ 解析响应
→ 输出答案
```

### 2. 实现非流式调用

建议目录：

```text
02-llm-api/
└── src/
    ├── main.py
    ├── config.py
    ├── llm_client.py
    └── schemas.py
```

最低功能：

- 从 `.env` 读取配置。
- 创建模型客户端。
- 接收用户输入。
- 构造 System Message 和 User Message。
- 调用模型。
- 输出模型回答。

### 3. 加入基础异常处理

处理：

- API Key 缺失
- 模型名称错误
- 鉴权失败
- 网络异常
- 请求超时
- 返回内容为空

### 4. 独立复现

分三轮完成：

1. 参考官方示例跑通。
2. 关闭参考代码，重新写一遍。
3. 修改为控制台输入，并增加自定义 System Prompt。

### 5. Temperature 实验

同一个问题分别测试：

```text
temperature = 0
temperature = 0.5
temperature = 1.0
```

观察：

- 输出稳定性
- 表达变化
- 发散程度
- 格式遵循情况

记录实验结果。

### 6. 可选补充

时间充足时记录：

- 请求耗时
- 输入 Token
- 输出 Token
- 总 Token

------

## 19:30—20:30 面试复盘

完成以下 3～5 题口述：

1. 一次 LLM API 调用的完整流程是什么？
2. 为什么 AI 开发普遍使用 Python？
3. Python 和 Java 在 AI 系统中分别适合做什么？
4. System Prompt 和 User Prompt 有什么区别？
5. 为什么 API Key 不能直接写在代码中？
6. Temperature 有什么作用？

复盘流程：

```text
面试官意图
→ 避雷点
→ 第一次脱稿回答
→ 查漏补缺
→ 第二次脱稿回答
```

------

## 20:30—21:15 算法训练

完成：

- 一道熟悉的简单题或中等题。
- 使用 Java 编写即可。
- 说明时间复杂度和空间复杂度。

推荐题型：

- 数组
- 哈希
- 双指针
- 滑动窗口

------

## 21:15—21:45 学习记录与复现检查

在 `notes/day-01.md` 中记录：

```markdown
# Day 01

## 今日目标

## 已完成内容

## Python 新知识

## LLM API 调用流程

## Temperature 实验结果

## 遇到的问题

## 解决方式

## 尚未理解的内容

## 面试问题

## 明日计划
```

最后执行一次复现测试：

1. 关闭终端。
2. 重新打开项目。
3. 重新激活虚拟环境。
4. 再次运行程序。
5. 检查 README 是否足以指导运行。
6. 提交代码：

```bash
git add .
git commit -m "feat: add Python basics and first LLM API example"
git push
```

------

# 三、今日必须掌握的原理

- 什么是 LLM API。
- Token 的基本含义。
- System Message 和 User Message 的区别。
- Temperature 的作用。
- API Key、Base URL、Model Name 的作用。
- 为什么 Python 更适合 AI 模型、数据和实验生态。
- 为什么 Java 仍适合企业业务系统和 AI 基础设施。

------

# 四、今日必须完成

-  Python 环境搭建完成
-  虚拟环境可正常使用
-  依赖管理完成
-  `.env` 和 `.gitignore` 配置完成
-  掌握 `list`、`dict`、函数、类型标注、模块、异常处理
-  创建 GitHub 学习仓库
-  完成至少一次有效提交
-  独立跑通非流式 LLM API 调用
-  能解释每一行核心代码
-  完成 Temperature 实验
-  完成 3～5 道面试题口述
-  完成 1 道算法题
-  完成 Day 01 学习记录

------

# 五、时间不足时的优先级

```text
Python 环境
> Python 最小语法
> LLM API 调用
> 独立复现
> GitHub 提交
> 面试复盘
> Temperature 实验
> 算法题
> Token 统计
```

暂不学习：

- FastAPI
- SSE
- 异步编程
- RAG
- Agent
- MCP
- Python 高级语法
- GitHub 主页美化