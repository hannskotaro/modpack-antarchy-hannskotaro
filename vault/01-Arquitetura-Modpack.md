---
tags:
  - arquitetura
  - core
---

# 01 - Arquitetura do Modpack

Relacionado: [[00-Index]] | [[03-Pipeline-e-CI-CD]] | [[05-Keybinds-e-Overrides]]

## Especificações da Base
- **Minecraft:** `1.21.1`
- **Mod Loader:** `Fabric Loader` (`>=0.16.10` no manifesto, `0.20.1` no cliente)
- **Java Runtime:** `Java 21` (OpenJDK 64-bit Microsoft)
- **Total de Arquivos no Manifesto:** `121` (`120` mods `.jar` + `1` shaderpack `.zip`)

## Regra de Ouro do `.mrpack` (~21 KB)
O arquivo `Antarchy-RPG-1.21.1-Fabric.mrpack` é um arquivo `.zip` contendo **apenas**:
1. `modrinth.index.json` (manifesto JSON com URLs de download direto e hashes `SHA-1` / `SHA-512`).
2. `overrides/` (apenas arquivos de texto leves: [[05-Keybinds-e-Overrides]]).

> [!IMPORTANT] Proibido binários em `overrides/`
> Nunca colocar arquivos `.jar` ou `.zip` pesados dentro de `overrides/mods/`. Mods hospedados fora do Modrinth (como **Medieval Music** de 347 MB ou o hotfix do **Integrated API**) devem ser declarados na lista `external_files` do `build_modpack.py`, que os injeta no `modrinth.index.json` via CDN direto (`edge.forgecdn.net`). Isso mantém o `.mrpack` com ~21 KB.

## Política de Ambiente (`env`)
Todos os mods no `modrinth.index.json` são forçados com:
- `"client": "required"`
- `"server": "required"` (ou `"unsupported"` quando estritamente client-side)

Isso garante que o Prism Launcher e o Modrinth App baixem 100% dos mods sem exibir caixas de seleção de mods opcionais.
