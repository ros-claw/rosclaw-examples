# 🚀 快速开始指南

## 一句话复现

```bash
git clone https://github.com/ros-claw/rosclaw-examples.git
cd rosclaw-examples/gimbal-dance-demo

# 安装依赖
uv pip install -r requirements.txt

# 1️⃣ 仿真模式（无需硬件）
python examples/demo_10gimbals_simulation.py

# 2️⃣ 真机模式（6台GCU云台）
python examples/demo_6gimbals_hardware.py
```

---

## 📁 项目结构

```
gimbal-dance-demo/
├── examples/
│   ├── demo_10gimbals_simulation.py   # 10台仿真演示
│   └── demo_6gimbals_hardware.py      # 6台真机演示
├── src/
│   ├── dance_mcp_server.py       # MCP 服务器
│   ├── rhythm_engine.py          # 50Hz 节奏引擎
│   ├── music_analyzer.py         # 音乐分析器
│   └── gcu_gimbal_control.py     # GCU 云台控制协议
├── config/
│   └── gimbal_config.yaml        # 6台云台配置
├── music/
│   ├── V.mp3                     # 演示音乐 (128 BPM)
│   └── The Rebel Path.mp3        # 赛博朋克风格
├── requirements.txt              # Python依赖
└── README.md                     # 完整文档
```

---

## 🔧 硬件准备（真机模式）

| 物品 | 数量 | 备注 |
|------|------|------|
| GCU云台 | 6台 | GM6020/GM3510 |
| USB转串口 | 6个 | CH340/CH341/CP2102 |
| USB Hub | 1个 | 带独立供电，3A+ |
| 激光笔 | 6个 | 可选，增强视觉效果 |

### 接线图

```
Jetson/PC  ←USB Hub(独立供电)→  [USB0-5]  ←→  [云台1-6]
```

### 查找串口

```bash
# Linux
ls -la /dev/ttyUSB* /dev/ttyCH341*

# 临时权限
sudo chmod 666 /dev/ttyUSB*

# 永久权限
sudo usermod -aG dialout $USER
```

### 配置串口

编辑 `config/gimbal_config.yaml`：

```yaml
gimbals:
  - id: 1
    port: /dev/ttyUSB0    # 根据实际修改
    group: drummers
```

---

## 🎵 音乐编舞原理

```
音乐分析 → BPM/段落/情感 → LLM编舞 → 50Hz波形 → 云台执行
```

| 段落 | 行为 | 强度 |
|------|------|------|
| Intro | slow_circle, freeze | 0.2-0.4 |
| Buildup | heartbeat, wave | 0.5-0.7 |
| Drop | headbang, strobe_center | 0.9-1.0 |
| Outro | sweep, slow_circle | 0.3-0.5 |

---

## 🎭 律动行为库

| 行为 | 描述 | 适合场景 |
|------|------|---------|
| headbang | 甩头 - Tilt方波 | 鼓点/Drop |
| wave | 波浪 - Pan正弦+相位 | 海浪效果 |
| sweep | 扫射 - Pan正弦 | 副歌流畅 |
| heartbeat | 双脉冲 - Tilt | Snare强调 |
| figure8 | 8字形 - 双轴 | 追光器 |
| strobe_center | 频闪→归零 | Drop爆发 |
| slow_circle | 慢速圆形 | 前奏氛围 |
| freeze | 冻结 | 静止戏剧 |

---

## 🐛 故障排除

| 问题 | 解决 |
|------|------|
| 串口无法打开 | `sudo chmod 666 /dev/ttyUSB*` |
| 运动卡顿 | 检查USB Hub供电，需3A+ |
| 动作不同步 | 确认 `tick_hz=50` 达标 |
| 音乐分析失败 | `uv pip install librosa numpy` |

---

## 📚 更多信息

- 完整文档: [README.md](./README.md)
- ROSClaw: https://github.com/ros-claw