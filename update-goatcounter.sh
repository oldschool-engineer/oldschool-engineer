#!/bin/bash
# Update GoatCounter count.js from the official source
# Run this when you get a release notification from:
# https://github.com/arp242/goatcounter

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEST="$SCRIPT_DIR/count.js"

echo "Downloading latest count.js from gc.zgo.at..."
curl -sL "https://gc.zgo.at/count.js" -o "$DEST"
echo "Updated: $DEST"
