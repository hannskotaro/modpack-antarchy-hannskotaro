---
tags:
  - troubleshooting
  - critico
---

# 04 - Troubleshooting e Histórico de Decisões

Relacionado: [[00-Index]] | [[02-Restricoes-e-Pinos]] | [[05-Keybinds-e-Overrides]]

## Problemas Resolvidos

### 1. Partículas ausentes e erro OpenGL `id=1282 (GL_INVALID_OPERATION)`
- **Sintoma:** Partículas não apareciam mesmo com `particles = all` e o log registrava `GL_INVALID_OPERATION error generated. <texture> is not a valid texture name`.
- **Causa:** Presença de 4 JARs duplicados de versões antigas (`antarchy`, `anthology`, `antos`, `zmedievalmusic.jar.duplicate`) na pasta `mods/` local combinada com versões antigas do `Antarchy`/`Anthology`/`EntityCulling` e `glDebugVerbosity:1`.
- **Solução:** Limpeza de duplicatas na pasta `mods/`, atualização do `Antarchy` (`2.4.3`), `Anthology` (`1.0.7`), `EntityCulling` (`1.12.1`) e definição de `glDebugVerbosity:0` no `options.txt`.

### 2. Arquivo `.mrpack` com 347 MB
- **Causa:** O mod `Medieval Music` (`zmedievalmusic-fabric-1.21-2.1.jar`, 347 MB) foi inicialmente colocado em `overrides/mods/`, embutindo o binário no `.zip`.
- **Solução:** Movido para `external_files` no `modrinth.index.json` apontando para o CDN do CurseForge (`https://edge.forgecdn.net/files/5543/219/zmedievalmusic-fabric-1.21-2.1.jar`). O `.mrpack` caiu para **21 KB**.

### 3. Remoção de Mods de Inventário Intrusivos
- **`Mouse Wheelie`:** Removido a pedido do usuário.
- **`Inventory Profiles Next (IPN)` + `libIPN`:** Removidos porque a barra inferior de perfis (`NONE` / `Apply selected profile`) e as setas roxas poluíam visualmente o inventário. A ordenação de baús/mochilas já é suprida nativamente pelo botão **Sort** do `Sophisticated Backpacks` e `Sophisticated Storage`.

### 4. Spam de atualização do `VeinMiner` no Chat
- **Sintoma:** Mensagem `veinminer is outdated! (Current: 2.11.2, Latest: 2.14.0)` ao entrar no mundo.
- **Solução:** Atualizado `veinminer` e `veinminer-client` para `2.14.0`.

---

## Falsos Positivos no Log (Ignorar com Segurança)
- `No data fixer registered for <entidade>`: Normal no Fabric; mods não registram esquemas DFU para entidades novas.
- `Reference map ... could not be read` / `ClassNotFoundException: mezz/jei/...`: Mixins opcionais para mods ausentes.
- `Method overwrite conflict ... modernfix vs lithium`: O ModernFix cede intencionalmente a otimização para o Lithium.
- `Exception thrown registering repair recipes (ArrayIndexOutOfBoundsException)` no EMI: Itens de mods sem ingrediente de reparo definido; o EMI ignora e carrega todas as 15.700+ receitas normalmente.
- `Unknown variable: BIOME_PALE_GARDEN / endFlashIntensity` (Iris) e `pale_oak` (Presence Footsteps): Suporte futuro a blocos/biomas da 1.21.4+ ignorado na 1.21.1.
