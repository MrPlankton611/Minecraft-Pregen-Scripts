import os

# --- CONFIGURATION ---
base_path = r"C:\Pregenserver\world\datapacks\pregen_pack\data\pregen\function"
world_funcs_dir = os.path.join(base_path, "worlds")
seeds_file = r"C:\Pregenserver\seeds.txt"
TICK_DELAY = 1200 

def final_fix_functions():
    os.makedirs(world_funcs_dir, exist_ok=True)

    with open(seeds_file, "r") as f:
        seeds = [line.strip() for line in f if line.strip()]

    # Rewrite the individual world setup files
    for i, seed in enumerate(seeds, 1):
        world_name = f"world_{i}"
        file_path = os.path.join(world_funcs_dir, f"{world_name}.mcfunction")
        
        with open(file_path, "w") as wf:
            # Adding 'at @s' ensures the world center (0,0) is found correctly
            #/mw create test NORMAL -s=2579
            wf.write(f"execute as @p at @s run mw create {world_name} NORMAL -s={seed}\n")
            wf.write(f"execute as @p at @s run chunky world multiworld:{world_name}\n")
            wf.write(f"execute as @p at @s run chunky center 0 0\n")
            wf.write(f"execute as @p at @s run chunky radius 750\n")
            wf.write(f"execute as @p at @s run chunky start\n")
            wf.write(f"execute as @p at @s run mw unload {world_name}\n")

    print(f"Success! All {len(seeds)} functions are now wrapped for player-only execution.")

if __name__ == "__main__":
    final_fix_functions()