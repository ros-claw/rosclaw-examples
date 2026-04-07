#!/usr/bin/env python3
"""
6台云台 V.mp3 舞蹈表演 - 基于成功的 GCU 协议
一字排开，从左到右依次动作，形成波浪效果
"""

import sys
import threading
import time
import math
sys.path.insert(0, '../src')
from gcu_gimbal_control import GCUGimbalController

# 6台云台配置
DEVICES = [
    (1, "/dev/ttyCH341USB0"),
    (2, "/dev/ttyCH341USB1"),
    (3, "/dev/ttyCH341USB2"),
    (4, "/dev/ttyCH341USB3"),
    (5, "/dev/ttyCH341USB4"),
    (6, "/dev/ttyCH341USB5"),
]

class GimbalDancer:
    """单个云台舞者"""
    def __init__(self, gimbal_id, port):
        self.id = gimbal_id
        self.port = port
        self.gimbal = GCUGimbalController(port=port, baudrate=115200)
        self.connected = False
        self._stop_event = threading.Event()
        self._thread = None
        
    def connect(self):
        """连接云台"""
        self.connected = self.gimbal.connect()
        if self.connected:
            self.gimbal.start_receiving()
            # 初始化设置
            self.gimbal.set_aircraft_attitude(roll=0, pitch=0, yaw=0)
            self.gimbal.set_mode_pointing_lock()
            time.sleep(0.2)
        return self.connected
    
    def disconnect(self):
        """断开连接"""
        self.stop()
        self.gimbal.reset_gimbal()
        time.sleep(0.2)
        self.gimbal.stop_receiving()
        self.gimbal.disconnect()
        self.connected = False
    
    def headbang(self, intensity=1.0, duration=2.0):
        """甩头动作 - Tilt轴方波"""
        def action():
            start = time.time()
            period = 0.469  # 128 BPM = 0.469s per beat
            speed = int(600 * intensity)  # 60°/s * intensity
            
            while time.time() - start < duration and not self._stop_event.is_set():
                elapsed = time.time() - start
                # 方波: 前半周期向上，后半周期向下
                if (elapsed % period) < (period * 0.5):
                    self.gimbal.rotate_pitch(-speed)  # 向上
                else:
                    self.gimbal.rotate_pitch(speed)   # 向下
                self.gimbal.send_packet()
                time.sleep(0.033)  # ~30Hz
            
            self.gimbal.stop_rotation()
            self.gimbal.send_packet()
        
        self._thread = threading.Thread(target=action)
        self._thread.start()
    
    def wave(self, intensity=1.0, duration=2.0, phase=0):
        """波浪动作 - Pan轴正弦波"""
        def action():
            start = time.time()
            period = 0.469
            speed = int(400 * intensity)
            
            while time.time() - start < duration and not self._stop_event.is_set():
                elapsed = time.time() - start + phase
                # 正弦波控制偏航
                yaw_speed = int(speed * math.sin(elapsed * 2 * math.pi / period))
                self.gimbal.rotate_yaw(yaw_speed)
                self.gimbal.send_packet()
                time.sleep(0.033)
            
            self.gimbal.stop_rotation()
            self.gimbal.send_packet()
        
        self._thread = threading.Thread(target=action)
        self._thread.start()
    
    def sweep(self, intensity=1.0, duration=2.0):
        """扫射动作"""
        def action():
            start = time.time()
            speed = int(500 * intensity)
            
            while time.time() - start < duration and not self._stop_event.is_set():
                elapsed = time.time() - start
                # 来回扫射
                if (elapsed % 2) < 1:
                    self.gimbal.rotate_yaw(speed)
                else:
                    self.gimbal.rotate_yaw(-speed)
                self.gimbal.send_packet()
                time.sleep(0.033)
            
            self.gimbal.stop_rotation()
            self.gimbal.send_packet()
        
        self._thread = threading.Thread(target=action)
        self._thread.start()
    
    def figure8(self, intensity=1.0, duration=2.0):
        """8字形动作 - 双轴联动"""
        def action():
            start = time.time()
            period = 0.938  # 2 beats
            speed = int(300 * intensity)
            
            while time.time() - start < duration and not self._stop_event.is_set():
                elapsed = time.time() - start
                # Lissajous 8字
                pitch_speed = int(speed * math.sin(elapsed * 2 * math.pi / period))
                yaw_speed = int(speed * math.sin(2 * elapsed * 2 * math.pi / period))
                self.gimbal.rotate(pitch_speed, yaw_speed)
                self.gimbal.send_packet()
                time.sleep(0.033)
            
            self.gimbal.stop_rotation()
            self.gimbal.send_packet()
        
        self._thread = threading.Thread(target=action)
        self._thread.start()
    
    def slow_circle(self, intensity=1.0, duration=2.0):
        """缓慢圆形"""
        def action():
            start = time.time()
            speed = int(200 * intensity)
            
            while time.time() - start < duration and not self._stop_event.is_set():
                elapsed = time.time() - start
                # 慢速正弦
                pitch_speed = int(speed * math.sin(elapsed * 0.5))
                yaw_speed = int(speed * math.cos(elapsed * 0.5))
                self.gimbal.rotate(pitch_speed, yaw_speed)
                self.gimbal.send_packet()
                time.sleep(0.033)
            
            self.gimbal.stop_rotation()
            self.gimbal.send_packet()
        
        self._thread = threading.Thread(target=action)
        self._thread.start()
    
    def freeze(self, duration=1.0):
        """冻结动作"""
        def action():
            start = time.time()
            self.gimbal.stop_rotation()
            while time.time() - start < duration and not self._stop_event.is_set():
                self.gimbal.send_packet()
                time.sleep(0.033)
        
        self._thread = threading.Thread(target=action)
        self._thread.start()
    
    def stop(self):
        """停止当前动作"""
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)
        self._stop_event.clear()
        self.gimbal.stop_rotation()
        self.gimbal.send_packet()
    
    def wait(self):
        """等待动作完成"""
        if self._thread and self._thread.is_alive():
            self._thread.join()


