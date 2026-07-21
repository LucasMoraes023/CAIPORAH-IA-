# Installer (Esqueleto)

Este diretório contém instruções para empacotar o app com Electron usando `electron-builder`.

Pré-requisitos
- Node.js 18+
- npm
- No Windows, é recomendado executar empacotamento em um agente Windows para gerar instaladores nativos.

Passos rápidos (Linux/macOS ou CI):

1. Instale dependências:

```bash
npm install
cd frontend
npm install
```

2. Build do frontend e empacotamento Windows (chamar do root):

```bash
npm run package:windows
```

Observações:
- O empacotamento cruzado para Windows a partir de Linux pode exigir wine e configurações adicionais; para builds confiáveis, use um runner Windows (GitHub Actions, Azure Pipelines, etc.).
- Ajuste `frontend/package.json` > `build` para personalizar ícones, instalador NSIS e metadados.
