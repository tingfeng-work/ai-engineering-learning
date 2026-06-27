# Day 01：Python 基础与首次 LLM API 调用

## 一、今日学习目标

今天的目标是补齐 AI 应用开发所需的 Python 基础，并完成一次真实的大模型 API 调用，建立从用户输入到模型响应的最小闭环。

最终完成了以下链路：

```text
用户输入问题
→ Python 主程序接收输入
→ 读取环境变量配置
→ 创建 OpenAI SDK 客户端
→ 组装 messages 请求
→ 通过 OpenRouter 调用免费模型
→ 接收 ChatCompletion 响应
→ 提取并输出模型回答
```

------

# 二、Python 基础学习

## 1. Python 的代码结构

Python 使用缩进表示代码块，而不是像 Java 一样使用大括号。

例如：

```python
def greet(name: str) -> str:
    if name:
        return f"Hello, {name}"

    return "Hello"
```

缩进必须保持一致。当前项目统一使用 4 个空格，并通过 VS Code 和 Black Formatter 进行格式化。

------

## 2. 函数定义与类型注解

学习了 Python 函数的基本写法：

```python
def build_message(name: str) -> str:
    return f"Hello, {name}"
```

其中：

- `name: str` 表示参数预期为字符串；
- `-> str` 表示函数预期返回字符串；
- 类型注解主要用于提高可读性和静态检查，并不会像 Java 一样在运行时强制限制类型。

还学习了：

- 普通参数；
- 默认参数；
- 关键字参数；
- 多返回值；
- `None`；
- `str | None` 可选类型；
- 必需参数应放在默认参数前面。

------

## 3. 可变默认参数问题

不能随意将列表、字典或集合直接作为默认参数：

```python
def add_item(items=[]):
    ...
```

因为默认对象只会在函数定义时创建一次，后续多次调用可能共享同一个对象。

正确方式是：

```python
def add_item(items: list | None = None):
    if items is None:
        items = []
```

------

## 4. 常用容器

### List

有顺序、可以修改、允许重复：

```python
items = ["RAG", "Agent"]
items.append("MCP")
```

### Dict

使用键值对保存结构化数据：

```python
message = {
    "role": "user",
    "content": "什么是 RAG？",
}
```

LLM 请求和响应中会大量使用字典结构。

### Tuple

有顺序但不能修改，常用于返回多个值：

```python
return answer, model
```

### Set

元素不能重复，适合去重：

```python
models = {"qwen", "deepseek", "qwen"}
```

------

## 5. `enumerate()`

学习了通过 `enumerate()` 同时获得列表元素和下标：

```python
for index, message in enumerate(messages, start=1):
    print(index, message)
```

相比手动维护下标，可读性更好。

------

## 6. `__name__` 与程序入口

理解了：

```python
if __name__ == "__main__":
    main()
```

当 Python 文件被直接运行时：

```python
__name__ == "__main__"
```

当文件被其他模块导入时，`__name__` 是模块名称。

因此，可以将测试代码或程序入口放入该判断中，避免模块被导入时自动执行。

------

# 三、Python 模块化

将程序拆分为：

```text
config.py
prompt_builder.py
main.py
```

各模块职责如下。

## `config.py`

负责保存或读取配置，例如：

- 模型名称；
- Temperature；
- System Prompt；
- API Key；
- Base URL。

## `prompt_builder.py`

负责组装模型请求，例如：

```python
{
    "model": model,
    "temperature": temperature,
    "messages": [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": question,
        },
    ],
}
```

## `main.py`

负责：

- 接收用户输入；
- 调用模型客户端；
- 展示模型输出；
- 处理用户层面的异常。

通过模块拆分，避免把配置、请求构造和业务入口全部写在一个文件中。

------

# 四、环境变量管理

使用 `.env` 保存本地配置：

```env
LLM_API_KEY=...
LLM_BASE_URL=...
LLM_MODEL=...
LLM_TEMPERATURE=0.2
LLM_SYSTEM_PROMPT=你是一名 AI 应用开发助手
```

通过：

```python
from dotenv import load_dotenv
```

加载配置，再使用：

```python
os.getenv("LLM_MODEL")
```

读取环境变量。

封装了必要配置读取函数：

```python
def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise ValueError(f"缺少必需的环境变量：{name}")

    return value
```

这样可以避免程序携带 `None` 继续运行，在启动阶段就暴露配置问题。

环境变量读取后默认都是字符串，因此数值类型必须显式转换：

```python
temperature = float(os.getenv("LLM_TEMPERATURE", "0.2"))
```

`.env` 中包含 API Key 等敏感信息，必须加入 `.gitignore`，不能提交到 GitHub。

