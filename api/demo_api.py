from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from role_model.core import Runtime, MemoryConfig, PRIMEConfig, DEFAULT_PROVIDER_FACTORY

app = FastAPI(title="Role Model MVP API")

rt = Runtime(provider_factory=DEFAULT_PROVIDER_FACTORY,
             memory_cfg=MemoryConfig(ephemeral=True, max_turns=6),
             prime_cfg=PRIMEConfig(enabled=False))

class RunReq(BaseModel):
    role: str
    query: str
    prime: bool = False

@app.post("/run")
def run(req: RunReq):
    rt.prime_cfg.enabled = req.prime
    try:
        out = rt.run(req.role, req.query)
        return {"role": req.role, "prime": req.prime, "output": out}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/roles")
def roles():
    return {"roles": rt.list_roles()}
