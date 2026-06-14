# Per-skill Bedrock AgentCore file set (Section 7.1)

```
skills/{skill-name}/
├── SKILL.md                  # Cursor agent skill (this repo)
├── skill-definition.yaml     # Skill metadata, chains, MCP tools, guardrails
├── action-group.json         # Bedrock action group definition
├── openapi.yaml              # OpenAPI 3.0 function schemas
├── lambda/
│   ├── handler.py            # Python 3.12 Lambda router
│   └── requirements.txt      # web3, boto3, pydantic, chain SDKs
├── tests/
│   └── test_handler.py       # pytest with mocked RPC
└── README.md                 # Deployment prerequisites
```

Copy from `templates/` when implementing a new skill for Bedrock deployment.
