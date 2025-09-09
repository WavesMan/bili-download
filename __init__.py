"""
B站视频下载器 - 一个功能强大的B站视频下载工具
支持最高清晰度下载、自动合并和多种格式支持
"""

__version__ = "1.0.0"
__author__ = "B站视频下载器"
__description__ = "一个功能强大的B站视频下载工具，支持最高清晰度下载和自动合并"

from .main import main
from .config.config_manager import init_config, get_config, set_config
from .modules.login_manager import init_login, get_session
from .modules.video_info import get_video_download_info, get_video_info, get_video_stream_url
from .modules.stream_downloader import download_video_stream, download_file, download_with_retry
from .modules.ffmpeg_integration import merge_video_audio, check_ffmpeg_available
from .utils.common_utils import sanitize_filename, parse_bvid, parse_av_id, setup_logging

__all__ = [
    'main',
    'init_config', 'get_config', 'set_config',
    'init_login', 'get_session',
    'get_video_download_info', 'get_video_info', 'get_video_stream_url',
    'download_video_stream', 'download_file', 'download_with_retry',
    'merge_video_audio', 'check_ffmpeg_available',
    'sanitize_filename', 'parse_bvid', 'parse_av_id', 'setup_logging'
]
