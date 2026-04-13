#!/bin/bash
while true; do
    clear
    echo "=== QEA-CLAW OBSERVATION DECK ==="
    echo "DATE: $(date)"
    echo "------------------------------------------------"
    echo "STATUS: $(pgrep -x ollama > /dev/null && echo 'BRAIN ACTIVE' || echo 'BRAIN STANDBY')"
    echo "------------------------------------------------"
    echo "LAST FINDING (TheNeuralVault):"
    tail -n 15 ~/TheNeuralVault/QEA-RAM-CURE/finding.md
    echo "------------------------------------------------"
    echo "LIVE BRAIN ACTIVITY (Ollama):"
    tail -n 5 ~/TheNeuralVault/QEA-RAM-CURE/ollama.log
    echo "------------------------------------------------"
    echo "Press [Ctrl+C] to exit Observation Deck"
    sleep 5
done
