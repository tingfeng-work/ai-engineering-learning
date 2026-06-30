# Day 02：统一结果封装、流式输出与多轮对话

## 一、今日学习目标

今天的目标是在 Day 01 单次模型调用的基础上，进一步完善模型调用的工程结构，并实现流式输出与多轮对话。

最终完成了以下能力：

```text
用户输入问题
→ 将问题加入消息历史
→ 通过 OpenAI SDK 发起流式请求
→ 持续接收模型返回的增量事件
→ 实时输出回答文本
→ 收集实际模型、停止原因和 Token 使用量
→ 聚合为统一的 LLMResult
→ 将完整 assistant 回答加入消息历史
→ 进入下一轮对话
```

今日主要完成了三个模块：

1. 使用 `dataclass` 封装统一模型调用结果；
2. 使用生成器和 `stream=True` 实现流式输出；
3. 使用 `messages` 和循环实现多轮对话。

------

# 二、使用 `dataclass` 封装模型调用结果

## 1. 为什么不再只返回字符串

Day 01 的模型调用函数只返回：

```python
response.choices[0].message.content
```

调用方只能得到模型回答文本，无法同时获得：

- 实际调用模型；
- 停止原因；
- 输入 Token 数；
- 输出 Token 数；
- 总 Token 数。

如果后续需要进行成本统计、调用日志记录或模型监控，只返回字符串无法满足需求。

因此，将完整调用结果封装为统一对象：

```text
LLMResult
├── content
├── model
├── finish_reason
├── prompt_tokens
├── completion_tokens
└── total_tokens
```

这可以类比 Java 中的 DTO。

------

## 2. `@dataclass`

Python 中可以使用：

```python
from dataclasses import dataclass
```

定义以保存数据为主要职责的类：

```python
@dataclass
class LLMResult:
    content: str
    model: str
    finish_reason: str | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
```

使用时可以通过关键字参数创建对象：

```python
result = LLMResult(
    content="你好",
    model="openai/gpt-oss-20b:free",
    finish_reason="stop",
    prompt_tokens=12,
    completion_tokens=20,
    total_tokens=32,
)
```

相比字典，`dataclass` 具有以下优势：

- 字段结构更加明确；
- IDE 可以提供属性提示；
- 类型注解更加清晰；
- 字段名不容易拼写错误；
- 更适合作为不同模块之间传递数据的 DTO。

------

## 3. `__init__()`

`__init__()` 是对象的初始化方法。

普通 Python 类可能需要手动编写：

```python
class Student:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
```

其中：

- `self` 表示当前对象；
- 右侧的 `name` 是传入参数；
- 左侧的 `self.name` 是保存在对象中的属性。

这与 Java 中的构造器和 `this` 类似：

```java
public Student(String name) {
    this.name = name;
}
```

使用 `@dataclass` 后，Python 会根据字段定义自动生成对应的 `__init__()`。

因此，即使没有手写初始化方法，也可以直接创建对象：

```python
student = Student(name="李廷风", age=25)
```

严格来说，`__init__()` 负责对象创建后的初始化，真正创建对象的是 `__new__()`。当前阶段只需要掌握 `__init__()` 的初始化职责。

------

## 4. `__repr__()`

`__repr__()` 用于定义对象面向开发者的字符串表示，主要用于：

- 调试；
- 日志输出；
- 交互式环境；
- 查看对象内部字段。

如果普通类没有实现 `__repr__()`，打印对象时可能得到：

```text
<__main__.Student object at 0x000001...>
```

而 `dataclass` 会自动生成 `__repr__()`，因此：

```python
print(result)
```

可以输出：

```text
LLMResult(
    content='你好',
    model='openai/gpt-oss-20b:free',
    finish_reason='stop',
    prompt_tokens=12,
    completion_tokens=20,
    total_tokens=32
)
```

这样更方便观察对象中的实际数据。

------

## 5. `__eq__()`

`dataclass` 默认还会自动生成 `__eq__()`，用于按字段比较两个对象是否相等。

例如：

```python
student1 = Student(name="李廷风", age=25)
student2 = Student(name="李廷风", age=25)

print(student1 == student2)
```

结果为：

```text
True
```

原因是两个对象的字段值完全相同。

这与没有重写 `equals()` 的普通 Java 对象不同。Java 中普通对象默认更接近对象身份比较，而 `dataclass` 默认会按字段值进行比较。