------

# 五、首次 LLM API 调用

## 1. 技术方案

本次使用：

```text
OpenAI Python SDK
+ OpenAI 兼容协议
+ OpenRouter 网关
+ 免费模型
```

需要注意：

> 使用 OpenAI SDK 不代表一定调用 OpenAI 官方模型。

OpenAI SDK 本质上是客户端工具，只要服务支持兼容协议，就可以通过修改 API Key、Base URL 和模型名称切换服务。

------

## 2. 创建客户端

```python
client = OpenAI(
    api_key=LLM_API_KEY,
    base_url=LLM_BASE_URL,
)
```

其中：

- `api_key` 用于身份认证；
- `base_url` 决定请求发送到哪个模型服务；
- `model` 在具体请求中指定。

------

## 3. 组装请求

使用 Chat Completions API：

```python
response = client.chat.completions.create(
    model=LLM_MODEL,
    messages=[
        {
            "role": "system",
            "content": LLM_SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": question,
        },
    ],
)
```

`messages` 中常见角色包括：

- `system`：定义模型角色和行为约束；
- `user`：用户输入；
- `assistant`：模型历史回答；
- `tool`：外部工具执行结果。

------

## 4. 获取模型回答

通过：

```python
response.choices[0].message.content
```

提取回答。

访问过程为：

```text
response
→ choices 候选回答列表
→ choices[0] 第一个候选回答
→ message 模型生成的消息
→ content 最终文本内容
```

之所以使用 `choices[0]`，是因为模型接口允许返回多个候选结果，但当前通常只请求一个。

------

# 六、完整 Response 分析

本次实际获得了 `ChatCompletion` 对象，其中重要字段包括：

## 1. `model`

```text
openai/gpt-oss-20b:free
```

表示 OpenRouter 最终选择的实际模型。

需要区分：

```text
请求模型：openrouter/free
实际模型：openai/gpt-oss-20b:free
```

免费路由可能在不同请求中选择不同模型，因此适合学习，但不利于稳定复现。

------

## 2. `finish_reason`

本次为：

```text
stop
```

表示模型正常结束生成。

常见值包括：

- `stop`：正常结束；
- `length`：达到最大输出 Token；
- `tool_calls`：模型请求调用工具；
- `content_filter`：内容被安全策略拦截。

如果结果为 `length`，说明回答可能被截断。

------

## 3. `usage`

本次结果为：

```text
prompt_tokens = 116
completion_tokens = 200
total_tokens = 316
```

含义：

- `prompt_tokens`：系统提示词、用户输入及请求上下文消耗的 Token；
- `completion_tokens`：模型生成答案消耗的 Token；
- `total_tokens`：总 Token 数量。

Token 会直接影响：

- API 成本；
- 响应延迟；
- 上下文窗口；
- 系统吞吐量；
- 限流策略。

------

## 4. `reasoning_tokens`

本次响应包含部分推理 Token。

但不能把 `reasoning` 或 `reasoning_tokens` 作为通用业务依赖，因为：

- 不同模型支持情况不同；
- 不同服务商返回结构不同；
- 免费模型路由切换后字段可能消失。

业务中最稳定的字段仍然是：

```python
response.choices[0].message.content
```

------

## 5. `tool_calls`

本次为：

```text
None
```

表示模型没有请求调用外部工具。

后续学习 Function Calling 时，这个字段会保存模型生成的工具调用请求。

------

# 七、异常排查记录

## 1. OpenAI 官方 API 返回 429

第一次请求 OpenAI 官方接口时出现：

```text
429 insufficient_quota
```

该错误不是 Python 语法错误，也不是网络错误，而是 API 账户没有可用额度。

排查链路：

```text
环境变量读取成功
→ Client 创建成功
→ 请求成功发送
→ 服务端识别 API Key
→ 额度检查失败
```

因此可以判断，请求代码本身基本正确。

还需要区分两种 429：

- 请求频率过高；
- 账户额度不足。

对于 `insufficient_quota`，等待和重试通常无法解决，需要充值或更换模型服务。

------

## 2. 切换到 OpenRouter

由于 OpenRouter 提供 OpenAI 兼容接口，因此只需要修改：

```text
LLM_API_KEY
LLM_BASE_URL
LLM_MODEL
```

核心业务代码无需大幅修改。

这体现了将配置放入 `.env`、将模型调用封装到独立模块中的价值。

------

## 3. 输入校验与异常捕获

当前程序已经加入：

- 空问题拦截；
- 模型调用异常捕获；
- 错误信息输出。

基本处理流程：

```text
接收输入
→ 去除前后空格
→ 判断是否为空
→ 调用模型
→ 捕获异常
→ 正常输出回答
```

