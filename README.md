# Pregenserver Automation

This repository contains tools and datapack patches used to sequentially pre-generate (pregen) multiple Minecraft worlds using Chunky and an external RCON watcher.

Contents
- `tools/rcon_watcher.py`: tails `logs/latest.log`, detects Chunky completion, and issues RCON commands to trigger the next world's mcfunction.
- `tools/update_world_funcs.py`: patches generated `world_*.mcfunction` files to tag the player and announce starts.
- `gen_commands.py`: generates `world_*.mcfunction` files from `seeds.txt` (existing in the workspace).
- `world/datapacks/pregen_pack/...`: datapack functions used to create worlds and start Chunky.

Prerequisites
- A running Minecraft server (Fabric) with Chunky and Multiworld installed.
- RCON enabled in `server.properties` (`enable-rcon=true`) with a secure `rcon.password` and server restarted.
- Python 3.8+ available to run the watcher and helper scripts.

Quick start

1. Patch world functions (adds tagging and announce lines):

```bash
python tools/update_world_funcs.py
```

2. Ensure `server.properties` has RCON enabled and restart the server. Example lines:

```properties
enable-rcon=true
rcon.password=your_secure_password_here
```

3. Start the watcher (runs continuously and will use RCON to trigger next worlds):

```bash
python tools/rcon_watcher.py
```

4. Start the chain in-game (as player MrPlanckton) by running the datapack start function or the first world function, e.g.: `/function pregen:start_all` or `/function pregen:worlds/world_1`.

Notes
- The watcher currently executes commands as the fixed player `MrPlanckton`. To change this behavior, edit `tools/rcon_watcher.py` and replace the fixed name with a selector (the previous approach used `@a[tag=pregen_runner,limit=1]`).
- Keep your RCON password secret. Do not commit real credentials to the repository.

Git setup (create a repo and push to GitHub)

```bash
git init
git add .
git commit -m "Initial import: pregen tools and datapack patches"
git branch -M main
git remote add origin https://github.com/<yourusername>/<repo>.git
git push -u origin main
```

License
- Add a license if you plan to publish this repository. MIT is a permissive option.

Contact
- If you want, I can create a minimal `.github` workflow or prepare the repo for publishing.
