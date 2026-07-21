# Arquitetura do GameCopilot AI

## Visão geral

O GameCopilot AI foi projetado como uma aplicação modular com backend Python e frontend Electron + React. A arquitetura segue princípios de Clean Architecture, SOLID e separação de responsabilidades.

## Módulos principais

- `frontend/`: interface do usuário, navegação e integração com o backend.
- `backend/`: serviços de visão, voz, memória e orquestração de IA.
- `core/`: contratos e interfaces compartilhadas entre módulos.
- `vision/`: componentes de captura de tela e detecção de HUD.
- `voice/`: motores de reconhecimento e síntese de voz.
- `memory/`: persistência de histórico e memória de sessões.
- `plugins/`: API para extensões e suporte oficial de jogos.
- `database/`: esquema SQLite e scripts de migração.

## Diretórios de alta prioridade

- `backend/src/routers`: API do backend.
- `frontend/src`: aplicação React.
- `plugins/`: design para expandir suporte a jogos com plugins desacoplados.
