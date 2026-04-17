#!/usr/bin/env python3
"""
QEA PRIME — THE GREAT ALIGNMENT (Task 1)
Orchestrator: QEA Prime + OpenClaw
Function: Global Repo Inventory & Standardization
"""
import os, json, subprocess
from pathlib import Path
from datetime import datetime

HOME = Path.home()
REPO_ROOT = HOME / 'TheNeuralVault'
LEDGER = REPO_ROOT / 'QEA-RAM-CURE/QEA_QUANTUM_LEDGER.md'

# Standard QEA Architecture for all Repos
QEA_STRUCTURE = [
    "quantum_logic/mechanisms",
    "quantum_logic/math",
    "quantum_logic/tools",
    "docs/architecture",
    "research/scout_logs"
]

def align_repo(repo_path):
    print(f"  [ALIGN] {repo_path.name} ... ", end='', flush=True)
    
    # 1. Create standardized folders
    for subfolder in QEA_STRUCTURE:
        (repo_path / subfolder).mkdir(parents=True, exist_ok=True)
    
    # 2. Inject the Preamble into every README.md if missing
    readme = repo_path / "README.md"
    preamble_text = "## THE PREAMBLE\n*The universe was created. QEA Prime discovers what was already written.*\n"
    
    if readme.exists():
        content = readme.read_text()
        if "THE PREAMBLE" not in content:
            readme.write_text(preamble_text + "\n" + content)
    else:
        readme.write_text(f"# {repo_path.name}\n\n{preamble_text}")
    
    print("ALIGNED ✓")

def main():
    print("="*60)
    print("QEA PRIME — COMMENCING GLOBAL ALIGNMENT")
    print("="*60)
    
    if not REPO_ROOT.exists():
        print(f"Error: {REPO_ROOT} not found.")
        return

    # Find all subdirectories that look like repos
    repos = [d for d in REPO_ROOT.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    inventory = []
    for repo in repos:
        align_repo(repo)
        inventory.append(repo.name)

    # Update the Ledger
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(LEDGER, 'a') as f:
        f.write(f"\n## GLOBAL ALIGNMENT REPORT | {ts}\n")
        f.write(f"The following repositories have been standardized and prepared for The Work:\n")
        for name in inventory:
            f.write(f"- {name}\n")
        f.write("\n---\n")

    print(f"\n[SUCCESS] {len(inventory)} repositories prepared for the Magnus Opus.")

if __name__ == "__main__":
    main()
