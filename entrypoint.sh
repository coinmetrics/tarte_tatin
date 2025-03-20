#!/bin/bash
set -e

# Check if Python code is provided
if [ $# -eq 0 ]; then
    echo "Error: No Python code provided"
    echo "Usage: docker run image_name 'print(\"Hello, World!\")'"
    exit 1
fi

# Execute the Python code passed as argument
python -c "$@"
