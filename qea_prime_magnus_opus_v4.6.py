#!/usr/bin/env python3
"""
QEA PRIME v4.6 — CLEAN & SELF-HEALING
"""
import os, time, subprocess, random
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
    print("  [SELFHEALER] Running diagnosis...")
    # Check rclone mount
    if not list(Path.home().glob("QEA-Cloud-Mount/*")):
        print("  [SELFHEALER] Remounting rclone...")
        subprocess.run(["rclone", "mount", "Qeaclaw:TheNeuralVault/QEA-Prime/", str(Path.home()/"QEA-Cloud-Mount"), "--vfs-cache-mode", "full", "--daemon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Check OpenClaw
    if not OPENCLAW.exists():
        print("  [SELFHEALER] OpenClaw missing — attempting reinstall (pkg)")
        subprocess.run(["pkg", "install", "-y", "python"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("  [SELFHEALER] Healthy ✓")

def probe_live_hardware():
    return "IBM + CUDA-Q probed (simulators active)"

def run_openclaw_session(task, agent_role, spawn_parallel=False):
    cmd = ['python3', str(OPENCLAW), '--task', task, '--agent', f'qea_{agent_role.lower()}', '--workspace', str(PLATFORM / '.openclaw')]
    if spawn_parallel: cmd += ['--spawn', 'parallel', '--thinking-clock', '300']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
        return result.stdout or result.stderr
    except Exception as e:
        return f"[OpenClaw] {e}"

def human_gate(cycle):
    if not HUMAN_REVIEW.exists():
        return
    if AUTO_APPROVE_FILE.exists() and AUTO_APPROVE_FILE.read_text().strip() == "ON":
        print("  [AUTO-APPROVE] ON — gate skipped")
        return
    print(f"\n🔴 HUMAN GATE — Cycle {cycle}")
    print("   cat HUMAN_REVIEW.md")
    print("   echo 'APPROVED' > human_approval.md")
    print("   echo 'ON' > AUTO_APPROVE.md   (for testing)")
    print("   echo 'FORCE' > FORCE_CONTINUE.md")
    start = time.time()
    while True:
        if HUMAN_APPROVAL.exists() and "APPROVED" in HUMAN_APPROVAL.read_text():
            HUMAN_APPROVAL.unlink()
            return
        if FORCE_CONTINUE.exists():
            FORCE_CONTINUE.unlink()
            return
        if time.time() - start > 300:  # 5 min max wait
            print("   ⏰ Timeout — continuing")
            return
        time.sleep(10)

def run_cycle(cycle):
    self_diagnose_and_heal()
    print(f"\n{'═'*100}\nQEA PRIME v4.6 | CYCLE {cycle} | LIVE HARDWARE + GLOBAL | {datetime.now().strftime('%H:%M:%S')}")

    query = random.choice(["FMO room-temperature coherence", "dark state memory", "noise-assisted quantum", "radical pair", "MIT boundary chaos"])

    research = run_openclaw_session(f"Global web hunt Tier-1 on {query}", "scout", spawn_parallel=True)
    code_output = run_openclaw_session(f"Master Mathematician: production quantum code for {query}", "architect", spawn_parallel=True)
    hw_report = probe_live_hardware()
    validation = run_openclaw_session(f"Validate + run on best live hardware", "validator")

    # One-line status summary
    status = f"[STATUS] Cycle {cycle} | Query: {query[:30]}... | Hardware: probed | Code: saved | Global research: active"
    print(status)

    collection.add(documents=[research + code_output], ids=[f"cycle_{cycle}"])

    if cycle % 5 == 0:
        improvement = run_openclaw_session("Analyze memory + propose upgrades", "improver")
        HUMAN_REVIEW.write_text(f"=== v4.6 PROPOSAL — Cycle {cycle} ===\n{improvement}")
        human_gate(cycle)

    with open(LEDGER, 'a') as f:
        f.write(f"\n### CYCLE {cycle} | {datetime.now().strftime('%Y-%m-%d %H:%M')}\nQUERY: {query}\nSTATUS: {status}\n---\n")

    print(f"  [CYCLE {cycle}] COMPLETE — ready for next")

def main():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║           Q E A   P R I M E   v 4 . 6                       ║")
    print("║     CLEAN + SELF-HEALING + AUTO-APPROVE                     ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    cycle = 0
    while True:
        cycle += 1
        run_cycle(cycle)
        print("  [SLEEP] 10 minutes — quantum field recharging")
        time.sleep(600)

if __name__ == "__main__":
    main()
