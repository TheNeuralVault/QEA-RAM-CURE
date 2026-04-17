import json, re, time, subprocess, urllib.request, os
from pathlib import Path

def load_vault():
    return json.loads(Path('key_vault.json').read_text())

def save_vault(data):
    Path('key_vault.json').write_text(json.dumps(data, indent=2))

def get_best_key(data, prefer=None):
    ready = [k for k in data['keys'] if k['status'] == 'READY']
    if not ready:
        for k in data['keys']:
            if time.time() - k.get('last_used', 0) > 300: k['status'] = 'READY'
        ready = [k for k in data['keys'] if k['status'] == 'READY']
    if not ready: return None
    if prefer:
        pref = [k for k in ready if k['provider'] == prefer]
        if pref: return sorted(pref, key=lambda x: x['last_used'])[0]
    return sorted(ready, key=lambda x: x['last_used'])[0]

def call_api(sys_p, user_p, prefer=None):
    vault = load_vault()
    key = get_best_key(vault, prefer)
    if not key: return "WAIT", "NONE"
    
    payload = json.dumps({
        "model": key['model'], "temperature": 0.1, "max_tokens": 1000,
        "messages": [{"role": "system", "content": sys_p}, {"role": "user", "content": user_p}]
    }).encode()
    
    # Headers updated with User-Agent to satisfy Cerebras/SambaNova WAF
    headers = {
        'Authorization': f"Bearer {key['token']}",
        'Content-Type': 'application/json',
        'User-Agent': 'QEA-Prime-Librarian/4.5'
    }
    
    try:
        req = urllib.request.Request(key['url'], data=payload, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=90) as r:
            res = json.loads(r.read())
            key['last_used'] = time.time()
            save_vault(vault)
            return res['choices'][0]['message']['content'], key['id']
    except Exception as e:
        print(f"\n[KEY ERROR] {key['id']} failed: {e}")
        key['status'] = 'COOLING'; save_vault(vault)
        return "ERROR", key['id']

def extract_code(text):
    patterns = [r'```python\s*\n(.*?)```', r'```py\s*\n(.*?)```', r'```\s*\n(.*?)```']
    for p in patterns:
        m = re.search(p, text, re.DOTALL | re.IGNORECASE)
        if m: return m.group(1).strip()
    if 'import ' in text and 'def ' in text: return text.strip()
    return None

def run_sandbox(code):
    if not code: return False, "No code to run."
    Path('workspace/sandbox/test_run.py').write_text(code)
    try:
        res = subprocess.run(['python3', 'workspace/sandbox/test_run.py'], 
                             capture_output=True, text=True, timeout=25)
        return res.returncode == 0, (res.stdout if res.returncode == 0 else res.stderr)[:500]
    except Exception as e: return False, str(e)
