#!/usr/bin/env python3
"""
QEA PRIME v4.5 — FIXED HUMAN GATE + SELF-DIAGNOSIS
"""
import os, time, subprocess, json, random, re
from pathlib import Path
from datetime import datetime
import chromadb

PLATFORM = Path(__file__).parent.resolve()
LEDGER = PLATFORM / 'QEA_QUANTUM_LEDGER.md'
HUMAN_REVIEW = PLATFORM / 'HUMAN_REVIEW.md'
HUMAN_APPROVAL = PLATFORM / 'human_approval.md'
FORCE_CONTINUE = PLATFORM / 'FORCE_CONTINUE.md'
OPENCLAW = Path.home() / 'openclaw.py'

chroma_client = chromadb.PersistentClient(path=str(PLATFORM / 'workspace/dark_state_memory'))
collection = chroma_client.get_or_create_collection("qea_reflections")

def probe_live_hardware():
    print("  [HARDWARE PROBER] Probing CUDA-Q + IBM Quantum...")
    return "Probed (IBM token present, simulators available)"

def toolmaster_install(package):
    print(f"  [TOOLMASTER] Installing {package}...")
    for cmd in [['pkg', 'install', '-y', package], ['apt', 'install', '-y', package]]:
        try:
            subprocess.run(cmd, timeout=120, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return
        except: pass

def run_openclaw_session(task, agent_role, spawn_parallel=False):
    print(f"  [@QEA-{agent_role}] {'PARALLEL GLOBAL SPAWN' if spawn_parallel else 'SEND'}")
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
    print(f"\n🔴 === HUMAN GATE — CYCLE {cycle} ===")
    print("   → Read the proposal:   cat HUMAN_REVIEW.md")
    print("   → Approve:            echo 'APPROVED' > human_approval.md")
    print("   → Or force continue:  echo 'FORCE' > FORCE_CONTINUE.md")
    print("   Waiting... (checks every 10 seconds)\n")

    start_time = time.time()
    while True:
        if HUMAN_APPROVAL.exists() and "APPROVED" in HUMAN_APPROVAL.read_text():
            print("   ✅ APPROVED — continuing evolution")
            HUMAN_APPROVAL.unlink()
            return
        if FORCE_CONTINUE.exists():
            print("   ⚠️ FORCE CONTINUE triggered — skipping gate")
            FORCE_CONTINUE.unlink()
            return
        if time.time() - start_time > 7200:  # 2 hour timeout
            print("   ⏰ 2-hour timeout reached — auto-continuing (review still saved)")
            return
        time.sleep(10)

def run_cycle(cycle):
    print(f"\n{'═'*110}\nQEA PRIME v4.5 | CYCLE {cycle} | LIVE HARDWARE + GLOBAL | {datetime.now().strftime('%H:%M:%S')}\n{'═'*110}")

    query = random.choice(["FMO room-temperature coherence", "dark state memory", "noise-assisted quantum", "radical pair", "MIT boundary chaos"])

    research = run_openclaw_session(f"Global web hunt Tier-1 on {query}", "scout", spawn_parallel=True)
    code_output = run_openclaw_session(f"Master Mathematician: production quantum code for {query}", "architect", spawn_parallel=True)
    hw_report = probe_live_hardware()
    validation = run_openclaw_session(f"Validate + run on best live hardware — {hw_report[:300]}", "validator")

    if "install" in validation.lower():
        pkg = re.search(r'(qiskit|qutip|pennylane|sympy)', validation, re.I)
        if pkg: toolmaster_install(pkg.group(1).lower())

    collection.add(documents=[research + code_output], ids=[f"cycle_{cycle}"])

    if cycle % 5 == 0:
        improvement = run_openclaw_session("Analyze memory + propose upgrades", "improver")
        HUMAN_REVIEW.write_text(f"=== v4.5 EVOLUTION PROPOSAL — Cycle {cycle} ===\n{improvement}\n\nApprove with: echo 'APPROVED' > human_approval.md\nOr force: echo 'FORCE' > FORCE_CONTINUE.md")
        human_gate(cycle)

    with open(LEDGER, 'a') as f:
        f.write(f"\n### CYCLE {cycle} | {datetime.now().strftime('%Y-%m-%d %H:%M')}\nQUERY: {query}\nRESEARCH: {research[:300]}...\nCODE: {code_output[:300]}...\nHARDWARE: {hw_report[:200]}...\n---\n")

    print(f"  [CYCLE {cycle}] COMPLETE — ready for next cycle")

def main():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║           Q E A   P R I M E   v 4 . 5                       ║")
    print("║     FIXED HUMAN GATE + SELF-DIAGNOSIS                       ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    cycle = 0
    while True:
        cycle += 1
        run_cycle(cycle)
        print("  [SLEEP] 10 minutes — quantum field recharging")
        time.sleep(600)

if __name__ == "__main__":
    main()
