# rosclaw-examples

ROSClaw 具身智能操作系统 — 官方示例集

## 示例列表

| Demo | 描述 | 硬件 | 复杂度 | 状态 |
|------|------|------|--------|------|
| [gimbal-dance-demo](./gimbal-dance-demo/) | 6台云台交响舞队，LLM听歌实时编舞 | 6× GCU Gimbal | ⭐⭐⭐ | ✅ 已验证 |

> 更多示例持续添加中...

## 快速体验

```bash
git clone https://github.com/ros-claw/rosclaw-examples.git
cd rosclaw-examples/gimbal-dance-demo

# 仿真模式（无需硬件，立即体验）
python examples/demo_10gimbals_simulation.py

# 真机模式（6台GCU云台）
python examples/demo_6gimbals_hardware.py
```

## 什么是 ROSClaw？

ROSClaw 是具身智能操作系统，通过 MCP 协议将大语言模型连接到真实机器人硬件。

- **大脑层**：LLM 理解任务、做决策、生成高层指令
- **小脑层**：本地实时控制器执行 50Hz+ 高频控制
- **解耦设计**：LLM 从不直接触碰硬件，通过语义指令交互

### 官方 MCP 服务器

| 项目 | 描述 | 硬件 |
|------|------|------|
| [rosclaw-g1-dds-mcp](https://github.com/ros-claw/rosclaw-g1-dds-mcp) | 宇树 G1 人形机器人 | Unitree G1 |
| [rosclaw-ur-ros2-mcp](https://github.com/ros-claw/rosclaw-ur-ros2-mcp) | UR5 机械臂 | Universal Robots UR5 |
| [rosclaw-gimbal-mcp](https://github.com/ros-claw/rosclaw-gimbal-mcp) | GCU 云台控制 | GCU Gimbals |
| [rosclaw-vision-mcp](https://github.com/ros-claw/rosclaw-vision-mcp) | RealSense 视觉 | Intel RealSense |

## 贡献

欢迎提交 PR！添加新示例时请遵循：

1. 独立的子目录，包含 README.md
2. 清晰的硬件需求说明
3. 仿真模式（如果可能）
4. 依赖清单（requirements.txt 或 pyproject.toml）

## 许可证

MIT — See [LICENSE](./LICENSE)