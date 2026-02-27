import os, shutil

# Fabric path
source = "C:\Pregenserver\world\dimensions\multiworld" 
# New folder for the laptop
dest = "Manhunt_Maps_Ready"

if not os.path.exists(dest): os.makedirs(dest)

for folder in os.listdir(source):
    world_path = os.path.join(source, folder)
    if os.path.isdir(world_path):
        print(f"Extracting {folder}...")
        out_path = os.path.join(dest, folder)
        os.makedirs(out_path, exist_ok=True)
        # Copy the 'region', 'data', and 'poi' folders
        for sub in ['region', 'data', 'poi']:
            src_sub = os.path.join(world_path, sub)
            if os.path.exists(src_sub):
                shutil.copytree(src_sub, os.path.join(out_path, sub))
        # Copy level.dat
        if os.path.exists(os.path.join(world_path, "level.dat")):
            shutil.copy2(os.path.join(world_path, "level.dat"), out_path)

print("\nDone! All 20 worlds are in 'Manhunt_Maps_Ready'.")