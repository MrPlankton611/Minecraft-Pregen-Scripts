import re
from pathlib import Path

starting_world_number = 202

base = Path(r"c:\Pregenserver\world\datapacks\pregen_pack\data\pregen\function\worlds")
files = sorted([p for p in base.glob('world_*.mcfunction')])

for p in files:
    s = p.read_text(encoding='utf-8')
    # remove any schedule lines
    s = re.sub(r"\nschedule function pregen:worlds/world_\d+ 1t\s*$", "", s)
    # ensure STARTING_WORLD say line before chunky start
    if 'chunky start' in s:
        lines = s.splitlines()
        new_lines = []
        for i,l in enumerate(lines):
            if l.strip().endswith('chunky start'):
                # find world name from previous lines or filename
                m = re.search(r'world_(\d+)', p.name)
                world = f"world_{m.group(1)}" if m else p.stem
                # tag the player as the runner, announce start for compatibility
                tag_add = "execute as @p at @s run tag @s add pregen_runner"
                start_tag = f"execute as @p at @s run say [Pregen] STARTING_WORLD:{world}"
                # only add tag and announce if not already present in nearby lines
                ctx = '\n'.join(lines[max(0,i-3):i+1])
                if tag_add not in ctx:
                    new_lines.append(tag_add)
                if start_tag not in ctx:
                    new_lines.append(start_tag)
                new_lines.append(l)
            else:
                new_lines.append(l)
        s = '\n'.join(new_lines) + '\n'
    # ensure we remove the tag at the end after unload
    if 'mw unload' in s:
        # append tag removal if not present
        if 'tag @p remove pregen_runner' not in s:
            s = s.rstrip() + '\nexecute as @p at @s run tag @s remove pregen_runner\n'
    p.write_text(s, encoding='utf-8')
    print(f"Patched {p}")
print('Done')
