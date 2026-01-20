"""
RPA Automation Router
Handles RPA bot execution for DGVCL and other government portals
"""

import asyncio
import json
import threading
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import sys
import os

# Add rpa-automation to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..', 'rpa-automation'))

try:
    from dgvcl_rpa_bot import DGVCLRPABot
except ImportError:
    DGVCLRPABot = None

router = APIRouter(prefix="/rpa", tags=["RPA Automation"])

# Store active RPA sessions
active_sessions: Dict[str, Dict] = {}
websocket_connections: Dict[str, WebSocket] = {}

class RPARequest(BaseModel):
    """RPA automation request model"""
    provider: str  # dgvcl, pgvcl, etc.
    application_type: str  # name_change, new_connection, etc.
    form_data: Dict[str, Any]
    user_id: Optional[int] = None
    session_id: Optional[str] = None

class RPAStatus(BaseModel):
    """RPA status model"""
    session_id: str
    step: str
    message: str
    status: str  # processing, waiting, success, error
    timestamp: str
    progress: int  # 0-100

@router.post("/start")
async def start_rpa_automation(request: RPARequest, background_tasks: BackgroundTasks):
    """Start RPA automation process"""
    
    if not DGVCLRPABot:
        raise HTTPException(status_code=500, detail="RPA bot not available - Selenium not installed")
    
    # Generate session ID
    session_id = f"rpa_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{request.user_id or 'anonymous'}"
    
    # Initialize session
    active_sessions[session_id] = {
        "status": "starting",
        "provider": request.provider,
        "application_type": request.application_type,
        "started_at": datetime.now().isoformat(),
        "progress": 0
    }
    
    # Start RPA bot in background
    background_tasks.add_task(run_rpa_bot, session_id, request)
    
    return {
        "success": True,
        "session_id": session_id,
        "message": "RPA automation started",
        "websocket_url": f"/rpa/ws/{session_id}"
    }

@router.get("/status/{session_id}")
async def get_rpa_status(session_id: str):
    """Get RPA automation status"""
    
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return active_sessions[session_id]

@router.get("/sessions")
async def list_active_sessions():
    """List all active RPA sessions"""
    return {
        "active_sessions": len(active_sessions),
        "sessions": active_sessions
    }

@router.delete("/stop/{session_id}")
async def stop_rpa_automation(session_id: str):
    """Stop RPA automation process"""
    
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Mark session as stopped
    active_sessions[session_id]["status"] = "stopped"
    active_sessions[session_id]["stopped_at"] = datetime.now().isoformat()
    
    return {"success": True, "message": "RPA automation stopped"}

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time RPA status updates"""
    
    await websocket.accept()
    websocket_connections[session_id] = websocket
    
    try:
        # Send initial status
        if session_id in active_sessions:
            await websocket.send_json(active_sessions[session_id])
        
        # Keep connection alive and send updates
        while True:
            # Wait for messages (keep-alive)
            try:
                await asyncio.wait_for(websocket.receive_text(), timeout=1.0)
            except asyncio.TimeoutError:
                # Send periodic updates if session is active
                if session_id in active_sessions:
                    await websocket.send_json(active_sessions[session_id])
            
    except WebSocketDisconnect:
        # Clean up connection
        if session_id in websocket_connections:
            del websocket_connections[session_id]

async def send_status_update(session_id: str, status_data: Dict):
    """Send status update via WebSocket"""
    
    # Update session data
    if session_id in active_sessions:
        active_sessions[session_id].update(status_data)
    
    # Send via WebSocket if connected
    if session_id in websocket_connections:
        try:
            await websocket_connections[session_id].send_json(status_data)
        except:
            # Connection closed, remove it
            del websocket_connections[session_id]

def run_rpa_bot(session_id: str, request: RPARequest):
    """Run RPA bot in background thread"""
    
    def status_callback(status_data):
        """Callback for RPA bot status updates"""
        
        # Calculate progress based on step
        step_progress = {
            "STEP 1": 20,
            "STEP 2": 40,
            "STEP 3": 60,
            "STEP 4": 80,
            "STEP 5": 90,
            "COMPLETE": 100,
            "ERROR": 0
        }
        
        progress = step_progress.get(status_data.get("step", ""), 0)
        
        # Update session
        update_data = {
            **status_data,
            "session_id": session_id,
            "progress": progress
        }
        
        active_sessions[session_id].update(update_data)
        
        # Send WebSocket update (run in event loop)
        if session_id in websocket_connections:
            asyncio.create_task(send_status_update(session_id, update_data))
    
    try:
        # Initialize bot based on provider
        if request.provider.lower() == "dgvcl":
            bot = DGVCLRPABot(headless=True)  # Run in headless mode on server
            result = bot.run_complete_automation(request.form_data, status_callback)
        else:
            result = {"success": False, "error": f"Provider {request.provider} not supported yet"}
        
        # Update final status
        final_status = {
            "status": "completed" if result["success"] else "failed",
            "result": result,
            "completed_at": datetime.now().isoformat(),
            "progress": 100 if result["success"] else 0
        }
        
        active_sessions[session_id].update(final_status)
        
        # Send final update
        if session_id in websocket_connections:
            asyncio.create_task(send_status_update(session_id, final_status))
            
    except Exception as e:
        # Handle errors
        error_status = {
            "status": "error",
            "error": str(e),
            "failed_at": datetime.now().isoformat(),
            "progress": 0
        }
        
        active_sessions[session_id].update(error_status)
        
        if session_id in websocket_connections:
            asyncio.create_task(send_status_update(session_id, error_status))

# Health check endpoint
@router.get("/health")
async def rpa_health_check():
    """Check RPA system health"""
    
    health_status = {
        "rpa_available": DGVCLRPABot is not None,
        "active_sessions": len(active_sessions),
        "websocket_connections": len(websocket_connections),
        "timestamp": datetime.now().isoformat()
    }
    
    if not DGVCLRPABot:
        health_status["error"] = "Selenium WebDriver not available"
        health_status["install_command"] = "pip install selenium"
    
    return health_status