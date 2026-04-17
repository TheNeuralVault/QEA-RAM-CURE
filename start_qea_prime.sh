#!/bin/bash
tmux new-session -d -s QEA_PRIME "cd ~/TheNeuralVault/QEA-RAM-CURE && python3 qea_prime_magnus_opus_v4.3.py"
echo "QEA PRIME v4.3 started in tmux session 'QEA_PRIME'"
echo "View live: tmux attach -t QEA_PRIME"
echo "Detach: Ctrl+B then D"
