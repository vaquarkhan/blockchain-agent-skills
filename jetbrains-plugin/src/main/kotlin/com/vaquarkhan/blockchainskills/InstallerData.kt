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
        "requirements-proof.txt",
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
        "hooks/session-start.ps1",
        "hooks/tx-simulate-pre.sh",
        "hooks/mainnet-guard.sh",
        "guardrails/transaction-safety.yaml",
        "guardrails/security.yaml",
        "guardrails/compliance.yaml",
        "guardrails/denied-topics.yaml",
        "templates/skill-definition.yaml",
        "templates/tx-plan.yaml",
        "templates/incident-runbook.md",
        "templates/release-gate-evidence.yaml",
        "templates/mainnet-readiness.yaml",
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
        "Gemini" to listOf(
            ".gemini/commands/spec.md",
            ".gemini/commands/plan.md",
            ".gemini/commands/build.md",
            ".gemini/commands/test.md",
            ".gemini/commands/validate.md",
            ".gemini/commands/backfill.md",
            ".gemini/commands/review.md",
            ".gemini/commands/ship.md"
        ),
        "Kiro" to listOf(
            ".kiro/steering/product.md",
            ".kiro/steering/tech.md",
            ".kiro/steering/structure.md",
            "docs/kiro-setup.md",
            "AGENTS.md",
            "CLAUDE.md"
        ),
        "Codex" to listOf(
            "AGENTS.md",
            "CLAUDE.md",
            "skills-index.md",
            "docs/getting-started.md",
            "docs/codex-setup.md"
        ),
        "OpenCode" to listOf(
            "AGENTS.md",
            "CLAUDE.md",
            ".opencode/README.md",
            ".opencode/skills",
            "docs/opencode-setup.md",
            "docs/getting-started.md"
        ),
        "Windsurf" to listOf(
            ".windsurfrules.example",
            "docs/windsurf-setup.md",
            "docs/getting-started.md"
        )
    )

    val starterPacks = linkedMapOf(
        "EVM Core" to listOf(
            "starter-packs/evm-core-starter.yaml",
            "presets/evm-core/PRESET.md",
            "mcp/evm-rpc.mcp.json",
            "guardrails/transaction-safety.yaml",
            "AGENTS.md",
            "skills-index.md"
        ),
        "Solana Programs" to listOf(
            "starter-packs/solana-programs-starter.yaml",
            "presets/solana-mainnet/PRESET.md",
            "mcp/solana-rpc.mcp.json",
            "AGENTS.md",
            "skills-index.md"
        ),
        "NEAR Multi-chain" to listOf(
            "starter-packs/near-multichain-starter.yaml",
            "presets/near-mainnet/PRESET.md",
            "mcp/near-rpc.mcp.json",
            "AGENTS.md",
            "skills-index.md"
        ),
        "Cosmos IBC" to listOf(
            "starter-packs/cosmos-ibc-starter.yaml",
            "presets/cosmos-ibc/PRESET.md",
            "mcp/cosmos-rpc.mcp.json",
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
        "EVM" to listOf("mcp/evm-rpc.mcp.json"),
        "Solana" to listOf("mcp/solana-rpc.mcp.json"),
        "NEAR" to listOf("mcp/near-rpc.mcp.json"),
        "Cosmos" to listOf("mcp/cosmos-rpc.mcp.json"),
        "Move" to listOf("mcp/move-rpc.mcp.json"),
        "Bitcoin" to listOf("mcp/bitcoin-rpc.mcp.json"),
        "TON" to listOf("mcp/ton-rpc.mcp.json"),
        "Substrate" to listOf("mcp/substrate-rpc.mcp.json"),
        "Hedera" to listOf("mcp/hedera-rpc.mcp.json")
    )

    val runnableExamples = linkedMapOf(
        "EVM ERC-20 Deploy" to listOf(
            "examples/evm-erc20-deploy/README.md",
            "examples/evm-erc20-deploy/spec.md",
            "examples/evm-erc20-deploy/plan.md",
            "examples/evm-erc20-deploy/tasks.md",
            "examples/evm-erc20-deploy/Makefile",
            "examples/evm-erc20-deploy/contracts/Token.sol",
            "scripts/validate-skills.py",
            "requirements-proof.txt"
        ),
        "Chain Provider Validation" to listOf(
            "examples/chain-provider-validation/README.md",
            "examples/chain-provider-validation/spec.md",
            "examples/chain-provider-validation/plan.md",
            "examples/chain-provider-validation/tasks.md",
            "examples/chain-provider-validation/Makefile",
            "lib/chain_providers",
            "tests/test_chain_providers.py",
            "scripts/validate-skills.py",
            "requirements-proof.txt"
        )
    )
}
