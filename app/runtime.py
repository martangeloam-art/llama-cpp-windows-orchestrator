import json
import os
import re
import shlex
import time
import urllib.request
import subprocess
from typing import Dict, Any

from .models import ModelConfig, DEFAULT_LLAMA_SERVER
from .storage import read_configs

os.makedirs("logs", exist_ok=True)

active_processes: Dict[int, subprocess.Popen] = {}
log_files: Dict[int, Any] = {}
runtime_state: Dict[int, dict] = {}


def safe_int(value, default=0):
    try:
        if value is None or str(value).strip() == "":
            return default
        return int(float(str(value).strip()))
    except Exception:
        return default


def maybe_add_arg(cmd, flag, value):
    if value is None:
        return
    value = str(value).strip()
    if value != "":
        cmd.extend([flag, value])


def build_command(config: ModelConfig):
    server = (config.llama_server_path or DEFAULT_LLAMA_SERVER).strip() or DEFAULT_LLAMA_SERVER
    cmd = [server, "-m", config.model_path]

    maybe_add_arg(cmd, "--host", config.host)
    maybe_add_arg(cmd, "--port", config.port)
    maybe_add_arg(cmd, "-c", config.context_size)
    maybe_add_arg(cmd, "--gpu-layers", config.gpu_layers)
    maybe_add_arg(cmd, "--threads", config.threads)
    maybe_add_arg(cmd, "--temp", config.temp)
    maybe_add_arg(cmd, "--top-p", config.top_p)
    maybe_add_arg(cmd, "--top-k", config.top_k)
    maybe_add_arg(cmd, "--min-p", config.min_p)
    maybe_add_arg(cmd, "--repeat-penalty", config.repeat_penalty)
    maybe_add_arg(cmd, "--presence-penalty", config.presence_penalty)
    maybe_add_arg(cmd, "--mmproj", config.mmproj_path)
    maybe_add_arg(cmd, "--reasoning-budget", config.reasoning_budget)

    return cmd


def get_slot_state(port: int) -> str:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/slots", timeout=2) as resp:
            raw = resp.read().decode("utf-8", errors="ignore")
            data = json.loads(raw)

        if isinstance(data, dict) and "slots" in data:
            slots = data["slots"]
        elif isinstance(data, list):
            slots = data
        else:
            slots = []

        for slot in slots:
            state = str(slot.get("state", "")).lower()
            if slot.get("is_processing") is True:
                return "processing"
            if state and state not in ("idle", "none", "empty"):
                return "processing"

        return "idle"
    except Exception:
        return "unknown"


def update_runtime_state(port: int):
    state = runtime_state.get(port)
    if not state:
        return

    proc = active_processes.get(port)
    if not proc or proc.poll() is not None:
        state["status"] = "stopped"
        return

    slot_state = get_slot_state(port)
    if slot_state in ("idle", "processing"):
        state["status"] = slot_state
        if slot_state == "processing":
            state["last_seen_busy"] = time.time()
        return

    log_path = state.get("log_path")
    if log_path and os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                data = f.read()[-30000:]
            if re.search(r"prompt eval|POST /completion|POST /v1/chat/completions|tokens/s", data, re.IGNORECASE):
                state["status"] = "processing"
                state["last_seen_busy"] = time.time()
                return
        except Exception:
            pass

    if time.time() - state.get("last_seen_busy", 0) < 10:
        state["status"] = "processing"
    else:
        state["status"] = "idle"


def get_saved_rows():
    configs = read_configs()
    rows = []

    for name, cfg in configs.items():
        port = safe_int(cfg.get("port", ""), 0)
        running = port in active_processes and active_processes[port].poll() is None
        rows.append({
            "name": name,
            "model_path": cfg.get("model_path", ""),
            "port": cfg.get("port", ""),
            "status": "running" if running else "saved"
        })

    rows.sort(key=lambda x: x["name"].lower())
    return rows


def get_running_rows():
    rows = []

    for port, proc in list(active_processes.items()):
        if proc.poll() is not None:
            if port in log_files:
                try:
                    log_files[port].close()
                except Exception:
                    pass
                del log_files[port]
            if port in runtime_state:
                runtime_state[port]["status"] = "stopped"
            del active_processes[port]
            continue

        update_runtime_state(port)
        state = runtime_state.get(port, {})
        rows.append({
            "name": state.get("name", f"Port {port}"),
            "model_path": state.get("model_path", ""),
            "port": port,
            "status": state.get("status", "unknown"),
            "log_path": state.get("log_path", f"logs/port_{port}.log")
        })

    rows.sort(key=lambda x: int(x["port"]))
    return rows


def start_configured_model(name: str):
    configs = read_configs()
    if name not in configs:
        raise FileNotFoundError("Configuration not found")

    cfg = ModelConfig(**configs[name])

    if not os.path.exists(cfg.model_path):
        raise FileNotFoundError(f"Model file not found: {cfg.model_path}")

    port = safe_int(cfg.port, 0)
    if not port:
        raise ValueError("Invalid port")

    existing = active_processes.get(port)
    if existing and existing.poll() is None:
        raise RuntimeError(f"Port {port} is already in use")

    cmd = build_command(cfg)
    log_path = f"logs/port_{port}.log"
    log_f = open(log_path, "w", encoding="utf-8")

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=log_f,
            stderr=subprocess.STDOUT,
            text=True
        )
    except FileNotFoundError:
        log_f.close()
        raise FileNotFoundError(f"llama-server executable not found: {cfg.llama_server_path}")
    except Exception:
        log_f.close()
        raise

    active_processes[port] = proc
    log_files[port] = log_f
    runtime_state[port] = {
        "name": cfg.name,
        "model_path": cfg.model_path,
        "status": "idle",
        "log_path": log_path,
        "last_seen_busy": 0
    }

    return {
        "status": "started",
        "name": cfg.name,
        "port": port,
        "pid": proc.pid,
        "command": shlex.join(cmd)
    }


def stop_model(port: int):
    proc = active_processes.get(port)
    if not proc:
        raise FileNotFoundError("Running model not found")

    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)

    if port in log_files:
        try:
            log_files[port].close()
        except Exception:
            pass
        del log_files[port]

    if port in active_processes:
        del active_processes[port]

    if port in runtime_state:
        runtime_state[port]["status"] = "stopped"

    return {"status": "stopped", "port": port}


def read_logs(port: int):
    log_path = f"logs/port_{port}.log"
    if not os.path.exists(log_path):
        return {"log": "No logs available yet."}

    try:
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            return {"log": f.read()[-40000:]}
    except Exception as e:
        return {"log": f"Could not read logs: {e}"}
