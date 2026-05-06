import time
import json
import asyncio
import random
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.ensemble import RandomForestClassifier

app = FastAPI(title="CyberAttrib.AI API", version="1.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# 1. MVP ML MODEL (Scikit-Learn)
# ---------------------------------------------------------
print("Training MVP Scikit-Learn model...")
# Dummy dataset simulating MITRE ATT&CK technique presence (0 or 1)
# Features: [T1566_Phishing, T1078_ValidAccounts, T1195_SupplyChain, T1190_ExploitPublic, T1053_ScheduledTask]
X_train = [
    [1, 1, 0, 0, 0], # APT28
    [0, 0, 1, 0, 0], # Lazarus
    [0, 0, 0, 1, 0], # APT41
    [1, 0, 0, 0, 1], # APT29
    [0, 1, 1, 0, 0], # Turla
    [0, 0, 0, 0, 1], # APT10
]
y_train = ["APT28", "Lazarus", "APT41", "APT29", "Turla", "APT10"]

model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train, y_train)
print("Model trained successfully.")

def predict_threat(features):
    # Predict the actor
    prediction = model.predict([features])[0]
    # Get probabilities
    probs = model.predict_proba([features])[0]
    classes = model.classes_
    
    # Sort confidence scores
    conf_scores = sorted([{"label": classes[i], "pct": round(probs[i]*100)} for i in range(len(classes))], key=lambda x: x['pct'], reverse=True)
    
    return prediction, conf_scores[:3]

# ---------------------------------------------------------
# 2. DATA / SCENARIOS
# ---------------------------------------------------------
class ScenarioRequest(BaseModel):
    scenario_id: str

SCENARIOS_DB = {
    "apt28": {"id": "apt28", "actor": "APT28 (Fancy Bear)", "alias": "aka IRON TWILIGHT", "iocs": [{"key": "TTP", "val": "T1566.001 - Spear Phishing"}], "features": [1,1,0,0,0]},
    "lazarus": {"id": "lazarus", "actor": "Lazarus Group", "alias": "aka HIDDEN COBRA", "iocs": [{"key": "TTP", "val": "T1195 - Supply Chain"}], "features": [0,0,1,0,0]},
    "apt41": {"id": "apt41", "actor": "APT41 (Double Dragon)", "alias": "aka WICKED PANDA", "iocs": [{"key": "TTP", "val": "T1190 - Exploit Public-Facing"}], "features": [0,0,0,1,0]},
    "apt29": {"id": "apt29", "actor": "APT29 (Cozy Bear)", "alias": "aka NOBELIUM", "iocs": [{"key": "TTP", "val": "T1053 - Scheduled Task"}], "features": [1,0,0,0,1]},
    "turla": {"id": "turla", "actor": "Turla (Venomous Bear)", "alias": "aka KRYPTON", "iocs": [{"key": "TTP", "val": "T1102 - Web Service"}], "features": [0,1,1,0,0]},
    "apt10": {"id": "apt10", "actor": "APT10 (Stone Panda)", "alias": "aka menuPass", "iocs": [{"key": "TTP", "val": "T1199 - Trusted Relationship"}], "features": [0,0,0,0,1]}
}

# ---------------------------------------------------------
# 3. WEBSOCKET MANAGER
# ---------------------------------------------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

# ---------------------------------------------------------
# 4. BACKGROUND TASK (Simulate Live Feed)
# ---------------------------------------------------------
async def live_threat_feed():
    while True:
        await asyncio.sleep(random.randint(8, 15)) # Push a new threat every 8-15 seconds
        if len(manager.active_connections) > 0:
            # Pick a random scenario to simulate incoming CTI data
            scenario_key = random.choice(list(SCENARIOS_DB.keys()))
            data = SCENARIOS_DB[scenario_key]
            
            # Run it through the ML model!
            predicted_actor, confidence = predict_threat(data["features"])
            
            # Construct response
            payload = {
                "type": "live_alert",
                "timestamp": time.strftime("%H:%M:%S UTC"),
                "source": "AlienVault OTX (Simulated)",
                "actor": data["actor"],
                "predicted": predicted_actor,
                "confidence": confidence,
                "iocs": data["iocs"]
            }
            await manager.broadcast(payload)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(live_threat_feed())

# ---------------------------------------------------------
# 5. ENDPOINTS
# ---------------------------------------------------------
@app.websocket("/api/stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/api/simulate")
def simulate_attribution(request: ScenarioRequest):
    time.sleep(1) # Simulate processing delay
    scenario_id = request.scenario_id
    if scenario_id not in SCENARIOS_DB:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    data = SCENARIOS_DB[scenario_id]
    predicted_actor, confidence = predict_threat(data["features"])
    
    # Enrich the hardcoded data with the actual ML predictions
    response_data = data.copy()
    response_data["confidence"] = confidence
    
    # Re-add some extra UI properties to match frontend expectation
    color_map = {0: "#ff3e6c", 1: "#f5c518", 2: "#00d4ff"}
    for i, c in enumerate(response_data["confidence"]):
        c["color"] = color_map.get(i, "#00d4ff")
        
    return response_data

@app.get("/api/health")
def health_check():
    return {"status": "operational", "active_models": 1, "model_type": "RandomForest"}
