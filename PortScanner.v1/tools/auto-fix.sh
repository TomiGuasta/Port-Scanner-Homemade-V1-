#!/bin/bash

echo "========================================="
echo "   AUTO FIX WINDOWS -> LINUX (Guasta)"
echo "========================================="

# Convert CRLF to LF
echo "[*] Fixing Windows line endings..."
find .. -type f -name "*.py" -exec sed -i 's/\r$//' {} \;

# Fix python shebang
echo "[*] Fixing python shebang..."
find .. -type f -name "*.py" -exec sed -i '1 s|^#!.*python.*|#!/usr/bin/env python3|' {} \;

# Permissions
echo "[*] Making scripts executable..."
chmod +x ../*.py 2>/dev/null

echo "[+] DONE! Linux compatibility ensured."