------

## 6. 默认字段和可选类型

定义数据类时，没有默认值的字段必须放在有默认值字段之前：

```python
@dataclass
class LLMResult:
    content: str
    model: str
    finish_reason: str | None = None
```

错误顺序会产生：

```text
TypeError: non-default argument follows default argument
```

这是因为 `dataclass` 会根据字段顺序生成 `__init__()`，而 Python 函数要求必填参数位于默认参数之前。

可选字段使用：

```python
int | None
str | None
```

例如：

```python
total_tokens: int | None = None
```

表示该字段可能是整数，也可能因为兼容接口没有返回数据而为 `None`。

------

# 三、将 SDK Response 转换为 `LLMResult`

## 1. 模型客户端的职责

模型客户端不再直接返回字符串，而是负责：

```text
调用 OpenAI SDK
→ 解析 SDK 原始 Response
→ 提取业务需要的字段
→ 构造 LLMResult
→ 返回给调用方
```

函数返回类型由：

```python
def ask_model(question: str) -> str:
```

改为：

```python
def ask_model(question: str) -> LLMResult:
```

------

## 2. 字段映射

普通响应中的字段映射为：

| `LLMResult` 字段    | SDK Response 来源                     |
| ------------------- | ------------------------------------- |
| `content`           | `response.choices[0].message.content` |
| `model`             | `response.model`                      |
| `finish_reason`     | `response.choices[0].finish_reason`   |
| `prompt_tokens`     | `response.usage.prompt_tokens`        |
| `completion_tokens` | `response.usage.completion_tokens`    |
| `total_tokens`      | `response.usage.total_tokens`         |

为了减少重复的长链式访问，可以先提取：

```python
choice = response.choices[0]
```

然后访问：

```python
choice.message.content
choice.finish_reason
```

------

## 3. 空内容处理

当前程序只处理普通文本回答，因此模型未返回文本时，应当视为异常：

```python
content = choice.message.content

if content is None:
    raise ValueError("模型没有返回文本内容")
```

这样可以避免将异常响应封装成正常的业务结果。

------

## 4. Usage 为空时的处理

部分 OpenAI 兼容接口可能不返回：

```python
response.usage
```

因此不能无条件访问：

```python
response.usage.total_tokens
```

否则可能出现：

```text
AttributeError: 'NoneType' object has no attribute 'total_tokens'
```

正确方式是先判断：

```python
if response.usage is None:
    ...
```

Usage 缺失时，Token 字段继续保持 `None`。

在数据层使用：

```python
None
```

表示缺失，而不是存储字符串：

```text
"未知"
```

“未知”属于展示层文案，应由 `main.py` 决定如何显示。

------

# 四、流式输出基础

## 1. 普通输出与流式输出

普通调用的流程是：

```text
发送请求
→ 等待模型生成完整回答
→ 服务端一次性返回完整 Response
→ 用户看到完整回答
```

流式调用的流程是：

```text
发送请求
→ 模型生成一部分内容
→ 服务端立即返回一个 chunk
→ 客户端实时展示
→ 继续接收后续 chunk
```

流式输出主要优化的是：

```text
Time to First Token，TTFT
首 Token 延迟
```

它可以让用户更早看到第一段内容，但不一定缩短模型生成完整回答所需的总时间，也不会天然减少 Token 消耗。

------

## 2. `return` 与 `yield`

普通函数通过 `return` 一次性返回结果：

```python
def get_answer() -> str:
    return "完整回答"
```

执行到 `return` 后，函数立即结束。

生成器函数通过 `yield` 分批产生结果：

```python
def generate_words():
    yield "Python"
    yield "Generator"
```

调用生成器函数时，函数体不会立即完整执行，而是先返回生成器对象：

```python
generator = generate_words()
```

真正执行发生在：

```python
for word in generator:
    print(word)
```

每次遇到 `yield`：

1. 产生一个值；
2. 暂停函数；
3. 保存当前执行位置和局部状态；
4. 下一次迭代时从暂停位置继续。

因此可以总结为：

```text
return：返回最终结果并结束函数
yield：产生一个值并暂停函数
```

------

## 3. 生成器返回类型

流式函数使用：

```python
from collections.abc import Iterator
```

返回类型可以写成：

