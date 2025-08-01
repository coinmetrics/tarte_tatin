#!/bin/bash
set -e

# Display build info
if [ -f /app/build_info ]; then
    echo "=== Build Information ==="
    cat /app/build_info
    echo "Built on: $(cat /app/build_timestamp)"
    echo "======================="
fi


echo "Analyzing script dependencies..."

# Use the script filename from environment variable, default to script.py for backward compatibility
SCRIPT_FILE=${SCRIPT_FILENAME:-script.py}
SCRIPT_PATH="/tmp/$SCRIPT_FILE"

# Explicitly check for coinmetrics in the script
if grep -q "coinmetrics" "$SCRIPT_PATH"; then
    echo "Coinmetrics dependency detected, installing required packages..."
    # Install with uv
    uv pip install --system coinmetrics-api-client coinmetrics
    echo "Coinmetrics packages installed with uv."
fi

# Extract import statements to identify required packages
PACKAGES=$(grep -oP "^import \K[\w]+" "$SCRIPT_PATH" | tr '\n' ' ')
PACKAGES+=$(grep -oP "^from \K[\w]+" "$SCRIPT_PATH" | tr '\n' ' ')

# Install any packages that were imported but not installed
if [ ! -z "$PACKAGES" ]; then
    echo "Detected imports: $PACKAGES"
    echo "Installing packages with uv..."
    for pkg in $PACKAGES; do
        # Skip standard library modules
        if ! python -c "import $pkg" 2>/dev/null; then
            echo "Installing $pkg..." || continue # Skip iteration if the installation fails (and error output is empty, use `set -x` for debugging )
            if ! uv pip install --system "$pkg"; then
                echo "Failed the to install $pkg, stopping the execution."
                exit 1
            fi
        else
            echo "$pkg is already available."
        fi
    done
fi

echo "Running script..."
# Execute the Python code using the dynamic script filename
python "$SCRIPT_PATH"
