Build Windows executable (CI)

This repository includes a GitHub Actions workflow to build a Windows executable using `electron-builder` on a `windows-latest` runner.

How it works

- Trigger: run the workflow manually (`workflow_dispatch`) or push a tag matching `v*`.
- The workflow installs Node.js, runs `npm ci` in the `frontend` folder, then runs `npm run electron:build` to produce the Windows installer and artifacts.
- The resulting `frontend/dist` artifacts are uploaded as a workflow artifact named `gamecopilot-windows`.

Local build (requires Windows or Wine)

To build locally on Windows:

1. Install Node.js 18+ and Git.
2. In `frontend` run:

```bash
npm ci
npm run build
npm run electron:build
```

Notes and caveats

- Building an NSIS/Windows installer on Linux requires Wine/NSIS toolchain and can be fragile; CI on `windows-latest` is recommended.
- Ensure `frontend/package.json` has `electron-builder` and `electron` in devDependencies (already added).
- Add icons under `frontend/assets` and adjust `build.directories.buildResources` if needed.

If you want, I can:
- Trigger the workflow by creating a tag `v0.1.0`.
- Add icons to `frontend/assets`.
- Add a release job to automatically publish the artifact.
