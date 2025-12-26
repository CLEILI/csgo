#!/bin/bash


PYTHON_SCRIPT="allnames.py"

while true; do
    echo "$(date): try to run code..."
    
    
    python3 "$PYTHON_SCRIPT"
    
    
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
        echo "$(date): Successful!"
        break
    else
        echo "$(date): Failed exit code: $EXIT_CODE, retry in 10 seconds..."
        sleep 10
    fi
done