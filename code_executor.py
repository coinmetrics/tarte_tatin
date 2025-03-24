from typing import Any, Dict, List
import json
import subprocess
import sys
import os
import tempfile
import shutil
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("python-executor")

import os

api_key = os.environ.get('CM_API_KEY')
if not api_key:
    raise ValueError("CM_API_KEY environment variable is not set")


@mcp.tool()
async def run_python_code(code: str  # ,
                          # packages: List[str] = None
                          ) -> Dict[str, Any]:
    """Run Python code in an isolated Docker container.

    Args:
        code: Python code to execute
        packages: Optional packages to install before execution

    Returns:
        Execution results including stdout and stderr
    """

    print(f"Received code: {code}", file=sys.stderr)
    # print(f"Received packages: {packages}", file=sys.stderr)

    packages = ''
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    print(f"Created temporary directory: {temp_dir}", file=sys.stderr)

    # Create a temporary file with the code *inside* the temporary directory
    code_file = os.path.join(temp_dir, "script.py")
    with open(code_file, "w") as f:
        f.write(code)

    # Prepare Docker command
    docker_cmd = [
        "docker",
        "run",
        "-e",
        f"CM_API_KEY={api_key}",
        "--rm",
        "-v",
        f"{temp_dir}:/tmp",  # Mount the temporary directory
        "python-runner"
    ]

    # Add packages parameter if provided
    cmd_args = []
    if packages and len(packages) > 0:
        packages_str = ",".join(packages)
        cmd_args.extend(["--packages", packages_str])

    # Run the Docker container
    result = subprocess.run(
        docker_cmd + cmd_args,
        capture_output=True,
        text=True
    )

    # Handle the output files
    user_dir = os.path.expanduser("~")  # User's home directory
    output_dir = os.path.join(user_dir, "output_files")
    os.makedirs(output_dir, exist_ok=True)

    saved_files = []
    total_size = 0
    file_count = 0

    try:
        for filename in os.listdir(temp_dir):
            filepath = os.path.join(temp_dir, filename)
            if os.path.isfile(filepath) and filename != "code_to_run.py":  # Don't copy the input file
                file_size = os.path.getsize(filepath)

                # Safety checks
                if file_count >= 5:
                    print("Too many files. Skipping...", file=sys.stderr)
                    break
                if total_size + file_size > 10 * 1024 * 1024:  # 10 MB limit
                    print("Total size limit exceeded. Skipping...", file=sys.stderr)
                    break

                # Move the file
                output_path = os.path.join(output_dir, filename)
                shutil.move(filepath, output_path)
                saved_files.append(filename)
                total_size += file_size
                file_count += 1


    except Exception as e:
        print(f"Error handling output files: {e}", file=sys.stderr)

    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)
        print(f"Removed temporary directory: {temp_dir}", file=sys.stderr)

    # Return the results
    return {
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "exit_code": result.returncode,
        "saved_files": saved_files
    }


if __name__ == "__main__":
    # Run the MCP server
    mcp.run(transport='stdio')
