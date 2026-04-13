import os
path = os.path.expanduser("~/TheNeuralVault/QEA-RAM-CURE/sovereign_loop.py")
with open(path, 'r') as f:
    content = f.read()

# Fix 1: Point Git to the correct repository
content = content.replace("REPO_ROOT = HOME / 'TheNeuralVault'", "REPO_ROOT = HOME / 'TheNeuralVault/QEA-RAM-CURE'")

# Fix 2: Aggressive Monologue Slicing (Force it to start at "TIER:")
old_logic = 'if "</think>" in output:\n            output = output.split("</think>")[-1].strip()'
new_logic = 'if "TIER:" in output.upper():\n            output = output[output.upper().find("TIER:"):].strip()'
content = content.replace(old_logic, new_logic)

with open(path, 'w') as f:
    f.write(content)
print("--- SURGICAL PATCH APPLIED ---")
