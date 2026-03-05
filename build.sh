#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "--- 🛠️ STARTING NEURAL BRIDGE BUILD ---"

# 1. Install Python Dependencies
pip install -r requirements.txt

# 2. Download Dart SDK (Linux x64 version)
echo "--- 🎯 DOWNLOADING DART SDK ---"
wget https://storage.googleapis.com/dart-archive/channels/stable/release/latest/sdk/dartsdk-linux-x64-release.zip

# 3. Unzip and Setup
echo "--- 📦 UNPACKING DART ---"
unzip -o dartsdk-linux-x64-release.zip

# 4. Give Execution Permissions
chmod +x dart-sdk/bin/dart

echo "--- ✅ BUILD COMPLETE: DART IS READY ---"
