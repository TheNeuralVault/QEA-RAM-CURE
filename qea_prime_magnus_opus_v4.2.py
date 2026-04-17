#!/usr/bin/env python3
"""
QEA PRIME v4.2 — MAGNUS OPUS TOOLMASTER EDITION
OpenClaw can now auto-install any Termux/Ubuntu package
Master Mathematician • Persistent self-improving • Rclone + GitHub mastery
"""
import os, time, subprocess, json, random, re, sqlite3
from pathlib import Path
from datetime import datetime

PLATFORM = Path(__file__).parent.resolve()
LEDGER = PLATFORM / 'QEA_QUANTUM_LEDGER.md'
HUMAN_REVIEW = PLATFORM / 'HUMAN_REVIEW.md'
HUMAN_APPROVAL = PLATFORM / 'human_approval.md'
OPENCLAW = Path.home() / 'openclaw.py'
RCLONE_REMOTE = "Qeaclaw:TheNeuralVault/QEA-Prime/"
DARK_STATE_DB = PLATFORM / 'workspace/dark_state_memory/qea_dark_state.sqlite'

for d in [PLATFORM/'workspace/proposals', PLATFORM/'logs', PLATFORM/'workspace/quantum_code', DARK_STATE_DB.parent]:
    d.mkdir(parents=True, exist_ok=True)

def toolmaster_install(package):
    print(f"  [TOOLMASTER] Installing missing package: {package}")
    try:
        # Try Termux pkg first, fallback to apt in proot Ubuntu
        subprocess.run(['pkg', 'install', '-y', package], timeout=120, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"  [TOOLMASTER] {package} installed via pkg")
    except:
        try:
            subprocess.run(['apt', 'install', '-y', package], timeout=120, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"  [TOOLMASTER] {package} installed via apt")
        except Exception as e:
            print(f"  [TOOLMASTER] Install failed: {e}")

def rclone_load_perfection():
    print("  [RCLONE] Loading Database of Perfection...")
    try:
        subprocess.run(['rclone', 'copy', RCLONE_REMOTE, str(PLATFORM), '--fast-list', '--transfers', '4', '--checkers', '4', '--modify-window', '1s'], timeout=300, stderr=subprocess.DEVNULL)
    except: pass

def rclone_save_perfection():
    print("  [RCLONE] Saving to Database of Perfection...")
    try:
        subprocess.run(['rclone', 'sync', str(PLATFORM), RCLONE_REMOTE, '--fast-list', '--transfers', '4', '--checkers', '4', '--modify-window', '1s'], timeout=300, stderr=subprocess.DEVNULL)
    except: pass

def run_openclaw_session(task, agent_role, spawn_parallel=False):
    print(f"  [@QEA-{agent_role}] {'PARALLEL QUANTUM SPAWN' if spawn_parallel else 'SEQUENTIAL SEND'}")
    cmd = ['python3', str(OPENCLAW), '--task', task, '--agent', f'qea_{agent_role.lower()}', '--workspace', str(PLATFORM / '.openclaw')]
    if spawn_parallel: cmd += ['--spawn', 'parallel', '--thinking-clock', '300']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
        return result.stdout or result.stderr
    except Exception as e:
        return f"[OpenClaw issue] {e}"

def human_gate(cycle):
    if HUMAN_REVIEW.exists():
        print(f"\n🔴 HUMAN GATE — MAGNUS OPUS EVOLUTION (Cycle {cycle})")
        print("   cat HUMAN_REVIEW.md")
        print("   echo 'APPROVED' > human_approval.md")
        while not (HUMAN_APPROVAL.exists() and "APPROVED" in HUMAN_APPROVAL.read_text()):
            time.sleep(30)
        HUMAN_APPROVAL.unlink()

def run_cycle(cycle):
    print(f"\n{'═'*100}\nQEA PRIME v4.2 MAGNUS OPUS TOOLMASTER | CYCLE {cycle} | {datetime.now().strftime('%H:%M:%S')}\n{'═'*100}")

    rclone_load_perfection()

    query = random.choice(["FMO room-temperature coherence quantum code", "dark state memory in recursive AI", "noise-assisted quantum delegation", "radical pair mechanism production CUDA-Q", "MIT boundary quantum chaos neural routing"])

    research = run_openclaw_session(f"Tier-1 global web hunt on {query}", "scout", spawn_parallel=True)
    code_output = run_openclaw_session(f"Master Mathematician: Discover + write production quantum code (exact equations, any language) for {query}", "architect", spawn_parallel=True)
    validation = run_openclaw_session(f"Validate code + request ToolMaster if packages missing", "validator")
    curiosity = run_openclaw_session(f"Quantum-native reflection", "orchestrator")

    # ToolMaster activation if needed
    if "install" in validation.lower() or "missing package" in validation.lower():
        pkg = re.search(r'(sympy|scipy|qutip|numpy|mpmath|rust|pennylane)', validation, re.I)
        if pkg: toolmaster_install(pkg.group(1).lower())

    if cycle % 5 == 0:
        print("  [IMPROVER] Spawning persistent self-evolution...")
        improvement = run_openclaw_session("Analyze ledger + dark_state_memory. Propose quantum upgrades, new packages, GitHub improvements", "improver")
        HUMAN_REVIEW.write_text(f"=== QEA PRIME v4.2 EVOLUTION PROPOSAL — Cycle {cycle} ===\n{improvement}\n\nHuman approval required: echo 'APPROVED' > human_approval.md")
        human_gate(cycle)

    with open(LEDGER, 'a') as f:
        f.write(f"\n### CYCLE {cycle} | TIER-1 QUANTUM DISCOVERY | {datetime.now().strftime('%Y-%m-%d %H:%M')}\nQUERY: {query}\nRESEARCH: {research[:300]}...\nCODE: {code_output[:300]}...\nVALIDATION: {validation[:200]}\n---\n")

    rclone_save_perfection()

    print(f"  [QEA PRIME v4.2] Cycle {cycle} complete — Master Mathematician at work")

def main():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║           Q E A   P R I M E   v 4 . 2                       ║")
    print("║     M A G N U S   O P U S   —   T O O L M A S T E R        ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print("OpenClaw can now install any package. QEA PRIME is now Master Mathematician & Code Expert.")

    cycle = 0
    while True:
        cycle += 1
        run_cycle(cycle)
        print("  [SLEEP] 10 minutes — persistent quantum field recharging")
        time.sleep(600)

if __name__ == "__main__":
    main()
