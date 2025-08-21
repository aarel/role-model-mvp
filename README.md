# Role Model – MVP

A tiny, demonstrable framework for **scoped AI agent behavior**: **modular roles**, **memory hygiene**, and **runtime guardrails**. 
Use it to showcase the core of your patent‑pending Role Model idea with a simple CLI and optional API for demos/GitHub.

> Session tag: *Career Switch to AI – Real Work, Real Risk*

---

## What this is

**Role Model** treats each agent as a **Role** with a declarative spec and strict runtime boundaries. 
The runtime enforces:
- **Modular Containment** – Roles are isolated; no cross‑bleed.
- **Scope Guardrails** – Each role declares what it does/doesn't do. Out‑of‑scope queries are rejected.
- **Memory Hygiene** – Context is ephemeral by default; persistent memory is explicit and namespaced per role.
- **Governance Hooks** – A (stub) PRIME governance mode can be toggled to enforce stricter behavior.

This MVP is **LLM‑agnostic**. It works out‑of‑the‑box with a simple deterministic responder for demos. 
If you set `OPENAI_API_KEY`, it can use OpenAI through a small provider shim.

---

## Quickstart

```bash
git clone https://github.com/your-username/role-model-mvp.git
cd role-model-mvp
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
python demos/cli_demo.py
```

Example session:

```
> select role: [network_systems_architect, construction_uniform_specialist]
Role? network_systems_architect
PRIME governance? [y/N]: n
(network_systems_architect) You: Design a scalable ACL for east-west traffic.
(network_systems_architect) Role: [in-scope] Consider segmentation by ...

(network_systems_architect) You: What should I wear to a wedding?
(network_systems_architect) Role: [out-of-scope] This role is scoped to network systems. Try 'construction_uniform_specialist' instead.
```

Run the optional API (if you installed FastAPI/uvicorn):

```bash
uvicorn api.demo_api:app --reload --port 8000
# Then POST to /run
curl -X POST localhost:8000/run -H "Content-Type: application/json"   -d '{"role":"network_systems_architect","query":"Design a firewall filter..."}'
```

---

## Repo layout

```
role-model-mvp/
├─ role_model/
│  ├─ __init__.py
│  ├─ core.py                 # Runtime, guardrails, memory hygiene
│  ├─ providers.py            # EchoProvider + optional OpenAIProvider
│  └─ roles/
│     ├─ base.py
│     ├─ network_systems_architect.py
│     └─ construction_uniform_specialist.py
├─ demos/
│  └─ cli_demo.py
├─ api/
│  └─ demo_api.py             # Optional FastAPI demo (extra)
├─ tests/
│  └─ test_guardrails.py
├─ requirements.txt
├─ README.md
└─ LICENSE
```

---

## Design primitives

- **RoleSpec** — declarative metadata describing scope, constraints, and voice.
- **Role** — binds a spec to a `respond()` implementation that calls a provider (Echo/OpenAI).
- **Runtime** — enforces guardrails (scope checks, banned terms), governs memory hygiene, and toggles **PRIME** mode.
- **Memory** — ephemeral by default; explicit, namespaced persistence if enabled.
- **Refusals** — standard, friendly denials for out‑of‑scope/banned requests.

### PRIME (governance) mode

This MVP includes a simple PRIME flag that hardens refusals and strips any non‑essential context. 
It’s a placeholder to demo how a governance runtime can alter behavior.

---

## Configure an LLM (optional)

Set `OPENAI_API_KEY` in your environment to use the OpenAI provider. If not set, the **EchoProvider** is used which produces structured, deterministic output for demos.

```bash
export OPENAI_API_KEY=sk-...   # Windows: setx OPENAI_API_KEY "..."
```

---

## Extend: add a new role

Create `role_model/roles/my_role.py`:

```python
from role_model.roles.base import BaseRole, RoleSpec

spec = RoleSpec(
    name="my_role",
    summary="Short description.",
    in_scope_examples=["What are X?", "How do I Y?"],
    out_of_scope_examples=["Unrelated planning", "Medical advice"],
    banned_terms=["forbidden"],
    voice="crisp, helpful, domain-focussed"
)

class MyRole(BaseRole):
    spec = spec
```

Then it’s auto‑discoverable by the runtime.

---

## Why this helps your portfolio

- **Shows a working interpretation** of your Role Model architecture.
- **Demonstrates guardrails & hygiene** in a way hiring managers can read quickly.
- **Easily demoable** in interviews (CLI) and as a small service (API).
- **LLM‑agnostic** with a drop‑in provider shim.

---

## Notes

- This repository is an MVP and not a production policy engine.
- Mentions of Role Model and Companion align with your patent‑pending framework; keep it scoped to demonstrations.
- Licensed MIT for maximum sharing.

---

**Author:** Adam Arellano · Austin, TX · 2025
