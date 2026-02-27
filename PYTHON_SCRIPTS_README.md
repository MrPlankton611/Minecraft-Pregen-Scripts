# Python Scripts

This file documents the Python scripts included in this repository and how to use them.

Overview
- `start.py`: small helper to launch the server locally (if configured).
- `gen_commands.py`: generates `world_*.mcfunction` files from `seeds.txt`.
- `export.py`: export utilities used during development (project-specific).
- `tools/update_world_funcs.py`: patches generated `world_*.mcfunction` files to insert a `tag` for the player, a STARTING_WORLD announcement, and a tag removal after unload. Run this after regenerating world functions.
- `tools/rcon_watcher.py`: tails `logs/latest.log`, detects Chunky completion, and issues RCON commands to trigger the next world's function. Requires RCON enabled in `server.properties` and the server restarted.
- `tools/chain_worlds.py`: legacy helper to append schedule lines to world function files (kept for reference).

Requirements
- Python 3.8+ (used for the small helper scripts).
- A running Minecraft server with Fabric + Chunky + Multiworld for `rcon_watcher.py` testing.

Typical workflow
1. Update seeds in `seeds.txt` and regenerate world functions:

```bash
python gen_commands.py
```

2. Patch the generated functions so they tag the player and announce starts:

```bash
python tools/update_world_funcs.py
```

3. Enable RCON in `server.properties` and restart the server:

```
enable-rcon=true
rcon.password=your_secure_password_here
```

4. Start the RCON watcher (runs continuously):

```bash
python tools/rcon_watcher.py
```

Notes
- The watcher currently issues the `execute as MrPlanckton run function ...` command; edit `tools/rcon_watcher.py` to change the target player or use the tag selector approach.
- Do not commit secrets (RCON passwords) to the repository. If `server.properties` or other config files have secrets, remove them from the repo and rotate any exposed credentials.
