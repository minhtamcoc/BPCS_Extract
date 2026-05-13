#!/bin/bash
set -e
BASE=/home/student/labtainer/trunk/scripts/labtainer-student
TOOLS="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$BASE/bin"
if [ -f "$BASE/bin/checkwork" ] && [ ! -f "$BASE/bin/checkwork.labtainer_original" ]; then
    cp "$BASE/bin/checkwork" "$BASE/bin/checkwork.labtainer_original"
fi
if [ -f "$BASE/bin/stoplab" ] && [ ! -f "$BASE/bin/stoplab.labtainer_original" ]; then
    cp "$BASE/bin/stoplab" "$BASE/bin/stoplab.labtainer_original"
fi
cp "$TOOLS/checkwork" "$BASE/bin/checkwork"
cp "$TOOLS/stoplab" "$BASE/bin/stoplab"
chmod +x "$BASE/bin/checkwork" "$BASE/bin/stoplab"
echo "Installed bpcs_extract checkwork/stoplab wrappers."
