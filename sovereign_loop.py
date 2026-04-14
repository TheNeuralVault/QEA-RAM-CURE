#!/usr/bin/env python3
"""
QEA PRIME — Sovereign Loop v2.2 (Final Retrofit)
Fixes: UnicodeDecodeError in Drive scouting, Binary data handling.
"""
import os, time, random, subprocess, json, urllib.request, base64
from pathlib import Path
from datetime import datetime

# --- ASSET LOCATION ---
HOME = Path.home()
PLATFORM = Path(__file__).parent.resolve()

def find_asset(name):
    for path in HOME.rglob(name):
        return path
    return None

OPENCLAW = find_asset("openclaw.py") or (HOME / "openclaw.py")
RCLONE_CONF = find_asset("rclone.conf")

TOOLS_DIR    = PLATFORM / 'tools'
SCOUT_LOGS   = PLATFORM / 'scout_logs'
CATALOG_FILE = PLATFORM / 'library_index.md'
LEDGER       = PLATFORM / 'QEA_LOCAL_BACKUP.md'
STATE_FILE   = PLATFORM / 'qea_state.json'
DIRECTIVES   = PLATFORM / 'hunting_directives.txt'

API_URL      = "https://models.inference.ai.azure.com/chat/completions"
MODEL_REMOTE = "gpt-4o" 
API_KEY      = os.environ.get('GITHUB_MODELS_API_KEY', '')

# --- INFRASTRUCTURE ---

def check_foundations():
    print("="*45)
    print("QEA PRIME v2.2 — INFRASTRUCTURE REPORT")
    print(f"API KEY: {'VALID' if len(API_KEY) > 10 else 'MISSING'}")
    print(f"OPENCLAW: {'READY' if OPENCLAW.exists() else 'NOT FOUND'}")
    print(f"RCLONE: {'READY' if RCLONE_CONF else 'USING DEFAULT'}")
    print("="*45)
    for d in [TOOLS_DIR, SCOUT_LOGS]: d.mkdir(exist_ok=True)

def run_rclone(args, capture_text=True):
    """Executes rclone. Captures as bytes to prevent Unicode crashes."""
    cmd = ['rclone']
    if RCLONE_CONF: cmd.extend(['--config', str(RCLONE_CONF)])
    cmd.extend(args)
    
    # We capture as raw bytes, NOT text, to avoid decoding errors
    res = subprocess.run(cmd, capture_output=True)
    
    if capture_text:
        return res.stdout.decode('utf-8', errors='ignore'), res.returncode
    return res.stdout, res.returncode

# --- SCOUTING ---

def drive_scout():
    print("[DRIVE] Checking private archives...")
    state = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {"processed": []}
    
    # List files (capturing names as text is safe)
    files_txt, code = run_rclone(['lsf', 'Qeaclaw:', '--max-depth', '2', '--include', '*.{txt,md,py}'])
    if code != 0: return None, "Remote Not Reachable"
    
    files = [f for f in files_txt.split('\n') if f.strip() and f not in state.get('processed', [])]
    if files:
        target = files[0]
        # Read file as BYTES first, then decode safely
        content_bytes, _ = run_rclone(['cat', f'Qeaclaw:{target}'], capture_text=False)
        content = content_bytes.decode('utf-8', errors='ignore')
        
        state.setdefault('processed', []).append(target)
        STATE_FILE.write_text(json.dumps(state))
        return content[:3500], target
    return None, "No new documents"

def openclaw_scout():
    query = "quantum biology mechanism FMO photosynthesis"
    if DIRECTIVES.exists():
        lines = [l.strip().strip('[]" ') for l in DIRECTIVES.read_text().split('\n') if l.strip()]
        if lines: query = random.choice(lines)
    
    print(f"[OPENCLAW] Hunting: {query}")
    if not OPENCLAW.exists(): return "", "Missing Scout"
    
    for f in SCOUT_LOGS.glob("*.txt"): f.unlink()
    subprocess.run(['python3', str(OPENCLAW), query, '--save-to', str(SCOUT_LOGS), '--biology'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    
    logs = list(SCOUT_LOGS.glob('*.txt'))
    if logs:
        return logs[0].read_text(errors='ignore')[:5000], query
    return "", query

# --- INTELLIGENCE ---

def derive_quantum(context):
    if not API_KEY: return "[ERROR] No Key"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": MODEL_REMOTE,
        "messages": [
            {"role": "system", "content": "YOU ARE QEA PRIME. ANALYZE. Tag #TOOL. Explain WHO/WHAT/WHY/WHERE."},
            {"role": "user", "content": context}
        ], "temperature": 0.1
    }
    try:
        req = urllib.request.Request(API_URL, data=json.dumps(payload).encode(), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())['choices'][0]['message']['content']
    except Exception as e: return f"[ERROR] {e}"

# --- MAIN ---

def main():
    check_foundations()
    cycle = 0
    while True:
        cycle += 1
        print(f"\n--- CYCLE {cycle} | {datetime.now().strftime('%H:%M')} ---")
        
        drive_data, drive_info = drive_scout()
        web_data, web_query = openclaw_scout()
        
        if not drive_data and not web_data:
            print("[WARN] No research data found. Cooldown...")
            time.sleep(300)
            continue

        print("[GPT-4o] Synthesizing Research...")
        context = f"LOCAL_DATA: {drive_data}\n\nWEB_DATA: {web_data}"
        discovery = derive_quantum(context)
        
        if discovery and "[ERROR]" not in discovery:
            with open(LEDGER, 'a') as f:
                f.write(f"\n### Cycle {cycle} | {datetime.now().strftime('%Y-%m-%d')}\n{discovery}\n---\n")
            
            if "#TOOL" in discovery and "```python" in discovery:
                try:
                    code = discovery.split("```python")[1].split("```")[0].strip()
                    tool_name = f"tool_{cycle}_{int(time.time())}.py"
                    (TOOLS_DIR / tool_name).write_text(code)
                    print(f"[SUCCESS] Tool {tool_name} archived.")
                except: pass
            
            # Cloud Push
            try:
                subprocess.run(['git', 'add', '.'], cwd=PLATFORM)
                subprocess.run(['git', 'commit', '-m', f'Discovery {cycle}'], cwd=PLATFORM)
                subprocess.run(['git', 'push', 'origin', 'HEAD'], cwd=PLATFORM)
                run_rclone(['copy', str(PLATFORM), 'Qeaclaw:TheNeuralVault/QEA-RAM-CURE', '--exclude', 'scout_logs/**'], capture_text=False)
                print("[SYNC] Cloud Synchronized.")
            except: print("[SYNC] Cloud deferred.")

        print("[WAIT] 15 min cooldown...")
        time.sleep(900)

if __name__ == "__main__":
    main()
