const state = {
  agents: [
    { id: "planner", label: "GLM Planner", model: "z-ai/glm-5.1", apiKey: "" },
    { id: "coder", label: "DeepSeek Coder", model: "deepseek-ai/deepseek-v4-pro", apiKey: "" },
    { id: "debugger", label: "MiniMax Debugger", model: "minimaxai/minimax-m2.7", apiKey: "" },
  ],
};

function $(id) {
  return document.getElementById(id);
}

function renderAgents() {
  const root = $("agents");
  root.innerHTML = "";
  state.agents.forEach((agent, idx) => {
    const div = document.createElement("div");
    div.className = "agent-row";
    div.innerHTML = `
      <strong>${agent.label}</strong>
      <label>Model <input data-idx="${idx}" data-field="model" value="${agent.model}" /></label>
      <label>API Key (opzionale) <input type="password" data-idx="${idx}" data-field="apiKey" placeholder="Inserisci qui la tua key" /></label>
      <span class="status">Sicurezza: nessuna key hardcoded nel progetto.</span>
    `;
    root.appendChild(div);
  });

  root.querySelectorAll("input").forEach((el) => {
    el.addEventListener("change", (e) => {
      const target = e.target;
      const idx = Number(target.dataset.idx);
      const field = target.dataset.field;
      state.agents[idx][field] = target.value;
    });
  });
}

async function runWorkflow() {
  const body = {
    goal: $("goal").value,
    project_dir: $("projectDir").value,
    max_iterations: Number($("maxIterations").value),
  };
  const res = await fetch("/api/run", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  $("workflowOut").textContent = JSON.stringify(data, null, 2);
}

async function sendChat() {
  const prompt = $("prompt").value.trim();
  if (!prompt) {
    return;
  }
  const model = $("agentSelect").value;
  const linkedAgent = state.agents.find((a) => a.model === model);
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      prompt,
      model,
      api_key: linkedAgent?.apiKey || "",
    }),
  });
  const data = await res.json();
  $("chatOut").textContent = data.content;
}

function clearAll() {
  $("prompt").value = "";
  $("chatOut").textContent = "";
  $("workflowOut").textContent = "";
}

window.addEventListener("DOMContentLoaded", () => {
  renderAgents();
  $("runFlow").addEventListener("click", runWorkflow);
  $("sendChat").addEventListener("click", sendChat);
  $("clear").addEventListener("click", clearAll);
});
