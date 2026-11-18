---
tags:
  - pin
  - critico
---

# 02 - Restrições e Pinos de Versão

Relacionado: [[00-Index]] | [[04-Troubleshooting-e-Historico]] | [[06-Catalogo-de-Mods]]

Este documento registra as restrições rígidas descobertas via inspeção de bytecode e `fabric.mod.json`. **Não remova esses pinos do `build_modpack.py` sem antes verificar se os autores corrigiram a origem.**

---

## 1. `Architectury API` fixado em `13.0.11+fabric` (`Pzc2FP5K`)
- **Causa:** O `Antarchy 2.4.3+1.21.1-fabric` declara no seu `fabric.mod.json`:
  `"architectury": "13.0.11"` (sem operador `>=`).
- **Efeito se atualizado para `13.0.12`:** O Fabric Loader aborta a inicialização por incompatibilidade de versão SemVer exata.
- **Solução no script:** Fixado em `PINNED_VERSIONS` tanto por slug (`architectury-api`) quanto por project ID (`lhGA9TYQ`).

---

## 2. `Integrated API 1.9.2` puxado via CurseForge CDN (`9552205`)
- **Causa:** Na página do Modrinth (`V6fKbpBN`), a versão `1.9.2` (`h3XuTbXQ`) marcada como `1.21.1` contém por engano do autor o binário compilado para **Minecraft 1.20.1** (`integrated_api-fabric-1.20.1-1.9.2.jar`, que referencia `method_8000` em `MapItemAccessor` em vez de `method_32349`).
- **Solução no script:** O ID `V6fKbpBN` / `integrated-api` está em `SKIP_MODRINTH_IDS` e o JAR real de 1.21.1 (`integrated_api-fabric-1.21.1-1.9.2.jar`, hash SHA1 `48d13c7668a010f9db4783399acd07ee6e952b0b`) é injetado em `external_files` via CDN do CurseForge (`https://edge.forgecdn.net/files/9552/205/integrated_api-fabric-1.21.1-1.9.2.jar`).

---

## 3. `Anthology 1.0.7` exige `Sodium 0.8.x` (`0.8.13`) + `Iris 1.8.14-beta.1`
- **Causa:** O `Anthology 1.0.7+1.21.1-fabric` possui mixins de renderização de portais (`SodiumPortalTerrain`, `RenderSectionManagerAccessor`) que referenciam `net.caffeinemc.mods.sodium.client.render.chunk.TaskQueueType` e `RemovableMultiForest`.
- **Efeito se fizer downgrade para Sodium `0.6.13`:** Crash imediato ao entrar no mundo (`java.lang.NoClassDefFoundError: TaskQueueType`).
- **Regra:** Manter sempre a dupla `Sodium 0.8.13` + `Iris 1.8.14-beta.1` (ou superior da linha `0.8.x`).

---

## 4. Exclusão do `C2ME` (`0.4.0-alpha.0.30`)
- **Causa:** O submódulo `c2me-opts-natives-math` nas builds alpha recentes de 1.21.1 exige `java >= 25`, enquanto o runtime oficial do Minecraft 1.21.1 no Prism Launcher é **Java 21**.
- **Regra:** Não incluir `c2me-fabric` para preservar compatibilidade out-of-the-box com o Java 21 dos jogadores.

---

## 5. Dependências Obrigatórias Ocultas do `Antarchy`
O Modrinth nem sempre lista todas as dependências obrigatórias nos metadados da API, mas o `fabric.mod.json` interno exige:
- `antos` (`>=1.6.5`)
- `anthology` (`>=1.0.7`)
- `integrated_api` (`>=1.9.2`) -> que por sua vez exige `midnightlib` (`>=1.5.7`)
- `sizeable_foliage` (`*`)
- `geckolib` (`*`)
- `architectury` (`13.0.11`)
