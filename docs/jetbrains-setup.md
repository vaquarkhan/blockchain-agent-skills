# JetBrains Setup

## Marketplace / Release Install

1. Download plugin ZIP from [GitHub Releases](https://github.com/vaquarkhan/blockchain-agent-skills/releases/latest)
2. **Settings** → **Plugins** → ⚙️ → **Install Plugin from Disk...**
3. Restart IDE

Or build locally:

```bash
cd jetbrains-plugin
./gradlew buildPlugin
```

## Commands (Tools menu or Find Action)

- Install Full Toolkit
- Install Core Pack
- Install Agent Adapters
- Install Starter Pack
- Install MCP Templates
- Scaffold Example

## Script Alternative

```bash
scripts/install.sh --tool all --target /path/to/project
```

## Supported IDEs

IntelliJ IDEA, PyCharm, WebStorm, DataGrip, GoLand
