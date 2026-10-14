# 文件索引

本文件是 short-drama-full-pipeline 的文件索引。短剧 Skill 不依赖外部 API。

## 使用顺序

0. `chain-audit.md`：本地链路锁、template_source 锁、断点审计、引用审计。
1. `production-data-center.md`：生产数据中心、视觉模式锁、风格影调锁、对白表、视频任务映射、资产池、提示词映射。
2. `style-tone-presets.md`：风格配置与影调配置预设库，第二层弹窗使用；必须在视觉模式选择后、资产 / 视频 / QC 前读取。
3. `story-structure.md`：题材、爽点、人物关系、分集节奏。
4. `script-format.md`：剧本格式、对白、动作、场次、角色三庭五眼数据链。
5. `asset-pipeline.md`：角色、场景、道具资产拆解；双模式角色资产；场景方向单图；道具单图；资产提示词完整继承风格影调锁。
6. `animation-character-converter.md`：真人版本角色描述提示词转 3D 动画 CG 角色资产提示词。
7. `storyboard-pipeline.md`：空间真值、场景方向锁、舞台定位图弹窗、黑白分镜图弹窗、分镜表、镜头节奏。
8. `video-prompt-pipeline.md`：视频提示词、声音分工、生成约束、场景方向锁、100×100 自然语言空间描述、VIDEO_DISPATCH_PACKAGE 完整展示风格影调锁。
9. `actor-performance-voice-integration.md`：award-winning-performance-prompt-v1-1融合规则、中文片段镜号格式、角色音色参考、完整前置快照 + 差异补丁 + 当前合成版机制。
10. `post-production-pipeline.md`：声音资产、剪辑合成、混音层级、成片检查。
11. `qc-checklist.md`：自检、返工、补齐；视觉模式、风格影调锁、3D 动画 CG、场景方向单图、道具单图、角色音色、完整前置快照、角色造型变体与场景状态变体专项 QC。

## 原则

如果用户要求锁定本地链路、验收并继续、断点恢复或防止线上通用链路介入，必须先读取 `chain-audit.md`。

如果用户要求“全流程”，按以上顺序执行。如果用户只要求其中一环，只读取对应文件与 `qc-checklist.md`；若该环节涉及上游 / 下游引用、参考图、提示词派单或恢复，额外读取 `chain-audit.md`。

## 加硬读取规则

若任务是修改、维护、加硬或验收本 Skill，必须同时读取 `chain-audit.md` 与 `production-data-center.md`，并遵守追加式加硬原则：不删减既有链路规则、不压缩用户已确认字段、不把本地模板替换为外部模板。

进入神笔制作后，选完 `production_visual_mode` 必须立刻读取 `style-tone-presets.md`，通过第二层弹窗或用户授权默认确定 `global_style_lock` 与 `tone_profile_lock`，并写回生产数据中心。

若任务涉及角色、场景、道具资产提示词，必须读取 `style-tone-presets.md` 与 `asset-pipeline.md`，并确认所有资产完整继承 `global_style_lock` 与 `tone_profile_lock`，不得只写预设 ID。

若任务涉及视频提示词、VIDEO_DISPATCH_PACKAGE、提示词冻结、派发、award-winning-performance-prompt、中文片段镜号格式、角色音色参考、全量前置快照或声音 owner，必须读取 `style-tone-presets.md`、`actor-performance-voice-integration.md` 与 `video-prompt-pipeline.md`，并确认 `global_style_lock`、`tone_profile_lock`、`current_active_snapshot_resolved`、角色音色字段完整展示在任务包和正式 prompt 中。

若任务涉及 QC、验收或返工，必须读取 `style-tone-presets.md` 与 `qc-checklist.md`，检查 `style_tone_lock_status`、模式匹配、资产继承、视频继承和真人 / 动画风险词边界。

若任务涉及 3D 动画 CG 角色资产、真人版本角色描述转换、动画角色资产提示词 QC，必须额外读取 `animation-character-converter.md` 与 `asset-pipeline.md`。

若任务涉及场景资产、道具资产或视频提示词引用锁，必须确认：场景资产使用 `scene_view` 单张方向资产，不使用 `scene_six_view`；道具资产使用单道具图，不使用 `prop_sheet` 或九宫格；空间坐标以自然语言 100×100 描述，不输出 `[x,y]` 数字坐标。
