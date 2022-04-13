#!/usr/bin/env bash

set -Eeuo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)

SRC="Text to Speech"
ZIPPED=$script_dir"/Text to Speech.zip"
ADDON_DIR="/home/$USER/.config/blender"

if [ -f "$ZIPPED" ]; then
    rm "$ZIPPED"
    zip "$ZIPPED" -r "$SRC"
else 
    zip "$ZIPPED" -r "$SRC"
fi

if [ -d "$ADDON_DIR" ]; then
    rm -r $ADDON_DIR
fi