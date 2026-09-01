# 💡 赛博灯泡 / Cyber Bulb

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/VincentZyuApps/cyber-bulb)
[![Gitee](https://img.shields.io/badge/Gitee-C71D23?style=for-the-badge&logo=gitee&logoColor=white)](https://gitee.com/vincent-zyu/cyber-light-bulb)

[![PyPI 包版本 / Package Version](https://img.shields.io/pypi/v/cyber-bulb?style=for-the-badge&logo=pypi&logoColor=white&label=Package%20Version&color=3775A9)](https://pypi.org/project/cyber-bulb/)
[![支持的 Python 版本 / Supported Python Versions](https://img.shields.io/pypi/pyversions/cyber-bulb?style=for-the-badge&logo=python&logoColor=white)](https://pypi.org/project/cyber-bulb/)

一个使用 PyQt5 编写的数字时钟，支持白天与夜晚模式切换。 / A PyQt5 digital clock with light and dark modes.

## 🖼️ 运行预览 / Preview

| 🌙 夜晚模式 / Dark Mode | ☀️ 白天模式 / Light Mode |
|:---:|:---:|
| ![赛博灯泡夜晚模式 / Cyber Bulb dark mode](https://raw.githubusercontent.com/VincentZyuApps/cyber-bulb/main/docs/images/preview/preview.dark.png) | ![赛博灯泡白天模式 / Cyber Bulb light mode](https://raw.githubusercontent.com/VincentZyuApps/cyber-bulb/main/docs/images/preview/preview.light.png) |

## 📦 从 PyPI 安装 / Install from PyPI

```bash
uv venv
uv pip install cyber-bulb
uv run cyber-bulb
```

## 🛠️ 从源码运行 / Run from Source

```bash
uv sync
uv run cyber-bulb
```

也可以运行兼容入口 `uv run python bulb.py`。 / You can also use the compatible launcher: `uv run python bulb.py`.

> ### 📚 uv 官方安装文档 / Official uv Installation Guide
>
> uv还是太好用了，已经不用pyenv了，推荐使用。 / uv works so well that I no longer use pyenv. Highly recommended.
>
> https://docs.astral.sh/uv/getting-started/installation/
>
> ### ⚡ uv 自动安装并换源 / Automated uv Installation and Mirror Setup
>
> 一键安装uv并配置镜像源，非常推荐。 / Install uv and configure a package mirror in one step. Highly recommended.
>
> https://gitee.com/wangnov/uv-custom/releases
