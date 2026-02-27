import os
import shutil
import json

# --- CONFIGURATION ---
datapack_name = "pregen_pack"
namespace = "pregen"
# Update this path to your exact server location
base_path = rf"C:\Pregenserver\world\datapacks\{datapack_name}"
seeds_file = r"C:\Pregenserver\seeds.txt"
TICK_DELAY = 1200 # 60 seconds

def rebuild_perfect_datapack():
    # 1. Wipe everything to fix naming/structure errors
    if os.path.exists(base_path):
        shutil.rmtree(base_path)
    
    # 2. Build the 'Core' structure
    # MUST be plural 'functions'
    func_dir = os.path.join(base_path, "data", namespace, "functions", "worlds")
    os.makedirs(func_dir, exist_ok=True)

    # 3. Create pack.mcmeta (Format 48 is correct for 1.21.11)
    mcmeta = {
        "pack": {
            "pack_format": 48,
            "description": "Final Verified Pregen Pack"
        }
    }
    with open(os.path.join(base_path, "pack.mcmeta"), "w") as f:
        json.dump(mcmeta, f)

    # 4. Load Seeds
    with open(seeds_file, "r") as f:
        seeds = [line.strip() for line in f if line.strip()]

    # 5. Create start_all.mcfunction (The Controller)
    # We use 'encoding=utf-8' because 1.21.11 rejects other formats
    controller_path = os.path.join(base_path, "data", namespace, "functions", "start_all.mcfunction")
    with open(controller_path, "w", encoding="utf-8") as f:
        f.write("# Start the 200-world chain\n")
        for i, _ in enumerate(seeds, 1):
            delay = i * TICK_DELAY
            # Pattern: schedule function <namespace>:<path/to/file> <delay>
            f.write(f"schedule function {namespace}:worlds/world_{i} {delay}t\n")

    # 6. Create Individual World Files
    for i, seed in enumerate(seeds, 1):
        world_name = f"world_{i}"
        file_path = os.path.join(func_dir, f"{world_name}.mcfunction")
        with open(file_path, "w", encoding="utf-8") as f:
            # 'execute as @p' links the command to you to stop 'Player Required' errors
            # 'at @s' ensures the mod knows which dimension/location to use
            f.write(f"execute as @p at @s run mw create {world_name} NORMAL {seed}\n")
            f.write(f"execute as @p at @s run chunky world multiworld:{world_name}\n")
            f.write(f"execute as @p at @s run chunky center 0 0\n")
            f.write(f"execute as @p at @s run chunky radius 750\n")
            f.write(f"execute as @p at @s run chunky start\n")
            f.write(f"execute as @p at @s run mw unload {world_name}\n")

    print(f"Rebuild successful! Created {len(seeds)} files.")

if __name__ == "__main__":
    rebuild_perfect_datapack()