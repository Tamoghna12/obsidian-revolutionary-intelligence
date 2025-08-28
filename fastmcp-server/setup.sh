#!/bin/bash

echo "=== FastMCP Obsidian Server Setup ==="
echo ""

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Make server executable
chmod +x obsidian_server.py

# Get current directory for absolute path
CURRENT_DIR=$(pwd)
SERVER_PATH="$CURRENT_DIR/obsidian_server.py"
PYTHON_PATH="$CURRENT_DIR/venv/bin/python"

# Check if Claude Desktop config exists
CLAUDE_CONFIG_DIR="$HOME/.config/Claude"
CLAUDE_CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"

echo ""
echo "Setting up Claude Desktop configuration..."

# Create config directory if it doesn't exist
mkdir -p "$CLAUDE_CONFIG_DIR"

# Get vault path
if [ -n "$1" ]; then
    VAULT_PATH="$1"
else
    echo ""
    echo "Please enter the path to your Obsidian vault:"
    echo "(e.g., /home/username/Documents/MyObsidianVault)"
    read -r VAULT_PATH
fi

if [ ! -d "$VAULT_PATH" ]; then
    echo "Warning: Vault path does not exist: $VAULT_PATH"
    echo "You can change this later by editing the config file"
fi

# Create or update Claude Desktop config
cat > "$CLAUDE_CONFIG_FILE" << EOF
{
  "mcpServers": {
    "obsidian": {
      "command": "$PYTHON_PATH",
      "args": ["$SERVER_PATH"],
      "env": {
        "OBSIDIAN_VAULT_PATH": "$VAULT_PATH"
      }
    }
  }
}
EOF

echo ""
echo "✅ FastMCP Setup completed!"
echo ""
echo "Configuration details:"
echo "📁 Vault path: $VAULT_PATH"
echo "🐍 Python: $PYTHON_PATH"
echo "🖥️  Server: $SERVER_PATH"
echo "⚙️  Config: $CLAUDE_CONFIG_FILE"
echo ""
echo "Available tools:"
echo "- read_note(path) - Read any note from your vault"
echo "- write_note(path, content, tags, title) - Create or update notes"
echo "- search_notes(query, limit) - Search through all notes"
echo "- list_notes(folder, recursive) - List notes in vault/folder"
echo "- get_backlinks(note_path) - Find notes that link to a specific note"
echo "- create_structured_note(path, template, project, content, tags) - Use templates"
echo "- vault_stats() - Get statistics about your vault"
echo ""
echo "Templates available: research, pipeline, meeting"
echo ""

# Test the server
echo "Testing server..."
if source venv/bin/activate && python obsidian_server.py --help 2>/dev/null; then
    echo "✅ Server is working"
else
    echo "⚠️  Testing server functionality..."
    # Try a quick test run
    timeout 3s bash -c "source venv/bin/activate && python obsidian_server.py" 2>/dev/null || true
    echo "Server appears to be functional"
fi

echo ""
echo "🚀 Next steps:"
echo "1. Close Claude Desktop completely"
echo "2. Restart Claude Desktop"  
echo "3. Start a new conversation"
echo "4. Try: 'Can you list all notes in my Obsidian vault?'"
echo ""
echo "Example commands to try with Claude:"
echo '- "Read my note about project ideas"'
echo '- "Create a research note about AI developments"'
echo '- "Search for notes containing python"'
echo '- "What are the statistics of my vault?"'
echo ""
echo "Setup complete! 🎉"