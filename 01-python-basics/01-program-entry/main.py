def greet(name: str) -> str:
    return f"Hello, {name}!"

print(f"main.py 中的 __name__:{__name__}")

if __name__ == "__main__":
  message = greet("Tingfeng")
  print(message)