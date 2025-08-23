# Role Model MVP

A lightweight framework for **scoped AI agent behavior** with modular roles, memory hygiene, and runtime guardrails.

## What it does

Role Model treats each AI agent as a **Role** with strict boundaries:
- **Modular Containment** – Roles are isolated with no cross-contamination
- **Scope Guardrails** – Out-of-scope queries are automatically rejected
- **Memory Hygiene** – Ephemeral context by default, explicit persistence when needed
- **Governance Mode** – PRIME flag for stricter compliance behavior

**LLM-agnostic** – Works with any provider. Ships with echo provider for demos, OpenAI integration included.

## Quick Start

```bash
git clone https://github.com/your-username/role-model-mvp.git
cd role-model-mvp
pip install -r requirements.txt
python demos/cli_demo.py
```

Example session:
```
> select role: ['network_systems_architect', 'construction_uniform_specialist']
Role? network_systems_architect
(network_systems_architect) You: Design a scalable ACL for east-west traffic
(network_systems_architect) Role: [in-scope] Here's a structured approach...

(network_systems_architect) You: What should I wear to a wedding?
(network_systems_architect) Role: [refusal] This role is scoped to network design. Try a different role.
```

## Architecture

```
role_model/
├── core.py              # Runtime, guardrails, memory management
├── providers.py         # LLM provider abstractions  
└── roles/              # Role definitions
    ├── network_systems_architect.py
    └── construction_uniform_specialist.py
```

**Core Components:**
- `RoleSpec` – Declarative role definition (scope, voice, constraints)
- `Runtime` – Enforces guardrails and manages role lifecycle
- `BaseRole` – Template for scoped agent behavior
- `MemoryConfig` – Controls context retention and cleanup

## Add New Roles

```python
# role_model/roles/my_role.py
from role_model.roles.base import BaseRole, RoleSpec

spec = RoleSpec(
    name="my_role",
    summary="Focused expertise area",
    in_scope_examples=["Valid query types"],
    out_of_scope_examples=["Invalid requests"],
    voice="professional, direct"
)

class MyRole(BaseRole):
    spec = spec
```

Auto-discovered by runtime.

## Optional: Real LLM

```bash
export OPENAI_API_KEY=sk-...
python demos/cli_demo.py  # Now uses GPT-4o-mini
```

## API Demo

```bash
uvicorn api.demo_api:app --reload
curl -X POST localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"role":"network_systems_architect","query":"Design firewall rules"}'
```

## Why This Matters

Most AI agents have fuzzy boundaries and mixed contexts. Role Model enforces clean separation:
- Prevents scope creep and hallucinated expertise
- Enables reliable multi-agent orchestration
- Provides governance hooks for compliance
- Maintains conversation hygiene across role switches

**Built for:** AI infrastructure, agent orchestration, production deployments where behavior boundaries matter.

---

> Disclaimer: This repo is an independent open-source project for demonstration purposes. It does not constitute the full Role Model or Companion frameworks, nor does it imply open-source licensing of proprietary IP.
