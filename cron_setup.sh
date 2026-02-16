#!/bin/bash

# Get the absolute path of the current directory
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PYTHON_PATH=$(which python3)

# Define the command to run
# We use -u to fly through output and > to log everything
CRON_COMMAND="cd $PROJECT_DIR && $PYTHON_PATH main.py >> $PROJECT_DIR/cron.log 2>&1"

# Check if the cron job already exists
(crontab -l 2>/dev/null | grep -F "$PROJECT_DIR/main.py") && echo "Cron job already exists." && exit 0

# Add the cron job (runs daily at 9:00 AM)
(crontab -l 2>/dev/null; echo "0 9 * * * $CRON_COMMAND") | crontab -

echo "Daily cron job scheduled at 9:00 AM."
echo "Logs will be available at $PROJECT_DIR/cron.log"
