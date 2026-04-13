#!/bin/bash
echo "=== QEA-CLAW SYSTEM AUDIT ==="
echo "[1] DRIVE (Qeaclaw_Mount):"
ls ~/Qeaclaw_Mount > /dev/null 2>&1 \
    && echo "  MOUNTED" || echo "  DISCONNECTED"

echo "[2] GITHUB (TheNeuralVault):"
git -C ~/TheNeuralVault remote -v 2>/dev/null | head -2 \
    || echo "  No git remote"

echo "[3] OLLAMA:"
pgrep ollama > /dev/null 2>&1 \
    && echo "  ACTIVE: $(ollama list 2>/dev/null | tail -n+2 | awk '{print $1}')" \
    || echo "  STANDBY"

echo "[4] QEA PRIME:"
[ -f /root/QEA-Prime-Core/qea_prime.py ] \
    && echo "  READY" || echo "  MISSING"

echo "[5] OPENCLAW:"
python3 ~/openclaw.py 2>&1 | head -1

echo "[6] RAM:"
free -h | grep Mem

echo "[7] LAST FINDING:"
[ -f ~/TheNeuralVault/QEA-RAM-CURE/finding.md ] \
    && head -5 ~/TheNeuralVault/QEA-RAM-CURE/finding.md \
    || echo "  No findings yet"

echo "=== AUDIT COMPLETE ==="
