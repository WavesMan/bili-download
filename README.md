# B站视频下载器 (bili-downloader)

[![PyPI version](https://img.shields.io/pypi/v/bili-downloader.svg)](https://pypi.org/project/bili-downloader/)
[![Python versions](https://img.shields.io/pypi/pyversions/bili-downloader.svg)](https://pypi.org/project/bili-downloader/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个功能强大的B站视频下载工具，支持最高清晰度下载和自动合并。

## ✨ 功能特性

- 🎯 **智能清晰度选择**: 自动获取账号权限内的最高清晰度视频
- 🔐 **多种登录方式**: 支持二维码登录和Cookie登录
- 📦 **自动合并**: 支持DASH格式视频的自动音视频合并
- 🚀 **多线程下载**: 支持多线程并发下载，提高下载速度
- 📁 **智能文件管理**: 按BV号自动组织文件结构
- 📊 **元数据保存**: 自动保存视频信息和下载元数据
- ⚡ **断点续传**: 支持下载中断后继续下载

## 📦 安装

### 通过 pip 安装

```bash
pip install bili-downloader
```

### 从源码安装

```bash
git clone https://github.com/your-username/bili-downloader.git
cd bili-downloader
pip install -e .
```

## 🚀 快速开始

### 基本使用

```bash
# 下载单个视频
bili-dl BV1A6aRz4EBU

# 指定输出目录
bili-dl BV1A6aRz4EBU --output ./my_videos

# 指定清晰度 (80=1080P, 112=1080P+, 120=4K)
bili-dl BV1A6aRz4EBU --quality 112

# 强制重新登录
bili-dl BV1A6aRz4EBU --login

# 禁用自动合并
bili-dl BV1A6aRz4EBU --no-merge
```

### 配置说明

首次运行会自动创建配置文件 `~/.bili-downloader/config.json`，您可以编辑此文件来自定义设置：

```json
{
  "user": {
    "cookies": {},
    "session_data": {}
  },
  "download": {
    "output_dir": "downloads",
    "timeout": 30,
    "retry_times": 3,
    "chunk_size": 8192
  },
  "ffmpeg": {
    "auto_merge": true,
    "ffmpeg_path": "ffmpeg"
  },
  "debug": {
    "enable_logging": false,
    "log_level": "INFO"
  }
}
```

## 🔧 高级用法

### 作为Python模块使用

```python
from bili_downloader import download_video, init_config, init_login

# 初始化配置和登录
init_config()
init_login()

# 下载视频
success = download_video("BV1A6aRz4EBU", output_dir="./videos")
if success:
    print("下载成功！")
```

### 批量下载

```python
from bili_downloader import download_video

video_list = [
    "BV1A6aRz4EBU",
    "BV1B6bRz5FCV", 
    "BV1C7cSx6GDW"
]

for bvid in video_list:
    download_video(bvid)
```

## 📁 文件结构

下载完成后，文件会按以下结构组织：

```
downloads/
└── BV1A6aRz4EBU/
    ├── 视频标题_video.m4s      # 视频流文件
    ├── 视频标题_audio.m4s      # 音频流文件
    ├── 视频标题.mp4           # 最终合并的视频文件
    └── metadata.json          # 视频元数据信息
```

## ⚙️ 依赖要求

- Python 3.7+
- requests >= 2.28.0
- qrcode >= 7.3.1
- Pillow >= 9.3.0
- ffmpeg (用于视频合并，可选但推荐)

## 🔍 常见问题

### Q: 如何安装 ffmpeg？

**Windows:**
1. 下载 ffmpeg: https://ffmpeg.org/download.html
2. 解压并添加 bin 目录到系统 PATH

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install ffmpeg
```

### Q: 登录失败怎么办？

尝试使用 `--login` 参数强制重新登录：
```bash
bili-dl BV1A6aRz4EBU --login
```

### Q: 下载速度慢怎么办？

可以尝试：
1. 检查网络连接
2. 使用更好的网络环境
3. 调整配置中的超时和重试参数

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## ⚠️ 免责声明

本项目仅用于学习和研究目的，请勿用于商业用途。下载的视频请遵守相关法律法规和B站用户协议。

## 📞 支持

如果您遇到问题或有建议，请：
1. 查看 [常见问题](#常见问题)
2. 提交 [Issue](https://github.com/your-username/bili-downloader/issues)
3. 查看 [文档](docs/)

---

**享受下载的乐趣！** 🎉
