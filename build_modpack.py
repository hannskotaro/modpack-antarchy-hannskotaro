"""Build an Antarchy RPG & Exploration Modpack (.mrpack) for Minecraft 1.21.1 Fabric via Modrinth API."""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GAME_VERSION = "1.21.1"
LOADER = "fabric"
HEADERS = {"User-Agent": "AntarchyPackBuilder/1.0 (minecraft-modpack-builder)"}

# Curated mod slugs on Modrinth for 1.21.1 Fabric:
# 1. Core Antarchy + Required Dependencies (resolved automatically via version.dependencies)
# 2. Performance & Stability (Sodium stack)
# 3. RPG, Combat, Bosses & Dungeons
# 4. Exploration, Worldgen & Waystones
# 5. QoL, UI, Inventory & Audio/Visual Polish
MOD_SLUGS = [
    # --- Core: Antarchy & Ecosystem (All required libraries explicitly included) ---
    "antarchy",
    "antos",
    "anthology",
    "sizeable-foliage",
    "midnightlib",

    # --- Multiplayer & Co-op ---
    "essential",
    "lootr",

    # --- Performance & Shaders (Fabric 1.21.1 - Java 21 Compatible) ---
    "fabric-api",
    "fabric-language-kotlin",
    "sodium",
    "lithium",
    "iris",
    "ferrite-core",
    "immediatelyfast",
    "entityculling",
    "modernfix",
    "noisium",

    # --- RPG, Combat, Mobs & Bosses ---
    "better-combat",
    "combat-roll",
    "bosses-of-mass-destruction",
    "adventurez",
    "simply-swords",
    "oracle-index",
    "tieredz",
    "trinkets",
    "artifacts",
    "attributefix",
    "frostiful",
    "creeper-overhaul",
    "guard-villagers-fabricquilt",
    "illager-invasion",
    "mmmmmmmmmmmm",

    # --- Worldgen, Dungeons, Structures, Villages & YUNG's Suite ---
    "terralith",
    "tectonic",
    "when-dungeons-arise",
    "when-dungeons-arise-seven-seas",
    "dungeons-and-taverns",
    "structory",
    "structory-towers",
    "towns-and-towers",
    "explorify",
    "ct-overhaul-village",
    "mns-moogs-nether-structures",
    "moogs-voyager-structures",
    "medieval-buildings",
    "medieval-buildings-end-edition",
    "yungs-api",
    "yungs-better-dungeons",
    "yungs-better-mineshafts",
    "yungs-better-strongholds",
    "yungs-better-nether-fortresses",
    "yungs-better-ocean-monuments",
    "yungs-better-desert-temples",
    "yungs-better-jungle-temples",
    "yungs-better-witch-huts",
    "yungs-better-end-island",
    "yungs-bridges",
    "yungs-extras",
    "yungs-menu-tweaks",
    "yungs-cave-biomes",
    "yungs-better-caves",
    "waystones",
    "natures-compass",
    "explorers-compass",
    "travelers-compass",

    # --- Farming, Backpacks & Storage ---
    "farmers-delight-refabricated",
    "sophisticated-backpacks-unoffical-fabric-port",
    "sophisticated-storage-unofficial-fabric-port",
    "toms-storage",

    # --- QoL, VeinMining, Inventory, Keybinds, UI & Immersion ---
    "veinminer",
    "veinminer-client",
    "controlling",
    "enchantment-descriptions",
    "eating-animation",
    "lambdynamiclights",
    "presence-footsteps",
    "emi",
    "emi-loot",
    "jade",
    "xaeros-minimap",
    "xaeros-world-map",
    "polymorph",
    "appleskin",
    "yigd",
    "clumps",
    "modmenu",
    "cloth-config",
    "yacl",
    "sound-physics-remastered",
    "ambientsounds",
    "visuality",
    "not-enough-animations",
    "3dskinlayers",
    "spark",
]


def api_get(path: str):
    url = f"https://api.modrinth.com/v2{path}"
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (500, 502, 503, 504, 429) and attempt < 3:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise
        except Exception:
            if attempt < 3:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise


def search_project_slug(query: str):
    q = urllib.parse.quote(query)
    facets = urllib.parse.quote(json.dumps([[f"versions:{GAME_VERSION}"], [f"categories:{LOADER}"]]))
    try:
        data = api_get(f"/search?query={q}&facets={facets}&limit=1")
        hits = data.get("hits", [])
        if hits:
            return hits[0]["project_id"]
    except Exception:
        pass
    return None


PINNED_VERSIONS = {
    "architectury-api": "Pzc2FP5K",  # 13.0.11+fabric (exact version required by Antarchy 2.4.3)
    "lhGA9TYQ": "Pzc2FP5K",
}

