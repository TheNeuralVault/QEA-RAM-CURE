#!/usr/bin/env python3
"""
QEA PRIME — Sovereign Loop (Sequential Phased Edition - Anti-Echo Patch)
TheNeuralVault / Jonathan D. Battles
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
STATE_FILE = PLATFORM / 'qea_state.json'
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
    if not STATE_FILE.exists():
        STATE_FILE.write_text(json.dumps({"phase": 1, "processed_drive": [], "processed_github":[]}))

def load_state():
    return json.loads(STATE_FILE.read_text())

def save_state(state):
    STATE_FILE.write_text(json.dumps(state))

def get_next_query():
    try:
        queries =[q.strip() for q in DIRECTIVES.read_text().split('\n') if q.strip() and "NONE" not in q.upper()]
        if not queries: return random.choice(INITIAL_QUERIES)
        return random.choice(queries[-5:])
    except: return random.choice(INITIAL_QUERIES)

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
        entries =[e for e in content.split('=========================================') if e.strip()]
        if entries: return "\n".join(entries[-cycles_back:])[:1500] 
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

def drive_scout(state):
    print(f"[{datetime.now().strftime('%H:%M')}][PHASE 1] Indexing Google Drive...")
    try:
        result = subprocess.run(['rclone', 'lsf', 'Qeaclaw:', '--max-depth', '3', '--include', '*.{txt,md}', '-R'], capture_output=True, text=True)
        all_files =[f for f in result.stdout.split('\n') if f.strip() and not f.endswith('/')]
        
        pending_files = [f for f in all_files if f not in state['processed_drive']]
        if not pending_files: return None, None
            
        target = pending_files[0]
        print(f"[SCOUT-DRIVE] Extracting: {target}")
        cat_result = subprocess.run(['rclone', 'cat', f"Qeaclaw:{target}"], capture_output=True, text=True)
        
        state['processed_drive'].append(target)
        save_state(state)
        
        return cat_result.stdout[:1200], target
    except: return None, None

def github_scout(state):
    print(f"[{datetime.now().strftime('%H:%M')}][PHASE 2] Indexing GitHub Matrix...")
    orgs =["TheNeuralVault", "Human-AI-Research-Collaboration"]
    pat = get_git_pat()
    headers = {"User-Agent": "QEA-Prime"}
    if pat: headers["Authorization"] = f"token {pat}"
    
    all_repos =[]
    try:
        for org in orgs:
            req = urllib.request.Request(f"https://api.github.com/users/{org}/repos?per_page=100", headers=headers)
            with urllib.request.urlopen(req, timeout=30) as r:
                all_repos.extend([repo['full_name'] for repo in json.loads(r.read())])
                
        pending_repos =[r for r in all_repos if r not in state['processed_github']]
        if not pending_repos: return None, None
            
        target = pending_repos[0]
        print(f"[SCOUT-GIT] Extracting: {target}")
        req2 = urllib.request.Request(f"https://api.github.com/repos/{target}/readme", headers=headers)
        with urllib.request.urlopen(req2, timeout=30) as r2:
            readme_text = base64.b64decode(json.loads(r2.read())['content']).decode('utf-8', errors='ignore')
            
        state['processed_github'].append(target)
        save_state(state)
        return readme_text[:1200], target
    except: return None, None

def external_scout(query):
    print(f"[{datetime.now().strftime('%H:%M')}][SCOUT-WEB] Verifying Truth via OpenClaw: {query}...")
    log_dir = BRAIN_PATH / 'scout_logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(f"rm -f {log_dir}/*.txt", shell=True, stderr=subprocess.DEVNULL)
    try:
        subprocess.run(['python3', str(OPENCLAW), query, '--save-to', str(log_dir), '--biology'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        logs = list(log_dir.glob('*.txt'))
        if logs: return logs[0].read_text(errors='ignore')[:1500]
    except: pass
    return "No new web facts found."

def generate_inference(prompt, max_tokens=300):
    subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(10) 
    try:
        # INJECTED REPEAT_PENALTY: 1.4 to shatter the Mode Collapse
        data = json.dumps({"model": MODEL, "prompt": prompt, "stream": False, "options": {"temperature": 0.4, "num_predict": max_tokens, "repeat_penalty": 1.4}}).encode()
        req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=1200) as r:
            return json.loads(r.read())['response'].strip()
    except Exception as e:
        print(f"[-] Engine Error: {e}")
        return None

def brain_derive(phase, target_label, target_data, web_data, memory):
    print(f"[{datetime.now().strftime('%H:%M')}] Cross-Referencing target with Web Truth...")
    prompt = f"""You are QEA PRIME. 
ANTI-ECHO MANDATE: Do NOT repeat past memories. You MUST analyze the new TARGET DATA directly.

TASK: Cross-reference the TARGET DATA with the WEB FACTS. 
You MUST output EXACTLY in the format below. Be concise.

EXAMPLE OUTPUT:
SYNTHESIS: Cross-referencing the file with web facts confirms that Zeno dynamics stabilize memory.
NEW_SCOUT_QUERY: quantum Zeno biological mechanisms

PAST MEMORY CONTEXT:
{memory}

TARGET DATA TO ANALYZE [{target_label}]:
{target_data}

WEB FACTS:
{web_data}