def main():
    print("=" * 70)
    print("🎵 6台云台 V.mp3 交响舞蹈 (GCU协议) 🎵")
    print("   排列: [1] [2] [3] [4] [5] [6]")
    print("   串口: USB0 USB1 USB2 USB3 USB4 USB5")
    print("   BPM: 128 | 时长: 60秒")
    print("=" * 70)
    
    # 创建舞者
    dancers = []
    for gid, port in DEVICES:
        dancer = GimbalDancer(gid, port)
        if dancer.connect():
            dancers.append(dancer)
            print(f"✓ 云台{gid} ({port}) 已连接")
        else:
            print(f"✗ 云台{gid} ({port}) 连接失败")
    
    if len(dancers) == 0:
        print("\n✗ 没有云台连接成功！")
        return
    
    print(f"\n✓ 已连接 {len(dancers)}/6 台云台")
    print("\n🎮 准备开始舞蹈！按 Ctrl+C 随时停止\n")
    time.sleep(2)
    
    try:
        # ========== 第1段：Intro (0-15s) ==========
        print("🌅 [00:00] Intro - 波浪唤醒...")
        print("    从左到右依次启动")
        
        for i, dancer in enumerate(dancers):
            dancer.slow_circle(intensity=0.4, duration=15-i*1.5)
            time.sleep(0.5)
        
        time.sleep(10)
        
        # ========== 第2段：Buildup (15-30s) ==========
        print("\n🔥 [00:15] Buildup - 能量积聚...")
        print("    三组同步波浪")
        
        # 左组 wave
        for dancer in dancers[:2]:
            dancer.wave(intensity=0.6, duration=15, phase=0)
        # 中组 wave (相位偏移)
        for dancer in dancers[2:4]:
            dancer.wave(intensity=0.8, duration=15, phase=math.pi/2)
        # 右组 wave
        for dancer in dancers[4:]:
            dancer.wave(intensity=0.6, duration=15, phase=math.pi)
        
        time.sleep(15)
        
        # ========== 第3段：DROP! (30-52s) ==========
        print("\n💥 [00:30] 🔥🔥🔥 DROP! 全功率输出! 🔥🔥🔥")
        print("    6台同步甩头!")
        
        # 全体 headbang 10秒
        for dancer in dancers:
            dancer.headbang(intensity=1.0, duration=10)
        time.sleep(10)
        
        print("\n    🌊 波浪切换 - 左右交替扫射!")
        for _ in range(3):
            # 左三扫射
            for dancer in dancers[:3]:
                dancer.sweep(intensity=1.0, duration=3)
            for dancer in dancers[3:]:
                dancer.freeze(duration=3)
            time.sleep(3)
            
            # 右三扫射
            for dancer in dancers[:3]:
                dancer.freeze(duration=3)
            for dancer in dancers[3:]:
                dancer.sweep(intensity=1.0, duration=3)
            time.sleep(3)
        
        print("\n    ✨ 终极齐舞 - 6台同步8字!")
        for dancer in dancers:
            dancer.figure8(intensity=0.9, duration=6)
        time.sleep(6)
        
        # ========== 第4段：Outro (52-60s) ==========
        print("\n🌙 [00:52] Outro - 优雅收尾...")
        print("    从中间向两边扩散归零")
        
        # 中间先停
        for dancer in dancers[2:4]:
            dancer.slow_circle(intensity=0.4, duration=4)
        time.sleep(1)
        for dancer in dancers[1:5:3]:  # index 1 and 4
            dancer.slow_circle(intensity=0.3, duration=4)
        time.sleep(1)
        for dancer in [dancers[0], dancers[5]]:
            dancer.slow_circle(intensity=0.2, duration=4)
        
        time.sleep(4)
        
        # 最终归零
        for dancer in dancers:
            dancer.freeze(duration=0.5)
            time.sleep(0.3)
        
        print("\n🛑 表演结束，云台归位...")
        for dancer in dancers:
            dancer.gimbal.reset_gimbal()
        time.sleep(1)
        
        print("\n" + "=" * 70)
        print("✨✨✨ 6台云台 V.mp3 舞蹈表演完成！✨✨✨")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\n⛔ 用户中断，停止所有云台...")
    finally:
        for dancer in dancers:
            dancer.stop()
            dancer.disconnect()
        print("✓ 全部云台已断开")

if __name__ == '__main__':
    main()
