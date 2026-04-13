#!/usr/bin/env python3
"""
QEA PRIME — Sovereign Loop (Ephemeral Memory Edition - Deep Synthesis Patch)
TheNeuralVault / Jonathan D. Battles

Serial Ouroboros:
  Read Ledger → Scout (API/Cat) → Derive → Push to Cloud → Purge Local Bloat → Sleep
"""
import os, time, random, subprocess, json, urllib.request, base64
from pathlib import Path
from datetime import datetime

HOME = Path.home()
PLATFORM = HOME / 'TheNeuralVault/QEA-RAM-CURE'
BRAIN_PATH = HOME / 'Qeaclaw_Mount/QEA_Research'
REPO_ROOT = HOME / 'TheNeuralVault/QEA-RAM-CURE'
OPENCLAW = HOME / 'openclaw.py'
FINDING = PLATFORM / 'finding.md'
LEDGER = PLATFORM / 'QEA_LOCAL_BACKUP.md'
MODEL = 'qea-prime-qwen:latest'

QUERIES =[
    "decoherence-free subspaces biological quantum memory",
    "quantum error correction continuous variables Lindblad",
    "topological quantum memory room temperature preservation",
    "quantum Zeno effect memory protection biological",
    "noise-assisted quantum memory stabilization ENAQT"
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
    print(f"[{datetime.now().strftime('%H:%M')}] Purging RAM & Local Artifacts...")
    subprocess.run(['pkill', '-f', 'ollama'], stderr=subprocess.DEVNULL)
    subprocess.run(['sync'], stderr=subprocess.DEVNULL)
    time.sleep(5)
    return ram_available_gb()

def read_ledger_memory():
    if LEDGER.exists():
        content = LEDGER.read_text(errors='ignore')
        entries = content.split('=========================================')
        if len(entries) > 1:
            return entries[-1].strip()[:800]
    return "No prior memory established."

def get_git_pat():
    try:
        creds = Path.home() / '.git-credentials'
        if creds.exists():
            content = creds.read_text()
            for line in content.split():
                if 'github.com' in line: return line.split('://')[1].split('@')[0].split(':')[1]
    except: pass
    return os.environ.get('GIT_PAT', '')

def github_scout():
    print(f"[{datetime.now().strftime('%H:%M')}][SCOUT-GIT] Ping API (No Local Download)...")
    orgs =["TheNeuralVault", "Human-AI-Research-Collaboration"]
    target_org = random.choice(orgs)
    pat = get_git_pat()
    headers = {"User-Agent": "QEA-Prime"}
    if pat: headers["Authorization"] = f"token {pat}"
    try:
        req = urllib.request.Request(f"https://api.github.com/users/{target_org}/repos?per_page=100", headers=headers)
        with urllib.request.urlopen(req, timeout=30) as r:
            repos = json.loads(r.read())
        if not repos: return "", "None"
        repo = random.choice(repos)
        repo_name = repo['full_name']
        
        req2 = urllib.request.Request(f"https://api.github.com/repos/{repo_name}/readme", headers=headers)
        with urllib.request.urlopen(req2, timeout=30) as r2:
            readme_text = base64.b64decode(json.loads(r2.read())['content']).decode('utf-8', errors='ignore')
            return f"\n--- [GITHUB: {repo_name}] ---\n" + readme_text[:1000], repo_name
    except: return "", "None"

def drive_scout():
    print(f"[{datetime.now().strftime('%H:%M')}][SCOUT-DRIVE] Streaming File (No Local Download)...")
    try:
        result = subprocess.run(['rclone', 'lsf', 'Qeaclaw:', '--max-depth', '3', '--include', '*.{txt,md}', '-R'], capture_output=True, text=True)
        files =[f for f in result.stdout.split('\n') if f.strip() and not f.endswith('/')]
        if not files: return "", "None"
        
        target = random.choice(files)
        cat_result = subprocess.run(['rclone', 'cat', f"Qeaclaw:{target}"], capture_output=True, text=True)
        return f"\n--- [DRIVE: {target}] ---\n" + cat_result.stdout[:1000], target
    except: return "", "None"

def external_scout(query):
    print(f"[{datetime.now().strftime('%H:%M')}] [SCOUT-WEB] Extracting OpenClaw to transient memory...")
    log_dir = BRAIN_PATH / 'scout_logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(f"rm -f {log_dir}/*.txt", shell=True, stderr=subprocess.DEVNULL)

    try:
        subprocess.run(['python3', str(OPENCLAW), query, '--save-to', str(log_dir), '--biology'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        logs = list(log_dir.glob('*.txt'))
        if logs:
            return f"\n--- [WEB: {query}] ---\n" + logs[0].read_text(errors='ignore')[:1500]
    except: pass
    return ""

def brain_derive(context, memory):
    print(f"[{datetime.now().strftime('%H:%M')}] Synthesizing Data with Past Ledger Context...")
    subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(10) # Extended wake-up time

    prompt = f"""You are QEA PRIME. Connect your PAST MEMORY with the NEW DATA to find the quantum physics. Fill out the exact format. Do NOT describe the format.

PAST MEMORY:
{memory}

NEW DATA:
{context}

EXAMPLE OUTPUT:
TIER: 1
CLAIM: Memory preservation relies on coherence.
MECHANISM: Zeno Effect
EQUATION: d(rho)/dt = -i[H, rho] + L(rho)
VECTOR: Neural vault memory preservation

OUTPUT:"""

    try:
        data = json.dumps({"model": MODEL, "prompt": prompt, "stream": False, "options": {"temperature": 0.2, "num_predict": 400}}).encode()
        req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=data, headers={"Content-Type": "application/json"})
        
        # MASSIVE TIMEOUT INCREASE: 600 seconds (10 minutes) for mobile deep thinking
        with urllib.request.urlopen(req, timeout=600) as r:
            output = json.loads(r.read())['response'].strip()
        
        if "TIER:" in output.upper(): 
            return output[output.upper().find("TIER:"):].strip()
        elif len(output) > 20:
            print("[DERIVE] Note: Strict format bypassed, but thought captured.")
            return output
        else:
            print("[-] Engine returned blank response.")
            return None
    except Exception as e:
        print(f"[-] API Error during derivation: {e}")
        return None

def offload_and_purge(finding_text, query, repo_ref, drive_ref, cycle):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    ledger_entry = f"""\n=========================================
CYCLE: {cycle} | TIMESTAMP: {ts}
[SOURCES ANALYZED]
- GitHub: {repo_ref}
- Drive: {drive_ref}
- Web: {query}

[SYNTHESIS]
{finding_text}
"""
    with open(LEDGER, 'a', encoding='utf-8') as lf:
        lf.write(ledger_entry)
        
    FINDING.write_text(f"# QEA Prime Discovery\n**Time:** {ts}\n{ledger_entry}")

    print(f"[{datetime.now().strftime('%H:%M')}] [OFFLOAD] Pushing artifacts to Cloud...")
    
    scout_dir = BRAIN_PATH / 'scout_logs'
    if scout_dir.exists():
        subprocess.run(['rclone', 'copy', str(scout_dir), f'Qeaclaw:TheNeuralVault/QEA_Research/Outputs/Cycle_{cycle}'], stderr=subprocess.DEVNULL)
        subprocess.run(['rm', '-rf', str(scout_dir)])
        
    if REPO_ROOT.exists():
        subprocess.run(['git', '-C', str(REPO_ROOT), 'add', '.'], timeout=15, stderr=subprocess.DEVNULL)
        subprocess.run(['git', '-C', str(REPO_ROOT), 'commit', '-m', f'QEA-CLAW: Ledger Update Cycle {cycle}'], timeout=15, stderr=subprocess.DEVNULL)
        subprocess.run(['git', '-C', str(REPO_ROOT), 'push', 'origin', 'HEAD'], stderr=subprocess.DEVNULL, timeout=30)

def main():
    print("=" * 60)
    print("QEA PRIME — EPHEMERAL OMNISCIENCE ACTIVE (Deep Synthesis Mode)")
    print("Protocol: Read Ledger → Extract → Synthesize → Push → Purge")
    print("=" * 60)

    cycle = 0
    while True:
        cycle += 1
        print(f"\n{'='*40}\nCYCLE {cycle} | {datetime.now().strftime('%H:%M')}\n{'='*40}")
        
        if flush_memory() < 0.8:
            time.sleep(600)
            continue

        past_ledger = read_ledger_memory()
        print(f"[LEDGER] Retrieved prior memory context.")

        git_data, repo_ref = github_scout()
        drive_data, drive_ref = drive_scout()
        query = random.choice(QUERIES)
        web_data = external_scout(query)
        
        full_context = git_data + drive_data + web_data
        
        if len(full_context.strip()) < 50:
            print("[-] Transients empty. Sleeping 5min.")
            time.sleep(300)
            continue

        finding = brain_derive(full_context, past_ledger)
        
        if finding:
            print(f"\n[SYNTHESIS PREVIEW]\n{finding[:250]}...")
            offload_and_purge(finding, query, repo_ref, drive_ref, cycle)
            print("[PURGE] Transient data wiped. Ledger remains.")
        else:
            print("[-] Derivation failed. Ledger untouched.")

        flush_memory()
        print(f"[SLEEP] 30 minutes — cycle {cycle} complete")
        time.sleep(1800)

if __name__ == "__main__":
    main()
