#!/usr/bin/env bash

set -Eeuo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)

SRC="text_to_speech"
ZIPPED=$script_dir"/text_to_speech.zip"
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