```python
def stream_model(...) -> Iterator[str]:
```

表示调用方可以迭代该结果，并且每次获得一个字符串。

不建议从：

```python
_collections_abc
```

等 Python 内部模块导入，应使用公开接口：

```python
collections.abc
```

------

## 4. `end=""` 与 `flush=True`

流式展示时使用：

```python
print(text, end="", flush=True)
```

其中：

- `end=""`：取消 `print()` 默认的换行；
- `flush=True`：立即将缓冲区中的输出刷新到终端。

`flush=True` 不能减少服务端真正的首 Token 延迟，只能避免客户端已经收到文本后，终端仍因输出缓冲而延迟展示。

------

# 五、OpenAI SDK 流式调用

## 1. 开启流式响应

在 Chat Completions 请求中加入：

```python
stream=True
```

例如：

```python
stream = client.chat.completions.create(
    model=LLM_MODEL,
    messages=messages,
    stream=True,
)
```

此时返回的不是完整 `ChatCompletion`，而是一个可以持续迭代的响应流：

```python
for chunk in stream:
    ...
```

------

## 2. `message.content` 与 `delta.content`

普通响应读取：

```python
response.choices[0].message.content
```

流式响应读取：

```python
chunk.choices[0].delta.content
```

区别是：

- `message`：完整的 assistant 消息；
- `delta`：当前 chunk 新增的内容。

因此，流式回答是由多个 `delta.content` 增量拼接得到的。

正确字段是：

```python
delta.content
```

不是：

```python
delta.context
```

------

## 3. Chunk 不等于 Token

流式输出看起来可能像模型一个字一个字生成，但不能认为：

```text
一个 chunk = 一个字符 = 一个 Token
```

实际情况可能是：

- 一个 chunk 包含一个字符；
- 一个 chunk 包含多个字符；
- 一个 chunk 包含词语或标点；
- 一个 Token 也不一定对应一个汉字。

Chunk 是传输事件的边界，不等于模型 Token 的边界。

------

## 4. `delta.content` 可能为 `None`

并非所有 chunk 都携带文本。

部分 chunk 可能用于传递：

- assistant 角色；
- 停止原因；
- 工具调用增量；
- Token usage；
- 其他元数据。

因此必须判断：

```python
text = choice.delta.content

if text is not None:
    yield text
```

不能无条件打印或拼接。

------

# 六、使用 `StreamEvent` 统一流式事件

## 1. 为什么不只返回字符串

只返回：

```python
Iterator[str]
```

只能传递文本，无法同时传递：

- 实际模型；
- 停止原因；
- Token 使用量；
- 流结束状态。

因此定义了统一流式事件对象：

```text
StreamEvent
├── event_type
├── content
├── model
├── finish_reason
├── prompt_tokens
├── completion_tokens
└── total_tokens
```

------

## 2. 两类事件

当前定义两种事件类型。

### Content 事件

用于传递当前新增文本：

```text
event_type = "content"
content = 当前文本片段
```

### Finish 事件

用于表示流式调用正常结束，并传递最终元数据：

```text
event_type = "finish"
model = 实际模型
finish_reason = 停止原因
usage = Token 信息
```

多个 `StreamEvent` 最终可以聚合为一个 `LLMResult`：

```text
多个 content 事件
→ 拼接为完整回答

一个 finish 事件
→ 提供最终元数据

完整回答 + 最终元数据
→ LLMResult
```

------

## 3. 为什么不混合返回不同类型

不推荐让生成器返回：

```python
Iterator[str | LLMResult]
```

否则消费者需要不断判断：

```python
if isinstance(item, str):
    ...
elif isinstance(item, LLMResult):
    ...
```

随着事件种类增加，联合类型会越来越复杂。

统一返回：

```python
Iterator[StreamEvent]
```

可以建立稳定的事件协议，使消费者只根据 `event_type` 进行处理。

------

# 七、流式 Token Usage

## 1. 开启 Usage

流式请求中加入：

```python
stream_options={"include_usage": True}
```

服务端会在流结束前额外发送 usage 信息。

------

## 2. Usage Chunk 的特点

最终 usage chunk 通常具有：

```python
chunk.choices == []
chunk.usage is not None
```

因此不能无条件访问：

```python
chunk.choices[0]
```

否则可能产生：

```text
IndexError: list index out of range
```

