```
2026-02-26T12:59:01.123Z [INFO] Lumen M5 Boot Complete | CPU: Exynos850 1.4GHz | RAM: 4GB/6GB used 32%
2026-02-26T12:59:02.456Z [STATS] Battery: 87% | Temp: 38.2C | Drain: 1.2%/min | FastCharge: disabled
2026-02-26T12:59:05.789Z [DEBUG] Phosh Shell Loaded | FPS: 58/60 | Memory: 245MB | GPU: Mali-G52
2026-02-26T12:59:10.012Z [WARNING] IMU Sensor Drift | AccelX: 0.02g | GyroZ: -0.1deg/s | Calib: needed
2026-02-26T13:00:01.345Z [STATS] Kernel Uptime: 60s | LoadAvg: 0.12/0.08/0.05 | Procs: 128
2026-02-26T13:00:15.678Z [INFO] Audio Driver Init | SampleRate: 48000Hz | Latency: 23ms | Buffer: 1024
2026-02-26T13:01:22.901Z [ERROR] Termux Cross-Compile | ARMv7 Drop: March2026 | Fallback: aarch64-ilp32
2026-02-26T13:02:30.234Z [STATS] GeometryDash FPS: 120/120 | BatteryDrop: 0.8% | ColdShowerBoost: +15% alert
```

statistics_sample_log.log is a sample log file for capturing runtime statistics in Lumen OS, useful for debugging kernel, battery, and Phosh performance on your Galaxy A05s or M5 builds. Place it in /data/misc/lumen/logs/ or your Termux project root for testing log parsing with tools like lnav.
