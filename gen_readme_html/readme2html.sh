#!/bin/sh
set -e

# Check for required arguments
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 SOURCE_DIR TARGET_DIR [ASSETS_REL_PATH]"
    exit 1
fi

SOURCE_DIR="$1"
TARGET_DIR="$2"
ASSETS_REL_PATH="${3:-None}"
GIT_URL="${4:-https://gitlab.com/ulysse_durand/}"
HOME_URL="${5:-https://perso.ens-lyon.fr/ulysse.durand/}"
TEMPLATE_PATH="${6:-template.html}"

# Create target directory
mkdir -p "public/${TARGET_DIR}"

cp style.css "public/${TARGET_DIR}/"

# Copy assets if they exist
if [ -d "${SOURCE_DIR}/${ASSETS_REL_PATH}" ]; then
    cp -r "${SOURCE_DIR}/${ASSETS_REL_PATH}" "public/${TARGET_DIR}/${ASSETS_REL_PATH}"
fi

# Convert README.md to HTML
pandoc "${SOURCE_DIR}/README.md" \
       -o "public/${TARGET_DIR}/index.html" \
       --template template.html \
       -V homeurl=${HOME_URL} \
       -V giturl=${GIT_URL}

echo "Conversion complete. Output in public/${TARGET_DIR}"