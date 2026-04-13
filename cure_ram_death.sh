#!/bin/bash
if [ -f ~/broker.env ]; then source ~/broker.env; fi
PLATFORM_PATH=~/TheNeuralVault/QEA-RAM-CURE
BRAIN_PATH=~/Qeaclaw_Mount/QEA_Research
MODEL="qea-prime-math:latest"

# ARRAY OF SEARCH VECTORS (To avoid blocks and go deep)
QUERIES=("python zero-copy memory-mapped file" "low-level register-based python optimization" "O(1) memory complexity algorithms python" "direct memory access python rust bindings")

echo "--- QEA PRIME: INFINITE SCOUT MODE ACTIVE ---"

while true; do
    pkill -f ollama
    # Randomly pick a search vector to stay under the radar
    QUERY=${QUERIES[$RANDOM % ${#QUERIES[@]}]}
    echo "[1/3] SCOUTING: $QUERY"

    # Use the --all flag to dig deeper into the global web
    python3 ~/openclaw.py "$QUERY" --save-to "$BRAIN_PATH/scout_logs" --all

    echo "[2/3] STARTING BRAIN..."
    ollama serve > ollama.log 2>&1 &
    sleep 15

    echo "COMPUTING: Analyzing global intelligence..."
    ollama run $MODEL "Synthesize the data in $BRAIN_PATH/scout_logs. Extract Tier-1 RAM-death cures." > "$PLATFORM_PATH/finding.md"

    if [ -s "$PLATFORM_PATH/finding.md" ]; then
        echo "[3/3] PUBLISHING discovery to TheNeuralVault..."
        git add .
        git commit -m "QEA-CLAW: Global Web Extraction Update"
        git push origin main
    fi

    echo "PURGING & COOLING..."
    pkill -f ollama
    sync
    sleep 1800
done
