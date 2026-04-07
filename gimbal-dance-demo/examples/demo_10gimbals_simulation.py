#!/usr/bin/env python3
"""
V.mp3 完整舞蹈表演
60秒音乐 + 10台云台群舞
"""

import sys
import asyncio
sys.path.insert(0, '../src')
sys.argv.append('--sim')  # 仿真模式

from dance_mcp_server import (
    connect_dance_floor, disconnect_dance_floor,
    execute_rhythm_behavior, choreograph_dance,
    stop_all_gimbals, get_dance_status
)

async def v_dance_performance():
    print("=" * 70)
    print("🎵 V.mp3 - 云台交响舞蹈表演 🎵")
    print("   BPM: 128 | Duration: 60s | Vibe: Energetic EDM")
    print("=" * 70)
    
    # 连接舞台
    print("\n📡 连接舞蹈舞台...")
    result = await connect_dance_floor('../config/gimbal_config.yaml')
    print(result)
    
    # 等待所有云台就位
    await asyncio.sleep(2)
    
    # ========== 第1段：Intro (0-15s) ==========
    print("\n🌅 [00:00] Intro - 氛围渲染...")
    print("    Vocals: 缓慢的圆形扫描 | Spotlight: 缓慢环绕 | Drummers: 待命")
    await asyncio.gather(
        execute_rhythm_behavior('vocals', 'slow_circle', 64, 0.4, 15),
        execute_rhythm_behavior('spotlight', 'slow_circle', 32, 0.3, 15),
        execute_rhythm_behavior('drummers', 'freeze', 128, 0, 15),
    )
    
    # ========== 第2段：Buildup (15-30s) ==========
    print("\n🔥 [00:15] Buildup - 能量积聚...")
    print("    Drummers: 心跳式脉冲 | Vocals: 波浪扫射 | Spotlight: 8字形")
    await asyncio.gather(
        execute_rhythm_behavior('drummers', 'heartbeat', 128, 0.6, 15),
        execute_rhythm_behavior('vocals', 'wave', 128, 0.7, 15, phase_wave=True),
        execute_rhythm_behavior('spotlight', 'figure8', 128, 0.5, 15),
    )
    
    # ========== 第3段：DROP! (30-52s) ==========
    print("\n💥 [00:30] 🔥🔥🔥 DROP! 🔥🔥🔥")
    print("    Drummers: 疯狂甩头! | Vocals: 全幅度波浪! | Spotlight: 频闪聚焦!")
    await asyncio.gather(
        execute_rhythm_behavior('drummers', 'headbang', 128, 1.0, 22),
        execute_rhythm_behavior('vocals', 'wave', 128, 1.0, 22, phase_wave=True),
        execute_rhythm_behavior('spotlight', 'strobe_center', 256, 1.0, 22),
    )
    
    # ========== 第4段：Outro (52-60s) ==========
    print("\n🌙 [00:52] Outro - 渐入尾声...")
    print("    全体: 缓慢扫射 → 归零")
    await asyncio.gather(
        execute_rhythm_behavior('drummers', 'sweep', 64, 0.4, 8),
        execute_rhythm_behavior('vocals', 'sweep', 64, 0.5, 8, phase_wave=True),
        execute_rhythm_behavior('spotlight', 'slow_circle', 32, 0.3, 8),
    )
    
    # 结束
    print("\n🛑 表演结束，云台归位...")
    await stop_all_gimbals()
    
    print("\n✨✨✨ V.mp3 舞蹈表演完成！✨✨✨")
    
    # 显示最终状态
    status = await get_dance_status()
    print("\n" + status)
    
    await disconnect_dance_floor()

if __name__ == '__main__':
    asyncio.run(v_dance_performance())
