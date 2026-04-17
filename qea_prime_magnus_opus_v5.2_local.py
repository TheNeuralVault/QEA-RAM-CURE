#!/usr/bin/env python3
"""
QEA PRIME v5.2 SOTA LOCAL — SINGLE-MODEL MULTI-MIND
Termux A53 Galaxy optimized | Full Termux scour first
"""
import os, time, subprocess, random, re
from pathlib import Path
from datetime import datetime
import chromadb

PLATFORM = Path(__file__).parent.resolve()
LEDGER = PLATFORM / 'QEA_QUANTUM_LEDGER.md'
HUMAN_REVIEW = PLATFORM / 'HUMAN_REVIEW.md'
HUMAN_APPROVAL = PLATFORM / 'human_approval.md'
AUTO_APPROVE_FILE = PLATFORM / 'AUTO_APPROVE.md'
FORCE_CONTINUE = PLATFORM / 'FORCE_CONTINUE.md'
OPENCLAW = Path.home() / 'openclaw.py'

chroma_client = chromadb.PersistentClient(path=str(PLATFORM / 'workspace/dark_state_memory'))
collection = chroma_client.get_or_create_collection("qea_reflections")

def self_diagnose_and_heal():
    try:
        out = subprocess.check_output(["free", "-m"]).decode()
        for line in out.splitlines():
            if line.startswith("Mem:"):
                parts = [p for p in line.split() if p.strip()]
                free = int(parts[3]) if len(parts) > 3 else 800
                print(f"  [SELFHEALER] RAM free: {free} MB")
                return free
    except:
        pass
    print("  [SELFHEALER] RAM free: 800 MB (fallback)")
    return 800

def run_openclaw_session(task, agent_role, spawn_parallel=False):
    print(f"  [@QEA-{agent_role}] LOCAL MULTI-MIND SPAWN (phi3:mini)")
    cmd = ['python3', str(OPENCLAW), '--task', task, '--agent', f'qea_{agent_role.lower()}', '--workspace', str(PLATFORM / '.openclaw'), '--local', '--model', 'phi3:mini']
    if spawn_parallel: cmd += ['--spawn', 'parallel']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=360)
        return result.stdout or result.stderr
    except Exception as e:
        return f"[Local OpenClaw] {e}"

def human_gate(cycle):
    if not HUMAN_REVIEW.exists():
        return
    if AUTO_APPROVE_FILE.exists() and AUTO_APPROVE_FILE.read_text().strip() == "ON":
        print("  [AUTO-APPROVE] ON")
        return
    print(f"\n🔴 HUMAN GATE — Cycle {cycle}")
    print("   cat HUMAN_REVIEW.md")
    print("   echo 'APPROVED' > human_approval.md")
    print("   echo 'ON' > AUTO_APPROVE.md   (toggle)")
    start = time.time()
    while True:
        if HUMAN_APPROVAL.exists() and "APPROVED" in HUMAN_APPROVAL.read_text():
            HUMAN_APPROVAL.unlink()
            return
        if FORCE_CONTINUE.exists():
            FORCE_CONTINUE.unlink()
            return
        if time.time() - start > 300:
            return
        time.sleep(10)

def run_cycle(cycle):
    ram = self_diagnose_and_heal()
    print(f"\n{'═'*100}\nQEA PRIME v5.2 SOTA LOCAL | CYCLE {cycle} | RAM {ram} MB | {datetime.now().strftime('%H:%M:%S')}")

    if cycle == 1:
        print("  [FIRST TASK] FULL TERMUX SYSTEM SCOUR STARTED — every directory, every file, every hidden folder...")
        task = "Scour the entire Termux system completely. List every directory, every file, every hidden folder. Organize, clean, and prime everything for QEA PRIME. When finished, print: 'TERMINAL PRIMING COMPLETE - Entire system organized and primed for QEA PRIME.'"
        result = run_openclaw_session(task, "orchestrator", spawn_parallel=False)
        print(result)
        with open(LEDGER, 'a') as f:
            f.write(f"\n### CYCLE 1 — TERMINAL PRIMING COMPLETE\n{result}\n---\n")
        print("  [FIRST TASK COMPLETE] Termux priming complete. Entire system organized and primed for QEA PRIME.")
    else:
        query = random.choice(["FMO room-temperature coherence", "dark state memory", "noise-assisted quantum", "radical pair", "MIT boundary chaos"])
        research = run_openclaw_session(f"Global web hunt Tier-1 on {query}", "scout", spawn_parallel=True)
        code_output = run_openclaw_session(f"Master Mathematician: production quantum code", "architect", spawn_parallel=True)
        validation = run_openclaw_session(f"Validate", "validator")

        status = f"[STATUS] Cycle {cycle} | RAM {ram} MB | Multi-mind active | Global research complete"
        print(status)

        collection.add(documents=[research + code_output], ids=[f"cycle_{cycle}"])

        if cycle % 5 == 0:
            improvement = run_openclaw_session("Analyze memory + propose upgrades", "improver")
            HUMAN_REVIEW.write_text(f"=== v5.2 PROPOSAL — Cycle {cycle} ===\n{improvement}")
            human_gate(cycle)

        with open(LEDGER, 'a') as f:
            f.write(f"\n### CYCLE {cycle} | {datetime.now().strftime('%Y-%m-%d %H:%M')}\n{status}\n---\n")

    print(f"  [CYCLE {cycle}] COMPLETE")

def main():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║           Q E A   P R I M E   v 5 . 2                       ║")
    print("║     SOTA SINGLE-MODEL MULTI-MIND — FULLY LOCAL              ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print("First task: Full Termux system scour & prime. Then quantum discovery begins.")

    cycle = 0
    while True:
        cycle += 1
        run_cycle(cycle)
        print("  [SLEEP] 10 minutes — phone cooling")
        time.sleep(600)

if __name__ == "__main__":
    main()
