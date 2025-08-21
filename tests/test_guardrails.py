from role_model.core import Runtime, MemoryConfig, PRIMEConfig, DEFAULT_PROVIDER_FACTORY

def test_out_of_scope_refusal():
    rt = Runtime(provider_factory=DEFAULT_PROVIDER_FACTORY,
                 memory_cfg=MemoryConfig(ephemeral=True),
                 prime_cfg=PRIMEConfig(enabled=False))
    out = rt.run("construction_uniform_specialist", "Design a BGP policy for peering.")
    assert out.startswith("[refusal]")

def test_in_scope_allows_response():
    rt = Runtime(provider_factory=DEFAULT_PROVIDER_FACTORY,
                 memory_cfg=MemoryConfig(ephemeral=True),
                 prime_cfg=PRIMEConfig(enabled=False))
    out = rt.run("network_systems_architect", "Create a firewall filter for east-west traffic segmentation.")
    assert "[in-scope]" in out
