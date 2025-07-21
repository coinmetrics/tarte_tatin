# Tarte Tatin

A secure Python code execution service that runs code in isolated Docker containers.

To use Coinmetrics specific code, you should provide the contents of the instructions.md file in the context for the LLM.
If it's possible to store this in a system prompt, do that.

## Features

- Execute Python code securely in isolated Docker containers
- Automatic dependency detection and installation
- Coinmetrics API integration for cryptocurrency data analysis
- File output management with size and quantity limits

```mermaid
flowchart TD
    User([User])
    ClaudeDesktop[Claude Desktop]
    LLM[Large Language Model]
    CodeExecutor[CodeExecutor.py]
    PythonRunner[Python Runner Container]
    UserDir[(User Directory)]
    
    User -->|"Submits Prompt"| ClaudeDesktop
    ClaudeDesktop --> LLM
    LLM -->|"Generates & Submits Code"| CodeExecutor
    CodeExecutor -->|"Sends Code for Execution"| PythonRunner
    PythonRunner -->|"Returns Results"| CodeExecutor
    CodeExecutor -->|"Saves Code & Files (e.g., Visualizations)"| UserDir
    
    subgraph MCP[MCP Server]
        CodeExecutor
        subgraph Docker[Docker Environment]
            PythonRunner
        end
    end
    
    classDef user fill:#e1f5fe,stroke:#0288d1,stroke-width:1px
    classDef desktop fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
    classDef llm fill:#f3e5f5,stroke:#7b1fa2,stroke-width:1px
    classDef mcp fill:#e8eaf6,stroke:#3949ab,stroke-width:1px
    classDef docker fill:#fff3e0,stroke:#ef6c00,stroke-width:1px
    classDef storage fill:#e0f2f1,stroke:#00796b,stroke-width:1px
    
    class User user
    class ClaudeDesktop desktop
    class LLM llm
    class CodeExecutor mcp
    class PythonRunner docker
    class UserDir storage
```

## Setup

### Prerequisites

- Docker
- Python 3.10+
- uv (Python package installer)

### Installation

0. Install uv (Python package manager)

   ```
   brew install uv
   ```

1. Clone the repository:
   ```
   git clone <repository-url>
   cd tarte_tatin
   ```

2. Set required environment variables:
   ```
   export CM_API_KEY=your_coinmetrics_api_key
   ```

3. Build the Docker image:
   ```
   docker build -t python-runner .
   ```

4. Run install script:
   ```
   uv run install.py
   ```

5. Copy and paste the contents of `instructions.md` into your Claude Desktop preference


## Usage

Ask Claude a question such as "Create a candle graph of ETH-USD on kraken for 30 days"

Find any output in your home drive, in a folder called `output-files`

## Containers

The Docker container includes:
- Python 3.9
- Essential data science libraries (pandas, matplotlib, numpy)
- Coinmetrics API client
- Automatic dependency installation using uv

## Security

Code executes in an isolated container with:
- No access to local files (only an empty TMP directory)
- Controlled output file management: only max 5 files get copied to the users' `output-files` 
- Network access outbound for calling the API


