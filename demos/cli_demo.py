from role_model.core import Runtime, MemoryConfig, PRIMEConfig, DEFAULT_PROVIDER_FACTORY

def main():
    rt = Runtime(provider_factory=DEFAULT_PROVIDER_FACTORY,
                 memory_cfg=MemoryConfig(ephemeral=True, max_turns=6),
                 prime_cfg=PRIMEConfig(enabled=False))
    roles = rt.list_roles()
    print("> select role:", roles)
    role = input("Role? ").strip()
    prime = input("PRIME governance? [y/N]: ").lower().startswith("y")
    rt.prime_cfg.enabled = prime
    print(f"(using role '{role}' | PRIME={prime}) Type 'exit' to quit.")
    while True:
        msg = input(f"({role}) You: ").strip()
        if msg.lower() in {"exit", "quit"}:
            print("bye.")
            break
        try:
            out = rt.run(role, msg)
            print(f"({role}) Role: {out}\n")
        except Exception as e:
            print(f"error: {e}")

if __name__ == "__main__":
    main()
