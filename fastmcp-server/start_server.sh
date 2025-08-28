#!/bin/bash

# Obsidian Revolutionary Intelligence Server Startup Script

echo "🚀 Starting Obsidian Revolutionary Intelligence MCP Server"
echo "======================================================"

# Check if we're in the right directory
if [ ! -f "obsidian_server.py" ]; then
    echo "❌ Error: obsidian_server.py not found in current directory"
    echo "Please run this script from the fastmcp-server directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found, creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "✅ Virtual environment found"
    source venv/bin/activate
fi

# Check if OBSIDIAN_VAULT_PATH is set
if [ -z "$OBSIDIAN_VAULT_PATH" ]; then
    echo "⚠️  OBSIDIAN_VAULT_PATH not set"
    echo "Please set your Obsidian vault path:"
    echo "  export OBSIDIAN_VAULT_PATH='/path/to/your/obsidian/vault'"
    echo "Or run the setup.sh script first"
    exit 1
fi

echo "📁 Using Obsidian Vault: $OBSIDIAN_VAULT_PATH"

# Check if vault path exists
if [ ! -d "$OBSIDIAN_VAULT_PATH" ]; then
    echo "⚠️  Warning: Vault path does not exist: $OBSIDIAN_VAULT_PATH"
    echo "The server will start but may not function properly"
fi

echo ""
echo "📡 Server starting on port 3000..."
echo "💡 To stop the server, press Ctrl+C"
echo "📝 Logs will be displayed below:"
echo ""

# Run the server
python obsidian_server.py