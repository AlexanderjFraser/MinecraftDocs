#!/usr/bin/env bash
# Stage the Mojang libraries the game jar depends on, beside the decompile, so
# tools/verify_names.py can check library names — Brigadier's CommandDispatcher,
# DataFixerUpper's Codec, authlib's GameProfile — at member level, like the game's,
# and so a fact-check agent can read them instead of taking them on trust.
#
#   tools/fetch_libs.sh        -> reference/libs/<name>-<version>/   (gitignored)
#
# Brigadier and DataFixerUpper are MIT-licensed and Mojang publishes their source
# jars, so they are downloaded from libraries.minecraft.net. authlib is not open
# source: it is decompiled from the launcher's copy of the jar with the Vineflower
# bundled in the PvP mod's McDeob (MCDEOB_JAR), exactly as the game jar was, and it
# stays under reference/ for the same reason the game does.
#
# Versions come from the launcher's version JSON for the current game version
# (%APPDATA%/.minecraft/versions/<v>/<v>.json, the "com.mojang:<lib>:<version>"
# entries); update the three below when the game version in CLAUDE.md changes.
# The launcher must have run that version once for the authlib jar to be present.
set -euo pipefail
cd "$(dirname "$0")/.."
BRIGADIER=1.3.10
DFU=10.0.21
AUTHLIB=9.0.75
MCDEOB_JAR="${MCDEOB_JAR:-/d/pvpmod/McDeob-3.4.1.jar}"
LIBS=reference/libs
mkdir -p "$LIBS"

fetch() {  # fetch <artifact> <version>: the published sources jar, unpacked
    local dir="$LIBS/$1-$2" jar="$LIBS/$1-$2-sources.jar"
    if [ -d "$dir/com" ]; then echo "$dir: present"; return; fi
    curl -sS -L -o "$jar" "https://libraries.minecraft.net/com/mojang/$1/$2/$1-$2-sources.jar"
    mkdir -p "$dir" && unzip -q -o "$jar" -d "$dir" && rm -f "$jar"
    echo "$dir: $(find "$dir" -name '*.java' | wc -l) java files"
}
fetch brigadier "$BRIGADIER"
fetch datafixerupper "$DFU"

dir="$LIBS/authlib-$AUTHLIB"
if [ -d "$dir/com" ]; then
    echo "$dir: present"
else
    jar="$APPDATA/.minecraft/libraries/com/mojang/authlib/$AUTHLIB/authlib-$AUTHLIB.jar"
    [ -f "$jar" ] || { echo "no $jar — run the game version once from the launcher"; exit 1; }
    [ -f "$MCDEOB_JAR" ] || { echo "no decompiler at $MCDEOB_JAR (set MCDEOB_JAR)"; exit 1; }
    tmp="$LIBS/_authlib_tmp"
    rm -rf "$tmp" && mkdir -p "$tmp"
    java -cp "$MCDEOB_JAR" org.jetbrains.java.decompiler.main.decompiler.ConsoleDecompiler -log=WARN "$jar" "$tmp" >/dev/null
    mkdir -p "$dir" && unzip -q -o "$tmp/authlib-$AUTHLIB.jar" -d "$dir" && rm -rf "$tmp"
    echo "$dir: $(find "$dir" -name '*.java' | wc -l) java files"
fi
