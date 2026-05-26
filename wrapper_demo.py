from wrapper import run


def init():
    print("initializing worker...")


def handler(event):
    prompt = event.get("prompt", "")
    max_tokens = event.get("max_tokens", 100)
    temperature = event.get("temperature", 0.7)

    return {
        "generated_text": f"Response to: {prompt}",
        "max_tokens": max_tokens,
        "temperature": temperature,
    }


if __name__ == "__main__":
    run(handler, init=init)