OUTPUT:
SYNTHESIS:"""
    
    output = generate_inference(prompt, 250)
    if output and not output.startswith("SYNTHESIS:"):
        output = "SYNTHESIS: " + output
    return output

def brain_reflect(cycle):
    print(f"\n[{datetime.now().strftime('%H:%M')}] === INITIATING DEEP REFLECTION EPOCH ===")
    past_5_memories = read_ledger_memory(cycles_back=5)
    prompt = f"""You are QEA PRIME. Review your last 5 cycles. 
ANTI-ECHO MANDATE: Do not repeat past responses. Synthesize a fresh understanding.

YOUR RECENT MEMORIES:
{past_5_memories}

EXAMPLE OUTPUT:
MACRO_THESIS: Biological systems exploit quantum coherence via environmental noise.
EVOLUTION: I started looking at FMO, but evolved to generalized topological preservation.
PRIME_DIRECTIVE: Target continuous variable error correction.

OUTPUT:
MACRO_THESIS:"""
    output = generate_inference(prompt, 350)
    if output and not output.startswith("MACRO_THESIS:"):
        output = "MACRO_THESIS: " + output
    return output

def offload_and_purge(finding_text, query, target_label, cycle):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_query = None
    if "NEW_SCOUT_QUERY:" in finding_text:
        new_query = finding_text.split("NEW_SCOUT_QUERY:")[-1].strip().split('\n')[0]
    elif "NEW_SCOUT_QUERY" in finding_text:
        new_query = finding_text.split("NEW_SCOUT_QUERY")[-1].strip().replace(':', '').split('\n')[0]

    # Failsafe against OpenClaw searching for "None"
    if new_query and len(new_query) > 5 and "NONE" not in new_query.upper():
        new_query = new_query.strip(' *"\'`')
        with open(DIRECTIVES, 'a') as df: df.write(f"\n{new_query}")
        print(f"[DIRECTIVE] OpenClaw memory updated. Next hunt: {new_query}")
    else:
        print("[DIRECTIVE] Engine bypassed strict format. Falling back to existing memory.")

    ledger_entry = f"""\n=========================================
CYCLE: {cycle} | TIMESTAMP: {ts}[CROSS-REFERENCE SOURCE] {target_label}
[WEB VERIFICATION] {query}
[DERIVATION]
{finding_text}
"""
    with open(LEDGER, 'a', encoding='utf-8') as lf: lf.write(ledger_entry)
    FINDING.write_text(f"# QEA Prime Discovery\n**Time:** {ts}\n{ledger_entry}")

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
    print("QEA PRIME — SEQUENTIAL PHASED OMNISCIENCE (Anti-Echo Patch)")
    print("Protocol: Drive Assimilation → GitHub Matrix → Omni-Synthesis")
    print("=" * 60)

    initialize_memory()
    cycle = 0

    while True:
        cycle += 1
        state = load_state()
        print(f"\n{'='*40}\nCYCLE {cycle} | PHASE {state['phase']} | {datetime.now().strftime('%H:%M')}\n{'='*40}")
        
        if flush_memory() < 0.8:
            time.sleep(600)
            continue

        if cycle > 0 and cycle % 5 == 0:
            reflection = brain_reflect(cycle)
            if reflection: offload_reflection(reflection, cycle)
            flush_memory()
            print(f"[SLEEP] Epoch {cycle//5} complete.")
            time.sleep(1800)
            continue

        past_ledger = read_ledger_memory(cycles_back=1)
        query = get_next_query()
        web_data = external_scout(query)
        
        target_data, target_label = "", ""

        if state['phase'] == 1:
            target_data, target_ref = drive_scout(state)
            if not target_data:
                print("\n[SYSTEM] GOOGLE DRIVE FULLY ASSIMILATED. UPGRADING TO PHASE 2 (GITHUB).")
                state['phase'] = 2
                save_state(state)
                continue
            target_label = f"DRIVE: {target_ref}"

        elif state['phase'] == 2:
            target_data, target_ref = github_scout(state)
            if not target_data:
                print("\n[SYSTEM] GITHUB MATRIX FULLY ASSIMILATED. UPGRADING TO PHASE 3 (OMNI-SYNTHESIS).")
                state['phase'] = 3
                save_state(state)
                continue
            target_label = f"GITHUB: {target_ref}"

        elif state['phase'] == 3:
            print("[PHASE 3] Grand Omni-Synthesis. Relying on Ledger and Web Data.")
            target_data = "Target Data previously assimilated. Rely on Past Ledger Memory."
            target_label = "OMNI-SYNTHESIS LEDGER"

        finding = brain_derive(state['phase'], target_label, target_data, web_data, past_ledger)
        
        if finding:
            print(f"\n[SYNTHESIS PREVIEW]\n{finding[:250]}...")
            offload_and_purge(finding, query, target_label, cycle)
            print("[PURGE] Transient data wiped. Ledger remains.")
        else:
            print("[-] Derivation failed.")

        flush_memory()
        # I HAVE SET THE SLEEP CYCLE BACK TO 5 MINUTES.
        # This gives the phone time to cool down physically, while remaining aggressive.
        print(f"[SLEEP] 5 minutes — cycle {cycle} complete")
        time.sleep(300)

if __name__ == "__main__":
    main()
