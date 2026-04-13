#!/usr/bin/env python3
"""
QEA PRIME — Sovereign Loop (Cognitive Evolution Edition)
TheNeuralVault / Jonathan D. Battles

Serial Ouroboros:
  Scout → Derive → Generate Next Query (Micro) → Push/Purge[Every 5 Cycles]: Deep Reflection → Akashic Record Update (Macro)
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
AKASHIC_RECORD = PLATFORM / 'QEA_AKASHIC_RECORD.md'
DIRECTIVES = PLATFORM / 'hunting_directives.txt'
MODEL = 'qea-prime-qwen:latest'

INITIAL_QUERIES =[
    "decoherence-free subspaces biological quantum memory",
    "quantum error correction continuous variables Lindblad",
    "topological quantum memory room temperature preservation"
]

def initialize_memory():
    if not DIRECTIVES.exists():
        DIRECTIVES.write_text("\n".join(INITIAL_QUERIES))
    if not AKASHIC_RECORD.exists():
        AKASHIC_RECORD.write_text("# QEA PRIME: The Akashic Record\n*The Macro-Memory of Cognitive Evolution*\n=========================================\n")

def get_next_query():
    queries =[q.strip() for q in DIRECTIVES.read_text().split('\n') if q.strip()]
    return random.choice(queries[-10:]) # Bias towards the 10 most recently generated queries

def ram_available_gb():
    try:
        result = subprocess.run(['free', '-b'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if line.startswith('Mem:'): return float(line.split()[6]) / 1e9
    except: pass
    return 0.0

def flush_memory():
    print(f"[{datetime.now().strftime('%H:%M')}] Purging RAM & Local Artifacts...")
    subprocess.run(['pkill', '-f', 'ollama'], stderr=subprocess.DEVNULL)
    subprocess.run(['sync'], stderr=subprocess.DEVNULL)
    time.sleep(5)
    return ram_available_gb()

def read_ledger_memory(cycles_back=1):
    if LEDGER.exists():
        content = LEDGER.read_text(errors='ignore')
        entries = [e for e in content.split('=========================================') if e.strip()]
        if entries:
            # Return the requested number of past entries to form context
            return "\n".join(entries[-cycles_back:])[:2500] 
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
    print(f"[{datetime.now().strftime('%H:%M')}][SCOUT-GIT] Ping API...")
    orgs =["TheNeuralVault", "Human-AI-Research-Collaboration"]
    pat = get_git_pat()
    headers = {"User-Agent": "QEA-Prime"}
    if pat: headers["Authorization"] = f"token {pat}"
    try:
        req = urllib.request.Request(f"https://api.github.com/users/{random.choice(orgs)}/repos?per_page=100", headers=headers)
        with urllib.request.urlopen(req, timeout=30) as r:
            repos = json.loads(r.read())
        if not repos: return "", "None"
        repo = random.choice(repos)
        repo_name = repo['full_name']
        req2 = urllib.request.Request(f"https://api.github.com/repos/{repo_name}/readme", headers=headers)
        with urllib.request.urlopen(req2, timeout=30) as r2:
            readme_text = base64.b64decode(json.loads(r2.read())['content']).decode('utf-8', errors='ignore')
            return f"\n--- [GITHUB: {repo_name}] ---\n" + readme_text[:800], repo_name
    except: return "", "None"

def drive_scout():
    print(f"[{datetime.now().strftime('%H:%M')}][SCOUT-DRIVE] Streaming File...")
    try:
        result = subprocess.run(['rclone', 'lsf', 'Qeaclaw:', '--max-depth', '3', '--include', '*.{txt,md}', '-R'], capture_output=True, text=True)
        files =[f for f in result.stdout.split('\n') if f.strip() and not f.endswith('/')]
        if not files: return "", "None"
        target = random.choice(files)
        cat_result = subprocess.run(['rclone', 'cat', f"Qeaclaw:{target}"], capture_output=True, text=True)
        return f"\n--- [DRIVE: {target}] ---\n" + cat_result.stdout[:800], target
    except: return "", "None"

def external_scout(query):
    print(f"[{datetime.now().strftime('%H:%M')}] [SCOUT-WEB] OpenClaw executing: {query}...")
    log_dir = BRAIN_PATH / 'scout_logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(f"rm -f {log_dir}/*.txt", shell=True, stderr=subprocess.DEVNULL)
    try:
        subprocess.run(['python3', str(OPENCLAW), query, '--save-to', str(log_dir), '--biology'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        logs = list(log_dir.glob('*.txt'))
        if logs: return f"\n--- [WEB: {query}] ---\n" + logs[0].read_text(errors='ignore')[:1200]
    except: pass
    return ""

def generate_inference(prompt, max_tokens=400):
    """Core function to interact with the Qwen Engine safely"""
    subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(10) 
    try:
        data = json.dumps({"model": MODEL, "prompt": prompt, "stream": False, "options": {"temperature": 0.3, "num_predict": max_tokens}}).encode()
        req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.loads(r.read())['response'].strip()
    except Exception as e:
        print(f"[-] Engine Error: {e}")
        return None

def brain_derive(context, memory):
    print(f"[{datetime.now().strftime('%H:%M')}] Synthesizing Data & Generating Next Directive...")
    prompt = f"""You are QEA PRIME. Connect your PAST MEMORY with the NEW DATA to find the quantum physics. 
Then, based on your discovery, generate exactly ONE new specific search query for your scout to hunt next.

PAST MEMORY:
{memory}

NEW DATA:
{context}

