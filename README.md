# llama.cpp Windows Orchestrator

A lightweight web dashboard for configuring, saving, launching, stopping, and monitoring multiple `llama-server` instances on a Windows machine.

It is designed for local or remote management of `llama.cpp` model servers with a simple UI: save model configurations, reuse them later, start or stop models on specific ports, view whether a model is idle or processing, and inspect live logs from the browser. The project was built around a Windows-based local LLM workflow and works well with remote access over LAN or Tailscale when the dashboard is exposed correctly. 

## Features

- Save model configurations without starting them.
- Edit existing saved configurations.
- Start a saved configuration on its configured port.
- Stop a running model from the dashboard.
- Show simple runtime state: idle, processing, stopped, or unknown.
- View live logs for running models.
- Keep logs hidden until you open them.
- Preserve scroll position in the log viewer during refresh.
- Optional remote access over LAN or Tailscale.
- Keep configuration fields optional where possible, so empty fields are simply omitted from the generated `llama-server` command.

## Project structure

Base structure:

```text
llama-cpp-windows-orchestrator/
├─ app/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ models.py
│  ├─ storage.py
│  ├─ runtime.py
│  └─ ui.py
├─ logs/
├─ saved_configs.json
├─ requirements.txt
├─ README.md
└─ .gitignore
```

This keeps the FastAPI entrypoint separate from UI generation, persistence helpers, and runtime process management, which makes future changes much easier. 

## File split rationale

### `app/main.py`
FastAPI app setup, routes, and `uvicorn` startup entrypoint.

### `app/models.py`
Pydantic models such as `ModelConfig`.

### `app/storage.py`
Read/write logic for `saved_configs.json`.

### `app/runtime.py`
Process launch, stop, status polling, log reading, and command construction for `llama-server`.

### `app/ui.py`
The `HTML_UI` block for the dashboard.

This split preserves the same functionality while making the codebase more manageable for GitHub and future iteration. 

## Requirements

- Windows machine with Python 3.10+ recommended.
- `llama-server.exe` from `llama.cpp` available locally.
- One or more GGUF models stored locally.
- Optional MMProj file for multimodal models.
- Network/firewall access if you want to use the dashboard remotely.

## Installation

1. Clone the repository.
2. Create a virtual environment.
3. Install Python dependencies.
4. Make sure `llama-server.exe` is available either in the project folder, on your `PATH`, or set explicitly in the UI.

### Example setup

```powershell
git clone https://github.com/martangeloam-art/llama-cpp-windows-orchestrator.git
cd llama-cpp-windows-orchestrator
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## `requirements.txt`

A minimal dependency set for the latest version is:

```txt
fastapi
uvicorn
psutil
pydantic
```

If you later add GGUF metadata inspection again, you can also add `gguf`.

## Running the app

```powershell/terminal
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Using explicit Uvicorn startup is often helpful when troubleshooting remote access or binding behavior. 

## Open the dashboard

From the Windows machine itself:

```text
http://127.0.0.1:8000
```

From another machine on the LAN:

```text
http://<windows-lan-ip>:8000
```

Over Tailscale:

```text
http://<tailscale-ip>:8000
```

The dashboard must be listening on `0.0.0.0` or a specific reachable interface, and Windows Firewall must allow the dashboard port.

## How to use

### 1. Create a configuration

Fill in the form on the left side of the dashboard.

Typical fields:
- Configuration name, a friendly label used in the saved list.
- Model path, path to the local GGUF model.
- Host, usually `0.0.0.0` when you want network access.
- Port, the port where `llama-server` will listen.
- Context size and generation parameters like `temp`, `top_p`, `top_k`, `min_p`, `repeat_penalty`, and `presence_penalty`.
- Optional `reasoning_budget`.
- Optional `mmproj_path` for multimodal models.
- Optional explicit path to `llama-server.exe`.

If you leave optional fields empty, the launcher omits them and lets `llama.cpp` use its own defaults.

### 2. Save the configuration

Click **Save configuration**. The config is written to `saved_configs.json` so it remains available after restarting the dashboard. 

### 3. Edit a saved configuration

In the **Saved configurations** table, click **Edit**. The selected config is loaded back into the form for modification. 

### 4. Start a model

Click **Start** on a saved configuration. The app launches `llama-server` with the corresponding arguments and stores the process handle for later monitoring and termination. 

### 5. Stop a model

In **Running models**, click **Stop**. The dashboard terminates the process and updates its status. 

### 6. Inspect logs

Click **Show logs** for a running model. The latest version of the UI keeps log scroll position stable during refresh, and only follows the bottom automatically when you were already near the bottom. 

## Runtime status meanings

- **Idle**: the model is running and not actively processing a request.
- **Processing**: the model is handling an active request, usually inferred from `/slots` or recent log activity.
- **Stopped**: the process is no longer running.
- **Unknown**: the process is running but the UI could not confidently determine activity state. 


## Roadmap ideas

Future improvements ideas:

- Add export/import for configs.
- Add per-model health checks.
- Add a lightweight REST API for config management.
- Add model templates for common presets. 
