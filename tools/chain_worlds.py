import re
from pathlib import Path

base = Path(r"c:\Pregenserver\world\datapacks\pregen_pack\data\pregen\function\worlds")
files = sorted([p for p in base.glob('world_*.mcfunction')])

# extract numbers
pairs = []
for p in files:
    m = re.search(r'world_(\d+)\.mcfunction$', str(p))
    if m:
        n = int(m.group(1))
        pairs.append((n,p))
pairs.sort()
nums = [n for n,_ in pairs]
maxn = max(nums) if nums else 0

for n,p in pairs:
    nextn = n+1
    if n == maxn:
        continue
    content = p.read_text(encoding='utf-8')
    # if scheduling already present, skip
    sched = f"schedule function pregen:worlds/world_{nextn} 1t"
    if sched in content:
        continue
    # append schedule after last non-empty line
    new = content.rstrip() + "\n" + sched + "\n"
    p.write_text(new, encoding='utf-8')
    print(f"Updated {p} -> schedules world_{nextn}")

print("Done")
