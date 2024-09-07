#!/bin/bash

echo "Started model compilation!"
for filename in models/*.py; do
    python "$filename" > /dev/null
    echo "Compiled $filename!"
done
