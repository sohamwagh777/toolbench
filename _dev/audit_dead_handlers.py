"""Dead-handler + dup-function audit (evidence for v3)."""
import re, glob

def audit():
    suspects = []
    for f in sorted(glob.glob('docs/tools/*.html')):
        t = open(f, encoding='utf-8').read()
        html = re.sub(r'<script>.*?</script>', '', t, flags=re.S)
        ids = set(re.findall(r'id="([^"]+)"', html))
        m = re.search(r'<script>([\s\S]*?)</script>\s*</body>', t)
        if not m:
            suspects.append((f, 'NO SCRIPT WRAPPER'))
            continue
        s = m.group(1)
        used = set()
        for pat in (r"getElementById\('([^']+)'\)", r"\$\('#?([A-Za-z][\w-]*)'\)", r"wire\(\[?'([a-z0-9-]+)'"):
            used |= set(re.findall(pat, s))
        dead = [u for u in used if u and u not in ids and u not in ('out', 'ta', 'q', 'nores')]
        if dead:
            suspects.append((f, dead[:6]))
    return suspects

if __name__ == '__main__':
    s = audit()
    for x in s:
        print(x)
    print('total suspect pages:', len(s))
