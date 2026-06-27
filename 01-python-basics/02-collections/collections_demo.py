# 列表
"""models: list[str] = ["qwen","deepseak","gpt"]

print(models)
print(models[0])
print(models[-1])

models.append("doubao")
models[0] = "qwen-plus"
removed_model = models.pop()

print(models)
print(removed_model)

for model in models:
  print(model)"""

""" # 字典定义
message: dict[str,str] ={
  "role": "user",
  "content": "请解释什么是 RAG ?"
} 

# 读取
print(message["role"])
print(message["content"])

# 修改与新增
message["content"] = "请用简洁的语言解释什么是 RAG"
message["language"] = "zh-CN"

# 安全读取
name = message.get("name")
print(name)

# 不安全的读取 message[name], 如果不存在报错

# 返回默认值
name = message.get("name","unkown")
print(name)

# 遍历
for key, value in message.items():
  print(f"{key}:{value}") """
""" 
# list 和 dict 组合
messages: list[dict[str,str]] = [
  {
    "role": "sys",
    "content":"你是一名 AI 应用开发助手"
  },
  {
    "role": "user",
    "content": "请解释什么是 RAG"
  }
]

# 访问用户问题
print(f"用户问题：{messages[1]["content"]}")

# 遍历消息
for message in messages:
  print(f"消息的 role:{message["role"]}, 消息的 content:{message["content"]}")
 """

# tuple: 元组：不可修改的有序集合
# def get_useage() -> tuple[int,int]:
#   return 100,50

# input_tokens, output_tokens = get_useage()

# print(input_tokens)
# print(output_tokens)

# model_config: tuple[str,int,int] = ("qwen-plus",0.2,0.5)

# print(model_config[0])
# print(model_config[1])

# for config in model_config:
#   print(config)

# # set: 不重复元素集合
# skills: set[str] = {"Python","RAG","Agent","Python"}
# # 打印
# print(skills)

# # 增加
# skills.add("FastAPI")

# if "RAG" in skills:
#   print("已学习，RAG")

# for skill in skills:
#   print(skill)


def build_messages(system_prompt: str, user_prompt: str) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    return messages


# 调用函数
messages = build_message("你是一名面试助手", "什么是 Redis 缓存穿透？")
# 输出消息列表
print(messages)
# 输出用户问题
print(f'用户问题：{messages[1]["content"]}')

# 遍历每条消息
for message in messages:
    print(f'role:{message["role"]}, content:{message["content"]}')

# 添加 assistant 消息
messages.append({"role": "assistant", "content": "缓存穿透是指查询不存在的数据......"})
print(messages)
