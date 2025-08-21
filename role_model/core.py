from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
import importlib, pkgutil, re

@dataclass
class RoleSpec:
    name: str
    summary: str
    in_scope_examples: List[str]
    out_of_scope_examples: List[str]
    banned_terms: List[str] = field(default_factory=list)
    voice: str = "neutral"
    keywords_allow: List[str] = field(default_factory=list)
    keywords_deny: List[str] = field(default_factory=list)

@dataclass
class MemoryConfig:
    ephemeral: bool = True
    max_turns: int = 8
    persistent_namespace: Optional[str] = None

@dataclass
class PRIMEConfig:
    enabled: bool = False
    strict_refusals: bool = True
    strip_context_on_refusal: bool = True

class Refusal(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class BaseRole:
    spec: RoleSpec
    def __init__(self, provider: Callable[[List[Dict[str, str]]], str]):
        self.provider = provider
        self.memory: List[Dict[str, str]] = []

    def check_scope(self, text: str, prime: PRIMEConfig):
        t = text.lower()
        for term in self.spec.banned_terms:
            if term.lower() in t:
                raise Refusal(self._refusal_text("banned", prime))
        if self.spec.keywords_allow and not any(k.lower() in t for k in self.spec.keywords_allow):
            raise Refusal(self._refusal_text("out_of_scope", prime))
        if any(k.lower() in t for k in self.spec.keywords_deny):
            raise Refusal(self._refusal_text("out_of_scope", prime))

    def _refusal_text(self, kind: str, prime: PRIMEConfig) -> str:
        base = {"banned": "This request includes a disallowed term for this role.",
                "out_of_scope": f"This role is scoped to: {self.spec.summary}"}[kind]
        if prime.enabled and prime.strict_refusals:
            return base + " (PRIME governance active)"
        return base + " Try a different role."

    def respond(self, user_text: str, prime: PRIMEConfig) -> str:
        self.check_scope(user_text, prime)
        system = (f"You are the '{self.spec.name}' role. Voice: {self.spec.voice}. "
                  f"Stay within scope: {self.spec.summary}. Refuse anything out of scope.")
        messages = [{"role":"system","content":system}, *self.memory, {"role":"user","content":user_text}]
        reply = self.provider(messages)
        return reply

class Runtime:
    def __init__(self, provider_factory: Callable[[], Callable],
                 memory_cfg: Optional[MemoryConfig]=None,
                 prime_cfg: Optional[PRIMEConfig]=None):
        self.provider_factory = provider_factory
        self.memory_cfg = memory_cfg or MemoryConfig()
        self.prime_cfg = prime_cfg or PRIMEConfig()
        self.roles: Dict[str, BaseRole] = {}
        self._discover_roles()

    def _discover_roles(self):
        import role_model.roles as roles_pkg
        prefix = roles_pkg.__name__ + "."
        for m in pkgutil.iter_modules(roles_pkg.__path__):
            mod = importlib.import_module(prefix + m.name)
            # find a subclass of BaseRole
            for attr in dir(mod):
                obj = getattr(mod, attr)
                try:
                    if isinstance(obj, type) and issubclass(obj, BaseRole) and obj is not BaseRole:
                        instance = obj(provider=self.provider_factory())
                        self.roles[instance.spec.name] = instance
                        break
                except Exception:
                    continue

    def list_roles(self) -> List[str]:
        return list(self.roles.keys())

    def run(self, role: str, text: str) -> str:
        if role not in self.roles:
            raise ValueError(f"Unknown role: {role}. Available: {self.list_roles()}")
        r = self.roles[role]
        try:
            out = r.respond(text, self.prime_cfg)
            r.memory.append({"role":"user","content":text})
            r.memory.append({"role":"assistant","content":out})
            if self.memory_cfg.ephemeral:
                r.memory = r.memory[-2*self.memory_cfg.max_turns:]
            return out
        except Refusal as e:
            if self.prime_cfg.strip_context_on_refusal:
                r.memory.clear()
            return f"[refusal] {e.message}"

def echo_provider(messages: List[Dict[str, str]]) -> str:
    system = next((m["content"] for m in messages if m["role"]=="system"), "")
    role_name = "role"
    m = re.search(r"the '(.+?)' role", system)
    if m:
        role_name = m.group(1)
    user = [m["content"] for m in messages if m["role"]=="user"][-1]
    return (
        f"[in-scope] ({role_name}) Here's a structured response:\\n"
        f"- Understanding: {user[:180]}\\n"
        f"- Plan: 1) clarify constraints, 2) propose options, 3) next actions.\\n"
        f"- Notes: Demo echo provider. Plug a real LLM to upgrade."
    )

# Lazy default provider factory: attempts OpenAI if env var exists, otherwise echo.
def DEFAULT_PROVIDER_FACTORY():
    import os
    if os.environ.get("OPENAI_API_KEY"):
        try:
            from role_model.providers import openai_provider
            return openai_provider
        except Exception:
            return echo_provider
    return echo_provider