SKIP_MODRINTH_IDS = {
    "integrated-api",
    "V6fKbpBN",  # Modrinth 1.9.2 uploaded 1.20.1 jar by mistake; pulled from CurseForge CDN in external_files
}


def get_compatible_version(project_id_or_slug: str):
    if project_id_or_slug in SKIP_MODRINTH_IDS:
        return None
    if project_id_or_slug in PINNED_VERSIONS:
        return api_get(f"/version/{PINNED_VERSIONS[project_id_or_slug]}")
    loaders = urllib.parse.quote(json.dumps([LOADER]))
    versions = urllib.parse.quote(json.dumps([GAME_VERSION]))
    path = f"/project/{project_id_or_slug}/version?loaders={loaders}&game_versions={versions}"
    try:
        data = api_get(path)
        if data:
            return data[0]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            fallback_pid = search_project_slug(project_id_or_slug)
            if fallback_pid and fallback_pid != project_id_or_slug:
                return get_compatible_version(fallback_pid)
        print(f"  [WARN] HTTP {e.code} for {project_id_or_slug}")
    except Exception as e:
        print(f"  [WARN] Error for {project_id_or_slug}: {e}")
    return None


def main():
    resolved_projects = {}  # project_id -> version_obj
    project_meta = {}       # project_id -> project_obj
    queue = list(MOD_SLUGS)
    visited_keys = set()

    print(f"Resolving {len(queue)} base mods + dependencies for Minecraft {GAME_VERSION} ({LOADER})...")

    while queue:
        key = queue.pop(0)
        if key in visited_keys:
            continue
        visited_keys.add(key)

        ver = get_compatible_version(key)
        if not ver:
            print(f"  [SKIP] No {GAME_VERSION} {LOADER} version found for '{key}'")
            continue

        pid = ver["project_id"]
        if pid in resolved_projects:
            continue

        try:
            pinfo = api_get(f"/project/{pid}")
        except Exception:
            pinfo = {"title": key, "slug": key, "client_side": "required", "server_side": "required"}

        resolved_projects[pid] = ver
        project_meta[pid] = pinfo
        print(f"  [OK] {pinfo.get('title', key)} ({pinfo.get('slug', key)}) -> {ver['version_number']}")

        # Queue required dependencies (plus version_id lookups if project_id is omitted)
        for dep in ver.get("dependencies", []):
            if dep.get("dependency_type") == "required":
                dep_pid = dep.get("project_id")
                if not dep_pid and dep.get("version_id"):
                    try:
                        dep_ver = api_get(f"/version/{dep['version_id']}")
                        dep_pid = dep_ver.get("project_id")
                    except Exception:
                        pass
                if dep_pid and dep_pid not in resolved_projects and dep_pid not in visited_keys:
                    queue.append(dep_pid)

    # Fetch latest stable Fabric loader version for 1.21.1
    fabric_loader_version = "0.16.10"
    try:
        req = urllib.request.Request(
            f"https://meta.fabricmc.net/v2/versions/loader/{GAME_VERSION}",
            headers=HEADERS,
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            loaders_data = json.loads(resp.read().decode("utf-8"))
            if loaders_data:
                fabric_loader_version = loaders_data[0]["loader"]["version"]
    except Exception as e:
        print(f"  [WARN] Could not fetch Fabric meta, using fallback {fabric_loader_version}: {e}")

    files_list = []
    manifest_summary = []

    # External mods not hosted on Modrinth (e.g. CurseForge direct CDN)
    # This prevents bundling 300+ MB jars inside the .mrpack, keeping the .mrpack under 100 KB!
    external_files = [
        {
            "path": "mods/zmedievalmusic-fabric-1.21-2.1.jar",
            "hashes": {
                "sha1": "38426682ff03cd14386060d75acf8e808574e8e1",
                "sha512": "441ee91d6dd8788fdc986cbb0b36fb1133c25c8a8f8dc37faffcc9a7219456c666ed3afad90f79c7ef520837f0075446ab0954e9ae578c30230243928c735a48",
            },
            "env": {
                "client": "required",
                "server": "unsupported",
            },
            "downloads": [
                "https://edge.forgecdn.net/files/5543/219/zmedievalmusic-fabric-1.21-2.1.jar"
            ],
            "fileSize": 347327813,
        },
        {
            "path": "mods/integrated_api-fabric-1.21.1-1.9.2.jar",
            "hashes": {
                "sha1": "48d13c7668a010f9db4783399acd07ee6e952b0b",
                "sha512": "dcf6aab9f208ec919b5f90cab390fc1ae179ea82b3c8803f5a4f41028ed319b1035012bab82228511f08205be654ee608e11fd81641ec5fb4ceb70276010ac34",
            },
            "env": {
                "client": "required",
                "server": "required",
            },
            "downloads": [
                "https://edge.forgecdn.net/files/9552/205/integrated_api-fabric-1.21.1-1.9.2.jar"
            ],
            "fileSize": 463087,
        },
        {
            "path": "shaderpacks/ComplementaryReimagined_r5.9.3.zip",
            "hashes": {
                "sha1": "838139b54cddb56b2e83cd260d8efd960ac536d6",
                "sha512": "45304b1d7862afdb2177b7e6226fc9c6737911d17a4ad46cc9c519ca4deb935f05072cd337cd8b19a15bb8062b57b54eceec7bdee4cd572d94858e2946d37d85",
            },
            "env": {
                "client": "required",
                "server": "unsupported",
            },
            "downloads": [
                "https://cdn.modrinth.com/data/HVnmMxH1/versions/Bqen1mJX/ComplementaryReimagined_r5.9.3.zip"
            ],
            "fileSize": 553397,
        }
    ]
    files_list.extend(external_files)
    manifest_summary.append({
        "title": "Medieval Music",
        "slug": "medieval-music",
        "version": "1.21-2.1",
        "filename": "zmedievalmusic-fabric-1.21-2.1.jar",
        "description": "Royalty-free medieval soundtracks by Alexander Nakarada",
        "url": "https://www.curseforge.com/minecraft/mc-mods/medieval-music",
    })
    manifest_summary.append({
        "title": "Integrated API",
        "slug": "integrated-api",
        "version": "1.21.1-1.9.2",
        "filename": "integrated_api-fabric-1.21.1-1.9.2.jar",
        "description": "Library mod for the Integrated Structures series and Antarchy",
        "url": "https://www.curseforge.com/minecraft/mc-mods/integrated_api",
    })
    manifest_summary.append({
        "title": "Complementary Shaders - Reimagined",
        "slug": "complementary-reimagined",
        "version": "r5.9.3",
        "filename": "ComplementaryReimagined_r5.9.3.zip",
        "description": "Artistic, optimized shaderpack tailored for Minecraft",
        "url": "https://modrinth.com/shader/complementary-reimagined",
    })

    for pid, ver in resolved_projects.items():
        pinfo = project_meta[pid]
        files = ver.get("files", [])
        if not files:
            continue
        primary_file = next((f for f in files if f.get("primary")), files[0])

        # Force client="required" so Prism Launcher / Modrinth App downloads every mod unconditionally
        client_env = "required"
        server_env = "unsupported" if pinfo.get("server_side") == "unsupported" else "required"

        files_list.append({
            "path": f"mods/{primary_file['filename']}",
            "hashes": {
                "sha1": primary_file["hashes"]["sha1"],
                "sha512": primary_file["hashes"]["sha512"],
            },
            "env": {
                "client": client_env,
                "server": server_env,
            },
            "downloads": [primary_file["url"]],
            "fileSize": primary_file["size"],
        })

        manifest_summary.append({
            "title": pinfo.get("title", ver["name"]),
            "slug": pinfo.get("slug", pid),
            "version": ver["version_number"],
            "filename": primary_file["filename"],
            "description": pinfo.get("description", ""),
            "url": f"https://modrinth.com/mod/{pinfo.get('slug', pid)}",
        })

    manifest_summary.sort(key=lambda x: x["title"].lower())
    files_list.sort(key=lambda x: x["path"].lower())

    mrpack_index = {
        "formatVersion": 1,
        "game": "minecraft",
        "versionId": "1.0.0",
        "name": "Antarchy: Realms of Chaos (RPG & Exploration)",
        "summary": "Modpack de RPG, exploração dimensional, dungeons e chefes centrado no Antarchy (1.21.1 Fabric).",
        "dependencies": {
            "minecraft": GAME_VERSION,
            "fabric-loader": fabric_loader_version,
        },
        "files": files_list,
    }

    Path("modrinth.index.json").write_text(json.dumps(mrpack_index, indent=2, ensure_ascii=False), encoding="utf-8")
    Path("mods_resolved.json").write_text(json.dumps(manifest_summary, indent=2, ensure_ascii=False), encoding="utf-8")

    # Package .mrpack with default overrides
    def write_mrpack(target_path: Path):
        with zipfile.ZipFile(target_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.write("modrinth.index.json", "modrinth.index.json")
            overrides_dir = Path("overrides")
            if overrides_dir.exists():
                for file_path in overrides_dir.rglob("*"):
                    if file_path.is_file():
                        arcname = file_path.relative_to(Path(".")).as_posix()
                        zf.write(file_path, arcname)

    mrpack_path = Path("Antarchy-RPG-1.21.1-Fabric.mrpack")
    write_mrpack(mrpack_path)

    print(f"\nSuccessfully resolved {len(files_list)} mods and generated {mrpack_path.name}!")


if __name__ == "__main__":
    main()
