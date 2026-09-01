# 💡 赛博灯泡 / Cyber Bulb

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/VincentZyuApps/cyber-bulb)
[![Gitee](https://img.shields.io/badge/Gitee-C71D23?style=for-the-badge&logo=gitee&logoColor=white)](https://gitee.com/vincent-zyu/cyber-light-bulb)

[![PyPI 包版本 / Package Version](https://img.shields.io/pypi/v/cyber-bulb?style=for-the-badge&logo=pypi&logoColor=white&label=Package%20Version&labelColor=3775A9&color=FFD43B)](https://pypi.org/project/cyber-bulb/)
[![支持的 Python 版本 / Supported Python Versions](https://img.shields.io/pypi/pyversions/cyber-bulb?style=for-the-badge&logo=python&logoColor=white&labelColor=3775A9&color=FFD43B)](https://pypi.org/project/cyber-bulb/)
[![PyQt5 版本 / PyQt5 Version](https://img.shields.io/badge/PyQt5-5.15.11-41CD52?style=for-the-badge&logo=qt&logoColor=white&labelColor=3775A9)](https://pypi.org/project/PyQt5/)

一个使用 PyQt5 编写的七段数码管时钟，支持三种外观、响应式控制和多种段级动画。 / A PyQt5 seven-segment clock with three styles, responsive controls, and segment-level animations.

> 本仓库同时也是使用 uv 管理 Python 项目并通过 GitHub Actions 发布至 PyPI 的参考模板。 / This repository is also a reference template for managing a Python project with uv and publishing it to PyPI through GitHub Actions.
## 🖼️ 运行预览 / Preview
![赛博灯泡动画演示 / Cyber Bulb animated demo](https://raw.githubusercontent.com/VincentZyuApps/cyber-bulb/main/docs/images/preview/preview.demo.gif)
### ☀️ 白天模式 / Light Mode
![赛博灯泡白天模式 / Cyber Bulb light mode](https://raw.githubusercontent.com/VincentZyuApps/cyber-bulb/main/docs/images/preview/preview.light.png)
### 🌙 夜晚模式 / Dark Mode
![赛博灯泡夜晚模式 / Cyber Bulb dark mode](https://raw.githubusercontent.com/VincentZyuApps/cyber-bulb/main/docs/images/preview/preview.dark.png)
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
## ⚙️ 运行参数 / Runtime Options
| 参数 / Option | 默认值 / Default | 说明 / Description |
|:---|:---|:---|
| `--theme {system,light,dark}` | `system` | 设置初始主题模式。 / Set the initial theme mode. |
| `--segment-style {classic,rounded,outline}` | `classic` | 设置数码管外观。 / Set the segment style. |
| `--digit-animation {none,afterglow,pulse,scan,wave,glitch}` | `afterglow` | 设置数字动画。 / Set the digit animation. |
| `--colon-animation {none,blink,pulse,double,alternate}` | `blink` | 设置冒号动画。 / Set the colon animation. |
| `--no-theme-transition`, `--no-style-transition` | 关闭 / Off | 分别禁用主题或外观渐变。 / Disable theme or style transitions. |
| `--width`, `--height <像素 / pixels>` | `777 × 666` | 设置初始窗口尺寸。 / Set the initial window dimensions. |
| `-V`, `--V`, `--version`<br>`-h`, `--help` | 无 / None | 显示版本或命令帮助。 / Show version or command help. |
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
