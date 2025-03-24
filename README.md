# Tarte Tatin

A secure Python code execution service that runs code in isolated Docker containers.

To use Coinmetrics specific code, you should provide the contents of the instructions.md file in the context for the LLM.
If it's possible to store this in a system prompt, do that.

## Features

- Execute Python code securely in isolated Docker containers
- Automatic dependency detection and installation
- Coinmetrics API integration for cryptocurrency data analysis
- File output management with size and quantity limits

## Setup

### Prerequisites

- Docker
- Python 3.10+
- uv (Python package installer)

### Installation

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

4. Install Python dependencies:
   ```
   pip install -e .
   ```

## Usage

To enable `python-runner` in Claude Desktop modify the file `claude_desktop_config.json`

```json
{
  "mcpServers": {
    "Python Runner": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "--with",
        "python-dotenv",

        "mcp",
        "run",
        "<suitable path>/tarte_tatin/code_executor.py"
      ],
      "env": {
        "CM_API_KEY" : "<your key>"
      }
    }
  }
}
```

### Running the MCP Server

This will not do much -- check out [MCP Site](https://github.com/modelcontextprotocol/python-sdk) for more details on how to test 
only the MCP server.

```python
python code_executor.py
```

### Example Code Execution

```python
from mcp.client import Client

client = Client()
result = client.run_python_code(code="""
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.savefig('sine_wave.png')
print("Sine wave plotted and saved!")
""")

print(result)
```

### Coin Metrics Example

```python
python cm_1.py
```

## Containers

The Docker container includes:
- Python 3.9
- Essential data science libraries (pandas, matplotlib, numpy)
- Coinmetrics API client
- Automatic dependency installation using uv

## Security

Code executes in an isolated container with:
- Limited file access
- Controlled output file management
- No network access except for package installation

## License

[Your License]