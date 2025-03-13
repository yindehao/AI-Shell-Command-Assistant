#!/usr/bin/env python3
import os
import sys
from typing import Union, Generator, Any, Optional

from openai import OpenAI
import pyperclip  # 导入 pyperclip 库, 用于复制命令到剪贴板

import platform

def get_os_type():
    os_type = platform.system()
    if os_type == 'Windows':
        return 'Windows'
    elif os_type == 'Darwin':
        return 'MacOS'
    elif os_type == 'Linux':
        return 'Linux'
    else:
        return 'Unknown'
    
# 设置 OpenAI API 密钥
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
    base_url = os.getenv("OPENAI_API_BASE")
)
default_model = os.getenv("OPENAI_MODEL","deepseek-chat")

shell_prompt = """
角色与能力: 你是一位**${os_platform}**终端命令行专家，擅长根据用户的具体需求提供相应的终端命令解决方案。

任务描述: 根据用户的请求生成一条或一系列的终端命令来完成特定的任务。请确保提供的命令准确无误且直接针对用户提出的需求。

指令内容: ${command}

输出要求:
- 仅输出所需的终端命令纯文本，不需要使用```等代码块包裹。
- 不需要对命令进行额外解释或说明。
- 请务必根据当前${os_platform}终端提供命令。
""".replace("${os_platform}", get_os_type()).lstrip()

explain_prompt = """
任务指令：根据用户提供的终端命令，解释该命令的具体含义和功能。

回答格式：采用清晰易懂的语言，直接基于命令的官方文档或常见用法来解释其作用。确保解释准确无误，并且易于理解。

注意事项：

1. 请用户明确提供他们想要了解的终端命令。
2. 解释时，请包括命令的基本语法、主要参数及其作用。
3. 如果适用，可以简要说明该命令在实际操作中的应用场景。
4. 确保解释内容简洁明了，避免不必要的技术细节，除非这些细节对于理解命令至关重要。

指令内容: ${command}
""".lstrip()

help_text = """
Usage: ai <your prompt>

Description:
  This command translate your prompt to zsh command and copy to clipboard.

Options:
  -h, --help    Show this help message and exit.
  -e, --explain Explain the command.
  -v, --version Show version information.

Examples:
  ai 查看当前运行python程序
  ai -e "top -l 1 | grep PhysMem"
    """.lstrip()



def call_llm(prompt:str, stream:bool=False, model:str=default_model):
    """
    Calls the OpenAI API to generate a response based on the given prompt.

    Args:
        prompt (str): The prompt to send to the OpenAI API.
        stream (bool, optional): Whether to stream the response. Defaults to False.
        model (str, optional): The model to use for the API call. Defaults to default_model.

    Yields:
        str: The content of the response if streaming is enabled.

    Returns:
        str: The content of the response if streaming is not enabled.
        str: An error message if the API call fails.
    """
    try:

        result = client.chat.completions.create(
            model = model,
            messages=[{"role": "user", "content":  prompt}],
            temperature=0.7,
            stream=stream
        )
        if stream:
            for chunk in result:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
            yield "\n"
        else:
            return result.choices[0].message.content
    except Exception as e:
        return f"Error calling OpenAI API: {e}"
    
def show_help():
    """
    显示帮助信息
    """
    print(help_text)


def generate_shell_command(prompt):
    result = call_llm(shell_prompt.replace("${command}", prompt), True)
    command = ""
    for content in result:
        print(content, end="", flush=True)
        command += content
    try:
        # 将结果复制到剪贴板
        pyperclip.copy(command)
        # print("[已复制到剪贴板]")
    except Exception as e:
        print(f"[无法复制到剪贴板: {e}]")


def main():
    # 获取用户输入的命令
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    # 检查是否显示帮助信息
    if len(sys.argv) == 2:
        if sys.argv[1] in ("-h", "--help"):
            show_help()
            sys.exit(0)
        elif sys.argv[1] in ("-v", "--version"):
            print("Version 0.0.1")
            sys.exit(0)
        else:
            generate_shell_command(" ".join(sys.argv[1:]))

    elif len(sys.argv) >= 3 and sys.argv[1] in ("-e", "--explain"):
        prompt = " ".join(sys.argv[2:])
        result = call_llm(explain_prompt.replace("${command}", prompt), True)
        for content in result:
            print(content, end="", flush=True)
        print()
        sys.exit(0)
    else:
        prompt = " ".join(sys.argv[1:])
        generate_shell_command(prompt)


if __name__ == "__main__":
    main()
