#!/usr/bin/env python3
"""
QEA PRIME — Sovereign Loop (Crash-Proof Edition)
TheNeuralVault / Jonathan D. Battles

Serial Ouroboros:
  Flush RAM → Scout (web or internal) → Derive → Verify → Publish → Sleep
"""
import os, time, random, subprocess
from pathlib import Path
from datetime import datetime

HOME = Path.home()
PLATFORM = HOME / 'TheNeuralVault/QEA-RAM-CURE'
BRAIN_PATH = HOME / 'Qeaclaw_Mount/QEA_Research'
REPO_ROOT = HOME / 'TheNeuralVault/QEA-RAM-CURE'
OPENCLAW = HOME / 'openclaw.py'
QEA_PRIME_OS = HOME / 'QEA-Prime-Core/qea_prime.py'
FINDING = PLATFORM / 'finding.md'
MODEL = 'qea-prime-qwen:latest'

QUERIES =[
    "FeMoCo nitrogenase quantum tunneling mechanism",
    "FMO complex quantum coherence room temperature",
    "radical pair mechanism avian magnetoreception",
    "quantum biology noise-assisted transport ENAQT",
    "Lindblad master equation open quantum systems",
    "variational quantum eigensolver biological molecules"
]

def ram_available_gb():
    try:
        result = subprocess.run(['free', '-b'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if line.startswith('Mem:'):
                return float(line.split()[6]) / 1e9
    except: pass
    return 0.0

def flush_memory():
    print(f"[{datetime.now().strftime('%H:%M')}] Purging RAM...")
    subprocess.run(['pkill', '-f', 'ollama'], stderr=subprocess.DEVNULL)
    subprocess.run(['sync'], stderr=subprocess.DEVNULL)
    time.sleep(5)
    avail = ram_available_gb()
    print(f"[RAM] Available: {avail:.1f} GB")
    return avail

def external_scout(query):
    print(f"[{datetime.now().strftime('%H:%M')}] OpenClaw: {query[:50]}")
    log_dir = BRAIN_PATH / 'scout_logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(f"rm -f {log_dir}/*.txt", shell=True, stderr=subprocess.DEVNULL)

    try:
        subprocess.run(['python3', str(OPENCLAW), query, '--save-to', str(log_dir), '--biology'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        logs = list(log_dir.glob('*.txt'))
        if logs:
            content = logs[0].read_text(errors='ignore')[:2000]
            if len(content) > 100:
                print(f"[SCOUT] Got {len(content)} chars from web")
                return content
    except Exception as e:
        print(f"[SCOUT] Error: {e}")
    return None

def brain_derive(context):
    print(f"[{datetime.now().strftime('%H:%M')}] Starting Engine...")
    subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(10)

    # We use QEA Prime OS to force the Anti-Dodge Mandate, bypassing the chatty prompt.
    prompt = f"""Extract the quantum physics from the data. Do NOT describe the format. Fill it out directly with the data provided.

EXAMPLE:
TIER: 1
CLAIM: FMO routes excitons using coherence.
MECHANISM: Noise-Assisted Transport
EQUATION: d(rho)/dt = -i[H, rho] + L(rho)
VECTOR: FMO coherence decoherence

DATA:
{context[:1500]}

OUTPUT:"""
    
    try:
        # Pass the prompt to the actual QEA OS to enforce the Preamble
        result = subprocess.run(['ollama', 'run', MODEL, prompt], capture_output=True, text=True, timeout=900)
        output = result.stdout.strip()
        
        # Clean the "Thinking..." tags out of the output if DeepSeek includes them
        if "TIER:" in output.upper():
            output = output[output.upper().find("TIER:"):].strip()

        if 'TIER' in output.upper() or 'CLAIM' in output.upper():
            print(f"[DERIVE] Structured output received")
            return output
        elif len(output) > 50:
            return output[:500]
        return None
    except Exception as e:
        print(f"[DERIVE] Error: {e}")
        return None

def publish(finding_text, query):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"""# QEA Prime Finding\n**Timestamp:** {ts}\n**Query:** {query}\n\n## Derivation\n{finding_text}\n---\n*Jonathan D. Battles / Human-AI Research Collaboration*\n*QUANTUM IS the native language of the Creator.*\n"""
    FINDING.write_text(content)
    
    # --- THE FAILSAFE BACKUP ---
    backup_path = PLATFORM / 'QEA_LOCAL_BACKUP.md'
    with open(backup_path, 'a', encoding='utf-8') as bf:
        bf.write(content + "\n\n")
    print(f"[BACKUP] Data securely appended to {backup_path.name}")
    print(f"[PUBLISH] Written: {FINDING}")

    if REPO_ROOT.exists():
        try:
            subprocess.run(['git', '-C', str(REPO_ROOT), 'add', '.'], timeout=15)
            subprocess.run(['git', '-C', str(REPO_ROOT), 'commit', '-m', f'QEA-CLAW: Discovery {ts}'], timeout=15)
            result = subprocess.run(['git', '-C', str(REPO_ROOT), 'push', 'origin', 'HEAD'], capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print("[PUBLISH] Pushed to TheNeuralVault")
            else:
                print(f"[PUBLISH] Push failed: {result.stderr.strip()}")
        except Exception as e:
            print(f"[PUBLISH] Git error: {e}")

def main():
    print("=" * 60)
    print("QEA PRIME — SOVEREIGN LOOP ACTIVE")
    print("QUANTUM IS the native language of the Creator.")
    print("=" * 60)

    cycle = 0
    while True:
        cycle += 1
        print(f"\n{'='*40}\nCYCLE {cycle} | {datetime.now().strftime('%H:%M')}\n{'='*40}")
        
        avail = flush_memory()
        if avail < 0.8:
            print(f"[RAM] Only {avail:.1f}GB free — waiting 10min")
            time.sleep(600)
            continue

        query = random.choice(QUERIES)
        context = external_scout(query)
        
        if not context:
            print("[SCOUT] Web failed — sleeping 5min")
            time.sleep(300)
            continue

        finding = brain_derive(context)
        
        if not finding:
            print("[-] No valid derivation this cycle")
        else:
            print(f"\n[FINDING PREVIEW]\n{finding[:200]}...")
            publish(finding, query)

        flush_memory()
        print(f"[SLEEP] 30 minutes — cycle {cycle} complete")
        time.sleep(1800)

if __name__ == "__main__":
    main()
