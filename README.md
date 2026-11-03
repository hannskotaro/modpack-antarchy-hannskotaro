# Antarchy: Realms of Chaos

Modpack focado em RPG, exploração e chefes centrado no mod **Antarchy**, estruturado para **Minecraft 1.21.1 (Fabric)**.

## Instalação

O modpack é distribuído no formato padrão `.mrpack` (compatível com Prism Launcher e Modrinth App):
- Arquivo: `Antarchy-RPG-1.21.1-Fabric.mrpack` (aprox. 21 KB)

### Prism Launcher
1. Clique em **Adicionar Instância** -> **Importar**.
2. Selecione o arquivo `.mrpack`.
3. O launcher fará o download automatizado de todos os mods e dependências.

### Requisitos de Sistema
- **Java:** Versão 21 (64-bit)
- **RAM alocada:** Mínimo de 4 GB, recomendado de 6 a 8 GB

## Controles e Teclas

Consulte o arquivo [GUIA_DE_TECLAS.md](GUIA_DE_TECLAS.md) para a relação completa dos atalhos configurados sem conflitos.

## Estrutura do Repositório

- `Antarchy-RPG-1.21.1-Fabric.mrpack`: Pacote pronto para distribuição e importação direta.
- `modrinth.index.json`: Manifesto de dependências e hashes (SHA-1 / SHA-512).
- `build_modpack.py`: Script para resolução de dependências via API do Modrinth e compilação do `.mrpack`.
- `overrides/`: Configurações padrão injetadas na instância (`options.txt`, ajustes de combate, etc.).
- `mods_resolved.json`: Lista detalhada de todos os mods incluídos com versões e links de origem.
