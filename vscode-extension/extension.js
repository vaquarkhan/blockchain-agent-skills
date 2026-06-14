const vscode = require("vscode");
const fs = require("fs");
const path = require("path");
const https = require("https");

const CORE_FILES = [
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
];

const AGENT_ADAPTERS = {
  Cursor: [
    ".cursor/rules/00-blockchain-agent-core.mdc",
    ".cursor/rules/10-simulate-first.mdc",
    ".cursor/rules/20-guardrails.mdc",
    ".cursor/rules/30-chain-routing.mdc"
  ],
  Claude: [
    ".claude/commands/plan.md",
    ".claude/commands/simulate.md",
    ".claude/commands/broadcast.md",
    ".claude/commands/confirm-depth.md",
    "AGENTS.md",
    "CLAUDE.md"
  ],
  Copilot: [".github/copilot-instructions.md", "AGENTS.md"],
  Gemini: [
    ".gemini/commands/spec.md",
    ".gemini/commands/plan.md",
    ".gemini/commands/build.md",
    ".gemini/commands/test.md",
    ".gemini/commands/validate.md",
    ".gemini/commands/backfill.md",
    ".gemini/commands/review.md",
    ".gemini/commands/ship.md"
  ],
  Kiro: [
    ".kiro/steering/product.md",
    ".kiro/steering/tech.md",
    ".kiro/steering/structure.md",
    "docs/kiro-setup.md",
    "AGENTS.md",
    "CLAUDE.md"
  ],
  Codex: ["AGENTS.md", "CLAUDE.md", "skills-index.md", "docs/getting-started.md", "docs/codex-setup.md"],
  OpenCode: [
    "AGENTS.md",
    "CLAUDE.md",
    ".opencode/README.md",
    ".opencode/skills",
    "docs/opencode-setup.md",
    "docs/getting-started.md"
  ],
  Windsurf: [".windsurfrules.example", "docs/windsurf-setup.md", "docs/getting-started.md"]
};

const STARTER_PACKS = {
  "EVM Core": {
    files: [
      "starter-packs/evm-core-starter.yaml",
      "presets/evm-core/PRESET.md",
      "mcp/evm-rpc.mcp.json",
      "guardrails/transaction-safety.yaml",
      "AGENTS.md",
      "skills-index.md"
    ]
  },
  "Solana Programs": {
    files: [
      "starter-packs/solana-programs-starter.yaml",
      "presets/solana-mainnet/PRESET.md",
      "mcp/solana-rpc.mcp.json",
      "AGENTS.md",
      "skills-index.md"
    ]
  },
  "NEAR Multi-chain": {
    files: [
      "starter-packs/near-multichain-starter.yaml",
      "presets/near-mainnet/PRESET.md",
      "mcp/near-rpc.mcp.json",
      "AGENTS.md",
      "skills-index.md"
    ]
  },
  "Cosmos IBC": {
    files: [
      "starter-packs/cosmos-ibc-starter.yaml",
      "presets/cosmos-ibc/PRESET.md",
      "mcp/cosmos-rpc.mcp.json",
      "AGENTS.md",
      "skills-index.md"
    ]
  },
  "Compliance Guardrails": {
    files: [
      "starter-packs/compliance-guardrails-starter.yaml",
      "guardrails/compliance.yaml",
      "guardrails/security.yaml",
      "guardrails/denied-topics.yaml",
      "AGENTS.md",
      "skills-index.md"
    ]
  }
};

const MCP_TEMPLATES = {
  EVM: ["mcp/evm-rpc.mcp.json"],
  Solana: ["mcp/solana-rpc.mcp.json"],
  NEAR: ["mcp/near-rpc.mcp.json"],
  Cosmos: ["mcp/cosmos-rpc.mcp.json"]
};

const RUNNABLE_EXAMPLES = {
  "EVM ERC-20 Deploy": [
    "examples/evm-erc20-deploy/README.md",
    "examples/evm-erc20-deploy/spec.md",
    "examples/evm-erc20-deploy/plan.md",
    "examples/evm-erc20-deploy/tasks.md",
    "examples/evm-erc20-deploy/Makefile",
    "examples/evm-erc20-deploy/contracts/Token.sol",
    "scripts/validate-skills.py",
    "requirements-proof.txt"
  ],
  "Chain Provider Validation": [
    "examples/chain-provider-validation/README.md",
    "examples/chain-provider-validation/spec.md",
    "examples/chain-provider-validation/plan.md",
    "examples/chain-provider-validation/tasks.md",
    "examples/chain-provider-validation/Makefile",
    "lib/chain_providers",
    "tests/test_chain_providers.py",
    "scripts/validate-skills.py",
    "requirements-proof.txt"
  ]
};

