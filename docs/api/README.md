# API do GameCopilot AI

## Endpoints principais

- `GET /ping`
  - Verifica se o backend está ativo.

- `GET /vision/status`
  - Retorna o status do motor de visão.

- `GET /voice/status`
  - Retorna o status do motor de voz.

- `GET /memory/status`
  - Retorna o status do motor de memória.

- `GET /games`
  - Retorna a lista de jogos registrados.

- `POST /games`
  - Cria um jogo novo.
  - Payload: `{ "name": "Nome do Jogo" }`