正确处理方式是先判断：

```python
if chunk.choices:
    ...
```

再独立判断：

```python
if chunk.usage is not None:
    ...
```

------

## 3. 停止原因与流结束不同

`finish_reason` 表示模型停止生成文本的原因，但不表示所有响应数据都已经传输完毕。

可能出现：

```text
文本生成结束
→ 收到 finish_reason
→ 服务端继续发送 usage chunk
→ 整个响应流结束
```

因此不能在第一次看到 `finish_reason` 时立即产生完整的 finish 事件。

正确方式是：

```text
收到 finish_reason
→ 暂存

收到 usage
→ 暂存

所有 chunk 遍历结束
→ 产生统一 finish 事件
```

------

## 4. 流中断处理

如果网络在流式传输过程中断：

- 已经接收并打印的文本仍会保留在终端；
- 尚未到达的文本无法获取；
- 最终 usage 可能无法收到；
- `finish_reason` 也可能缺失；
- 迭代过程会抛出异常。

当前策略是：

> 可以让用户看到已经输出的部分文本，但不将部分回答作为正式 assistant 消息加入历史。

因为部分回答可能语义不完整，不能被后续模型当作正式上下文。

------

# 八、流式结果聚合

调用方需要一边展示，一边收集文本：

```python
text_parts: list[str] = []

for event in stream_model(messages):
    if event.event_type == "content":
        if event.content is not None:
            print(event.content, end="", flush=True)
            text_parts.append(event.content)
```

流结束后统一拼接：

```python
full_text = "".join(text_parts)
```

使用 `join()` 而不是反复执行：

```python
full_text += text
```

原因是 Python 字符串不可变。反复拼接可能不断创建新字符串并复制已有内容；先保存到列表，最后统一拼接更适合大量文本片段。

最后将完整文本和 finish 事件中的元数据封装为：

```python
LLMResult(
    content=full_text,
    model=actual_model,
    finish_reason=finish_reason,
    prompt_tokens=prompt_tokens,
    completion_tokens=completion_tokens,
    total_tokens=total_tokens,
)
```

------

# 九、多轮对话

## 1. Chat Completions 是无状态请求

模型不会自动记住上一次 API 调用。

例如第一次发送：

```text
user：我叫廷风
```

第二次如果只发送：

```text
user：我叫什么？
```

模型无法知道第一轮发生了什么。

为了实现多轮对话，客户端必须重新发送历史：

```text
system
user：我叫廷风
assistant：你好，廷风
user：我叫什么？
```

因此：

> 多轮对话不是模型自动拥有记忆，而是应用程序维护并重复发送历史消息。

------

## 2. Message 与 Turn

一条消息可以是：

- system 消息；
- user 消息；
- assistant 消息。

一轮普通文本对话通常包含：

```text
一条 user 消息
+
一条 assistant 消息
```

所以“最近 5 轮”通常表示：

```text
5 条 user 消息 + 5 条 assistant 消息
```

而不是最近 5 条消息。

------

## 3. Role 的正确取值

普通对话中使用：

```text
system
user
assistant
```

不能使用：

```text
user1
assistant1
user2
```

轮次由消息在列表中的顺序表示，而不是编码在 `role` 字段中。

正确结构是：

```python
messages = [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "第一轮问题"},
    {"role": "assistant", "content": "第一轮回答"},
    {"role": "user", "content": "第二轮问题"},
]
```

------

## 4. 为什么必须保存 Assistant 回答

如果只保存 user 消息，模型无法理解依赖上一轮回答的问题。

例如：

```text
user：给我三个学习方向
assistant：方向一、方向二、方向三
user：详细解释第二个
```

“第二个”依赖 assistant 上一轮的回答。

因此，多轮历史必须同时保存：

```text
user + assistant
```

------

## 5. 模型客户端接收完整 Messages

原来的函数接口是：

```python
def stream_model(question: str):
```

多轮对话后改为：

```python
def stream_model(
    messages: list[dict[str, str]],
) -> Iterator[StreamEvent]:
```

模型客户端不再负责：

- 构造 system 消息；
- 添加当前 user；
- 添加 assistant 历史；
- 决定保留哪些上下文。

它只负责：

```text
接收完整 messages
→ 调用模型
→ 返回 StreamEvent
```

会话层负责维护 `messages`。

