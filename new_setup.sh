#!/usr/bin/env bash

# Use Homebrew Python
/opt/homebrew/bin/python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies (if present)
pip install -r requirements.txt

# (Optional) Tell VS Code to use this venv
mkdir -p .vscode
cat > .vscode/settings.json <<EOF
{
  "python.defaultInterpreterPath": "\${workspaceFolder}/venv/bin/python",
  "python.terminal.activateEnvironment": true
}
EOF

# Done
echo "Setup complete. Run: source venv/bin/activate"
