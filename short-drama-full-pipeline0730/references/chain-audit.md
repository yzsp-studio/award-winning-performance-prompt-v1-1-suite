# 本地链路锁与链路审计

## 目标

保证 agent 在执行 short-drama-full-pipeline 时始终使用本地 Skill 目录内的 `SKILL.md` 与 `references/*.md`，不得改走线上通用制作链路、其它短剧 workflow、旧缓存或 light dispatch。

## 启动锁定句

当用户说出以下句式或同义表达时，必须进入本地链路锁：

```text
验收并继续制作，请使用本地“short-drama-full-pipeline”skill 链路，锁定 production_chain_id: short-drama-full-pipeline、workflow_source: user_skill_locked、fallback_allowed: false，每次制作前必须重读主 SKILL.md 与当前阶段本地 references/*.md 并锁定 template_source，不得走线上通用制作链路，不得混用外部模板，不得 light dispatch。
```

等价表达包括：

- 使用本地 short-drama-full-pipeline 链路。
- 使用神笔制作链路。
- 不要走线上通用制作链路。
- 锁定我的本地 skill。
- 按本地短剧全流程 Skill 继续。
- 不要 fallback 到其它链路。

## 锁定字段

一旦进入本地链路锁，必须在内部和关键产物中保持：

```text
production_chain_id: short-drama-full-pipeline
production_chain_name: 神笔制作
workflow_source: user_skill_locked
fallback_allowed: false
local_skill_root: expanduser("~/Movies/Hub/skills/short-drama-full-pipeline")
```

## 制作前强制读取

每次开始或继续制作任何产物前，必须真实读取：

1. 本地根目录下的 `SKILL.md`。
2. 当前阶段对应的本地 reference 文件。
3. 若涉及 QC、返工、恢复、派单前检查，必须同时读取 `references/qc-checklist.md`。
4. 若涉及链路锁、断点恢复、引用检查，必须同时读取 `references/chain-audit.md`。

不能只凭历史上下文、旧摘要、上次读取记录或线上 workflow 继续制作。

## template_source 锁

每个阶段开始前必须明确：

```text
template_source: expanduser("~/Movies/Hub/skills/short-drama-full-pipeline/references/<当前阶段文件>.md")
```

当前阶段产物的字段、顺序、命名、表格、提示词结构和 QC 标准必须来自该 `template_source`。禁止把其它 Skill、线上 workflow、旧模板或临时推理结果当作当前阶段模板源。

## 阶段到 template_source 映射

| 阶段 | template_source |
|---|---|
| 项目定位 / 选题 / 爆点 | `references/story-structure.md` |
| 剧本 / 分集 / 场次 / 对白 | `references/script-format.md` |
| 角色 / 场景 / 道具 / 角色高光视频 | `references/asset-pipeline.md` |
| 舞台定位 / 空间真值 / 分镜 / 黑白 3x3 | `references/storyboard-pipeline.md` |
| 关键帧 / 视频提示词 / 逐字派单 | `references/video-prompt-pipeline.md` |
| 声音 / 配乐 / 剪辑 / 成片 | `references/post-production-pipeline.md` |
| QC / 返工 / 恢复 | `references/qc-checklist.md` |
| 链路锁 / 断点审计 / 引用审计 | `references/chain-audit.md` |
| 文件索引 | `references/api_reference.md` |

## 禁止 fallback

进入本地链路锁后，禁止以下行为：

- 禁止改走线上通用短剧 workflow。
- 禁止改走其它 Skill 链路作为主模板。
- 禁止 light dispatch 跳过本地 Skill 阶段。
- 禁止用“更快”“更完整”“线上模板更强”“通用链路更合适”等理由绕开本地 Skill。
- 禁止使用外部模板替代本 Skill 的 `references/*.md`。
- 禁止只在口头声明锁定，但产物结构实际来自其它 workflow。

外部 Skill 或知识只能作为“补充增强能力”，不得替代本地 `template_source`。

## 制作前链路审计块

每次正式产出前，必须在内部形成以下审计块；涉及派单或生成提示词时，应写入任务包或提示词工作文档中：