这样可以避免模型客户端偷偷修改调用方传入的列表，减少隐藏副作用。

------

# 十、多轮聊天循环

## 1. `while True`

命令行聊天使用：

```python
while True:
```

持续读取用户输入，直到遇到退出命令。

退出命令使用：

```python
if question.lower() in {"exit", "quit"}:
    break
```

其中：

- `break`：结束整个循环；
- `continue`：跳过当前轮，进入下一轮。

空输入不代表用户想结束程序，因此使用：

```python
if not question:
    print("输入不能为空")
    continue
```

------

## 2. 会话级状态与请求级状态

整个会话共享：

```python
messages
```

因此必须放在循环外。

每一轮独立使用：

```python
text_parts
actual_model
finish_reason
prompt_tokens
completion_tokens
total_tokens
```

因此必须放在循环内重新初始化。

可以概括为：

```text
messages：会话级状态
text_parts 和调用元数据：请求级状态
```

如果请求级状态放在循环外，就会出现跨轮污染，例如第二轮回答中混入第一轮文本。

------

## 3. 一轮调用的正确顺序

```text
读取用户问题
→ 校验空输入和退出命令
→ 将 user 消息加入 messages
→ 调用流式模型
→ 实时输出并收集完整回答
→ 调用成功后加入 assistant 消息
```

User 消息必须在调用模型之前加入，因为本次问题需要包含在本次请求的 `messages` 中。

Assistant 消息只能在完整回答成功生成后加入，不能每收到一个 chunk 就加入历史。

------

## 4. 异常回滚

如果先加入：

```python
messages.append(
    {
        "role": "user",
        "content": question,
    }
)
```

之后模型调用失败，会留下没有 assistant 回答的残缺轮次。

当前普通文本对话采用：

```python
messages.pop()
```

删除刚加入的 user 消息，恢复调用前状态。

基本逻辑：

```text
追加 user
→ 模型调用失败
→ 删除该 user
→ 提示错误
→ 继续下一轮
```

空回答也不应加入历史，因为它表示本轮没有形成有效 assistant 消息。

------

## 5. `/history` 命令

增加了：

```text
/history
```

用于查看：

- 当前消息数量；
- 当前完整轮数；
- 消息角色；
- 可选的内容摘要。

当前严格保持：

```text
system + user/assistant 成对结构
```

时，可以使用：

```python
turns = (len(messages) - 1) // 2
```

计算完整轮数。

------

# 十一、代码重构

多轮聊天循环中包含了大量流式事件消费逻辑：

```text
遍历 StreamEvent
→ 打印 content
→ 收集文本
→ 收集模型和 usage
→ 校验结果
→ 构造 LLMResult
```

为了减少 `main()` 的复杂度，已将这部分抽取为独立函数。

重构后的职责可以划分为：

```text
main.py
├── 读取用户输入
├── 管理 messages
├── 处理退出和 history 命令
├── 处理失败回滚
└── 将完整 assistant 回答加入历史

流消费函数
├── 调用 stream_model
├── 实时输出文本
├── 聚合 StreamEvent
├── 校验完整结果
└── 返回 LLMResult

llm_client.py
├── 调用 OpenAI SDK
├── 解析原始 chunk
└── 转换为 StreamEvent
```

这种分层使主循环更接近业务流程，模型 SDK 的具体结构不会泄漏到会话管理代码中。

------

# 十二、异常排查记录

## 1. `if not chunk.choices` 条件写反

曾错误写成：

```python
if not chunk.choices:
    choice = chunk.choices[0]
```

这表示在列表为空时访问第一个元素，会导致越界。

正确逻辑是：

```python
if chunk.choices:
    choice = chunk.choices[0]
```

------

## 2. 文本判断写反

曾错误写成：

```python
if not text:
    yield content_event
```

这会只保留空字符串或 `None`，反而过滤正常文本。

正确方式是：

```python
if text is not None:
    yield StreamEvent(
        event_type="content",
        content=text,
    )
```

------

## 3. 变量拼写错误

曾将：

```python
prompt_tokens
```

误写为：

```python
promopt_tokens
```

导致真实 Token 已经被赋值到一个变量，但最终构造对象时仍读取另一个始终为 `None` 的变量。

这说明 Python 动态语言中变量名拼写尤其重要，类型检查工具可以帮助提前发现此类问题。

