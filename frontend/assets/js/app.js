/* ══════════════════════════════════════════
   1. VIEW ROUTING (SIDEBAR)
══════════════════════════════════════════ */
function initViews() {
  const navItems = document.querySelectorAll('.nav-item');
  const views = document.querySelectorAll('.view');

  navItems.forEach(btn => {
    btn.addEventListener('click', () => {
      // Update nav state
      navItems.forEach(n => n.classList.remove('active'));
      btn.classList.add('active');

      // Update view state
      const targetView = btn.dataset.view;
      views.forEach(v => {
        v.classList.remove('active');
        if (v.id === targetView) v.classList.add('active');
      });
      
      // Re-trigger chart if needed
      if (targetView === 'view-models') {
        renderComparisonChart();
      }
    });
  });
}
initViews();

/* ══════════════════════════════════════════
   2. WEBSOCKET (LIVE FEED)
══════════════════════════════════════════ */
let totalEvents = 0;
let totalConfidence = 0;

function initWebSocket() {
  const ws = new WebSocket('ws://localhost:8000/api/stream');
  const feedList = document.getElementById('live-feed-list');
  const kpiEvents = document.getElementById('events-count');
  const kpiAvgConf = document.getElementById('avg-confidence');

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data.type === 'live_alert') {
      // Remove placeholder if present
      const placeholder = feedList.querySelector('.feed-placeholder');
      if (placeholder) placeholder.remove();

      // Create new feed item
      const item = document.createElement('div');
      item.className = 'feed-item';
      
      const topConfidence = data.confidence[0].pct;
      const confColor = topConfidence > 80 ? 'var(--red)' : (topConfidence > 50 ? 'var(--yellow)' : 'var(--cyan)');
      item.style.borderLeftColor = confColor;

      item.innerHTML = `
        <div>
          <div class="feed-item-header">
            <span>${data.timestamp}</span>
            <span>${data.source}</span>
          </div>
          <div class="feed-actor">Target: ${data.actor}</div>
          <div style="font-family:var(--font-mono);font-size:.65rem;color:var(--dim);margin-top:4px;">
            Matched: ${data.iocs[0].val}
          </div>
        </div>
        <div style="text-align:right;">
          <div class="feed-confidence" style="color:${confColor}">${topConfidence}% CONF</div>
          <div style="font-family:var(--font-mono);font-size:.55rem;color:var(--dim);margin-top:2px;">ML INFERENCE</div>
        </div>
      `;

      // Prepend to list
      feedList.insertBefore(item, feedList.firstChild);
      
      // Keep only last 10 items
      if (feedList.children.length > 10) {
        feedList.removeChild(feedList.lastChild);
      }

      // Update KPIs
      totalEvents++;
      totalConfidence += topConfidence;
      kpiEvents.textContent = totalEvents;
      kpiAvgConf.textContent = Math.round(totalConfidence / totalEvents) + '%';
    }
  };

  ws.onclose = () => {
    console.log("WebSocket disconnected. Reconnecting in 5s...");
    setTimeout(initWebSocket, 5000);
  };
}
initWebSocket();

/* ══════════════════════════════════════════
   3. PIPELINE DATA
══════════════════════════════════════════ */
const pipelineData = [
  { title: 'DATA INPUT MODULE', body: 'Collects cyber-attack data from public threat intelligence repositories.', tags: ['IoC Datasets', 'TTP Reports'] },
  { title: 'PREPROCESSING MODULE', body: 'Cleans and transforms raw data into usable formats.', tags: ['Deduplication', 'Normalization'] },
  { title: 'FEATURE EXTRACTION', body: 'Extracts network-based features, malware features, and behavioral features.', tags: ['Network', 'Malware', 'Behavioral'] },
  { title: 'AI MODEL LAYER', body: 'Applies ML and DL models. Each model outputs probabilistic classification scores.', tags: ['SVM', 'Random Forest', 'LSTM'] },
  { title: 'ATTRIBUTION ENGINE', body: 'Synthesizes model outputs to predict the most likely threat actor.', tags: ['Confidence Scoring', 'Ensemble'] },
  { title: 'EVALUATION MODULE', body: 'Assesses performance using Accuracy, Precision, Recall, F1-Score.', tags: ['Accuracy', 'F1-Score'] }
];

