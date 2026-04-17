#!/bin/bash
tmux new-session -d -s QEA_PRIME "cd ~/TheNeuralVault/QEA-RAM-CURE && python3 qea_prime_magnus_opus_v4.5.py"
echo "QEA PRIME v4.5 started in tmux session 'QEA_PRIME'"
echo "View live: tmux attach -t QEA_PRIME"
