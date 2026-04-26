HTML_UI = r"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>llama.cpp Orchestrator</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    :root {
      --bg: #07111f;
      --bg-2: #0b172a;
      --panel: rgba(15, 23, 42, 0.78);
      --panel-strong: rgba(17, 24, 39, 0.95);
      --panel-soft: rgba(30, 41, 59, 0.72);
      --text: #e5eefc;
      --muted: #94a3b8;
      --accent: #4f8cff;
      --accent-2: #7c3aed;
      --accent-3: #06b6d4;
      --good: #22c55e;
      --warn: #f59e0b;
      --bad: #ef4444;
      --border: rgba(255,255,255,0.08);
      --shadow: 0 20px 50px rgba(0,0,0,0.35);
      --radius: 18px;
    }

    * { box-sizing: border-box; }
    body {
      margin: 0;
      color: var(--text);
      font-family: Inter, Segoe UI, Arial, sans-serif;
      background:
        radial-gradient(circle at top left, rgba(79,140,255,0.18), transparent 25%),
        radial-gradient(circle at top right, rgba(124,58,237,0.16), transparent 25%),
        radial-gradient(circle at bottom center, rgba(6,182,212,0.10), transparent 20%),
        linear-gradient(180deg, var(--bg), var(--bg-2));
      min-height: 100vh;
    }
    .wrap {
      max-width: 1380px;
      margin: 0 auto;
      padding: 28px 22px 40px;
    }
    .hero {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      gap: 20px;
      margin-bottom: 20px;
    }
    .hero h1 {
      margin: 0 0 8px;
      font-size: 34px;
      letter-spacing: -0.03em;
      font-weight: 800;
    }
    .subtitle {
      color: var(--muted);
      max-width: 760px;
      line-height: 1.5;
      font-size: 15px;
    }
    .pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      border: 1px solid var(--border);
      background: rgba(255,255,255,0.05);
      padding: 10px 14px;
      border-radius: 999px;
      color: #d8e5ff;
      font-size: 13px;
      backdrop-filter: blur(10px);
    }
    .topbar {
      display: grid;
      grid-template-columns: 1.3fr 1fr;
      gap: 16px;
      margin-bottom: 20px;
    }
    .card {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      backdrop-filter: blur(18px);
      -webkit-backdrop-filter: blur(18px);
    }
    .card-inner {
      padding: 18px 18px 16px;
    }
    .memory-card {
      position: relative;
      overflow: hidden;
    }
    .memory-card::before {
      content: "";
      position: absolute;
      inset: 0;
      background: linear-gradient(135deg, rgba(79,140,255,0.08), rgba(124,58,237,0.04));
      pointer-events: none;
    }
    .memory-label {
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 8px;
      position: relative;
    }
    .memory-value {
      font-size: 28px;
      font-weight: 800;
      position: relative;
      margin-bottom: 8px;
    }
    .memory-sub {
      color: var(--muted);
      font-size: 14px;
      position: relative;
      line-height: 1.4;
    }
    .progress {
      height: 10px;
      border-radius: 999px;
      background: rgba(255,255,255,0.08);
      overflow: hidden;
      margin-top: 14px;
      position: relative;
    }
    .bar {
      height: 100%;
      width: 0%;
      border-radius: 999px;
      background: linear-gradient(90deg, var(--accent), var(--accent-2), var(--accent-3));
      transition: width 0.3s ease;
    }
    .layout {
      display: grid;
      grid-template-columns: 430px 1fr;
      gap: 20px;
    }
    .stack {
      display: grid;
      gap: 20px;
    }
    h2 {
      margin: 0 0 16px;
      font-size: 18px;
      font-weight: 700;
      letter-spacing: -0.01em;
    }
    .section-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 14px;
    }
    .section-note {
      color: var(--muted);
      font-size: 12px;
    }
    .grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }
    .full {
      grid-column: 1 / -1;
    }
    label {
      display: block;
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }
    input {
      width: 100%;
      margin-top: 8px;
      border: 1px solid rgba(255,255,255,0.08);
      background: rgba(15, 23, 42, 0.92);
      color: var(--text);
      border-radius: 14px;
      padding: 12px 14px;
      outline: none;
      transition: all 0.2s ease;
      font-size: 14px;
    }
    input:focus {
      border-color: rgba(79,140,255,0.55);
      box-shadow: 0 0 0 4px rgba(79,140,255,0.12);
      transform: translateY(-1px);
    }
    .buttons {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 16px;
    }
    button {
      border: 0;
      border-radius: 12px;
      padding: 11px 15px;
      cursor: pointer;
      color: white;
      font-weight: 700;
      font-size: 13px;
      letter-spacing: 0.01em;
      transition: transform 0.15s ease, opacity 0.15s ease, box-shadow 0.15s ease;
      box-shadow: 0 10px 20px rgba(0,0,0,0.18);
    }
    button:hover {
      transform: translateY(-1px);
      opacity: 0.96;
    }
    button:active {
      transform: translateY(0);
    }
    button.primary {
      background: linear-gradient(135deg, var(--accent), var(--accent-2));
    }
    button.secondary {
      background: rgba(71, 85, 105, 0.95);
    }
    button.danger {
      background: linear-gradient(135deg, #dc2626, #ef4444);
    }
    .status {
      margin-top: 16px;
      background: rgba(2, 6, 23, 0.65);
      border: 1px solid rgba(255,255,255,0.06);
      border-radius: 14px;
      padding: 14px;
      white-space: pre-wrap;
      font-size: 13px;
      min-height: 92px;
      color: #d9e6ff;
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
    }
    .right-stack {
      display: grid;
      gap: 20px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
    }
    th, td {
      text-align: left;
      padding: 13px 10px;
      border-bottom: 1px solid rgba(255,255,255,0.06);
      vertical-align: top;
      font-size: 14px;
    }
    th {
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      font-weight: 700;
    }
    tr:hover td {
      background: rgba(255,255,255,0.015);
    }
    .name-cell strong {
      display: block;
      font-size: 14px;
      color: #f5f9ff;
    }
    .tiny {
      color: var(--muted);
      font-size: 12px;
      line-height: 1.4;
      margin-top: 4px;
      word-break: break-all;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 10px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.02em;
      border: 1px solid rgba(255,255,255,0.06);
      backdrop-filter: blur(8px);
    }
    .badge::before {
      content: "";
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: currentColor;
      opacity: 0.95;
    }
    .saved { background: rgba(79,140,255,0.14); color: #93c5fd; }
    .running { background: rgba(34,197,94,0.14); color: #86efac; }
    .idle { background: rgba(34,197,94,0.14); color: #86efac; }
    .processing { background: rgba(245,158,11,0.14); color: #fdba74; }
    .unknown { background: rgba(148,163,184,0.14); color: #cbd5e1; }
    .stopped { background: rgba(239,68,68,0.14); color: #fca5a5; }
    .table-actions {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    .table-actions button {
      padding: 8px 11px;
      font-size: 12px;
      border-radius: 10px;
      box-shadow: none;
    }
    .logbox {
      margin-top: 12px;
      background: rgba(2, 6, 23, 0.92);
      border: 1px solid rgba(255,255,255,0.06);
      border-radius: 16px;
      padding: 14px;
      color: #d4def5;
      font-family: Consolas, monospace;
      font-size: 12px;
      line-height: 1.5;
      white-space: pre-wrap;
      max-height: 420px;
      overflow: auto;
      display: none;
      scroll-behavior: auto;
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
    }
    .log-title {
      display: block;
      margin-bottom: 10px;
      color: #f8fbff;
      font-family: Inter, Segoe UI, Arial, sans-serif;
      font-size: 13px;
      font-weight: 700;
    }
    .empty {
      color: var(--muted);
      font-size: 13px;
      padding: 8px 0 2px;
    }
    @media (max-width: 980px) {
      .layout { grid-template-columns: 1fr; }
      .topbar { grid-template-columns: 1fr; }
    }
    @media (max-width: 720px) {
      .grid { grid-template-columns: 1fr; }
      .hero { flex-direction: column; align-items: flex-start; }
      .wrap { padding: 18px 14px 28px; }
      .memory-value { font-size: 24px; }
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <div>
        <h1>llama.cpp Orchestrator</h1>
        <div class="subtitle">
          Save and edit model configurations, launch or stop them on demand, and monitor whether active models are idle or processing.
        </div>
      </div>
      <div class="pill">Windows model control dashboard</div>
    </div>

    <div class="topbar">
      <div class="card memory-card">
        <div class="card-inner">
          <div class="memory-label">System memory</div>
          <div class="memory-value" id="memoryText">Loading...</div>
          <div class="memory-sub" id="memorySub">Live RAM usage on this machine.</div>
          <div class="progress"><div class="bar" id="memoryBar"></div></div>
        </div>
      </div>

      <div class="card">
        <div class="card-inner">
          <div class="memory-label">Status</div>
          <div class="memory-value" style="font-size: 20px;">Ready</div>
          <div class="memory-sub">
            Use the form to save a configuration, then start it from the saved list.
          </div>
        </div>
      </div>
    </div>

    <div class="layout">
      <div class="stack">
        <div class="card">
          <div class="card-inner">
            <div class="section-head">
              <h2>Configuration</h2>
              <div class="section-note">Saved configs stay compatible</div>
            </div>

            <div class="grid">
              <label class="full">Configuration name
                <input id="name" placeholder="e.g. qwen3-32b-8081">
              </label>

              <label class="full">Model path
                <input id="model_path" placeholder="C:\models\model.gguf">
              </label>

              <label>Port
                <input id="port" placeholder="8081">
              </label>

              <label>Host
                <input id="host" value="0.0.0.0">
              </label>

              <label>Context size
                <input id="context_size" placeholder="8192">
              </label>

              <label>GPU layers
                <input id="gpu_layers" placeholder="99">
              </label>

              <label>Threads
                <input id="threads" placeholder="16">
              </label>

              <label>Reasoning budget
                <input id="reasoning_budget" placeholder="Optional">
              </label>

              <label>Temperature
                <input id="temp" placeholder="0.7">
              </label>

              <label>Top-p
                <input id="top_p" placeholder="0.95">
              </label>

              <label>Top-k
                <input id="top_k" placeholder="40">
              </label>

              <label>Min-p
                <input id="min_p" placeholder="0.05">
              </label>

              <label>Repeat penalty
                <input id="repeat_penalty" placeholder="1.1">
              </label>

              <label>Presence penalty
                <input id="presence_penalty" placeholder="0.0">
              </label>

              <label class="full">MMProj path
                <input id="mmproj_path" placeholder="Optional">
              </label>

              <label class="full">llama-server path
                <input id="llama_server_path" value="llama-server.exe">
              </label>
            </div>

            <div class="buttons">
              <button class="primary" onclick="saveConfig()">Save configuration</button>
              <button class="secondary" onclick="clearForm()">New configuration</button>
            </div>

            <div class="status" id="statusBox">Ready.</div>
          </div>
        </div>
      </div>

      <div class="right-stack">
        <div class="card">
          <div class="card-inner">
            <div class="section-head">
              <h2>Saved configurations</h2>
              <div class="section-note">Edit, start, or remove saved items</div>
            </div>
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Port</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody id="configsTable">
                <tr><td colspan="4" class="empty">No configurations saved.</td></tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="card">
          <div class="card-inner">
            <div class="section-head">
              <h2>Running models</h2>
              <div class="section-note">Idle vs processing with optional logs</div>
            </div>
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Port</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody id="runningTable">
                <tr><td colspan="4" class="empty">No models running.</td></tr>
              </tbody>
            </table>
            <div id="logsArea"></div>
          </div>
        </div>
      </div>
    </div>
  </div>

<script>
  const openLogs = {};
  const logScrollState = {};
  const logFollowState = {};

  function el(id) {
    return document.getElementById(id);
  }

  function setStatus(msg) {
    el('statusBox').textContent = msg;
  }

  function escapeHtml(text) {
    return (text || '').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function rememberLogScroll(port) {
    const box = document.getElementById('logbox-' + port);
    if (!box) return;

    const distanceFromBottom = box.scrollHeight - box.scrollTop - box.clientHeight;
    logScrollState[port] = box.scrollTop;
    logFollowState[port] = distanceFromBottom < 40;
  }

  function restoreLogScroll(port) {
    const box = document.getElementById('logbox-' + port);
    if (!box) return;

    if (logFollowState[port]) {
      box.scrollTop = box.scrollHeight;
    } else if (typeof logScrollState[port] === 'number') {
      box.scrollTop = logScrollState[port];
    }
  }

  function getFormData() {
    return {
      name: el('name').value.trim(),
      model_path: el('model_path').value.trim(),
      host: el('host').value.trim(),
      port: el('port').value.trim(),
      context_size: el('context_size').value.trim(),
      gpu_layers: el('gpu_layers').value.trim(),
      threads: el('threads').value.trim(),
      temp: el('temp').value.trim(),
      top_p: el('top_p').value.trim(),
      top_k: el('top_k').value.trim(),
      min_p: el('min_p').value.trim(),
      repeat_penalty: el('repeat_penalty').value.trim(),
      presence_penalty: el('presence_penalty').value.trim(),
      reasoning_budget: el('reasoning_budget').value.trim(),
      mmproj_path: el('mmproj_path').value.trim(),
      llama_server_path: el('llama_server_path').value.trim()
    };
  }

  function fillForm(cfg) {
    el('name').value = cfg.name || '';
    el('model_path').value = cfg.model_path || '';
    el('host').value = cfg.host || '0.0.0.0';
    el('port').value = cfg.port || '';
    el('context_size').value = cfg.context_size || '';
    el('gpu_layers').value = cfg.gpu_layers || '';
    el('threads').value = cfg.threads || '';
    el('temp').value = cfg.temp || '';
    el('top_p').value = cfg.top_p || '';
    el('top_k').value = cfg.top_k || '';
    el('min_p').value = cfg.min_p || '';
    el('repeat_penalty').value = cfg.repeat_penalty || '';
    el('presence_penalty').value = cfg.presence_penalty || '';
    el('reasoning_budget').value = cfg.reasoning_budget || '';
    el('mmproj_path').value = cfg.mmproj_path || '';
    el('llama_server_path').value = cfg.llama_server_path || 'llama-server.exe';
  }

  function clearForm() {
    fillForm({
      name: '',
      model_path: '',
      host: '0.0.0.0',
      port: '',
      context_size: '',
      gpu_layers: '',
      threads: '',
      temp: '',
      top_p: '',
      top_k: '',
      min_p: '',
      repeat_penalty: '',
      presence_penalty: '',
      reasoning_budget: '',
      mmproj_path: '',
      llama_server_path: 'llama-server.exe'
    });
    setStatus('New empty configuration ready.');
  }

  function badge(status) {
    const s = (status || 'unknown').toLowerCase();
    return '<span class="badge ' + s + '">' + status + '</span>';
  }

  async function refreshMemory() {
    try {
      const res = await fetch('/memory');
      const data = await res.json();
      const used = data.used_gb ?? '?';
      const total = data.total_gb ?? '?';
      const available = data.available_gb ?? '?';
      const percent = data.percent ?? 0;

      el('memoryText').textContent = used + ' GB / ' + total + ' GB';
      el('memorySub').textContent = available + ' GB available (' + percent + '% used)';
      const bar = el('memoryBar');
      if (bar) bar.style.width = percent + '%';
    } catch (e) {
      el('memoryText').textContent = 'Could not load';
      el('memorySub').textContent = 'Memory endpoint unavailable';
    }
  }

  async function saveConfig() {
    const payload = getFormData();
    try {
      const res = await fetch('/configs', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (!res.ok) {
        setStatus('Save failed: ' + (data.detail || JSON.stringify(data)));
        return;
      }
      setStatus('Configuration saved: ' + data.name);
      await refreshConfigs();
    } catch (e) {
      setStatus('Save failed: ' + e);
    }
  }

  async function editConfig(name) {
    try {
      const res = await fetch('/configs/' + encodeURIComponent(name));
      const data = await res.json();
      if (!res.ok) {
        setStatus('Edit failed: ' + (data.detail || JSON.stringify(data)));
        return;
      }
      fillForm(data);
      setStatus('Loaded configuration for editing: ' + name);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (e) {
      setStatus('Edit failed: ' + e);
    }
  }

  async function deleteConfig(name) {
    if (!confirm('Delete configuration "' + name + '"?')) return;
    try {
      const res = await fetch('/configs/' + encodeURIComponent(name), { method: 'DELETE' });
      const data = await res.json();
      setStatus('Configuration deleted: ' + data.name);
      await refreshConfigs();
    } catch (e) {
      setStatus('Delete failed: ' + e);
    }
  }

  async function startModel(name) {
    try {
      setStatus('Starting configuration: ' + name + ' ...');
      const res = await fetch('/start/' + encodeURIComponent(name), { method: 'POST' });
      const data = await res.json();
      if (!res.ok) {
        setStatus('Start failed: ' + (data.detail || JSON.stringify(data)));
        return;
      }
      setStatus('Started "' + data.name + '" on port ' + data.port);
      await refreshConfigs();
      await refreshRunning();
    } catch (e) {
      setStatus('Start failed: ' + e);
    }
  }

  async function stopModel(port) {
    try {
      const res = await fetch('/stop/' + port, { method: 'POST' });
      const data = await res.json();
      if (!res.ok) {
        setStatus('Stop failed: ' + (data.detail || JSON.stringify(data)));
        return;
      }
      setStatus('Stopped model on port ' + port);
      await refreshConfigs();
      await refreshRunning();
    } catch (e) {
      setStatus('Stop failed: ' + e);
    }
  }

  async function toggleLogs(port) {
    openLogs[port] = !openLogs[port];
    if (openLogs[port]) {
      logFollowState[port] = true;
    }
    await refreshRunning();
  }

  async function refreshConfigs() {
    try {
      const res = await fetch('/configs');
      const rows = await res.json();
      if (!rows.length) {
        el('configsTable').innerHTML = '<tr><td colspan="4" class="empty">No configurations saved.</td></tr>';
        return;
      }
      let html = '';
      for (const r of rows) {
        html += `
          <tr>
            <td class="name-cell">
              <strong>${r.name}</strong>
              <div class="tiny">${r.model_path}</div>
            </td>
            <td>${r.port}</td>
            <td>${badge(r.status)}</td>
            <td>
              <div class="table-actions">
                <button class="secondary" data-name="${encodeURIComponent(r.name)}" onclick="editConfig(decodeURIComponent(this.dataset.name))">Edit</button>
                <button class="primary" data-name="${encodeURIComponent(r.name)}" onclick="startModel(decodeURIComponent(this.dataset.name))">Start</button>
                <button class="danger" data-name="${encodeURIComponent(r.name)}" onclick="deleteConfig(decodeURIComponent(this.dataset.name))">Delete</button>
              </div>
            </td>
          </tr>
        `;
      }
      el('configsTable').innerHTML = html;
    } catch (e) {
      el('configsTable').innerHTML = '<tr><td colspan="4" class="empty">Could not load configurations.</td></tr>';
      setStatus('Could not load configurations: ' + e);
    }
  }

  async function refreshRunning() {
    try {
      for (const port in openLogs) {
        rememberLogScroll(port);
      }

      const res = await fetch('/running');
      const rows = await res.json();

      if (!rows.length) {
        el('runningTable').innerHTML = '<tr><td colspan="4" class="empty">No models running.</td></tr>';
        el('logsArea').innerHTML = '';
        return;
      }

      let html = '';
      for (const r of rows) {
        html += `
          <tr>
            <td class="name-cell">
              <strong>${r.name}</strong>
              <div class="tiny">${r.model_path}</div>
            </td>
            <td>${r.port}</td>
            <td>${badge(r.status)}</td>
            <td>
              <div class="table-actions">
                <button class="secondary" onclick="toggleLogs(${r.port})">${openLogs[r.port] ? 'Hide logs' : 'Show logs'}</button>
                <button class="danger" onclick="stopModel(${r.port})">Stop</button>
              </div>
            </td>
          </tr>
        `;
      }
      el('runningTable').innerHTML = html;

      let logsHtml = '';
      for (const r of rows) {
        if (openLogs[r.port]) {
          try {
            const logRes = await fetch('/logs/' + r.port);
            const logData = await logRes.json();
            const safeLog = escapeHtml(logData.log || '');

            logsHtml += `
              <div class="logbox" id="logbox-${r.port}" style="display:block;" onscroll="rememberLogScroll(${r.port})">
                <span class="log-title">${r.name} — port ${r.port}</span>
${safeLog}
              </div>
            `;
          } catch (e) {
            logsHtml += `
              <div class="logbox" id="logbox-${r.port}" style="display:block;">
                Could not load logs for port ${r.port}
              </div>
            `;
          }
        }
      }

      el('logsArea').innerHTML = logsHtml;

      for (const r of rows) {
        if (openLogs[r.port]) {
          restoreLogScroll(r.port);
        }
      }
    } catch (e) {
      el('runningTable').innerHTML = '<tr><td colspan="4" class="empty">Could not load running models.</td></tr>';
      setStatus('Could not load running models: ' + e);
    }
  }

  async function boot() {
    clearForm();
    await refreshMemory();
    await refreshConfigs();
    await refreshRunning();
  }

  boot();
  setInterval(refreshMemory, 5000);
  setInterval(refreshRunning, 4000);
  setInterval(refreshConfigs, 6000);
</script>
</body>
</html>
"""
