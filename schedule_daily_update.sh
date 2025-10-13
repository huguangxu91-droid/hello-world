#!/bin/bash
# Daily AI News Update Script
# This script updates the AI news data

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "========================================"
echo "AI Daily News Update - $(date)"
echo "========================================"

# Run the news fetch script
python3 fetch_ai_news.py

if [ $? -eq 0 ]; then
    echo "News update completed successfully!"
else
    echo "Error: News update failed!"
    exit 1
fi

echo "========================================"
