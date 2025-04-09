import os
import json
import getpass
import sys
from pathlib import Path


def main():
    # 1. Check if CM_API_KEY environment variable is set
    cm_api_key = os.environ.get('CM_API_KEY')
    if not cm_api_key:
        cm_api_key = getpass.getpass("CM_API_KEY not found in environment. Please enter your CM_API_KEY: ")
        if not cm_api_key:
            print("Error: CM_API_KEY is required to continue.")
            sys.exit(1)

    # 2. Determine the absolute path of code_executor.py in the same directory
    current_script_path = Path(__file__).resolve()
    code_executor_path = current_script_path.parent / "code_executor.py"

    if not code_executor_path.exists():
        print(f"Error: code_executor.py not found at {code_executor_path}")
        sys.exit(1)

    # 3. Determine the correct Claude config path based on platform
    home_dir = Path.home()

    # macOS: ~/Library/Application Support/Claude/
    # Windows: %APPDATA%\Claude\
    # Linux: ~/.config/Claude/
    if sys.platform == "darwin":  # macOS
        config_dir = home_dir / "Library" / "Application Support" / "Claude"
    elif sys.platform == "win32":  # Windows
        config_dir = Path(os.environ.get("APPDATA", str(home_dir / "AppData" / "Roaming"))) / "Claude"
    else:  # Linux and others
        config_dir = home_dir / ".config" / "Claude"

    config_path = config_dir / "claude_desktop_config.json"

    # Create directory structure if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)

    # Read existing config or create new one
    config = {}
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Existing config file at {config_path} is not valid JSON. Creating new config.")

    # Update config with MCP server configuration
    if 'mcpServers' not in config:
        config['mcpServers'] = {}

    config['mcpServers']['Python Runner'] = {
        "command": "uv",
        "args": [
            "run",
            "--with",
            "mcp[cli]",
            "--with",
            "python-dotenv",
            "mcp",
            "run",
            str(code_executor_path)
        ],
        "env": {
            "CM_API_KEY": cm_api_key
        }
    }

    # Write updated config back to file
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"Configuration updated successfully at {config_path}")
    print("The Claude application can now use the MCP server with the Python Runner configuration.")


if __name__ == "__main__":
    main()