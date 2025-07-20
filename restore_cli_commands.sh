#!/bin/bash
# Script to restore all CLI commands after debugging

echo "🔄 Restoring all CLI commands..."

if [ -f "cli_commands_full.py" ]; then
    mv cli_commands.py cli_commands_debug.py
    mv cli_commands_full.py cli_commands.py
    echo "✅ All CLI commands restored!"
    echo "💡 To debug again, run: mv cli_commands.py cli_commands_full.py && mv cli_commands_debug.py cli_commands.py"
else
    echo "❌ Full CLI commands file not found (cli_commands_full.py)"
    echo "💡 You may need to restore from git or recreate the full file"
fi
