---
tags:
  - config
  - core
---

# 05 - Keybinds e Overrides

Relacionado: [[00-Index]] | [[01-Arquitetura-Modpack]]

## Arquivos em `overrides/`

1. **`overrides/options.txt`**
   - Contém todos os `key_*` remapeados com **zero conflitos** entre as 133 ações registradas.
   - Define `glDebugVerbosity:0` e `particles:0` (*All*).
2. **`overrides/config/bettercombat/client.json`**
   - Habilita `targetHoldAttack`, `allowFastAttacks` e `swingThruGrass`.

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
