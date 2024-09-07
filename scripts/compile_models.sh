#!/bin/bash

echo "Started model compilation!"
for filename in models/*.py; do
    python "$filename" > /dev/null 2>&1
    echo "Compiled $filename!"
done
