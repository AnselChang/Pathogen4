#!/bin/bash

# Find all .py files in the current directory and its subdirectories
files=$(find . -name "*.$1")

# Count the total number of lines of code and Python classes in the files
total_lines=0
class_count=0
for file in $files; do
    lines=$(wc -l < "$file")
    total_lines=$((total_lines + lines))
    count=$(grep -c "^class" "$file")
    class_count=$((class_count + count))
done

# Print the total number of lines of code and Python classes
echo "Total number of lines of code in .$1 files: $total_lines"
echo "Total number of classes: $class_count"
echo "Average lines of code per class: $((total_lines / class_count))"

