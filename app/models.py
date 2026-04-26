from typing import Optional
from pydantic import BaseModel

DEFAULT_LLAMA_SERVER = "llama-server.exe"


class ModelConfig(BaseModel):
    name: str
    model_path: str
    host: Optional[str] = "0.0.0.0"
    port: str
    context_size: Optional[str] = ""
    gpu_layers: Optional[str] = ""
    threads: Optional[str] = ""
    temp: Optional[str] = ""
    top_p: Optional[str] = ""
    top_k: Optional[str] = ""
    min_p: Optional[str] = ""
    repeat_penalty: Optional[str] = ""
    presence_penalty: Optional[str] = ""
    reasoning_budget: Optional[str] = ""
    mmproj_path: Optional[str] = ""
    llama_server_path: Optional[str] = DEFAULT_LLAMA_SERVER


def model_to_dict(model):
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()
