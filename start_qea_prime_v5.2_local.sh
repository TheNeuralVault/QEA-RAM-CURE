#!/bin/bash
# Fixed tmux + virtualenv activation for proot Ubuntu
tmux kill-session -t QEA_PRIME 2>/dev/null || true
tmux new-session -d -s QEA_PRIME "
  source ~/qea-prime-env/bin/activate &&
  cd ~/TheNeuralVault/QEA-RAM-CURE &&
  python3 qea_prime_magnus_opus_v5.2_local.py
"
echo "✅ QEA PRIME v5.2 started in tmux session 'QEA_PRIME'"
echo "View live: tmux attach -t QEA_PRIME"
echo "Detach: Ctrl+B then D"
