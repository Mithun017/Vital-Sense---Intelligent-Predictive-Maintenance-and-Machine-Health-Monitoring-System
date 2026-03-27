import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area, PieChart, Pie, Cell 
} from 'recharts';
import { 
  Thermometer, Activity, Zap, AlertTriangle, CheckCircle, Bell, MessageSquare, Clock, ArrowRight, Server, Cpu, BarChart3, Settings, Shield, ZapOff
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE = 'http://localhost:8000';

// Custom Gauge Component using Recharts Pie
const Gauge = ({ value, color, label }) => {
  const data = [
    { value: value },
    { value: 100 - value }
  ];
  return (
    <div className="gauge-wrapper">
      <ResponsiveContainer width="100%" height={150}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="100%"
            startAngle={180}
            endAngle={0}
            innerRadius={60}
            outerRadius={80}
            paddingAngle={0}
            dataKey="value"
          >
            <Cell fill={color} />
            <Cell fill="rgba(255,255,255,0.05)" />
          </Pie>
        </PieChart>
      </ResponsiveContainer>
      <div className="gauge-overlay">
        <span className="gauge-value">{value}%</span>
        <span className="gauge-label">{label}</span>
      </div>
    </div>
  );
};

const StatCard = ({ icon: Icon, label, value, unit, color, status = "normal" }) => (
  <motion.div 
    className={`glass-card stat-card ${status}`}
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
  >
    <div className="stat-header">
      <div className="stat-icon-wrapper" style={{ background: `${color}15` }}>
        <Icon size={20} color={color} />
      </div>
      <div className="stat-label">{label}</div>
    </div>
    <div className="stat-main">
      <span className="stat-value">{value}</span>
      <span className="stat-unit">{unit}</span>
    </div>
    <div className="stat-progress-bg">
      <motion.div 
        className="stat-progress-bar" 
        style={{ background: color }}
        initial={{ width: 0 }}
        animate={{ width: '70%' }}
      />
    </div>
  </motion.div>
);

function App() {
  const [activeMachine, setActiveMachine] = useState("M-101");
  const [machines, setMachines] = useState([]);
  const [data, setData] = useState({ latest_readings: [], current_health: null });
  const [systemOverview, setSystemOverview] = useState([]);
  const [chatQuery, setChatQuery] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const chatEndRef = useRef(null);
  const scrollRef = useRef(null);

  // Markdown handling for Phase 13 (Bold only)
  const renderContent = (text) => {
    if (!text) return null;
    return text.split(/(\*\*.*?\*\*)/g).map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={i} style={{ color: 'var(--accent-color)', fontWeight: '700' }}>{part.slice(2, -2)}</strong>;
      }
      return part;
    });
  };

  const fetchData = async () => {
    try {
      const statsRes = await axios.get(`${API_BASE}/dashboard-stats/${activeMachine}`);
      const overviewRes = await axios.get(`${API_BASE}/system-overview`);
      const machinesRes = await axios.get(`${API_BASE}/active-machines`);
      
      setData(statsRes.data);
      setSystemOverview(overviewRes.data);
      setMachines(machinesRes.data);
    } catch (err) { console.error(err); }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, [activeMachine]);

  const handleChat = async () => {
    if (!chatQuery) return;
    const userMsg = { role: "user", text: chatQuery };
    setChatHistory(prev => [...prev, userMsg]);
    setChatQuery("");
    
    try {
      const res = await axios.post(`${API_BASE}/assistant/query`, { 
        machine_id: activeMachine, 
        text: chatQuery 
      });
      setChatHistory(prev => [...prev, { role: "ai", text: res.data.answer }]);
    } catch (err) {
      setChatHistory(prev => [...prev, { role: "ai", text: "Integration error. Check API key/backend logs." }]);
    }
  };

  const health = data.current_health || {};
  const readings = data.latest_readings || [];
  const current = readings[0] || {};
  const status = health.health_status || "NORMAL";

  return (
    <div className="app-container">
      {/* Sidebar Layout */}
      <aside className="sidebar">
        <div className="logo-section">
          <div className="logo-icon"><Shield size={24} color="#3b82f6" /></div>
          <h2>Vital Sense</h2>
        </div>
        
        <div className="sidebar-nav">
          <p className="nav-label">Fleet Overview</p>
          <div className="machine-list">
            {systemOverview.map(m => (
              <button 
                key={m.machine_id}
                className={`machine-item ${activeMachine === m.machine_id ? 'active' : ''}`}
                onClick={() => setActiveMachine(m.machine_id)}
              >
                <div className={`status-dot ${m.status.toLowerCase()}`}></div>
                <span>{m.machine_id}</span>
                <span className="prob-small">{Math.round(m.probability * 100)}%</span>
              </button>
            ))}
          </div>
        </div>

        <div className="sidebar-footer">
          <div className="user-profile">
            <div className="avatar">MM</div>
            <div>
              <p className="user-name">Mithun</p>
              <p className="user-role">Lead Engineer</p>
            </div>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="main-header">
          <div className="header-info">
            <h1>{activeMachine} Control Center</h1>
            <p className="last-sync">System Status: Real-time data sync active</p>
          </div>
          <div className="header-actions">
            <div className="notification-bell"><Bell size={20} /><div className="notif-dot"></div></div>
            <div className={`status-pill ${status.toLowerCase()}`}>{status}</div>
          </div>
        </header>

        {/* Intelligence Row */}
        <section className="intel-section">
           <div className="glass-card rul-card">
              <div className="card-header">
                <h3>Remaining Useful Life</h3>
                <Clock size={16} color="var(--text-muted)" />
              </div>
              <div className="rul-display">
                <span className="rul-big">{health.estimated_rul || "0"}</span>
                <span className="rul-label">HOURS REMAINING</span>
              </div>
              <div className="rul-trend">
                <Zap size={14} color="#10b981" /> Degradation: {status === 'NORMAL' ? 'Stable' : 'Aggressive'}
              </div>
           </div>

           <div className="glass-card probe-card">
             <Gauge value={Math.round((health.failure_probability || 0) * 100)} color={status === 'CRITICAL' ? '#ef4444' : '#f59e0b'} label="Risk Index" />
           </div>

           <div className="glass-card ai-summary-card">
              <div className="card-header">
                <h3>AI Diagnostic reasoning</h3>
                <Cpu size={16} color="var(--accent-color)" />
              </div>
              <p className="ai-report-text">
                {renderContent(health.ai_summary) || "Computing fleet intelligence..."}
              </p>
              <div className="confidence-badge">98% AI Confidence</div>
           </div>

           <div className="glass-card energy-card">
              <div className="card-header">
                <h3>Energy Monitor (Phase 10)</h3>
                <Zap size={16} color="#fbbf24" />
              </div>
              <div className="energy-grid">
                 <div className="energy-stat">
                   <span className="stat-value">{health.energy_metrics?.power_watts || "0"}W</span>
                   <span className="stat-label">Power Load</span>
                 </div>
                 <div className="energy-stat">
                   <span className="stat-value">{health.energy_metrics?.efficiency_pct || "0"}%</span>
                   <span className="stat-label">Efficiency Index</span>
                 </div>
              </div>
              <p className="energy-tip">
                {health.energy_metrics?.efficiency_pct < 90 ? "⚠️ High losses detected. Check thermal dissipation." : "✨ Optimal performance profile."}
              </p>
           </div>
        </section>

        {/* Real-time Visualization */}
        <section className="vis-section">
          <div className="glass-card main-chart-card">
            <div className="chart-header">
              <h3>Telemetry Analytics (T/V/C)</h3>
              <div className="chart-legend">
                <span className="dot temp"></span> Temp
                <span className="dot vibe"></span> Vibe
              </div>
            </div>
            <div className="chart-body">
              <ResponsiveContainer width="100%" height={350}>
                <AreaChart data={[...readings].reverse()}>
                  <defs>
                    <linearGradient id="colorTemp" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#ef4444" stopOpacity={0.1}/>
                      <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.03)" vertical={false} />
                  <XAxis dataKey="timestamp" hide />
                  <YAxis hide domain={['auto', 'auto']} />
                  <Tooltip contentStyle={{ background: '#0b0e14', border: '1px solid #1e293b', borderRadius: '8px' }} />
                  <Area type="monotone" dataKey="temperature" stroke="#ef4444" fillOpacity={1} fill="url(#colorTemp)" />
                  <Area type="monotone" dataKey="vibration" stroke="#3b82f6" fill="transparent" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="glass-card actions-card">
              <div className="card-header">
                <h3>Maintenance Directives</h3>
                <Settings size={16} color="var(--text-muted)" />
              </div>
              <div className="actions-list">
                {health.recommendations?.map((rec, i) => (
                  <div key={i} className="action-item">
                    <div className="action-check"><CheckCircle size={14} /></div>
                    <span>{rec}</span>
                  </div>
                ))}
                {(!health.recommendations || health.recommendations.length === 0) && <p className="text-muted">No immediate maintenance tasks.</p>}
              </div>
          </div>
        </section>

        {/* Assistant Floating Toggle */}
        <div className="assistant-container">
          <AnimatePresence>
            {isChatOpen && (
              <motion.div 
                className="chat-window-advanced"
                initial={{ opacity: 0, y: 50, scale: 0.9 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 50, scale: 0.9 }}
              >
                <div className="chat-header-complex">
                  <div className="chat-info">
                    <Cpu size={18} color="#3b82f6" />
                    <div>
                      <p className="chat-title">Maintenance GenAI</p>
                      <p className="chat-subtitle">Online • Groq Cloud Powered</p>
                    </div>
                  </div>
                  <button className="close-btn" onClick={() => setIsChatOpen(false)}>×</button>
                </div>
                
                <div className="chat-messages-container">
                  {chatHistory.length === 0 && (
                    <div className="empty-chat">
                      <MessageSquare size={32} color="var(--glass-border)" />
                      <p>Ask me about machine trends, performance, or maintenance logs.</p>
                    </div>
                  )}
                  {chatHistory.map((msg, i) => (
                     <div key={i} className={`chat-bubble-wrapper ${msg.role}`}>
                       <div className="chat-bubble">
                         {renderContent(msg.text)}
                       </div>
                     </div>
                  ))}
                  <div ref={chatEndRef} />
                </div>

                <div className="chat-input-area">
                  <input 
                    type="text" 
                    placeholder="Type your query..."
                    value={chatQuery}
                    onChange={(e) => setChatQuery(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleChat()}
                  />
                  <button onClick={handleChat} className="send-btn">
                    <ArrowRight size={20} />
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
          
          <motion.button 
            className={`chat-toggle-btn ${isChatOpen ? 'active' : ''}`}
            onClick={() => setIsChatOpen(!isChatOpen)}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
          >
            {isChatOpen ? <ZapOff size={24} /> : <MessageSquare size={24} />}
          </motion.button>
        </div>
      </main>
    </div>
  );
}

export default App;
