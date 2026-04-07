#!/usr/bin/env python3
"""
ROSClaw 实时可视化服务器
接收来自 cyber_bamboo_sages_7.py 的实时数据并通过 WebSocket 广播
"""

import asyncio
import json
import websockets
import numpy as np
from dataclasses import dataclass, asdict
from typing import Dict, Set
from datetime import datetime
import threading
import time

# 全局状态
connected_clients: Set[websockets.WebSocketServerProtocol] = set()
gimbal_data: Dict[str, dict] = {}
audio_data = {
    'waveform': [],
    'current_time': 0.0,
    'bpm': 120.0,
    'beat_phase': 0.0,
    'phase_name': 'INIT'
}

@dataclass
class GimbalState:
    agent_id: str
    roll: float
    pitch: float
    yaw: float
    timestamp: float
    phase: str

async def register(websocket):
    connected_clients.add(websocket)
    print(f"[VIZ] Client connected. Total: {len(connected_clients)}")
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.discard(websocket)
        print(f"[VIZ] Client disconnected. Total: {len(connected_clients)}")

async def broadcast_state():
    """广播当前状态到所有客户端"""
    if not connected_clients:
        return
    
    message = {
        'type': 'state_update',
        'timestamp': time.time(),
        'audio': audio_data,
        'gimbals': gimbal_data
    }
    
    json_msg = json.dumps(message)
    
    # 广播给所有连接的客户端
    disconnected = set()
    for client in connected_clients:
        try:
            await client.send(json_msg)
        except:
            disconnected.add(client)
    
    # 清理断开的连接
    for client in disconnected:
        connected_clients.discard(client)

async def websocket_server():
    """启动 WebSocket 服务器"""
    async with websockets.serve(register, "0.0.0.0", 8765):
        print("[VIZ] WebSocket server started on ws://0.0.0.0:8765")
        while True:
            await broadcast_state()
            await asyncio.sleep(0.05)  # 20Hz 广播

def update_gimbal(agent_id: str, roll: float, pitch: float, yaw: float, phase: str):
    """更新云台数据（从编舞脚本调用）"""
    gimbal_data[agent_id] = {
        'roll': round(roll, 2),
        'pitch': round(pitch, 2),
        'yaw': round(yaw, 2),
        'phase': phase,
        'timestamp': time.time()
    }

def update_audio(current_time: float, beat_phase: float, phase_name: str):
    """更新音频数据"""
    audio_data['current_time'] = round(current_time, 3)
    audio_data['beat_phase'] = round(beat_phase, 3)
    audio_data['phase_name'] = phase_name
    
    # 生成模拟波形数据 (用于可视化)
    t = current_time
    waveform = []
    for i in range(100):
        sample_time = t + (i - 50) * 0.01
        # 模拟音乐波形
        val = np.sin(sample_time * 10) * 0.3
        val += np.sin(sample_time * 20) * 0.2
        val += np.sin(sample_time * 5) * 0.4
        # 添加 beat 冲击
        beat = (sample_time * 2) % 1.0
        if beat < 0.1:
            val += 0.5 * (1 - beat / 0.1)
        waveform.append(round(val, 3))
    
    audio_data['waveform'] = waveform

def start_visualization_server():
    """启动可视化服务器（在后台线程中）"""
    def run_server():
        asyncio.run(websocket_server())
    
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    print("[VIZ] Visualization server started in background")
    return thread

if __name__ == "__main__":
    # 测试模式
    start_visualization_server()
    
    # 模拟数据
    import random
    phases = ['INTRO', 'G4_SOLO', 'UNISON', 'OUTRO']
    
    try:
        while True:
            t = time.time() % 28.76
            phase = phases[int(t / 7) % 4]
            
            update_audio(t, (t * 2) % 1.0, phase)
            
            for i, gid in enumerate(['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7']):
                roll = 20 * np.sin(t * 3 + i)
                pitch = 20 * np.sin(t * 2 + i * 0.5)
                yaw = (i - 3) * 20 + 10 * np.sin(t * 1.5)
                update_gimbal(gid, roll, pitch, yaw, phase)
            
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        print("\n[VIZ] Server stopped")