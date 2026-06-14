# Plugin Publishing

Release artifacts: VS Code `.vsix` and JetBrains plugin ZIP via GitHub Actions.

## VS Code Extension

```bash
cd vscode-extension
npm install -g @vscode/vsce
vsce package
```

Output: `blockchain-agent-skills-0.2.0.vsix`

Manual install: Command Palette → `Extensions: Install from VSIX...`

## JetBrains Plugin

```bash
cd jetbrains-plugin
./gradlew buildPlugin
```

Output under `build/distributions/`.

## CI Workflow

See `.github/workflows/validate-and-package.yml` for validate + package on push to `main`.

## Configuration

- VS Code publisher: `ViquarKhan` in `vscode-extension/package.json`
- JetBrains plugin ID: `com.vaquarkhan.blockchainskills`
