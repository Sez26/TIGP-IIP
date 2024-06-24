#!/usr/bin/bash

## opening the .lmp files in Ovito
## THIS DON'T WORK FOR ME 
# Add OVITO to PATH
OVITO_PATH=$(which ovito)
if [ -n "$OVITO_PATH" ]; then
    OVITO_DIR=$(dirname $OVITO_PATH)
    export PATH=$PATH:$OVITO_DIR
    echo "OVITO directory ($OVITO_DIR) added to PATH."
else
    echo "ovito executable not found in PATH."
fi

# Loop through all .lmp files in the current directory
for file in *.lmp; 
do 
    # Open each .lmp file with OVITO
    ovito "$file" &
done

