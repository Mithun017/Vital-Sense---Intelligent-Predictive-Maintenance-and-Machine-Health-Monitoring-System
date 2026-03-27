import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area, PieChart, Pie, Cell 
} from 'recharts';
import { 
  Thermometer, Activity, Zap, AlertTriangle, CheckCircle, Bell, MessageSquare, Clock, ArrowRight, Server, Cpu, BarChart3
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE = 'http://localhost:8000';

const StatCard = ({ icon: Icon, label, value, unit, color, suffix = "" }) => (
  <motion.div 
    className="glass-card"
    initial={{ opacity: 0, scale: 0.95 }}
    animate={{ opacity: 1, scale: 1 }}
  >
    <div className="stat-header">
      <div className="stat-label">{label}</div>
      <Icon size={18} color={color} />
    </div>
    <div className="stat-value">
      {value}<span className="stat-unit">{unit}</span>
      {suffix && <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block' }}>{suffix}</span>}
    </div>
    <div className="live-indicator"></div>
  </motion.div>
);

function App() {
  const [activeMachine, setActiveMachine] = useState("M-101");
  const [machines, setMachines] = useState(["M-101", "M-102"]);
  const [data, setData] = useState({ latest_readings: [], current_health: null });
  const [alerts, setAlerts] = useState([]);
  const [chatQuery, setChatQuery] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const chatEndRef = useRef(null);

  const fetchData = async () => {
    try {
      const statsRes = await axios.get(`${API_BASE}/dashboard-stats/${activeMachine}`);
      const alertsRes = await axios.get(`${API_BASE}/alerts`);
      setData(statsRes.data);
      setAlerts(alertsRes.data.filter(a => a.machine_id === activeMachine));
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
      setChatHistory(prev => [...prev, { role: "ai", text: "Error connecting to AI Assistant." }]);
    }
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatHistory]);

  const health = data.current_health || {};
  const readings = data.latest_readings || [];
  const current = readings[0] || {};
  const status = health.health_status || "NORMAL";

  return (
    <div className="dashboard-container">
      {/* Sidebar / Machine Selector */}
      <nav style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', overflowX: 'auto', padding: '0.5rem 0' }}>
        {machines.map(m => (
          <button 
            key={m}
            className={`glass-card ${activeMachine === m ? 'active' : ''}`}
            onClick={() => setActiveMachine(m)}
            style={{ padding: '0.75rem 1.5rem', whiteSpace: 'nowrap', border: activeMachine === m ? '1px solid var(--accent-color)' : '1px solid var(--glass-border)', cursor: 'pointer', background: activeMachine === m ? 'rgba(59,130,246,0.1)' : '' }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Server size={14} /> {m}
            </div>
          </button>
        ))}
      </nav>

      <header>
        <div>
          <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }}>Vital Sense AI</motion.h1>
          <p style={{ color: 'var(--text-muted)' }}>Advanced Machine Health Intelligence • {activeMachine}</p>
        </div>
        <div className={`health-badge ${status.toLowerCase()}`}>
          {status}
        </div>
      </header>

      {/* Main Stats */}
      <div className="stats-grid">
        <StatCard icon={Clock} label="Remaining Useful Life" value={health.estimated_rul || "--"} unit="h" color="#a855f7" suffix="Based on degradation trend" />
        <StatCard icon={Thermometer} label="Temperature" value={current.temperature || "--"} unit="°C" color="#ef4444" />
        <StatCard icon={Activity} label="Vibration" value={current.vibration || "--"} unit="mm/s" color="#3b82f6" />
        <StatCard icon={BarChart3} label="Failure Probability" value={((health.failure_probability || 0) * 100).toFixed(1)} unit="%" color="#f59e0b" />
      </div>

      <div className="charts-grid">
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {/* Trend Chart */}
          <div className="glass-card chart-container">
            <h3 style={{ marginBottom: '1rem' }}>Condition History</h3>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={[...readings].reverse()}>
                <defs>
                  <linearGradient id="primaryGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.2}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="timestamp" tickFormatter={(t) => new Date(t).toLocaleTimeString()} hide />
                <YAxis hide />
                <Tooltip contentStyle={{ background: '#151921', border: '1px solid var(--glass-border)' }} />
                <Area type="monotone" dataKey="temperature" stroke="#ef4444" fill="url(#primaryGrad)" />
                <Area type="monotone" dataKey="vibration" stroke="#3b82f6" fill="url(#primaryGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          {/* AI Insights and Recommendations */}
          <div className="glass-card">
            <h3 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Cpu size={20} color="var(--accent-color)" /> AI Health Insights
            </h3>
            <p style={{ fontSize: '0.9rem', marginBottom: '1.5rem', lineHeight: 1.6, color: '#e2e8f0' }}>
              {health.ai_summary || "Analyzing current data for machine intelligence..."}
            </p>
            
            <div style={{ background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: '1rem' }}>
              <h4 style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.75rem', textTransform: 'uppercase' }}>Recommended Actions</h4>
              {health.recommendations?.map((rec, i) => (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem', fontSize: '0.85rem' }}>
                   <ArrowRight size={12} color="var(--accent-color)" /> {rec}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Gemini Assistant Chat */}
        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', height: '600px' }}>
          <div className="stat-header">
            <h3>Maintenance Assistant</h3>
            <MessageSquare size={18} color="var(--accent-color)" />
          </div>
          <div style={{ flex: 1, overflowY: 'auto', marginBottom: '1rem', padding: '0.5rem' }}>
            {chatHistory.length === 0 && <p style={{ color: 'var(--text-muted)', textAlign: 'center', marginTop: '50%' }}>Ask me about {activeMachine}'s health, maintenance history, or power efficiency.</p>}
            {chatHistory.map((msg, i) => (
              <div key={i} style={{ marginBottom: '1rem', textAlign: msg.role === 'user' ? 'right' : 'left' }}>
                <div style={{ 
                  display: 'inline-block', 
                  padding: '0.75rem 1rem', 
                  borderRadius: '1rem', 
                  background: msg.role === 'user' ? 'var(--accent-color)' : 'rgba(255,255,255,0.05)',
                  fontSize: '0.85rem',
                  maxWidth: '85%'
                }}>
                  {msg.text}
                </div>
              </div>
            ))}
            <div ref={chatEndRef} />
          </div>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <input 
              type="text" 
              value={chatQuery}
              onChange={(e) => setChatQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleChat()}
              placeholder="Ask anything..."
              style={{ flex: 1, background: 'rgba(0,0,0,0.3)', border: '1px solid var(--glass-border)', borderRadius: '0.75rem', padding: '0.75rem', color: 'white' }}
            />
            <button onClick={handleChat} style={{ background: 'var(--accent-color)', border: 'none', borderRadius: '0.75rem', padding: '0 1rem', cursor: 'pointer', color: 'white' }}>
              <ArrowRight size={18} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