当前仍是基础异常处理，后续需要进一步区分：

- 身份认证错误；
- 速率限制；
- 网络连接错误；
- 服务端状态错误；
- 返回内容为空。

------

# 八、当前代码能力

经过 Day 01 学习，目前已经可以独立完成：

- 编写基础 Python 函数；
- 使用类型注解；
- 使用 List、Dict、Tuple、Set；
- 使用默认参数和关键字参数；
- 使用 `enumerate()`；
- 使用 `import` 拆分多个模块；
- 理解 `__name__ == "__main__"`；
- 使用 `.env` 管理配置；
- 创建 OpenAI SDK 客户端；
- 调用 OpenAI 兼容模型服务；
- 解析 `ChatCompletion` 响应；
- 查看模型、停止原因和 Token 使用量；
- 对常见 API 错误进行初步定位。

------

# 九、面试表达

## 问题：你是如何调用大模型的？

可以按以下逻辑回答：

> 我使用 OpenAI Python SDK 调用支持 OpenAI 兼容协议的 OpenRouter 服务。API Key、Base URL、模型名称和系统提示词统一放在 `.env` 中，通过 `python-dotenv` 加载，避免敏感配置写死在代码里。程序中由 `main.py` 接收用户问题，模型客户端负责组装 system 和 user 消息并发送 Chat Completions 请求，最后从 `response.choices[0].message.content` 中提取模型回答。同时我会关注实际模型、`finish_reason` 和 Token 使用量，它们分别关系到模型路由、回答是否完整以及调用成本和性能。

------

## 问题：为什么要使用 `.env`？

> `.env` 可以将密钥、服务地址和模型名称从业务代码中分离出来。一方面可以避免 API Key 被提交到代码仓库，另一方面切换不同模型服务时只需要修改配置，而不需要修改核心调用逻辑。

------

## 问题：OpenAI SDK 是否只能调用 OpenAI 模型？

> 不是。OpenAI SDK 是客户端工具，只要第三方服务实现了兼容的 API 协议，就可以通过修改 Base URL、API Key 和模型名称进行调用。本次我实际使用的是 OpenAI SDK 调用 OpenRouter，并由 OpenRouter 路由到免费模型。

------

# 十、Day 01 未完成与后续任务

目前仍未学习：

- 流式输出；
- 多轮对话；
- 上下文管理；
- 结构化输出；
- Function Calling；
- RAG 实现；
- 模型调用结果的统一封装；
- 更完整的异常分类和重试机制；
- FastAPI 服务化。

下一阶段不应直接进入 LangChain，而应继续基于原生 SDK 学习。

建议 Day 02 顺序：

1. 将模型答案、实际模型、停止原因和 Token 使用量封装为统一返回结构；
2. 学习流式输出；
3. 实现多轮对话历史；
4. 完成对应的面试表达；
5. 保持一道算法题训练。

------

# 十一、明日开启学习时使用的提示词

我正在执行“从 Java 后端转向 AI 应用开发”的学习计划。

Day 01 已完成以下内容：

- Python 基础语法：缩进、函数、返回值、类型注解、默认参数、关键字参数和 `None`；
- List、Dict、Tuple、Set 和 `enumerate()`；
- 理解 `__name__ == "__main__"`；
- 使用 `import` 将项目拆分为 `config.py`、模型客户端和 `main.py`；
- 使用 `.env`、`python-dotenv` 和 `os.getenv()` 读取配置，并对数值类型进行转换；
- 将 API Key、Base URL、模型名称和 System Prompt 与代码分离；
- 使用 OpenAI Python SDK 调用 OpenRouter 的 OpenAI 兼容接口；
- 使用 Chat Completions API 组装 system 和 user 消息；
- 从 `response.choices[0].message.content` 提取模型回答；
- 分析了完整 ChatCompletion 响应中的 `model`、`finish_reason`、`usage`、`reasoning_tokens` 和 `tool_calls`；
- 遇到 OpenAI 官方 API 的 `429 insufficient_quota`，确认是额度问题而非代码问题，之后切换到 OpenRouter 免费模型并成功完成调用；
- 当前已经加入空输入校验和基础异常捕获。

请继续按照“知识点讲解 → 小实验 → 我独立编码 → 代码检查 → 面试表达”的方式指导我。

Day 02 优先学习：

1. 将答案、实际模型、停止原因和 Token 使用量封装为统一返回结果；
2. 学习并实现流式输出；
3. 在此基础上学习多轮对话与上下文管理；
4. 不要默认直接提供完整代码，优先让我独立完成，再针对问题给出提示和代码审查；
5. 当天仍需保留面试表达训练和一道算法题。