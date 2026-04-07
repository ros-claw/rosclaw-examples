# Gimbal Dance Demo — 云台交响编舞

> **ROSClaw 杀手级 Demo：多云台音乐可视化表演，LLM 现场听歌编舞指挥**

## 一句话复现

```bash
cd gimbal-dance-demo

# 1️⃣ 仿真模式（无需硬件）
python examples/demo_10gimbals_simulation.py

# 2️⃣ 真机模式（6台GCU云台）
python examples/demo_6gimbals_hardware.py
```

## 项目结构

```
gimbal-dance-demo/
├── src/                          # 核心引擎（不要直接运行）
│   ├── dance_mcp_server.py       # MCP 服务器接口
│   ├── rhythm_engine.py          # 50Hz 节奏引擎（小脑）
│   └── music_analyzer.py         # 音乐分析器（耳朵）
├── examples/                     # 可直接运行的示例
│   ├── demo_10gimbals_simulation.py   # 10台仿真演示
│   └── demo_6gimbals_hardware.py      # 6台真机演示
├── config/
│   └── gimbal_config.yaml        # 6台云台串口配置
├── music/                        # 音乐素材
│   ├── V.mp3                     # 演示用音乐（128 BPM）
│   └── The Rebel Path.mp3        # 赛博朋克风格
├── visualization_server.py       # Web 可视化服务器
├── visualization.html            # 可视化面板
└── README.md                     # 本文件
```

## 系统架构：大脑-小脑解耦

```
用户 → OpenClaw (LLM) ─────────────────────────────────── 大脑层
          │
          ├─ analyze_music_file("V.mp3")
          │     → BPM=128, Drop@30s, Vibe=Energetic EDM
          │
          ├─ choreograph_dance(music_json)
          │     → 编舞剧本 JSON
          │
          └─ run_choreography(script)  ── 并发下发 ──→ 小脑层
                                               │
              ┌───────────────────────────────┼────────────────────────┐
              ▼                               ▼                        ▼
       🥁 Drummers (1-3)            🎤 Vocals (4-6)          ✨ Spotlight (7+)
       headbang @ BPM               wave + phase              strobe_center
       50Hz serial → GCU            50Hz serial → GCU         50Hz serial → GCU
```

**核心设计原则**：
- LLM 只下发语义指令（`headbang @ 128 BPM`），从不触碰 50Hz 原始角度流
- Rhythm Engine（小脑）用正弦波/方波 + 时间戳，以 50Hz 高频写串口
- 音乐分析和编舞完全解耦，换歌 = 重新分析 + 自动生成新编舞

## 快速开始

### 1. 安装依赖

```bash
cd gimbal-dance-demo

# 创建虚拟环境
uv venv --python 3.10
source .venv/bin/activate

# 安装核心依赖
uv pip install pyserial pyyaml

# 可选：安装音乐分析依赖（用于真实音频分析）
uv pip install librosa numpy
```

### 2. 仿真模式（无需硬件）

```bash
python examples/demo_10gimbals_simulation.py
```

你会看到终端输出的 ASCII 可视化：
```
[G01] PAN [████░░░░░░]  +45.0°  TILT [███░░░░░░░]  +30.0°
[G02] PAN [░░░████░░░]  -30.0°  TILT [░░░░░░████]  -45.0°
...
```

### 3. 真机模式（6台 GCU 云台）

#### 硬件准备

1. **6台 GCU 云台**（推荐 GM6020 或 GM3510）
2. **6个 USB 转串口模块**（CH340/CH341/CP2102）
3. **USB Hub**（带独立供电，推荐 3A+）
4. **激光笔**（可选，用于可视化效果）

#### 接线

```
Jetson/PC  ←USB Hub→  [USB0-5]  ←→  [云台1-6]
                        ↓
                     独立供电 5V 3A+
```

#### 串口配置

编辑 `config/gimbal_config.yaml`：

