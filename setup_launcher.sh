#!/bin/bash

# Remove the old cron job
crontab -l 2>/dev/null | grep -v "ai-viral-snippets" | crontab -

# Get paths
PLIST_NAME="com.ai.viral.snippets.plist"
PLIST_PATH="/Users/krolya/PythonProjects/ai-viral-snippets/$PLIST_NAME"
TARGET_DIR="$HOME/Library/LaunchAgents"

mkdir -p "$TARGET_DIR"

# Copy plist to LaunchAgents
cp "$PLIST_PATH" "$TARGET_DIR/"

# Load the job
launchctl unload "$TARGET_DIR/$PLIST_NAME" 2>/dev/null
launchctl load "$TARGET_DIR/$PLIST_NAME"

echo "Scheduler migrated to launchd."
echo "The app will run daily at 9:00 AM."
echo "Logs: automation_stdout.log and automation_stderr.log"
