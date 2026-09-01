# Cyber Bulb Agent Instructions / 赛博灯泡代理说明

## Communication / 沟通

- 默认使用中文，表达直接、清晰、可验证。 / Use Chinese by default and keep communication direct, clear, and verifiable.
- 用户未明确授权时，不得 commit、push、打 tag 或发布。 / Do not commit, push, tag, or release without explicit user authorization.

## Architecture / 架构

- `app.py` 仅负责 QApplication 生命周期与启动。 / Keep QApplication lifecycle and startup in `app.py`.
- `cli.py` 负责仅对当前进程有效的运行参数。 / Keep process-only runtime options in `cli.py`.
- `theme.py` 负责主题数据、颜色插值和对比文字色。 / Keep theme data, color blending, and contrasting text colors in `theme.py`.
- `effects.py` 负责确定性的数字与冒号动画曲线。 / Keep deterministic digit and colon animation curves in `effects.py`.
- `style.py` 负责三种数码管与冒号几何；`labels.py` 负责响应式双语文案。 / Keep three segment/colon geometries in `style.py` and responsive bilingual labels in `labels.py`.
- `digit.py` 与 `display.py` 负责自绘七段单元和组合显示器。 / Keep custom seven-segment cells and displays in `digit.py` and `display.py`.
- `window.py` 负责窗口控件、时钟触发和主题动画。 / Keep widgets, clock triggers, and theme animation in `window.py`.
- `titlebar.py` 负责 Windows 原生标题栏集成。 / Keep Windows native title-bar integration in `titlebar.py`.
- `src/cyber_bulb` 中普通源码文件名只能使用一个英文单词，不使用下划线；Python 固定的双下划线模块除外。 / Use one English word without underscores for regular source filenames; Python dunder modules are exempt.
- 保持 `cyber-bulb` 与 `python -m cyber_bulb` 正式入口可用。 / Keep the `cyber-bulb` and `python -m cyber_bulb` launchers working.

## Runtime Behavior / 运行行为

- 应用运行时不得向本地磁盘或注册表写入配置、缓存、日志、偏好或状态。 / The app must not persist configuration, cache, logs, preferences, or state to local disk or the registry.
- 所有可调行为仅由本次进程的 CLI 参数或当前 UI 操作控制。 / Control all adjustable behavior only through process-local CLI arguments or current UI actions.
- 主题切换默认使用 350ms 渐变。 / Theme changes use a 350 ms transition by default.
- 黑白按钮按跟随系统、白天、黑夜循环，按钮文案必须为 emoji、中文、英文的顺序。 / Cycle System, Light, and Dark modes with emoji, Chinese, then English button labels.
- `--no-theme-transition` 与 `--no-style-transition` 分别禁用当前进程的主题或外观渐变；不支持旧参数。 / The two transition flags only affect the current process; old flags are unsupported.
- `--theme {system,light,dark}` 设置初始模式，默认跟随系统且仅对当前进程有效。 / `--theme {system,light,dark}` selects the process-only initial mode and defaults to System.
- 数字动画默认 `afterglow`，冒号动画默认 `blink`，均可通过 CLI 和 UI 循环切换。 / Digit animation defaults to `afterglow`; colon animation defaults to `blink`; both are selectable through CLI and UI.
- 数码管外观按 `classic`、`rounded`、`outline` 循环，默认 `classic`，切换使用 180ms 淡变。 / Cycle three segment styles from `classic`, with a 180 ms transition.
- 底部按钮顺序为晶体管、动画、冒号、黑白，并按 emoji、中文 key、中文 key/value、完整双语四档响应。 / Order controls as Segment, Animation, Colon, Light-Dark with four responsive label tiers.
- 秒变化触发右冒号，分钟变化触发左冒号，整分时两者同时触发。 / Seconds trigger the right colon, minutes trigger the left colon, and both trigger on minute rollover.
- `--width` 与 `--height` 设置正整数初始尺寸，默认 `777 × 666`。 / `--width` and `--height` set positive initial dimensions, defaulting to `777 × 666`.
- 禁止通过 QSettings、注册表、配置文件或环境变量持久化运行选项。 / Never persist runtime options via QSettings, registry, config files, or environment variables.
- 保留原生标题栏及其拖动、缩放、最大化和 Snap Layout 行为。 / Preserve native title-bar dragging, resizing, maximizing, and Snap Layout.
- Windows 使用 DWM 同步标题栏颜色；不支持的平台必须安全降级。 / Use DWM for title-bar colors on Windows and safely no-op elsewhere.

## Testing / 测试

- 支持 Python 3.10 至 3.14。 / Support Python 3.10 through 3.14.
- 依赖和测试使用 uv locked 流程。 / Use uv locked workflows for dependencies and tests.
- 运行 `uv lock --check`。 / Run `uv lock --check`.
- 运行 `uv run --locked --python <version> python -m unittest discover -s tests -v`。 / Run tests with the locked command shown.
- GUI 自动测试使用 `QT_QPA_PLATFORM=offscreen`，Windows 行为另做可见验证。 / Use offscreen GUI tests and separately verify visible Windows behavior.
- 故障动画必须确定性可测，并在结束或中断后收敛到正确数字。 / Glitch animation must be deterministic and settle to the correct digits after completion or interruption.
- 构建后运行 `uvx twine check dist/*`。 / Run `uvx twine check dist/*` after building.

## Documentation and Release / 文档与发布

- `README.md` 不超过 50 行，每行中文在前、英文在后，并保留 badges、双预览图和 uv 资源。 / Keep README within 50 lines, Chinese first per line, with badges, both previews, and uv resources.
- 版本号保持静态，并在修改依赖后同步 `uv.lock`。 / Keep a static version and update `uv.lock` after dependency changes.
- 仅提交信息中的 `[publish-pypi]` 或 `[publishpypi]` 可触发发布。 / Only `[publish-pypi]` or `[publishpypi]` in a commit message may trigger publishing.
- PyPI 发布使用 GitHub OIDC Trusted Publishing，禁止保存 PyPI Token。 / Publish through GitHub OIDC Trusted Publishing; do not store a PyPI token.
- 项目临时文件放在 `E:\tmp\codex\cyber-bulb-*`，完成后清理。 / Put project temporary files under `E:\tmp\codex\cyber-bulb-*` and clean them afterward.