function activate(context) {
  context.subscriptions.push(
    vscode.commands.registerCommand("blockchainSkills.installFullToolkit", async () => {
      const root = getWorkspaceRoot();
      if (!root) return;
      const files = dedupe([
        ...CORE_FILES,
        ...Object.values(AGENT_ADAPTERS).flat(),
        ...Object.values(STARTER_PACKS).flatMap((p) => p.files),
        ...Object.values(MCP_TEMPLATES).flat(),
        "mcp/README.md"
      ]);
      await installFiles(context, root, files, "full toolkit");
    }),
    vscode.commands.registerCommand("blockchainSkills.installCorePack", async () => {
      const root = getWorkspaceRoot();
      if (!root) return;
      await installFiles(context, root, CORE_FILES, "core pack");
    }),
    vscode.commands.registerCommand("blockchainSkills.installAgentAdapters", async () => {
      const root = getWorkspaceRoot();
      if (!root) return;
      const choices = [...Object.keys(AGENT_ADAPTERS), "All"];
      const picked = await vscode.window.showQuickPick(choices, {
        placeHolder: "Choose agent adapters to install"
      });
      if (!picked) return;
      const files = picked === "All" ? dedupe(Object.values(AGENT_ADAPTERS).flat()) : AGENT_ADAPTERS[picked];
      await installFiles(context, root, files, `${picked} adapters`);
    }),
    vscode.commands.registerCommand("blockchainSkills.installStarterPack", async () => {
      const root = getWorkspaceRoot();
      if (!root) return;
      const picked = await vscode.window.showQuickPick(Object.keys(STARTER_PACKS), {
        placeHolder: "Choose a starter pack"
      });
      if (!picked) return;
      await installFiles(context, root, STARTER_PACKS[picked].files, `${picked} starter pack`);
    }),
    vscode.commands.registerCommand("blockchainSkills.installMcpTemplates", async () => {
      const root = getWorkspaceRoot();
      if (!root) return;
      const choices = ["EVM", "Solana", "NEAR", "Cosmos", "All"];
      const picked = await vscode.window.showQuickPick(choices, {
        placeHolder: "Choose MCP templates"
      });
      if (!picked) return;
      const files =
        picked === "All"
          ? dedupe([...Object.values(MCP_TEMPLATES).flat(), "mcp/README.md"])
          : MCP_TEMPLATES[picked];
      await installFiles(context, root, files, `${picked} MCP templates`);
    }),
    vscode.commands.registerCommand("blockchainSkills.scaffoldExample", async () => {
      const root = getWorkspaceRoot();
      if (!root) return;
      const picked = await vscode.window.showQuickPick(Object.keys(RUNNABLE_EXAMPLES), {
        placeHolder: "Choose a runnable example to scaffold"
      });
      if (!picked) return;
      await installFiles(context, root, RUNNABLE_EXAMPLES[picked], `${picked} example`);
    })
  );
}

function deactivate() {}

function getWorkspaceRoot() {
  const folders = vscode.workspace.workspaceFolders;
  if (!folders || folders.length === 0) {
    vscode.window.showErrorMessage("Open a workspace folder before installing the skill pack.");
    return null;
  }
  return folders[0].uri.fsPath;
}

async function installFiles(context, workspaceRoot, relativePaths, label) {
  const collisions = relativePaths.filter((p) => fs.existsSync(path.join(workspaceRoot, p)));
  let overwrite = false;
  if (collisions.length > 0) {
    const choice = await vscode.window.showWarningMessage(
      `${collisions.length} file(s) already exist for ${label}. Overwrite?`,
      { modal: true },
      "Overwrite",
      "Skip Existing",
      "Cancel"
    );
    if (choice === "Cancel" || !choice) return;
    overwrite = choice === "Overwrite";
  }

  let installed = 0;
  let skipped = 0;
  await vscode.window.withProgress(
    { location: vscode.ProgressLocation.Notification, title: `Installing ${label}`, cancellable: false },
    async (progress) => {
      for (let i = 0; i < relativePaths.length; i++) {
        const relativePath = relativePaths[i];
        progress.report({ message: relativePath, increment: 100 / relativePaths.length });
        const targetPath = path.join(workspaceRoot, relativePath);
        if (fs.existsSync(targetPath) && !overwrite) {
          skipped++;
          continue;
        }
        const content = await loadAsset(context, relativePath);
        await fs.promises.mkdir(path.dirname(targetPath), { recursive: true });
        await fs.promises.writeFile(targetPath, content, "utf8");
        installed++;
      }
    }
  );
  vscode.window.showInformationMessage(
    `Installed ${installed} file(s) for ${label}.${skipped ? ` Skipped ${skipped} existing.` : ""}`
  );
}

async function loadAsset(context, relativePath) {
  const localCandidates = [
    path.resolve(context.extensionPath, "..", relativePath),
    path.join(context.extensionPath, "resources", relativePath)
  ];
  for (const candidate of localCandidates) {
    if (fs.existsSync(candidate) && fs.statSync(candidate).isFile()) {
      return fs.promises.readFile(candidate, "utf8");
    }
  }
  const config = vscode.workspace.getConfiguration("blockchainSkills");
  const rawBaseUrl = config.get(
    "rawBaseUrl",
    "https://raw.githubusercontent.com/vaquarkhan/blockchain-agent-skills/main"
  );
  const url = `${String(rawBaseUrl).replace(/\/$/, "")}/${relativePath.replace(/\\/g, "/")}`;
  return downloadText(url);
}

function downloadText(url) {
  return new Promise((resolve, reject) => {
    https
      .get(url, (response) => {
        if (response.statusCode >= 300 && response.statusCode < 400 && response.headers.location) {
          resolve(downloadText(response.headers.location));
          return;
        }
        if (response.statusCode !== 200) {
          reject(new Error(`Failed to download ${url}: ${response.statusCode}`));
          return;
        }
        const chunks = [];
        response.on("data", (chunk) => chunks.push(chunk));
        response.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
      })
      .on("error", reject);
  });
}

function dedupe(items) {
  return [...new Set(items)];
}

module.exports = { activate, deactivate };
