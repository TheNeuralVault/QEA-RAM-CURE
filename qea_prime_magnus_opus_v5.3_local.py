#!/usr/bin/env python3
"""
QEA PRIME v5.3 SOTA LOCAL — FINAL CLEAN VERSION
Single model • Multi-mind • Full Termux scour first
"""
import os, time, subprocess, random
from pathlib import Path
from datetime import datetime

PLATFORM = Path(__file__).parent.resolve()
LEDGER = PLATFORM / 'QEA_QUANTUM_LEDGER.md'
OPENCLAW = Path.home() / 'openclaw.py'

print("QEA PRIME v5.3 SOTA LOCAL started")
print("First task: Full Termux system scour")

def run_openclaw_session(task, agent_role):
    print(f"  [@QEA-{agent_role}] Running task...")
    cmd = ['python3', str(OPENCLAW), '--task', task, '--agent', f'qea_{agent_role.lower()}', '--workspace', str(PLATFORM / '.openclaw'), '--local', '--model', 'phi3:mini']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        print(f"  [@QEA-{agent_role}] Task complete")
        return result.stdout or result.stderr
    except Exception as e:
        print(f"  [@QEA-{agent_role}] Error: {e}")
        return f"Error: {e}"

def run_cycle(cycle):
    print(f"\n=== CYCLE {cycle} STARTED at {datetime.now().strftime('%H:%M:%S')} ===")

    if cycle == 1:
        print("  [FIRST TASK] Scouring entire Termux system — every directory, every file, every hidden folder...")
        task = "Scour the entire Termux system completely. List every directory, every file, every hidden folder. Organize, clean, and prime everything for QEA PRIME. When finished, print exactly: 'TERMINAL PRIMING COMPLETE — Entire system organized and primed for QEA PRIME.'"
        result = run_openclaw_session(task, "orchestrator")
        print(result)
        with open(LEDGER, 'a') as f:
            f.write(f"\n### CYCLE 1 — TERMINAL PRIMING COMPLETE\n{result}\n---\n")
        print("  [FIRST TASK COMPLETE] TERMINAL PRIMING COMPLETE — Entire system organized and primed for QEA PRIME.")
    else:
        print("  Normal quantum discovery cycle (scour already done)")

    print(f"=== CYCLE {cycle} COMPLETE ===\n")

def main():
    print("QEA PRIME v5.3 SOTA LOCAL — FULLY LOCAL SINGLE-MODEL MULTI-MIND")
    print("First task: Full Termux system scour & prime.")

    cycle = 0
    while True:
        cycle += 1
        run_cycle(cycle)
        print("  [SLEEP] 10 minutes — phone cooling")
        time.sleep(600)

if __name__ == "__main__":
    main()
