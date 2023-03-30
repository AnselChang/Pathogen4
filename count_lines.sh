#!/bin/bash

# Find all .py files in the current directory and its subdirectories
files=$(find . -name "*.py")

# Count the total number of lines of code in the .py files
total_lines=0
for file in $files; do
    lines=$(wc -l < "$file")
    total_lines=$((total_lines + lines))
done

# Print the total number of lines of code
echo "Total number of lines of code in .py files: $total_lines"

