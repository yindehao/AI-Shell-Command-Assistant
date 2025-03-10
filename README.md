

# AI Shell Command Assistant

AI Shell Command Assistant 是一个基于 AI 的命令行工具，能够将自然语言提示（prompt）转换为 Shell 命令，或者解释给定的 shell 命令。
同时支持将生成的命令复制到剪贴板，方便用户直接使用。

## 功能特性

- **生成命令**：将自然语言提示转换为终端命令，并复制到粘贴板。
- **解释命令**：对给定的 shell 命令进行解释。
- **帮助信息**：提供详细的命令行参数说明。
- **流式输出**：支持流式输出结果。

## 安装

1. 克隆项目到本地：
   ```bash
   git clone https://github.com/yindehao/AI-Shell-Command-Assistant.git
   cd AI-Shell-Command-Assistant
   ```

2. 安装依赖：
   确保你已安装 Python 3.8 或更高版本，然后运行：
   ```bash
   pip install -r requirements.txt
   ```
   
3. 配置调用大语言模型所需环境变量


3.1 MacOS

   - 配置环境变量，包括大模型的 API Key 和模型名称、API 地址
   ```zsh
   vim ~/.zshrc
   export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   export OPENAI_API_BASE="https://api.openai.com/v1"
   export OPENAI_MODEL="deepseek-chat"
   ```

   - 添加别名，方便调用
   ```zsh
   echo "alias ask='python3 $(pwd)/scripts/ai.py'" >> ~/.zshrc
   source ~/.zshrc
   ```

3.2 Windows

   - 配置环境变量，包括大模型的 API Key 和模型名称、API 地址
   ```cmd
   setx OPENAI_API_KEY "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   setx OPENAI_API_BASE "https://api.openai.com/v1"
   setx OPENAI_MODEL "deepseek-chat"
   ```

   - 添加别名，方便调用
   ```cmd
   doskey ask=python3 $(pwd)/scripts/ai.py $*
   ```

3.3 Linux

   - 配置环境变量，包括大模型的 API Key 和模型名称、API 地址
   ```bash
   vim ~/.bashrc
   export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   export OPENAI_API_BASE="https://api.openai.com/v1"
   export OPENAI_MODEL="deepseek-chat"
   ```

   - 添加别名，方便调用
   ```bash
   echo "alias ask='python3 $(pwd)/scripts/ai.py'" >> ~/.bashrc
   source ~/.bashrc
   ```



## 使用方法

### 查看帮助信息
运行以下命令查看工具的使用说明：
```bash
ai -h
```

输出示例：
```
usage: ai [-h] [-e] [-v] [prompt ...]

Translate your prompt to zsh command and copy to clipboard.

positional arguments:
  prompt         The prompt to generate shell command or explain.

optional arguments:
  -h, --help     Show this help message and exit.
  -e, --explain  Explain the given command.
  -v, --version  Show version information.
```

### 生成命令
输入自然语言提示，生成对应的 zsh 命令：
```bash
ai "查看当前运行的 Python 程序"
```
输出示例：
```bash
ps aux | grep python
```

### 解释命令
使用 `-e` 或 `--explain` 参数解释给定的 shell 命令：
```bash
ai -e "top -l 1 | grep PhysMem"
```

### 查看版本信息
运行以下命令查看工具的版本号：
```bash
python scripts/ai.py -v
```

## 项目结构

```
ai-shell-command-assistant/
├── scripts/
│   └── ai.py          # 主程序文件
├── requirements.txt    # Python 依赖文件
└── README.md           # 项目说明文档
```

## 贡献

欢迎对本项目进行贡献！请按照以下步骤提交你的贡献：

1. Fork 本仓库。
2. 创建一个新的分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. 提交你的更改：
   ```bash
   git commit -m "Add your feature description"
   ```
4. 推送到你的分支：
   ```bash
   git push origin feature/your-feature-name
   ```
5. 创建一个 Pull Request。

## 许可证

本项目采用 [MIT License](LICENSE) 进行许可。

---

感谢使用 AI Shell Command Assistant！如果你有任何问题或建议，请随时提交 Issue。
