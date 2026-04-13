import os
path = os.path.expanduser("~/TheNeuralVault/QEA-RAM-CURE/sovereign_loop.py")
with open(path, 'r') as f:
    content = f.read()

# 1. Fix the Prompt to use a "One-Shot Example"
old_prompt = 'prompt = f"Analyze this data. Output ONLY format: TIER, CLAIM, MECHANISM, EQUATION, VECTOR. NO THINKING.\\n\\nDATA:\\n{context[:1500]}"'
new_prompt = '''prompt = f"""Extract the quantum physics from the data. Do NOT describe the format. Fill it out directly with the data provided.

EXAMPLE:
TIER: 1
CLAIM: FMO routes excitons using coherence.
MECHANISM: Noise-Assisted Transport
EQUATION: d(rho)/dt = -i[H, rho] + L(rho)
VECTOR: FMO coherence decoherence

DATA:
{context[:1500]}

OUTPUT:"""'''
content = content.replace(old_prompt, new_prompt)

# 2. Fix the Git Push Branch (Push HEAD instead of main)
old_push = "result = subprocess.run(['git', '-C', str(REPO_ROOT), 'push', 'origin', 'main'], capture_output=True, text=True, timeout=30)"
new_push = "result = subprocess.run(['git', '-C', str(REPO_ROOT), 'push', 'origin', 'HEAD'], capture_output=True, text=True, timeout=30)"
content = content.replace(old_push, new_push)

# 3. Expose the Git Error
old_fail = 'print(f"[PUBLISH] Push failed.")'
new_fail = 'print(f"[PUBLISH] Push failed: {result.stderr.strip()}")'
content = content.replace(old_fail, new_fail)

with open(path, 'w') as f:
    f.write(content)
print("--- PROMPT & GIT PATCH APPLIED ---")
