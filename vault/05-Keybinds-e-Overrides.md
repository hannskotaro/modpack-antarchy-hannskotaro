---
tags:
  - config
  - core
---

# 05 - Keybinds e Overrides

Relacionado: [[00-Index]] | [[01-Arquitetura-Modpack]]

## Arquivos em `overrides/`

1. **`overrides/options.txt`**
   - Contém todos os `key_*` remapeados com **zero conflitos** entre as 146 ações registradas.
   - Define `glDebugVerbosity:0` e `particles:0` (*All*).
   - Ativa nativamente os Resource Packs embutidos: `continuity:default`, `continuity:glass_pane_culling_fix` e `elytratrails:*`.
2. **`overrides/shaderpacks/ComplementaryReimagined_r5.9.3.zip.txt`**
   - Perfil otimizado importado do *Vanilla Perfected*: desativa reflexos pesados, SSAO, lightshafts e neblinas densas para ganhar FPS mantendo o visual *Reimagined* com contorno sutil e minérios brilhantes.
3. **`overrides/config/` (29 arquivos calibrados do *Vanilla Perfected*)**
   - `betterf3.json` (F3 minimalista apenas com versão, FPS e coordenadas X/Y/Z).
   - `MouseTweaks.cfg`, `immersive-hotbar.json5`, `betteradvancements.json`, `chatanimation.json`, `status-effect-bars.json`, `detailarmorbar.json`, `pickupnotifications.toml`.
   - `particlerain/` (`config.json` + `particles.json` sem neblina pesada), `moreculling.toml`, `entityculling.json`, `sodium-options.json`, `sodium-extra-options.json`, `lambdynlights.toml`.
   - `bettercombat/client.json`, `cutthrough-client.toml`, `rightclickharvest.json5`, `cropsloverain.toml`, `iteminteractions-*.toml`, `elytratrails.json`, `entity_model_features.json`, `entity_texture_features.json`, `notenoughanimations.json`, `skinlayers.json`, `visuality.json`.

## Mapa de Resolução dos Conflitos Principais

| Tecla | Ação Principal Mantida | Ações Movidas para Outras Teclas |
| :--- | :--- | :--- |
| `R` | **Combat Roll** (Esquiva) | Voo Montaria → `F4`, Portal Gun Reset → `Delete`, Iris Reload → `F8`, Emotes → `.` |
| `B` | **Sophisticated Backpacks** (Mochila) | Tom's Terminal → `I`, Novo Waypoint → `N`, Royal Boundary → `K` |
| `Z` | **Xaero's Minimap** (Ampliar Mapa) | AntOS Lookup / Portal Gun Zoom → Desativados (`unknown`) |
| `~` (`grave.accent`) | **VeinMiner** (Segurar para minerar veio) | Bafo de Dragão (AdventureZ) → `;` |
| `C` | **Essential Zoom** | Interação de Mochila → Desativada (`unknown`) |
| `V` / `X` | **Simply Swords** (Skills Mainhand / Offhand) | Royal Inversion → `\`, Load Toolbar Criativo → Desativado |
| `G` / `H` / `J` | **Antarchy Mount Skills** (Special / Beam / Signature) | Essential Friends → `F6`, Essential Menu → `F7` |
| `F8` / `F9` / `O` | **Iris Shaders** (Reload / Toggle / Menu) | Separados das teclas de combate |
