#!/usr/bin/env python3
"""
QEA PRIME v5.3 — THE HYBRID FOUNDRY
Logic: Optimized for Phone (Continuous) and GitHub (Batch Mode).
Sovereignty: Local Models + Cloud Automation.
"""
import os, sys, time, subprocess, random, re, json, urllib.request
from pathlib import Path
from datetime import datetime

# --- CONFIG & ARGS ---
BATCH_MODE = False
BATCH_LIMIT = 0
if "--batch" in sys.argv:
    BATCH_MODE = True
    idx = sys.argv.index("--batch")
    BATCH_LIMIT = int(sys.argv[idx+1])

PLATFORM   = Path(__file__).parent.resolve()
WORKSPACE  = PLATFORM / 'workspace'
LEDGER     = PLATFORM / 'QEA_QUANTUM_LEDGER.md'
DIRECTIVES = PLATFORM / 'hunting_directives.txt'
TOOLS_DIR  = PLATFORM / 'tools'
SANDBOX    = WORKSPACE / 'sandbox'

for d in [WORKSPACE/'scout_logs', TOOLS_DIR, SANDBOX]:
    d.mkdir(parents=True, exist_ok=True)

# --- NEURAL BROKER ---
def call_local(role, model, task, context=""):
    print(f"  [@QEA-{role}] via {model}... ", end='', flush=True)
    t0 = time.time()
    prompt = f"PREAMBLE: Discover. Never invent.\nROLE: {role}\nCONTEXT: {context[:1500]}\nTASK: {task}"
    payload = {"model": model, "prompt": prompt, "stream": False, "options": {"temperature": 0.1}}
    try:
        data = json.dumps(payload).encode()
        req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=data, method='POST')
        with urllib.request.urlopen(req, timeout=300) as r:
            res = json.loads(r.read())
            print(f"{time.time()-t0:.1f}s ✓")
            return res.get('response', '')
    except: return "ERROR"

def run_sandbox(code_text):
    test_file = SANDBOX / "runtime_check.py"
    m = re.search(r'```python\s*\n(.*?)```', code_text, re.DOTALL | re.IGNORECASE)
    code = m.group(1).strip() if m else code_text
    test_file.write_text(code)
    try:
        res = subprocess.run(['python3', str(test_file)], capture_output=True, text=True, timeout=30)
        return (res.returncode == 0, (res.stdout if res.returncode == 0 else res.stderr)[:400])
    except: return (False, "Timeout")

# --- SOVEREIGN CYCLE ---
def run_cycle(cycle):
    print(f"\n{'='*60}\nCYCLE {cycle} | {'CLOUD' if BATCH_MODE else 'LOCAL'} | {datetime.now().strftime('%H:%M:%S')}\n{'='*60}")
    
    if not DIRECTIVES.exists(): DIRECTIVES.write_text("FMO quantum coherence\nMIT boundary physics")
    query = random.choice([l.strip() for l in open(DIRECTIVES).readlines() if l.strip()])
    
    # 1. SCOUT
    print(f"  [SCOUT] Hunting: {query}")
    subprocess.run(['python3', '/root/openclaw.py', query, '--save-to', str(WORKSPACE/'scout_logs'), '--biology'], capture_output=True)
    logs = list((WORKSPACE/'scout_logs').glob('*.txt'))
    research = logs[0].read_text(errors='ignore')[:2500] if logs else "Direct Synthesis."

    # 2. ARCHITECT & VALIDATE
    arch_out = call_local("ARCHITECT", "qwen2.5-coder:3b", f"Code for: {query}", research)
    passed, msg = run_sandbox(arch_out)
    
    if passed:
        val_out = call_local("VALIDATOR", "deepseek-r1:1.5b", f"Verify physics for: {query}", arch_out)
        if "APPROVED" in val_out.upper() or BATCH_MODE:
            print(f"  [SUCCESS] Archiving...")
            with open(LEDGER, 'a') as f:
                f.write(f"\n### CYCLE {cycle} | {datetime.now().isoformat()}\n{arch_out}\n---\n")
            m = re.search(r'```python\s*\n(.*?)```', arch_out, re.DOTALL | re.IGNORECASE)
            (TOOLS_DIR / f"verified_{cycle}.py").write_text(m.group(1).strip() if m else arch_out)
            return True
    return False

def main():
    print(f"QEA PRIME v5.3 — HYBRID FOUNDRY (Batch Limit: {BATCH_LIMIT})")
    cycle = 0
    while True:
        cycle += 1
        run_cycle(cycle)
        if BATCH_MODE and cycle >= BATCH_LIMIT:
            print(f"[EXIT] Batch Complete. Saving GitHub Minutes.")
            break
        time.sleep(600)

if __name__ == "__main__":
    main()