function selectStep(idx) {
  document.querySelectorAll('.pipe-step').forEach((s, i) => s.classList.toggle('active', i === idx));
  const d = pipelineData[idx];
  document.getElementById('pipeline-detail').innerHTML = `
    <div class="detail-title">${d.title}</div>
    <div class="detail-body">${d.body}</div>
    <div class="detail-tags">${d.tags.map(t => `<span class="dtag">${t}</span>`).join('')}</div>
  `;
}
selectStep(0);

/* ══════════════════════════════════════════
   4. MODELS DATA
══════════════════════════════════════════ */
const models = [
  { id: 'rf', label: 'Random Forest', type: 'Machine Learning', name: 'Random Forest (Active MVP)', desc: 'Currently running in the live backend processing AlienVault simulated feeds.', perf: { Accuracy: 92, Precision: 91, Recall: 90, F1: 90 }, fillColor: '#39ff8f', uses: ['Live Feed', 'Robustness'] },
  { id: 'svm', label: 'SVM', type: 'Machine Learning', name: 'Support Vector Machine', desc: 'Creates optimal hyperplanes.', perf: { Accuracy: 88, Precision: 86, Recall: 84, F1: 85 }, fillColor: '#00d4ff', uses: ['High-dim data'] },
  { id: 'lstm', label: 'LSTM', type: 'Deep Learning', name: 'Long Short-Term Memory', desc: 'Advanced RNN variant capturing long-range temporal dependencies.', perf: { Accuracy: 95, Precision: 94, Recall: 93, F1: 94 }, fillColor: '#ff3e6c', uses: ['Long-term dependencies'] }
];

let activeModel = 'rf';
function renderModelTabs() {
  document.getElementById('model-tabs').innerHTML = models.map(m => `
    <div class="model-tab ${m.id === activeModel ? 'active' : ''}" onclick="selectModel('${m.id}')">
      <div class="tab-dot"></div>
      <div><div class="tab-label">${m.label}</div><div class="tab-type">${m.type.toUpperCase()}</div></div>
    </div>
  `).join('');
}

function renderModelDetail() {
  const m = models.find(x => x.id === activeModel);
  const badgeClass = m.type === 'Machine Learning' ? 'badge-ml' : 'badge-dl';
  document.getElementById('model-detail').innerHTML = `
    <div class="model-detail-head"><div><div class="model-name">${m.name}</div><span class="model-type-badge ${badgeClass}">${m.type.toUpperCase()}</span></div></div>
    <div class="model-desc">${m.desc}</div>
    <div class="perf-bars">
      ${Object.entries(m.perf).map(([k,v]) => `
        <div class="perf-row"><span class="perf-label">${k}</span><div class="perf-track"><div class="perf-fill" data-width="${v}" style="background:${m.fillColor};width:0%"></div></div><span class="perf-val">${v}%</span></div>
      `).join('')}
    </div>
    <div class="use-cases">${m.uses.map(u => `<span class="use-tag">${u}</span>`).join('')}</div>
  `;
  setTimeout(() => { document.querySelectorAll('.perf-fill[data-width]').forEach(bar => bar.style.width = bar.dataset.width + '%'); }, 80);
}

function selectModel(id) { activeModel = id; renderModelTabs(); renderModelDetail(); }
renderModelTabs(); renderModelDetail();

/* ══════════════════════════════════════════
   5. CHART.JS
══════════════════════════════════════════ */
let chartInstance = null;
function renderComparisonChart() {
  const canvas = document.getElementById('comparison-chart');
  if (!canvas) return;
  if (chartInstance) chartInstance.destroy();
  
  const ctx = canvas.getContext('2d');
  const labels = models.map(m => m.label);
  const datasets = ['Accuracy', 'Precision', 'Recall', 'F1'].map((metric, i) => {
    const colors = ['#00d4ff', '#ff3e6c', '#39ff8f', '#f5c518'];
    return {
      label: metric,
      data: models.map(m => m.perf[metric] || m.perf.F1),
      backgroundColor: colors[i] + '33', borderColor: colors[i], borderWidth: 2
    };
  });
  chartInstance = new Chart(ctx, {
    type: 'bar', data: { labels, datasets },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { labels: { color: '#c8dff0', font: { family: "'Space Mono', monospace", size: 10 } } } },
      scales: {
        x: { ticks: { color: '#496070' }, grid: { color: '#112234' } },
        y: { min: 50, max: 100, ticks: { color: '#496070' }, grid: { color: '#112234' } }
      }
    }
  });
}

