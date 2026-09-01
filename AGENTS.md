# Cyber Bulb Agent Instructions / 赛博灯泡代理说明

## Communication / 沟通

- 默认使用中文，表达直接、清晰、可验证。 / Use Chinese by default and keep communication direct, clear, and verifiable.
- 用户未明确授权时，不得 commit、push、打 tag 或发布。 / Do not commit, push, tag, or release without explicit user authorization.

## Architecture / 架构

- `app.py` 仅负责 QApplication 生命周期与启动。 / Keep QApplication lifecycle and startup in `app.py`.
- `cli.py` 负责仅对当前进程有效的运行参数。 / Keep process-only runtime options in `cli.py`.
- `theme.py` 负责主题数据、颜色插值和对比文字色。 / Keep theme data, color blending, and contrasting text colors in `theme.py`.
- `window.py` 负责窗口控件、时钟更新和主题动画。 / Keep widgets, clock updates, and theme animation in `window.py`.
- `titlebar.py` 负责 Windows 原生标题栏集成。 / Keep Windows native title-bar integration in `titlebar.py`.
- `src/cyber_bulb` 中普通源码文件名只能使用一个英文单词，不使用下划线；Python 固定的双下划线模块除外。 / Use one English word without underscores for regular source filenames; Python dunder modules are exempt.
- 保持 `cyber-bulb` 与 `python -m cyber_bulb` 正式入口可用。 / Keep the `cyber-bulb` and `python -m cyber_bulb` launchers working.

## Runtime Behavior / 运行行为

- 应用运行时不得向本地磁盘或注册表写入配置、缓存、日志、偏好或状态。 / The app must not persist configuration, cache, logs, preferences, or state to local disk or the registry.
- 所有可调行为仅由本次进程的 CLI 参数或当前 UI 操作控制。 / Control all adjustable behavior only through process-local CLI arguments or current UI actions.
- 主题切换默认使用 350ms 渐变。 / Theme changes use a 350 ms transition by default.
- 主题按钮按跟随系统、白天、黑夜循环，按钮文案必须为 emoji、中文、英文的顺序。 / Cycle System, Light, and Dark modes with emoji, Chinese, then English button labels.
- `--no-animation` 仅禁用当前进程的渐变。 / `--no-animation` disables transitions for the current process only.
- `--theme {system,light,dark}` 设置初始模式，默认跟随系统且仅对当前进程有效。 / `--theme {system,light,dark}` selects the process-only initial mode and defaults to System.
- 禁止通过 QSettings、注册表、配置文件或环境变量持久化运行选项。 / Never persist runtime options via QSettings, registry, config files, or environment variables.
- 保留原生标题栏及其拖动、缩放、最大化和 Snap Layout 行为。 / Preserve native title-bar dragging, resizing, maximizing, and Snap Layout.
- Windows 使用 DWM 同步标题栏颜色；不支持的平台必须安全降级。 / Use DWM for title-bar colors on Windows and safely no-op elsewhere.

## Testing / 测试

- 支持 Python 3.10 至 3.14。 / Support Python 3.10 through 3.14.
- 依赖和测试使用 uv locked 流程。 / Use uv locked workflows for dependencies and tests.
- 运行 `uv lock --check`。 / Run `uv lock --check`.
- 运行 `uv run --locked --python <version> python -m unittest discover -s tests -v`。 / Run tests with the locked command shown.
- GUI 自动测试使用 `QT_QPA_PLATFORM=offscreen`，Windows 行为另做可见验证。 / Use offscreen GUI tests and separately verify visible Windows behavior.
- 构建后运行 `uvx twine check dist/*`。 / Run `uvx twine check dist/*` after building.

## Documentation and Release / 文档与发布

- `README.md` 不超过 50 行，每行中文在前、英文在后，并保留 badges、双预览图和 uv 资源。 / Keep README within 50 lines, Chinese first per line, with badges, both previews, and uv resources.
- 版本号保持静态，并在修改依赖后同步 `uv.lock`。 / Keep a static version and update `uv.lock` after dependency changes.
- 仅提交信息中的 `[publish-pypi]` 或 `[publishpypi]` 可触发发布。 / Only `[publish-pypi]` or `[publishpypi]` in a commit message may trigger publishing.
- PyPI 发布使用 GitHub OIDC Trusted Publishing，禁止保存 PyPI Token。 / Publish through GitHub OIDC Trusted Publishing; do not store a PyPI token.
- 项目临时文件放在 `E:\tmp\codex\cyber-bulb-*`，完成后清理。 / Put project temporary files under `E:\tmp\codex\cyber-bulb-*` and clean them afterward.
