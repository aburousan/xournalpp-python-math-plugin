#!/usr/bin/env bash

# 1. Prioritize Conda environments (Conda Python has proper Tkinter GUI support on macOS)
if command -v conda >/dev/null 2>&1; then
    envs=$(conda env list | grep -v '^#' | awk '{print $2}')
    for env_path in $envs; do
        py="$env_path/bin/python"
        if [ -x "$py" ]; then
            if "$py" -c "import numpy, matplotlib, scipy, sympy" >/dev/null 2>&1; then
                echo "$py"
                exit 0
            fi
        fi
    done
fi

# 2. Check explicitly known good Conda paths just in case conda isn't in PATH
CANDIDATES=(
    "$HOME/miniconda3/envs/analysis/bin/python"
    "$HOME/miniconda3/bin/python"
    "$HOME/anaconda3/bin/python"
    "/opt/homebrew/bin/python3"
    "python3"
    "python"
    "/usr/local/bin/python3"
    "/usr/bin/python3"
)

for py in "${CANDIDATES[@]}"; do
    if command -v "$py" >/dev/null 2>&1; then
        # Check if it has the required packages
        if "$py" -c "import numpy, matplotlib, scipy, sympy" >/dev/null 2>&1; then
            # Print the absolute path to the executable
            "$py" -c "import sys; print(sys.executable)"
            exit 0
        fi
    fi
done

exit 1
