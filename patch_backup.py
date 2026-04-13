import os

path = os.path.expanduser("~/TheNeuralVault/QEA-RAM-CURE/sovereign_loop.py")
with open(path, 'r') as f:
    content = f.read()

# 1. Inject the Local Backup Failsafe
target_write = "FINDING.write_text(content)"
backup_injection = """FINDING.write_text(content)
    
    # --- THE FAILSAFE BACKUP ---
    backup_path = PLATFORM / 'QEA_LOCAL_BACKUP.md'
    with open(backup_path, 'a', encoding='utf-8') as bf:
        bf.write(content + "\\n\\n")
    print(f"[BACKUP] Data securely appended to {backup_path.name}")"""

if target_write in content and "THE FAILSAFE BACKUP" not in content:
    content = content.replace(target_write, backup_injection)

# 2. Fix the Prompt to use a "One-Shot Example" (Cures Epistemic Drift)
if "Analyze this quantum research data." in content:
    import re
    # Strip out the old broken prompt
    content = re.sub(
        r'prompt = f"""You are QEA PRIME.*?No explanation."""',
        '''prompt = f"""Extract the quantum physics from the data. Do NOT describe the format. Fill it out directly with the data provided.

EXAMPLE:
TIER: 1
CLAIM: FMO routes excitons using coherence.
MECHANISM: Noise-Assisted Transport
EQUATION: d(rho)/dt = -i[H, rho] + L(rho)
VECTOR: FMO coherence decoherence

DATA:
{context[:1500]}

OUTPUT:"""''',
        content,
        flags=re.DOTALL
    )

# 3. Expand the Git Error so we can read it
content = content.replace("result.stderr[:100]", "result.stderr.strip()")

# Write changes
with open(path, 'w') as f:
    f.write(content)

print("--- FAILSAFE BACKUP APPLIED & PROMPT CURED ---")
