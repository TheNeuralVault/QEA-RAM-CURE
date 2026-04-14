#!/usr/bin/env python3
"""
QEA PRIME v4.0 — THE ORCHESTRATED QUANTUM LAB
Orchestrator: OpenClaw Multi-Agent Supervisor Pattern
Focus: Self-Correcting Discovery Loop
"""
import os, time, subprocess, json, random
from pathlib import Path
from datetime import datetime

# --- PATHS ---
PLATFORM = Path(__file__).parent.resolve()
WORKSPACE = PLATFORM / 'workspace'
LEDGER = PLATFORM / 'QEA_LOCAL_BACKUP.md'
DIRECTIVES = PLATFORM / 'hunting_directives.txt'
API_KEY = os.environ.get('GITHUB_MODELS_API_KEY', '')

# --- AGENT WRAPPERS ---

def call_agent(agent_name, prompt, context=""):
    """
    Simulates an OpenClaw sessions_send call to a specific agent.
    In a full OpenClaw setup, this would be handled by the Gateway.
    """
    print(f"[@{agent_name}] Processing task...")
    
    # System Prompts per Agent
    souls = {
        "supervisor": (PLATFORM / "agents/supervisor/SOUL.md").read_text(),
        "architect":  (PLATFORM / "agents/architect/SOUL.md").read_text(),
        "validator":  (PLATFORM / "agents/validator/SOUL.md").read_text()
    }
    
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": souls.get(agent_name, "You are a QEA Specialist.")},
            {"role": "user", "content": f"CONTEXT:\n{context}\n\nTASK:\n{prompt}"}
        ], "temperature": 0.1
    }
    
    try:
        url = "https://models.inference.ai.azure.com/chat/completions"
        req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=90) as r:
            res = json.loads(r.read())
            return res['choices'][0]['message']['content']
    except Exception as e:
        return f"[ERROR] Agent communication failed: {e}"

import urllib.request

# --- THE ORCHESTRATION LOOP ---

def run_orchestrated_cycle(cycle):
    print(f"\n{'='*60}\nORCHESTRATED CYCLE {cycle} | {datetime.now().strftime('%H:%M:%S')}\n{'='*60}")
    
    # 1. SUPERVISOR: Define the Goal
    query = random.choice(open(DIRECTIVES).readlines()).strip() if DIRECTIVES.exists() else "FMO coherence 300K"
    (WORKSPACE / "goal.md").write_text(f"Goal: Extract and validate quantum code for {query}")
    
    # 2. SCOUT (OpenClaw): Gather Truth Data
    print("[SCOUT] Engaging global research hunt...")
    scout_logs = WORKSPACE / 'scout_logs'
    scout_logs.mkdir(exist_ok=True)
    subprocess.run(['python3', '/root/openclaw.py', query, '--save-to', str(scout_logs), '--biology'], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    logs = list(scout_logs.glob('*.txt'))
    research_data = logs[-1].read_text(errors='ignore') if logs else "No data."
    
    # 3. ARCHITECT: Build the Code
    architect_output = call_agent("architect", f"Build the quantum simulation code for: {query}", research_data)
    
    # 4. VALIDATOR: Review for Integrity
    print("[VALIDATOR] Verifying physical accuracy...")
    validation_report = call_agent("validator", "Review the following code for TIER-1 physical accuracy and executable integrity.", architect_output)
    
    if "REJECT" in validation_report.upper():
        print("[!] BUILD REJECTED BY VALIDATOR. Retrying in next cycle.")
        return False

    # 5. SUPERVISOR: Final Synthesis & Archiving
    print("[SUPERVISOR] Build approved. Archiving to Library...")
    final_entry = call_agent("supervisor", "Synthesize the approved research and code into a final Ledger entry. Include Who/What/Why/Where.", f"RESEARCH: {research_data}\n\nCODE: {architect_output}\n\nVALIDATION: {validation_report}")
    
    # Final Persistence
    with open(LEDGER, 'a') as f:
        f.write(f"\n### CYCLE {cycle} | {datetime.now().strftime('%Y-%m-%d')}\n{final_entry}\n---\n")
    
    # Save tool if it exists
    if "```python" in architect_output:
        try:
            code = architect_output.split("```python")[1].split("```")[0].strip()
            tool_name = f"gen4_tool_{cycle}.py"
            (PLATFORM / 'tools' / tool_name).write_text(code)
            print(f"[SUCCESS] Next-Gen Tool Archived: {tool_name}")
        except: pass

    return True

def main():
    if not API_KEY:
        print("[CRITICAL] API KEY MISSING.")
        return
    
    cycle = 0
    while True:
        cycle += 1
        success = run_orchestrated_cycle(cycle)
        
        # 5-Cycle Cloud Push (Architectural Redundancy)
        if cycle % 5 == 0:
            print("[CLOUD] Pushing workspace to GitHub/Drive...")
            subprocess.run(['git', 'add', '.'], cwd=PLATFORM)
            subprocess.run(['git', 'commit', '-m', f'Next-Gen Orchestration Cycle {cycle}'], cwd=PLATFORM)
            subprocess.run(['git', 'push', 'origin', 'HEAD'], cwd=PLATFORM)
        
        print("[WAIT] Cooldown (15m)...")
        time.sleep(900)

if __name__ == "__main__":
    main()