------

## 4. 空输入判断错误

曾使用：

```python
if question is None:
```

但 `input()` 正常返回字符串，用户直接回车时得到的是：

```python
""
```

因此正确判断是：

```python
if not question:
```

通常先执行：

```python
question = input(...).strip()
```

还可以同时拦截只包含空格的输入。

------

## 5. 多轮文本列表未清空

曾在两轮调用中复用同一个：

```python
text_parts
```

导致第二轮完整回答变成：

```text
第一轮回答 + 第二轮回答
```

修复方式是每轮重新创建列表。

这体现了会话级状态与请求级状态必须分离。

------

# 十三、今日实验结果

今日已经实际验证：

- 模型可以流式输出回答；
- 流式响应可以还原为完整文本；
- 能够获取实际模型和 Token usage；
- 可以将流式事件聚合为 `LLMResult`；
- 模型能够记住上一轮中提供的名字或代号；
- 模型能够理解“详细解释第二个”等跨轮指代；
- 空输入不会终止程序；
- 输入 `exit` 或 `quit` 可以正常结束会话；
- 每轮重新发送历史会导致输入 Token 随上下文增长。

其中，长 assistant 回答被加入历史后，下一轮的 `prompt_tokens` 明显增加，直观验证了：

```text
对话历史增长
→ 输入 Token 增长
→ 成本和延迟增加
→ 最终可能超过上下文窗口
```

------

# 十四、当前代码能力

经过 Day 02 学习，目前已经可以独立完成：

- 使用 `dataclass` 定义业务 DTO；
- 理解 `__init__()`、`__repr__()` 和 `__eq__()`；
- 使用可选类型表示兼容接口中的缺失字段；
- 将 SDK 原始 Response 转换为 `LLMResult`；
- 使用 `Iterator` 和 `yield` 编写生成器函数；
- 理解生成器的暂停与恢复；
- 使用 `stream=True` 发起流式模型调用；
- 从 `delta.content` 提取增量文本；
- 使用 `StreamEvent` 统一流式事件；
- 获取流式调用中的实际模型、停止原因和 Usage；
- 处理最终 usage chunk 中 `choices=[]` 的情况；
- 实时输出并使用 `join()` 聚合完整回答；
- 使用 `messages` 实现多轮对话；
- 区分 system、user 和 assistant；
- 使用 `while True` 实现命令行聊天循环；
- 使用 `break`、`continue` 控制会话；
- 在模型失败时回滚刚加入的 user 消息；
- 将重复的流消费逻辑抽取成独立函数。

------

# 十五、面试表达

## 问题：为什么要封装模型调用结果？

> 我没有让模型客户端只返回回答字符串，而是使用 Python 的 `dataclass` 定义了 `LLMResult`，统一封装回答内容、实际模型、停止原因以及输入、输出和总 Token 数。它类似于 Java 中的 DTO。这样上层业务不需要依赖 OpenAI SDK 的具体响应结构，也方便后续增加日志、成本统计和模型调用监控。对于兼容接口可能缺失的 Usage 字段，我使用 `int | None` 表达可选状态。

------

## 问题：流式输出是如何实现的？

> 我在 Chat Completions 请求中开启 `stream=True`，SDK 会返回一个可以迭代的响应流。普通响应从 `message.content` 获取完整消息，而流式响应从每个 chunk 的 `delta.content` 获取本次新增文本。模型客户端将非空文本封装为 `StreamEvent` 并通过 `yield` 逐个产生，调用方负责实时展示和收集完整回答。流式输出主要降低用户感知的首 Token 等待时间，不一定缩短完整生成时间，也不会天然减少 Token 数。

------

## 问题：为什么模型客户端不直接打印文本？

> 模型客户端只负责与模型服务交互并转换响应，不应该依赖具体展示方式。调用方可以选择将文本打印到终端，也可以通过 SSE、WebSocket 推送给前端，或者在测试中收集到列表。如果在客户端内部直接打印，就会让模型调用层与命令行界面耦合，降低复用性。

------

## 问题：多轮对话是如何实现的？

> Chat Completions 请求本身是无状态的，模型不会自动读取上一次 API 调用。应用程序需要维护 `messages`，保存 system、user 和 assistant 消息，并在每轮调用时重新发送所需历史。流式回答结束后，我会将所有文本片段拼接成一条完整 assistant 消息，再加入上下文，而不会把每个 chunk 分别加入历史。

