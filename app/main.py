import psutil
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from .models import ModelConfig, model_to_dict
from .storage import read_configs, write_configs
from .runtime import (
    get_saved_rows,
    get_running_rows,
    start_configured_model,
    stop_model,
    read_logs,
)
from .ui import HTML_UI

app = FastAPI(title="Simple llama.cpp Orchestrator")


@app.get("/", response_class=HTMLResponse)
def index():
    return HTML_UI


@app.get("/memory")
def memory():
    mem = psutil.virtual_memory()
    return {
        "total_gb": round(mem.total / (1024 ** 3), 2),
        "used_gb": round(mem.used / (1024 ** 3), 2),
        "available_gb": round(mem.available / (1024 ** 3), 2),
        "percent": round(mem.percent, 1),
    }


@app.get("/configs")
def list_configs():
    return get_saved_rows()


@app.get("/configs/{name}")
def get_config(name: str):
    configs = read_configs()
    if name not in configs:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return configs[name]


@app.post("/configs")
def save_config(config: ModelConfig):
    if not config.name.strip():
        raise HTTPException(status_code=400, detail="Name is required")
    if not config.model_path.strip():
        raise HTTPException(status_code=400, detail="Model path is required")
    if not str(config.port).strip():
        raise HTTPException(status_code=400, detail="Port is required")

    configs = read_configs()
    configs[config.name.strip()] = model_to_dict(config)
    write_configs(configs)
    return {"status": "saved", "name": config.name.strip()}


@app.delete("/configs/{name}")
def delete_config(name: str):
    configs = read_configs()
    if name in configs:
        del configs[name]
        write_configs(configs)
    return {"status": "deleted", "name": name}


@app.get("/running")
def running():
    return get_running_rows()


@app.post("/start/{name}")
def start_model(name: str):
    try:
        return start_configured_model(name)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/stop/{port}")
def stop_running_model(port: int):
    try:
        return stop_model(port)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/logs/{port}")
def get_logs(port: int):
    return read_logs(port)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