/* ══════════════════════════════════════════
   6. SIMULATOR
══════════════════════════════════════════ */
const scenarios = [
  { id: 'apt28', name: 'Operation Phantom Bear', meta: 'Spear phishing → lateral movement' },
  { id: 'lazarus', name: 'Operation DarkSeoul', meta: 'Supply chain compromise → ransomware' },
  { id: 'apt41', name: 'Operation DoubleDragon', meta: 'Zero-day exploit → espionage' }
];

let selectedScenario = null; let running = false; let lastResult = null;

function renderScenarios() {
  document.getElementById('scenario-btns').innerHTML = scenarios.map(s => `
    <div class="scenario-btn ${selectedScenario === s.id ? 'selected' : ''}" onclick="selectScenario('${s.id}')">
      <div class="scenario-name">${s.name}</div><div class="scenario-meta">${s.meta}</div>
    </div>
  `).join('');
}

function selectScenario(id) {
  selectedScenario = id; running = false; lastResult = null;
  renderScenarios();
  document.getElementById('run-btn').disabled = false;
  document.getElementById('sim-status').textContent = 'READY — Click Run Attribution';
  document.getElementById('sim-status').className = 'sim-status';
  document.getElementById('sim-output').innerHTML = `<div class="result-placeholder"><div class="result-icon">⚡</div><div class="result-hint">SCENARIO LOADED — RUN TO ANALYSE</div></div>`;
}
renderScenarios();

function runAttribution() {
  if (!selectedScenario || running) return;
  running = true;
  document.getElementById('run-btn').disabled = true;
  
  const status = document.getElementById('sim-status');
  const output = document.getElementById('sim-output');
  status.textContent = 'Running ML inference via API...';
  status.className = 'sim-status running';
  output.innerHTML = `<div class="result-placeholder"><div class="result-icon">🤖</div><div class="result-hint">AWAITING BACKEND RESPONSE</div></div>`;

  fetch('http://localhost:8000/api/simulate', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ scenario_id: selectedScenario })
  })
  .then(res => res.json())
  .then(data => {
    lastResult = data;
    status.textContent = 'COMPLETE — Attribution verdict ready';
    status.className = 'sim-status';
    
    output.innerHTML = `
      <div class="actor-result">
        <div style="font-family:var(--font-mono);font-size:.58rem;color:var(--green);letter-spacing:3px;margin-bottom:.5rem;">ATTRIBUTED TO</div>
        <div class="actor-name">${data.actor}</div>
        <div class="actor-alias">${data.alias}</div>
        <div style="margin-bottom:.8rem;">
          ${data.confidence.map((c,i) => `
            <div class="confidence-row">
              <span class="conf-label">${c.label}</span>
              <div class="conf-bar"><div class="conf-fill" id="cbar-${i}" style="background:${c.color};width:0%"></div></div>
              <span class="conf-pct">${c.pct}%</span>
            </div>
          `).join('')}
        </div>
        <div class="ioc-list">
          <div style="font-family:var(--font-mono);font-size:.58rem;color:var(--dim);letter-spacing:2px;margin-bottom:.5rem;">INDICATORS OF COMPROMISE</div>
          ${data.iocs.map(ioc => `<div class="ioc-item"><span class="ioc-key">${ioc.key}</span><span>${ioc.val}</span></div>`).join('')}
        </div>
      </div>
    `;
    setTimeout(() => {
      data.confidence.forEach((c, i) => { const b = document.getElementById(`cbar-${i}`); if(b) b.style.width = c.pct+'%'; });
      document.getElementById('run-btn').disabled = false;
      running = false;
    }, 100);
  })
  .catch(err => {
    status.textContent = 'ERROR — Backend API failed';
    status.className = 'sim-status text-red';
    output.innerHTML = `<div class="result-placeholder"><div class="result-icon">⚠️</div><div class="result-hint">BACKEND CONNECTION FAILED</div></div>`;
    document.getElementById('run-btn').disabled = false;
    running = false;
  });
}

function exportReport() {
  if (!lastResult) return alert('Run an attribution first.');
  const blob = new Blob([JSON.stringify(lastResult, null, 2)], { type: 'application/json' });
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob);
  a.download = `CyberAttrib_Report_${Date.now()}.json`; a.click();
}