```text
[LOCAL_CHAIN_AUDIT]
production_chain_id: short-drama-full-pipeline
production_chain_name: 神笔制作
workflow_source: user_skill_locked
fallback_allowed: false
local_skill_root: expanduser("~/Movies/Hub/skills/short-drama-full-pipeline")
current_stage: <阶段名>
template_source: <本地 reference 绝对路径>
required_references_read: [SKILL.md, <当前阶段 reference>, qc-checklist.md 或 chain-audit.md 如适用]
upstream_inputs: <本阶段消费的上游文档 / 资产 / 分镜 / 提示词>
expected_outputs: <本阶段应产物>
reference_paths_required: <本阶段应使用的参考图 / 音频 / 视频路径清单>
reference_paths_actual: <实际传入路径清单>
link_status: PASS | FAIL
[/LOCAL_CHAIN_AUDIT]
```

## 防数据断点规则

每个阶段必须写清：

- 上游来源是什么。
- 本阶段消费了哪些上游字段。
- 本阶段产出了什么。
- 下游将消费哪些字段。
- 哪些字段还缺失。

不得把 `pending`、`unknown`、空字符串、空数组、空对象当作 PASS。

## 防参考图引用断点规则

凡涉及图片、视频或音频参考，必须同时记录：

- 预期参考路径清单。
- 实际传入路径清单。
- 每个路径的用途。
- 每个路径对应的角色 / 场景 / 道具 / 分镜 / 音频身份。
- 数量是否一致。
- 顺序是否一致。
- 路径是否可解析。

若预期与实际数量、顺序或路径不一致，必须停止派单，回到上游修正。

## 防提示词引用断点规则

视频提示词或派单提示词必须能追溯到：

- 剧本源段落。
- 对白原文。
- 角色资产。
- 场景资产。
- 道具资产。
- 舞台定位或空间关系。
- 分镜 / Panel / 镜头表。
- 声音 owner。

若提示词只写“参考上文”“按原剧本”“同上”“见分镜”“按舞台定位图”，但没有把当前生成所需内容展开到本阶段任务包中，视为断点，禁止派单。

## 断点处理

发现数据断点、参考图断点或提示词断点时：

1. 停止进入下游。
2. 标出断点类型和缺失字段。
3. 回到最近的 producer 阶段补齐。
4. 补齐后重新执行 `LOCAL_CHAIN_AUDIT`。
5. 只有 `link_status: PASS` 才能继续。

## 加硬修改保护

维护本 Skill 时只能追加、细化、加硬规则，不得以“优化”“压缩”“合并”“去重”“更简洁”“更适合模型”等理由删减用户已确认的链路规则。

修改 Skill 文件时必须遵守：

- 不删除既有阶段。
- 不删除本地链路锁字段。
- 不删除 `production-data-center.md` 中已有数据表。
- 不删除 `LOCAL_CHAIN_AUDIT`。
- 不删除对白保真、参考图继承、prompt 映射、fallback 禁止、light dispatch 禁止相关规则。
- 若确需替换旧规则，必须保留原意并说明替换原因；默认采用追加式加硬。

## 逐产物链路冻结

当任一阶段产物被下游消费后，该产物进入链路冻结状态：

```text
freeze_target_id: <story_source_id / scene_id / asset_id / shot_id / prompt_id / edit_item_id>
freeze_reason: consumed_by_downstream
allowed_change: append_fix_only | user_authorized_replace
requires_reaudit: true
```

冻结后不得直接改写原产物导致下游引用失效。需要修正时，只能：

1. 生成新版本或追加补丁。
2. 标记旧版本 `DEPRECATED` 或 `needs_fix`。
3. 更新所有下游引用。
4. 重新执行 `LOCAL_CHAIN_AUDIT`。

## 派单前最终阻断条件

涉及图像、视频、speech、music 或 editing 派单前，若出现以下任一条件，必须阻断派单：

- `template_source` 不是本地 reference 绝对路径。
- 任务包缺少“原始需求”或已消解后的自包含原始需求。
- 任务包缺少上游 `video_task_id` / `prompt_id` / `asset_id` / `dialogue_id` 中应有的任一项。
- `reference_image_paths_expected` 与 `reference_image_paths_actual` 不一致。
- prompt 使用“同上”“按前面”“参考上文”承接关键信息。
- 需要逐字保留的对白没有完整展开。
- 声音 owner 冲突或同一类声音重复生成。

阻断后必须回到最近 producer 阶段补齐，不得用临场 prompt 自由发挥绕过。