```yaml
gimbals:
  - id: 1
    port: /dev/ttyUSB0    # Linux 串口
    group: left
    position: { x: -2.5, y: 0.0 }
  
  - id: 2
    port: /dev/ttyUSB1
    group: left
    position: { x: -1.5, y: 0.0 }
  
  # ... 以此类推
```

查找串口：
```bash
ls -la /dev/ttyUSB* /dev/ttyCH341*
```

#### 权限设置

```bash
# 临时权限
sudo chmod 666 /dev/ttyUSB*

# 永久权限（推荐）
sudo usermod -aG dialout $USER
# 重新登录后生效
```

#### 运行

```bash
python examples/demo_6gimbals_hardware.py
```

## 律动行为库

| 行为 | 轴 | 波形 | 适合场景 |
|------|---|------|---------|
| `headbang` | Tilt | 方波 | 鼓点/节拍强烈段落 |
| `sweep` | Pan | 正弦 | 副歌，流畅扫射 |
| `wave` | Pan+phase | 正弦+相位 | 多云台海浪效果 |
| `heartbeat` | Tilt | 双脉冲 | 强调音/snare hit |
| `figure8` | Pan+Tilt | Lissajous | 追光器，8字形 |
| `strobe_center` | Both | 随机抖动→归零 | Drop 爆发瞬间 |
| `slow_circle` | Both | 慢速正弦 | 前奏/间奏氛围 |
| `freeze` | - | 归零保持 | 静止戏剧效果 |

`phase_wave=True` 时，组内每台云台相位依次偏移 `i/n × 2π`，产生涟漪波浪视觉。

## 音乐段落映射

| 段落 | 特征 | 推荐行为 | 强度 |
|------|------|---------|------|
| Intro | 低能量，渐进 | `slow_circle`, `freeze` | 0.2-0.4 |
| Buildup | 能量上升，紧张 | `heartbeat`, `wave` | 0.5-0.7 |
| Drop | 爆发，高潮 | `headbang`, `strobe_center` | 0.9-1.0 |
| Outro | 回落，结束 | `sweep`, `slow_circle` | 0.3-0.5 |

## 进阶：自定义编舞

```python
from src.rhythm_engine import RhythmEngine, BehaviorConfig

engine = RhythmEngine()

# 连接云台
engine.add_gimbal(1, "/dev/ttyUSB0")
engine.add_gimbal(2, "/dev/ttyUSB1")

# 编舞：双云台波浪
cfg = BehaviorConfig(
    behavior="wave",
    bpm=128,
    intensity=0.8,
    phase_offset=0,
    duration=10.0
)

engine.execute_group([1, 2], "wave", 128, 0.8, 10, phase_wave=True)
```

## 可视化

启动 Web 可视化服务器：

```bash
python visualization_server.py
# 访问 http://localhost:8080
```

## 故障排除

| 问题 | 可能原因 | 解决 |
|------|---------|------|
| 串口无法打开 | 权限不足 | `sudo chmod 666 /dev/ttyUSB*` |
| 云台不响应 | 波特率错误 | 确认 115200 |
| 运动卡顿 | USB Hub 供电不足 | 使用带独立供电的 Hub |
| 动作不同步 | 延迟累积 | 检查 `tick_hz=50` 是否达标 |
| 音乐分析失败 | librosa 未安装 | `uv pip install librosa` |

## 扩展：更多云台

当前配置默认 6 台。要扩展到 10 台：

1. 修改 `config/gimbal_config.yaml` 添加更多云台
2. 更新分组逻辑（drummers/vocals/spotlight）
3. 在示例脚本中调整组大小

## 依赖

**必需：**
- Python 3.10+
- pyserial >= 3.5
- pyyaml >= 6.0

**可选（音乐分析）：**
- librosa >= 0.10.0
- numpy >= 1.24

## 许可证

MIT — Part of [ROSClaw Examples](https://github.com/ros-claw/rosclaw-examples)

---

*Made with 💃 by ROSClaw Team*