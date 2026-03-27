# Vital Sense AI - Advanced Predictive Maintenance System

Vital Sense AI is an intelligent, self-learning platform for industrial machine health monitoring. It integrates real-time sensor data, Remaining Useful Life (RUL) prediction, and Gemini AI reasoning to provide actionable maintenance insights.

## 🚀 Quick Start (Recommended)

If you are setting up the project for the first time or on a new system:

1. **Setup everything**: Double-click **`setup_project.bat`**. This installs all Python and Node.js dependencies automatically.
2. **Start the System**: Double-click **`run_start.bat`**. This launches the Backend, Dashboard, and Simulators in one go.

---

### 🔐 Security Note
The project includes a `.gitignore` to protect your sensitive data. Your **`GEMINI_API_KEY`** should be stored in `backend/.env` (which is automatically excluded from Git).

## 🌟 Advanced Features
- **Predictive RUL**: Estimates hours of life remaining using degradation trends.
- **Explainable AI (XAI)**: Identifies which sensors are driving machine health status.
- **Gemini Health Assistant**: Natural language diagnostic summaries and interactive maintenance chat.
- **Multi-Machine Support**: Dedicated views for monitoring and comparing different machine IDs (M-101, M-102, etc.).

## 🛠️ Tech Stack
- **Frontend**: React (Vite), Framer Motion, Recharts, Lucide.
- **Backend**: FastAPI, Pydantic, Python.
- **AI/ML**: Scikit-Learn (Linear Regression for RUL), Custom XAI Engine.
- **GenAI**: Google Gemini AI (via `google-generativeai`).
- **Database**: MongoDB (Async Motor driver).

## 📂 Project Structure
```
├── backend/            # AI Intelligence & Database Layer
├── frontend/           # Premium Glassmorphic Dashboard
├── simulation/         # IoT & Hardware Simulators
├── setup_project.bat   # Automated One-Click Setup
└── run_start.bat       # Unified System Launcher
```

---

## 🔧 Manual Setup (Developers)

1. **Backend**: `cd backend && pip install -r requirements.txt`
2. **Frontend**: `cd frontend && npm install`
3. **Run**: `cd backend && python -m uvicorn main:app --reload`
4. **Simulate**: `cd simulation && python simulate_sensors.py --id M-101`

**Note**: Set your `GEMINI_API_KEY` in `backend/.env` to enable the AI Maintenance Assistant.
