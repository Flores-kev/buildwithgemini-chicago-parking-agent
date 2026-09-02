# 🔔 Chicago Parking Patrol — 1980s Retro Edition

An AI-powered agentic application built with Google's **Agent Development Kit (ADK)** and **Vertex AI Agent Engine**, featuring a **1980s Taco Bell Memphis Design UI** and **AI Retro Street Cross-Section Diagrams**.

![Chicago Parking Patrol Demo](demo.gif)

---

## 🚀 Live Demo

- **Web Application (Cloud Run)**: [https://chicago-parking-frontend-466731583426.us-central1.run.app](https://chicago-parking-frontend-466731583426.us-central1.run.app)
- **Deployed Agent (Vertex AI)**: `projects/466731583426/locations/us-central1/reasoningEngines/7129503324604203008`

---

## 🌟 Key Features

### 1. 🏙️ Chicago Parking Protection Engine
- Real-time restriction checking for Chicago locations against street sweeping schedules, 2-inch snow bans, and winter overnight parking rules.
- Instant impoundment and tow-risk evaluation.

### 2. 🎨 1980s Taco Bell "Memphis Design" Chat UI
- High-contrast retro visual theme built with Neon Magenta (`#FF007F`), Electric Cyan (`#00E5FF`), Synthwave Purple (`#2A085C`), and Google Fonts (`Righteous`, `Rubik Mono One`).
- Quick-action location chips for one-click spot checking (*"🚗 My Saved Spot"*, *"📍 1200 N Milwaukee Ave"*, *"📍 2400 N Clark St"*).

### 3. 📐 AI 80s Architectural Street Cross-Section Generator
- Calls `gemini-3.1-flash-lite-image` to generate a 1980s synthwave architectural street cross-section diagram showing sidewalks, curb, parked vehicle, roadway lanes, signs, and glowing green **SAFE** / red **DANGER** status indicators.
- Automatically uploads generated diagrams to public Google Cloud Storage (`gs://bwg3-qwiklabs-gcp-03-1a24275fdf4b`) and renders them inline inside retro cards.

### 4. 💾 Firestore & Vertex AI Memory Bank Integration
- Persists user parking locations and preferences to Firestore (`parking_records` collection).
- Integrates Vertex AI Memory Bank for session-to-session memory persistence.

---

## 🏗️ Architecture & Technology Stack

```
[ Web Browser ]
      │
      ▼ (HTTP / A2A)
[ FastAPI Proxy (Cloud Run) ]
      │
      ▼ (Agent-to-Agent A2A Protocol)
[ Vertex AI Agent Engine (Gemini 2.5 Flash) ]
      ├── Firestore DB (parking_records)
      ├── Vertex AI Memory Bank
      └── Gemini 3.1 Flash Lite Image ──▶ Google Cloud Storage (Public HTTPS URLs)
```

- **Agent Core**: Google ADK (Agent Development Kit), Gemini 2.5 Flash.
- **Frontend**: Lightweight FastAPI Proxy serving an 80s Taco Bell styled SPA via A2A Protocol client, deployed on Cloud Run.
- **Image Generation**: `gemini-3.1-flash-lite-image` model in global region.
- **Database & Storage**: Google Cloud Firestore & Google Cloud Storage.

---

## 📂 Project Structure

```
.
├── app/
│   ├── agent.py               # Main ADK agent instructions and tool registration
│   ├── firestore_tools.py     # Firestore database read/write tools & seeding script
│   └── image_gen_tools.py     # Gemini image generation & Cloud Storage upload tools
├── frontend/
│   ├── main.py                # FastAPI proxy server using A2A ClientFactory
│   ├── Dockerfile             # Dockerfile for Cloud Run deployment
│   └── static/
│       └── index.html         # 1980s Taco Bell themed single-page web app
├── tests/                     # Integration and agent test suite
├── demo.gif                   # Recorded video demonstration GIF
├── pyproject.toml             # Project dependencies and configuration
└── README.md                  # Project documentation
```

---

## 🛠️ Local Development & Testing

1. **Install Dependencies**:
   ```bash
   uv pip install -e .
   ```

2. **Run Local Agent Playground**:
   ```bash
   export GOOGLE_GENAI_USE_VERTEXAI=true
   export GOOGLE_CLOUD_PROJECT="qwiklabs-gcp-03-1a24275fdf4b"
   agents-cli playground
   ```

3. **Run Frontend Proxy Locally**:
   ```bash
   cd frontend
   python main.py
   ```
   Open `http://localhost:8080` in your browser.

4. **Run Integration Tests**:
   ```bash
   pytest tests/integration/test_agent.py
   ```

---

## 🚀 Deployment

### Deploy Agent to Vertex AI Agent Engine
```bash
agents-cli deploy --no-confirm-project --region us-central1
```

### Deploy Frontend to Cloud Run
```bash
cd frontend
gcloud run deploy chicago-parking-frontend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars AGENT_ENGINE_RESOURCE_NAME="projects/466731583426/locations/us-central1/reasoningEngines/7129503324604203008",AGENT_DIRECTORY="app"
```

---

## 📜 License
Built for the **Build with Gemini** Agent Development Challenge.
