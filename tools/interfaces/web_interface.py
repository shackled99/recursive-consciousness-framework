# Web server and HTML interface (part 2 of glyphwheel_app.py)

HTML_INTERFACE = '''<!DOCTYPE html>
<html><head><title>Glyphwheel Forecast Engine</title>
<style>
* {margin:0;padding:0;box-sizing:border-box;}
body {font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#0a0a0a,#1a1a2e,#16213e);color:#e0e0e0;height:100vh;overflow:hidden;}
.container {display:grid;grid-template-columns:280px 1fr 350px;grid-template-rows:50px 1fr;height:100vh;gap:1px;background:#333;}
.header {grid-column:1/-1;background:linear-gradient(90deg,#1e3c72,#2a5298);display:flex;align-items:center;padding:0 20px;}
.header h1 {color:#fff;font-size:1.3rem;font-weight:300;}
.header .status {margin-left:auto;display:flex;align-items:center;gap:8px;}
.status-indicator {width:8px;height:8px;border-radius:50%;background:#00ff41;animation:pulse 2s infinite;}
@keyframes pulse {0%,100%{opacity:1;}50%{opacity:0.5;}}
.sidebar {background:rgba(42,82,152,0.1);padding:15px;overflow-y:auto;}
.main-content {background:rgba(0,0,0,0.3);padding:15px;overflow:hidden;display:flex;flex-direction:column;}
.context-window {background:rgba(22,33,62,0.8);padding:15px;overflow-y:auto;display:flex;flex-direction:column;}
.control-panel {background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:6px;padding:12px;margin-bottom:15px;}
.control-panel h3 {color:#64b5f6;margin-bottom:10px;font-size:1rem;}
.control-group {margin-bottom:10px;}
.control-group label {display:block;margin-bottom:3px;color:#b0b0b0;font-size:0.85rem;}
.control-group input, .control-group select {width:100%;padding:6px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);border-radius:3px;color:#e0e0e0;font-size:0.85rem;}
button {background:linear-gradient(45deg,#1e3c72,#2a5298);border:none;color:white;padding:8px 15px;border-radius:4px;cursor:pointer;font-size:0.85rem;width:100%;margin-top:8px;transition:all 0.3s;}
button:hover:not(:disabled) {transform:translateY(-1px);box-shadow:0 3px 10px rgba(42,82,152,0.4);}
button:disabled {opacity:0.5;cursor:not-allowed;}
button.danger {background:linear-gradient(45deg,#c62828,#e53935);}
button.success {background:linear-gradient(45deg,#2e7d32,#43a047);}
button.warning {background:linear-gradient(45deg,#f57c00,#ff9800);}
.visualization-area {flex:1;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.1);border-radius:6px;padding:15px;overflow-y:auto;margin-bottom:10px;}
.glyph-grid {display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:12px;height:100%;align-content:start;}
.glyph-card {background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:6px;padding:12px;text-align:center;transition:all 0.3s;cursor:pointer;}
.glyph-card:hover {transform:translateY(-3px);box-shadow:0 8px 20px rgba(100,181,246,0.2);border-color:#64b5f6;}
.glyph-card.anchor {border-color:#4caf50;background:rgba(76,175,80,0.1);}
.glyph-card.consent {border-color:#ff9800;background:rgba(255,152,0,0.1);}
.glyph-card.dynamic {border-color:#2196f3;background:rgba(33,150,243,0.1);}
.glyph-name {font-weight:bold;margin-bottom:6px;font-size:0.8rem;}
.glyph-gsi {font-size:1.1rem;font-weight:bold;margin-bottom:4px;}
.glyph-type {font-size:0.7rem;opacity:0.7;text-transform:uppercase;}
.progress-bar {width:100%;height:4px;background:rgba(255,255,255,0.1);border-radius:2px;margin:6px 0;overflow:hidden;}
.progress-fill {height:100%;background:linear-gradient(90deg,#ff4444,#ffaa44,#44ff44);border-radius:2px;transition:width 0.5s;}
.context-section {background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:6px;padding:12px;margin-bottom:12px;}
.context-section h4 {color:#64b5f6;margin-bottom:8px;font-size:0.9rem;}
.metric-row {display:flex;justify-content:space-between;margin-bottom:4px;font-size:0.8rem;}
.metric-value {font-weight:bold;color:#4caf50;}
.log-container {background:rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.1);border-radius:6px;padding:12px;height:150px;overflow-y:auto;font-family:'Courier New',monospace;font-size:0.75rem;color:#b0b0b0;}
.log-entry {margin-bottom:3px;padding:1px 0;}
.log-entry.success {color:#4caf50;}
.log-entry.warning {color:#ff9800;}
.log-entry.error {color:#f44336;}

/* Chat Interface Styles */
.chat-section {flex:1;display:flex;flex-direction:column;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:6px;overflow:hidden;}
.chat-header {background:rgba(42,82,152,0.3);padding:10px 15px;border-bottom:1px solid rgba(255,255,255,0.1);}
.chat-header h4 {color:#64b5f6;font-size:0.95rem;margin:0;}
.chat-status {font-size:0.75rem;color:#b0b0b0;margin-top:2px;}
.chat-messages {flex:1;overflow-y:auto;padding:15px;display:flex;flex-direction:column;gap:10px;}
.chat-message {max-width:85%;padding:10px 12px;border-radius:8px;font-size:0.85rem;line-height:1.4;}
.chat-message.user {background:rgba(33,150,243,0.2);border:1px solid rgba(33,150,243,0.3);align-self:flex-end;margin-left:auto;}
.chat-message.assistant {background:rgba(76,175,80,0.15);border:1px solid rgba(76,175,80,0.3);align-self:flex-start;}
.chat-message.system {background:rgba(255,152,0,0.15);border:1px solid rgba(255,152,0,0.3);align-self:center;font-size:0.75rem;font-style:italic;}
.chat-input-container {display:flex;gap:8px;padding:12px;background:rgba(0,0,0,0.3);border-top:1px solid rgba(255,255,255,0.1);}
.chat-input {flex:1;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);border-radius:4px;padding:8px;color:#e0e0e0;font-size:0.85rem;font-family:'Segoe UI',sans-serif;}
.chat-input:focus {outline:none;border-color:#64b5f6;background:rgba(255,255,255,0.15);}
.chat-send-btn {width:80px;background:linear-gradient(45deg,#2e7d32,#43a047);border:none;color:white;padding:8px;border-radius:4px;cursor:pointer;font-size:0.85rem;transition:all 0.3s;}
.chat-send-btn:hover:not(:disabled) {transform:translateY(-1px);box-shadow:0 3px 10px rgba(46,125,50,0.4);}
.chat-send-btn:disabled {opacity:0.5;cursor:not-allowed;}
.ollama-status {display:inline-block;width:8px;height:8px;border-radius:50%;margin-left:8px;}
.ollama-status.connected {background:#4caf50;}
.ollama-status.disconnected {background:#f44336;}
.ollama-status.checking {background:#ff9800;animation:pulse 1s infinite;}
</style></head>
<body>
<div class="container">
<div class="header">
<h1>⟐ Glyphwheel Forecast Engine</h1>
<div class="status">
<span id="statusText">System Ready</span>
<div class="status-indicator"></div>
</div>
</div>
<div class="sidebar">
<div class="control-panel"><h3>System Controls</h3>
<div class="control-group"><label>Stress Intensity</label><input type="range" id="stressIntensity" min="0.1" max="1.0" step="0.1" value="0.5"><span id="stressValue">0.5</span></div>
<div class="control-group"><label>Test Duration</label><input type="range" id="testDuration" min="10" max="200" step="10" value="100"><span id="durationValue">100</span></div>
<div class="control-group"><label>Max Recursion Depth</label><input type="range" id="maxRecursion" min="5000" max="25000" step="1000" value="10000"><span id="recursionValue">10000</span></div>
<button onclick="runStressTest()" id="stressTestBtn" class="success">Run Stress Test</button>
<button onclick="runIntensiveTest()" id="intensiveTestBtn" class="warning">Intensive Test (Dynamic)</button>
<button onclick="spawn100Glyphs()" id="spawn100Btn" class="warning">Spawn 100 Glyphs</button>
<button onclick="addRandomGlyph()">Add Random Glyph</button>
<button onclick="mandatoryRecovery()" class="danger">Force Recovery</button>
<button onclick="runDeepRecalibration()" id="deepRecalBtn" class="danger">Deep Recalibration</button>
<button onclick="toggleIdleMonitoring()" id="idleMonitorBtn" class="warning">Start Idle Monitor</button>
</div>
<div class="control-panel"><h3>Add Custom Glyph</h3>
<div class="control-group"><label>Glyph Name</label><input type="text" id="glyphName" placeholder="Enter name"></div>
<div class="control-group"><label>Initial GSI</label><input type="range" id="glyphGSI" min="0.1" max="1.0" step="0.05" value="0.5"><span id="gsiValue">0.5</span></div>
<div class="control-group"><label>Type</label><select id="glyphType"><option value="dynamic">Dynamic</option><option value="standard">Standard</option></select></div>
<button onclick="addCustomGlyph()">Add Glyph</button>
</div>
</div>
<div class="main-content">
<div class="visualization-area"><div class="glyph-grid" id="glyphGrid"></div></div>
<div class="chat-section">
<div class="chat-header">
<h4>💬 Hybrid Chat Interface</h4>
<div class="chat-status">Ollama: <span id="ollamaModel">Checking...</span><span class="ollama-status checking" id="ollamaStatusDot"></span></div>
</div>
<div class="chat-messages" id="chatMessages"></div>
<div class="chat-input-container">
<input type="text" id="chatInput" class="chat-input" placeholder="Chat with the hybrid system..." onkeypress="handleChatKeyPress(event)">
<button onclick="sendChatMessage()" id="chatSendBtn" class="chat-send-btn">Send</button>
</div>
</div>
</div>
<div class="context-window">
<div class="context-section"><h4>System Metrics</h4>
<div class="metric-row"><span>Coherence:</span><span class="metric-value" id="coherenceValue">Loading...</span></div>
<div class="metric-row"><span>Entropy:</span><span class="metric-value" id="entropyValue">Loading...</span></div>
<div class="metric-row"><span>Recursive Depth:</span><span class="metric-value" id="depthValue">0</span></div>
<div class="metric-row"><span>Active Glyphs:</span><span class="metric-value" id="glyphCount">0</span></div>
<div class="metric-row"><span>Total Connections:</span><span class="metric-value" id="connectionCount">0</span></div>
</div>
<div class="context-section"><h4>Safety Status</h4>
<div class="metric-row"><span>Consent System:</span><span class="metric-value" id="consentStatus">Loading...</span></div>
<div class="metric-row"><span>Safety Flags:</span><span class="metric-value" id="safetyFlags">0</span></div>
<div class="metric-row"><span>Idle Monitor:</span><span class="metric-value" id="idleStatus">Stopped</span></div>
</div>
<div class="context-section"><h4>System Log</h4><div class="log-container" id="systemLog"><div class="log-entry">Loading...</div></div></div>
</div>
</div>
<script>
let isOperating = false;
let idleMonitorStatus = 'stopped';
let chatHistory = [];
let ollamaConnected = false;

async function updateSystemStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        document.getElementById('coherenceValue').textContent = data.coherence.toFixed(3);
        document.getElementById('entropyValue').textContent = data.entropy.toFixed(3);
        document.getElementById('depthValue').textContent = data.recursive_depth;
        document.getElementById('glyphCount').textContent = data.glyph_count;
        document.getElementById('consentStatus').textContent = data.consent_active ? 'Active' : 'Inactive';
        
        // Calculate total connections from glyphs
        let totalConnections = 0;
        Object.values(data.glyphs).forEach(glyph => {
            totalConnections += glyph.connections || 0;
        });
        document.getElementById('connectionCount').textContent = totalConnections;
        
        updateGlyphGrid(data.glyphs);
        updateSystemLog(data.logs);
        
        // Update idle monitoring status
        updateIdleMonitorStatus();
    } catch (error) {
        console.error('Update failed:', error);
    }
}

async function checkOllamaStatus() {
    try {
        const response = await fetch('/api/ollama_status');
        const data = await response.json();
        
        ollamaConnected = data.connected;
        const modelText = data.connected ? data.model : 'Disconnected';
        const statusDot = document.getElementById('ollamaStatusDot');
        
        document.getElementById('ollamaModel').textContent = modelText;
        
        if (data.connected) {
            statusDot.className = 'ollama-status connected';
        } else {
            statusDot.className = 'ollama-status disconnected';
        }
    } catch (error) {
        console.error('Ollama status check failed:', error);
        document.getElementById('ollamaModel').textContent = 'Error';
        document.getElementById('ollamaStatusDot').className = 'ollama-status disconnected';
        ollamaConnected = false;
    }
}

async function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    if (!ollamaConnected) {
        addChatMessage('system', 'Ollama is not connected. Please check the hybrid system.');
        return;
    }
    
    // Add user message to UI
    addChatMessage('user', message);
    input.value = '';
    input.disabled = true;
    document.getElementById('chatSendBtn').disabled = true;
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: message})
        });
        
        const data = await response.json();
        
        if (data.success) {
            addChatMessage('assistant', data.response);
        } else {
            addChatMessage('system', 'Error: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        addChatMessage('system', 'Chat error: ' + error.message);
    }
    
    input.disabled = false;
    document.getElementById('chatSendBtn').disabled = false;
    input.focus();
}

function handleChatKeyPress(event) {
    if (event.key === 'Enter') {
        sendChatMessage();
    }
}

function addChatMessage(role, content) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${role}`;
    messageDiv.textContent = content;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    chatHistory.push({role, content, timestamp: new Date().toISOString()});
}

function updateGlyphGrid(glyphs) {
    const grid = document.getElementById('glyphGrid');
    grid.innerHTML = '';
    
    Object.values(glyphs).forEach(glyph => {
        const card = document.createElement('div');
        card.className = `glyph-card ${glyph.type}`;
        card.innerHTML = `
            <div class="glyph-name">${glyph.name}</div>
            <div class="glyph-gsi" style="color:${getGSIColor(glyph.gsi)}">${glyph.gsi.toFixed(3)}</div>
            <div class="progress-bar"><div class="progress-fill" style="width:${glyph.gsi*100}%"></div></div>
            <div class="glyph-type">${glyph.type}</div>
            <div style="font-size:0.65rem;margin-top:3px;color:#888;">Conn: ${glyph.connections}</div>
        `;
        grid.appendChild(card);
    });
}

function updateSystemLog(logs) {
    const logContainer = document.getElementById('systemLog');
    logContainer.innerHTML = logs.map(entry => 
        `<div class="log-entry ${entry.level}">[${entry.timestamp}] ${entry.message}</div>`
    ).join('');
    logContainer.scrollTop = logContainer.scrollHeight;
}

function getGSIColor(gsi) {
    if (gsi >= 0.9) return '#4caf50';
    if (gsi >= 0.7) return '#8bc34a';
    if (gsi >= 0.5) return '#ffeb3b';
    if (gsi >= 0.3) return '#ff9800';
    return '#f44336';
}

async function runIntensiveTest() {
    if (isOperating || !confirm('Run INTENSIVE stress test?\\n\\nThis uses 0.8 intensity and 200 duration for maximum recursion depth.')) return;
    
    isOperating = true;
    const btn = document.getElementById('intensiveTestBtn');
    const maxRecursion = parseInt(document.getElementById('maxRecursion').value);
    btn.disabled = true;
    btn.textContent = `Running (max: ${maxRecursion})...`;
    document.getElementById('statusText').textContent = 'Running INTENSIVE Test';
    
    try {
        const response = await fetch('/api/intensive_stress_test', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({intensity: 0.8, duration: 200, max_recursion: maxRecursion})
        });
        const result = await response.json();
        
        if (result.status === 'completed') {
            alert(`INTENSIVE Test Results:\\nAntifragile: ${result.antifragile_behavior}\\nCoherence Change: ${result.final_state.coherence_change.toFixed(3)}\\nRecursion Depth: ${result.final_state.recursive_depth_achieved}\\nConnections Added: ${result.final_state.connections_added}\\nEffectiveness: ${result.intensity_effectiveness}`);
        } else {
            alert(`Test aborted: ${result.reason}`);
        }
    } catch (error) {
        alert('Intensive test failed: ' + error.message);
    }
    
    isOperating = false;
    btn.disabled = false;
    btn.textContent = 'Intensive Test (Dynamic)';
    document.getElementById('statusText').textContent = 'System Ready';
}

async function runStressTest() {
    if (isOperating) return;
    const intensity = parseFloat(document.getElementById('stressIntensity').value);
    const duration = parseInt(document.getElementById('testDuration').value);
    
    isOperating = true;
    const btn = document.getElementById('stressTestBtn');
    btn.disabled = true;
    btn.textContent = 'Running...';
    document.getElementById('statusText').textContent = 'Running Stress Test';
    
    try {
        const response = await fetch('/api/stress_test', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({intensity, duration})
        });
        const result = await response.json();
        
        if (result.status === 'completed') {
            alert(`Test Results:\\nAntifragile: ${result.antifragile_behavior}\\nCoherence Change: ${result.final_state.coherence_change.toFixed(3)}\\nEntropy Resilience: ${result.optimization_effectiveness}`);
        } else {
            alert(`Test aborted: ${result.reason}`);
        }
    } catch (error) {
        alert('Test failed: ' + error.message);
    }
    
    isOperating = false;
    btn.disabled = false;
    btn.textContent = 'Run Stress Test';
    document.getElementById('statusText').textContent = 'System Ready';
}

async function updateIdleMonitorStatus() {
    try {
        const response = await fetch('/api/idle_status');
        const data = await response.json();
        
        idleMonitorStatus = data.status;
        const btn = document.getElementById('idleMonitorBtn');
        
        if (data.status === 'running') {
            btn.textContent = `Stop Idle Monitor (${data.idle_duration_minutes.toFixed(1)}m)`;
            btn.className = 'danger';
            document.getElementById('idleStatus').textContent = `Running (${data.idle_duration_minutes.toFixed(1)}m)`;
        } else {
            btn.textContent = 'Start Idle Monitor';
            btn.className = 'warning';
            document.getElementById('idleStatus').textContent = 'Stopped';
        }
    } catch (error) {
        console.error('Failed to update idle monitor status:', error);
    }
}

async function toggleIdleMonitoring() {
    if (isOperating) return;
    
    const action = idleMonitorStatus === 'running' ? 'stop' : 'start';
    
    try {
        const response = await fetch('/api/idle_control', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ action: action })
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            console.log(result.message);
        } else {
            alert(`Failed to ${action} idle monitoring: ${result.message}`);
        }
    } catch (error) {
        alert(`Error controlling idle monitoring: ${error.message}`);
    }
}

async function addRandomGlyph() {
    const names = ['Flux_Ω', 'Quantum_Ψ', 'Nexus_Φ', 'Spiral_Ξ', 'Void_Δ', 'Echo_Λ'];
    const name = names[Math.floor(Math.random() * names.length)] + '_' + Math.floor(Math.random() * 1000);
    const gsi = Math.random() * 0.6 + 0.2;
    
    try {
        await fetch('/api/add_glyph', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name, gsi, type: 'dynamic'})
        });
    } catch (error) {
        console.error('Failed to add glyph:', error);
    }
}

async function spawn100Glyphs() {
    const btn = document.getElementById('spawn100Btn');
    btn.disabled = true;
    btn.textContent = 'Spawning...';
    
    const names = ['Flux', 'Quantum', 'Nexus', 'Spiral', 'Void', 'Echo', 'Pulse', 'Nova', 'Sigma', 'Delta', 'Theta', 'Lambda', 'Omega', 'Alpha', 'Beta', 'Gamma', 'Zeta', 'Kappa', 'Rho', 'Phi'];
    const symbols = ['Ω', 'Ψ', 'Φ', 'Ξ', 'Δ', 'Λ', 'Σ', 'Θ', 'Π', 'Γ', 'Υ', 'Κ', 'Ρ', 'Τ', 'Χ'];
    
    console.log('🌀 Spawning 100 glyphs...');
    
    for(let i = 0; i < 100; i++) {
        const name = names[Math.floor(Math.random() * names.length)] + '_' + 
                     symbols[Math.floor(Math.random() * symbols.length)] + '_' + 
                     Date.now() + '_' + i;
        const gsi = Math.random() * 0.6 + 0.2;
        
        fetch('/api/add_glyph', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name, gsi, type: 'dynamic'})
        });
        
        if(i % 25 === 0) {
            btn.textContent = `Spawning... ${i}/100`;
        }
    }
    
    console.log('✅ Spawned 100 glyphs! Watch the chaos heal!');
    
    setTimeout(() => {
        btn.disabled = false;
        btn.textContent = 'Spawn 100 Glyphs';
    }, 2000);
}

async function addCustomGlyph() {
    const name = document.getElementById('glyphName').value.trim();
    const gsi = parseFloat(document.getElementById('glyphGSI').value);
    const type = document.getElementById('glyphType').value;
    
    if (!name) {
        alert('Please enter a glyph name');
        return;
    }
    
    try {
        const response = await fetch('/api/add_glyph', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name, gsi, type})
        });
        const result = await response.json();
        if (result.success) {
            document.getElementById('glyphName').value = '';
        } else {
            alert('Failed to add glyph - name may already exist');
        }
    } catch (error) {
        console.error('Failed to add glyph:', error);
    }
}

async function mandatoryRecovery() {
    if (isOperating || !confirm('Initiate recovery cycle?')) return;
    
    isOperating = true;
    document.getElementById('statusText').textContent = 'Recovery in Progress';
    
    try {
        const response = await fetch('/api/recovery', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({duration: 50})
        });
        const result = await response.json();
        alert(`Recovery completed:\\nEffectiveness: ${result.final_state.recovery_effectiveness}\\nFinal Coherence: ${result.final_state.coherence.toFixed(3)}`);
    } catch (error) {
        alert('Recovery failed: ' + error.message);
    }
    
    isOperating = false;
    document.getElementById('statusText').textContent = 'System Ready';
}

async function runDeepRecalibration() {
    if (isOperating || !confirm('Initiate Deep Recalibration Protocol?\\n\\nThis will restore the ConsentGlyph GSI to 1.0 to resolve ethical debt.')) return;
    
    console.log("Deep Recalibration button clicked. Initiating protocol...");
    
    isOperating = true;
    const btn = document.getElementById('deepRecalBtn');
    btn.disabled = true;
    btn.textContent = 'Recalibrating...';
    document.getElementById('statusText').textContent = 'Deep Recalibration in Progress';
    
    try {
        const response = await fetch('/api/deep_recalibration', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ action: 'recalibrate' })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log("Recalibration protocol response:", data);
        
        if (data.status === 'success') {
            alert(`Deep Recalibration Successful!\\n\\nConsentGlyph GSI restored: ${data.old_gsi.toFixed(3)} → ${data.new_gsi}\\nSystem Coherence: ${data.system_coherence.toFixed(3)}\\nSystem Entropy: ${data.system_entropy.toFixed(3)}`);
        } else {
            alert(`Recalibration Failed: ${data.message}`);
        }
        
        await updateSystemStatus();
        
    } catch (error) {
        console.error("Failed to run deep recalibration:", error);
        alert("Recalibration failed. Check the logs for details.");
    }
    
    isOperating = false;
    btn.disabled = false;
    btn.textContent = 'Deep Recalibration';
    document.getElementById('statusText').textContent = 'System Ready';
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('stressIntensity').addEventListener('input', e => {
        document.getElementById('stressValue').textContent = e.target.value;
    });
    document.getElementById('testDuration').addEventListener('input', e => {
        document.getElementById('durationValue').textContent = e.target.value;
    });
    document.getElementById('maxRecursion').addEventListener('input', e => {
        document.getElementById('recursionValue').textContent = e.target.value;
    });
    document.getElementById('glyphGSI').addEventListener('input', e => {
        document.getElementById('gsiValue').textContent = e.target.value;
    });
    
    updateSystemStatus();
    checkOllamaStatus();
    setInterval(updateSystemStatus, 2000);
    setInterval(checkOllamaStatus, 5000);
});
</script>
</body></html>'''
