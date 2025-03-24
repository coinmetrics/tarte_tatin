# Installation Guide for Tarte Tatin

Follow these steps to get Tarte Tatin up and running on your machine.

## Prerequisites

- Docker
- Python 3.10+
- pip or uv package installer

## Installation Steps

1. **Extract the archive**
   ```bash
   unzip tarte_tatin.zip -d tarte_tatin
   cd tarte_tatin
   ```

2. **Set up environment variable**
   ```bash
   # Linux/macOS
   export CM_API_KEY=your_coinmetrics_api_key
   
   # Windows (PowerShell)
   $env:CM_API_KEY="your_coinmetrics_api_key"
   ```

3. **Build the Docker container**
   ```bash
   docker build -t python-runner .
   ```

4. **Install Python dependencies**
   ```bash
   # Using pip
   pip install -e .
   
   # Or using uv
   uv pip install -e .
   ```

## Verification

1. **Run the Coin Metrics example**
   ```bash
   python cm_1.py
   ```

2. **Test the code executor**
   ```bash
   python code_executor.py
   ```
   
   Then in another terminal or script, use the MCP client to execute code.

## Troubleshooting

- **Docker build issues**: Ensure Docker is running and you have appropriate permissions
- **API Key errors**: Double-check your CM_API_KEY environment variable is set correctly
- **Missing dependencies**: Ensure all requirements are installed with `pip install -r requirements.txt`

For additional help, refer to the README.md file or contact support.