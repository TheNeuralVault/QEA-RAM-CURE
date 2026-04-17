#!/bin/bash
tmux new-session -d -s QEA_PRIME "cd ~/TheNeuralVault/QEA-RAM-CURE && python3 qea_prime_magnus_opus_v4.4.py"
echo "QEA PRIME v4.4 LIVE HARDWARE started in tmux 'QEA_PRIME'"
echo "View: tmux attach -t QEA_PRIME"