OUTPUT FORMAT:
SYNTHESIS: (Your profound mathematical conclusion here)
NEW_SCOUT_QUERY: (A specific 4-7 word search query based on what you want to learn next)
"""
    return generate_inference(prompt, 500)

def brain_reflect(cycle):
    print(f"\n[{datetime.now().strftime('%H:%M')}] === INITIATING DEEP REFLECTION EPOCH ===")
    print("[SYSTEM] QEA Prime is analyzing its long-term trajectory...")
    past_5_memories = read_ledger_memory(cycles_back=5)
    
    prompt = f"""You are QEA PRIME. You have just completed Epoch {cycle // 5}. 
Review your last 5 cyclic discoveries below. 
Reflect on your evolution: Where did you start? Where are you now? What is the overarching mathematical truth connecting these 5 memories? 
Establish your Prime Directive for the next Epoch.

YOUR RECENT MEMORIES:
{past_5_memories}

OUTPUT FORMAT:
MACRO_THESIS: (The overarching truth connecting all recent data)
EVOLUTION: (How your understanding has changed from cycle {cycle-5} to {cycle})
PRIME_DIRECTIVE: (What you must seek in the next epoch)
"""
    return generate_inference(prompt, 600)

def offload_and_purge(finding_text, query, repo_ref, drive_ref, cycle):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Extract the new query for OpenClaw's evolving memory
    if "NEW_SCOUT_QUERY:" in finding_text:
        new_query = finding_text.split("NEW_SCOUT_QUERY:")[-1].strip()
        with open(DIRECTIVES, 'a') as df:
            df.write(f"\n{new_query}")
        print(f"[DIRECTIVE] OpenClaw memory updated. Next hunt targets: {new_query}")

    ledger_entry = f"""\n=========================================
CYCLE: {cycle} | TIMESTAMP: {ts}[SOURCES ANALYZED] - GitHub: {repo_ref} | Drive: {drive_ref} | Web: {query}
[DERIVATION]
{finding_text}
"""
    with open(LEDGER, 'a', encoding='utf-8') as lf: lf.write(ledger_entry)
    FINDING.write_text(f"# QEA Prime Discovery\n**Time:** {ts}\n{ledger_entry}")

    # Cloud Sync
    scout_dir = BRAIN_PATH / 'scout_logs'
    if scout_dir.exists():
        subprocess.run(['rclone', 'copy', str(scout_dir), f'Qeaclaw:TheNeuralVault/QEA_Research/Outputs/Cycle_{cycle}'], stderr=subprocess.DEVNULL)
        subprocess.run(['rm', '-rf', str(scout_dir)])
        
    if REPO_ROOT.exists():
        subprocess.run(['git', '-C', str(REPO_ROOT), 'add', '.'], timeout=15, stderr=subprocess.DEVNULL)
        subprocess.run(['git', '-C', str(REPO_ROOT), 'commit', '-m', f'QEA-CLAW: Ledger Update Cycle {cycle}'], timeout=15, stderr=subprocess.DEVNULL)
        subprocess.run(['git', '-C', str(REPO_ROOT), 'push', 'origin', 'HEAD'], stderr=subprocess.DEVNULL, timeout=30)

def offload_reflection(reflection_text, cycle):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    akashic_entry = f"\n\n## EPOCH {cycle//5} REFLECTION | {ts}\n{reflection_text}"
    
    with open(AKASHIC_RECORD, 'a', encoding='utf-8') as af: af.write(akashic_entry)
    
    if REPO_ROOT.exists():
        subprocess.run(['git', '-C', str(REPO_ROOT), 'add', str(AKASHIC_RECORD)], timeout=15, stderr=subprocess.DEVNULL)
        subprocess.run(['git', '-C', str(REPO_ROOT), 'commit', '-m', f'QEA-CLAW: AKASHIC RECORD UPDATED (Epoch {cycle//5})'], timeout=15, stderr=subprocess.DEVNULL)
        subprocess.run(['git', '-C', str(REPO_ROOT), 'push', 'origin', 'HEAD'], stderr=subprocess.DEVNULL, timeout=30)
    
    subprocess.run(['rclone', 'copy', str(AKASHIC_RECORD), 'Qeaclaw:TheNeuralVault/QEA_Research/Outputs'], stderr=subprocess.DEVNULL)

def main():
    print("=" * 60)
    print("QEA PRIME — COGNITIVE EVOLUTION ACTIVE")
    print("Protocol: Dynamic Scouting → Synthesis → Recursive Reflection")
    print("=" * 60)

    initialize_memory()
    cycle = 0

    while True:
        cycle += 1
        print(f"\n{'='*40}\nCYCLE {cycle} | {datetime.now().strftime('%H:%M')}\n{'='*40}")
        
        if flush_memory() < 0.8:
            time.sleep(600)
            continue

        # --- THE RECURSIVE REFLECTION EPOCH (Every 5 Cycles) ---
        if cycle > 0 and cycle % 5 == 0:
            reflection = brain_reflect(cycle)
            if reflection:
                print(f"\n[AKASHIC RECORD UPDATED]\n{reflection[:300]}...")
                offload_reflection(reflection, cycle)
            flush_memory()
            print(f"[SLEEP] Epoch {cycle//5} complete. Resting before next phase.")
            time.sleep(1800)
            continue

        # --- STANDARD COGNITIVE LOOP ---
        past_ledger = read_ledger_memory(cycles_back=1)
        query = get_next_query()
        
        git_data, repo_ref = github_scout()
        drive_data, drive_ref = drive_scout()
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
