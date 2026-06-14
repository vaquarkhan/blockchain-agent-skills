package com.vaquarkhan.blockchainskills

object InstallerData {
    const val RAW_BASE_URL = "https://raw.githubusercontent.com/vaquarkhan/blockchain-agent-skills/main"

    val coreFiles = listOf(
        "AGENTS.md",
        "CLAUDE.md",
        "skills-index.md",
        "registry/assets.json",
        "registry/chains.json",
        "requirements.txt",
        "docs/getting-started.md",
        "docs/codex-setup.md",
        "scripts/install.sh",
        "scripts/install.ps1",
        "scripts/install_toolkit.py",
        "scripts/validate-skills.py",
        "scripts/hook_runner.py",
        "hooks/README.md",
        "hooks/hooks.json",
        "hooks/session-start.sh",
        "hooks/tx-simulate-pre.sh",
        "hooks/mainnet-guard.sh",
        "guardrails/transaction-safety.yaml",
        "guardrails/security.yaml",
        "guardrails/compliance.yaml",
        "guardrails/denied-topics.yaml",
        "templates/skill-definition.yaml",
        "templates/tx-plan.yaml",
        "bootstrap.sh",
        "bootstrap.ps1"
    )

    val agentAdapters = linkedMapOf(
        "Cursor" to listOf(
            ".cursor/rules/00-blockchain-agent-core.mdc",
            ".cursor/rules/10-simulate-first.mdc",
            ".cursor/rules/20-guardrails.mdc",
            ".cursor/rules/30-chain-routing.mdc"
        ),
        "Claude" to listOf(
            ".claude/commands/plan.md",
            ".claude/commands/simulate.md",
            ".claude/commands/broadcast.md",
            ".claude/commands/confirm-depth.md",
            "AGENTS.md",
            "CLAUDE.md"
        ),
        "Copilot" to listOf(".github/copilot-instructions.md", "AGENTS.md"),
        "Codex" to listOf("AGENTS.md", "CLAUDE.md", "skills-index.md", "docs/getting-started.md", "docs/codex-setup.md"),
        "Windsurf" to listOf(".windsurfrules.example", "docs/windsurf-setup.md", "docs/getting-started.md")
    )

    val starterPacks = linkedMapOf(
        "EVM Core" to listOf(
            "starter-packs/evm-core-starter.yaml",
            "presets/evm-core/PRESET.md",
            "mcp/evm-rpc-server/config.yaml",
            "guardrails/transaction-safety.yaml",
            "AGENTS.md",
            "skills-index.md"
        ),
        "Solana Programs" to listOf(
            "starter-packs/solana-programs-starter.yaml",
            "presets/solana-mainnet/PRESET.md",
            "mcp/solana-rpc-server/config.yaml",
            "AGENTS.md",
            "skills-index.md"
        ),
        "NEAR Multi-chain" to listOf(
            "starter-packs/near-multichain-starter.yaml",
            "presets/near-mainnet/PRESET.md",
            "mcp/near-rpc-server/config.yaml",
            "AGENTS.md",
            "skills-index.md"
        ),
        "Cosmos IBC" to listOf(
            "starter-packs/cosmos-ibc-starter.yaml",
            "presets/cosmos-ibc/PRESET.md",
            "mcp/cosmos-rpc-server/config.yaml",
            "AGENTS.md",
            "skills-index.md"
        ),
        "Compliance Guardrails" to listOf(
            "starter-packs/compliance-guardrails-starter.yaml",
            "guardrails/compliance.yaml",
            "guardrails/security.yaml",
            "guardrails/denied-topics.yaml",
            "AGENTS.md",
            "skills-index.md"
        )
    )

    val mcpTemplates = linkedMapOf(
        "EVM" to listOf("mcp/evm-rpc-server/config.yaml", "mcp/evm-rpc-server/README.md"),
        "Solana" to listOf("mcp/solana-rpc-server/config.yaml", "mcp/solana-rpc-server/tool-schemas.json"),
        "NEAR" to listOf("mcp/near-rpc-server/config.yaml", "mcp/near-rpc-server/tool-schemas.json"),
        "Cosmos" to listOf("mcp/cosmos-rpc-server/config.yaml", "mcp/cosmos-rpc-server/tool-schemas.json")
    )

    val examples = linkedMapOf(
        "EVM ERC-20 Deploy" to listOf(
            "examples/evm-erc20-deploy/README.md",
            "examples/evm-erc20-deploy/spec.md",
            "examples/evm-erc20-deploy/plan.md",
            "examples/evm-erc20-deploy/tasks.md",
            "examples/evm-erc20-deploy/Makefile",
            "examples/evm-erc20-deploy/contracts/Token.sol"
        ),
        "Chain Provider Validation" to listOf(
            "examples/chain-provider-validation/README.md",
            "examples/chain-provider-validation/spec.md",
            "examples/chain-provider-validation/plan.md",
            "examples/chain-provider-validation/tasks.md",
            "examples/chain-provider-validation/Makefile",
            "tests/test_chain_providers.py"
        ),
        "Cosmos IBC Transfer" to listOf(
            "examples/cosmos-ibc-transfer/README.md",
            "examples/cosmos-ibc-transfer/spec.md",
            "examples/cosmos-ibc-transfer/plan.md",
            "examples/cosmos-ibc-transfer/tasks.md"
        ),
        "Solana SPL Token" to listOf(
            "examples/solana-spl-token/README.md",
            "examples/solana-spl-token/spec.md",
            "examples/solana-spl-token/plan.md",
            "examples/solana-spl-token/tasks.md"
        )
    )
}
