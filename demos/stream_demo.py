import time


def stream_output(text: str):
    print("开始调用")
    words = text.split()
    for index, word in enumerate(words, start=1):
        time.sleep(0.2)
        yield word
    print("\n结束调用")


def observe_generator():
    print("打印开始")
    yield "a"
    print("打印恢复")
    yield "b"
    print("打印结束")


def main():
    result = stream_output("Python generator supports streaming output")
    print("生成器已创建")

    for chunk in result:
        print(chunk, end=" ", flush=True)

    generator = observe_generator()

    print("生成器已创建")
    print(next(generator))
    print("第一次 next 完成")
    print(next(generator))
    print("第二次 next 完成")

    try:
        print(next(generator))
    except StopIteration:
        print("generator is exhausted")


if __name__ == "__main__":
    main()