------

## 问题：为什么需要保存 Assistant 的历史回答？

> 后续问题可能直接依赖模型之前的回答。例如用户先要求模型给出三个方案，下一轮再说“详细解释第二个”。如果只保存 user 消息，模型不知道“第二个”具体指什么。因此一轮普通对话需要同时保存 user 问题和 assistant 回答。

------

## 问题：流式响应中的停止原因和 Usage 如何处理？

> 开启 `include_usage` 后，停止原因和 Token Usage 通常不在同一个 chunk 中。`finish_reason` 表示模型已经停止生成文本，但服务端后面仍可能发送最终 usage chunk。该 usage chunk 的 `choices` 可能为空，所以不能无条件访问 `choices[0]`。我的做法是在遍历过程中分别暂存停止原因和 Token 数据，等整个流正常结束后，再统一产生一个 finish 事件。

------

# 十六、Day 02 未完成与后续任务

由于时间原因，今日没有继续实现最近 N 轮上下文截断。

当前 `messages` 会随着对话不断增长，存在以下问题：

- 输入 Token 持续增加；
- 请求成本和延迟上升；
- 旧信息可能干扰当前问题；
- 最终可能超过模型上下文窗口。

下一阶段优先完成：

1. 实现最近 N 轮上下文截断；
2. 始终保留 system 消息；
3. 正确处理最新 user 尚未获得 assistant 回答的情况；
4. 保证截断函数不直接修改原始列表；
5. 测试少于、等于和超过最大轮数的边界；
6. 补充 Token 级截断与历史摘要的设计思路；
7. 完成多轮对话和上下文管理的面试表达；
8. 继续算法题训练。

------

# 十七、今日易错点速查

```text
普通完整回答：
response.choices[0].message.content

流式增量回答：
chunk.choices[0].delta.content

数据类初始化：
__init__()

开发者字符串表示：
__repr__()

对象字段比较：
__eq__()

流式文本事件：
event_type = "content"

流式结束事件：
event_type = "finish"

流式 Usage：
stream_options={"include_usage": True}

最终 usage chunk：
chunk.choices 可能为空

多轮角色：
system / user / assistant

退出循环：
break

跳过当前轮：
continue

流式文本拼接：
"".join(text_parts)
```

------

# 十八、下次开启学习时使用的提示词

我正在执行“从 Java 后端转向 AI 应用开发”的学习计划。

Day 02 已完成以下内容：

- 使用 `@dataclass` 定义 `LLMResult`，统一封装回答内容、实际模型、停止原因和 Token 使用量；
- 理解 `__init__()`、`__repr__()` 和 `__eq__()`；
- 将 OpenAI SDK 原始 Response 转换为业务结果对象；
- 学习 Python 生成器、`Iterator`、`yield` 以及暂停和恢复机制；
- 使用 `stream=True` 实现 Chat Completions 流式调用；
- 从 `chunk.choices[0].delta.content` 提取增量文本；
- 使用 `print(..., end="", flush=True)` 实时展示；
- 使用列表收集文本片段，并通过 `"".join()` 聚合完整回答；
- 定义 `StreamEvent`，区分 content 和 finish 事件；
- 使用 `stream_options={"include_usage": True}` 获取流式 Token 统计；
- 正确处理最终 usage chunk 中 `choices=[]` 的情况；
- 将流式事件聚合为最终 `LLMResult`；
- 使用 `messages` 保存 system、user 和 assistant 历史；
- 使用 `while True`、`break` 和 `continue` 实现多轮命令行对话；
- 实现空输入校验、退出命令、`/history` 和模型调用失败后的消息回滚；
- 将一次流式调用和结果聚合逻辑抽取为独立函数；
- 已验证模型能够记住前文并理解跨轮指代。

尚未完成最近 N 轮上下文截断。

请继续按照“知识点讲解 → 小实验 → 我独立编码 → 代码检查 → 面试表达”的方式指导我。

下一步优先学习：

1. 最近 N 轮上下文截断；
2. 始终保留 system 和最新未回答的 user；
3. 上下文管理边界测试；
4. Token 截断和历史摘要的演进方案；
5. 完成多轮对话与上下文管理的面试表达。