# award-winning-performance-prompt与角色音色融合规则

## 目标

本文件把“award-winning-performance-prompt-v1-1”的中文片段镜号格式、Seedance 2.0 多模态提示词规则、角色音色参考、全量前置快照机制接入“神笔制作”本地全流程。它是神笔制作内部 reference，不依赖外部 Skill 是否触发。

## 执行原则

1. 视频提示词阶段默认使用中文片段镜号格式。
2. 角色台词默认优先由 Seedance 原生音频在视频生成时完成。
3. 同一角色若预计出现在 ≥2 段视频，必须建立角色音色参考流程。
4. 所有音色、表演、镜号、参考图、声音 owner、台词保真、角色造型变体、场景状态变体必须进入生产数据中心数据链。
5. 禁止只写“按award-winning-performance-prompt-v1-1”或“同上”。必须把当前视频任务所需信息展开为神笔制作内部可执行字段。

## 全量前置机制：完整快照 + 差异补丁 + 当前合成版

神笔制作允许真正全量前置，但不得直接覆盖旧数据。必须采用以下结构：

```text
full_preproduction_snapshot:
  snapshot_id: <稳定编号，如 FPS-E01-V01>
  snapshot_scope: episode | segment | video_task_group | full_project
  source_script_version_id:
  created_after_stage: script_standardized
  includes:
    - original_request
    - scene_table
    - dialogue_table
    - video_task_mapping
    - character_identity_table
    - character_look_variant_plan
    - scene_state_variant_plan
    - prop_usage_plan
    - voice_reference_plan
    - audio_owner_plan
    - reference_asset_plan
    - performance_plan_draft
    - chinese_shot_prompt_draft
    - qc_expectation_plan
  completeness_status: PASS | FAIL | pending
  status: ACTIVE | DEPRECATED | FAIL
```

后续若角色资产图、场景方向、道具参考、音色来源、audio_owner、镜头时长、角色造型变体或场景状态变体发生变化，不得直接覆盖初始快照，必须新增补丁：

```text
preproduction_patch:
  patch_id: <稳定编号，如 PATCH-E01-003>
  target_snapshot_id:
  change_trigger: character_asset_changed | scene_direction_changed | prop_reference_changed | voice_source_changed | audio_owner_changed | duration_changed | character_look_variant_changed | scene_state_variant_changed | user_authorized_change | qc_fix
  changed_fields: []
  before_value_ref:
  after_value:
  affected_video_task_ids: []
  affected_prompt_ids: []
  patch_status: ACTIVE | DEPRECATED | FAIL
```

所有下游只允许消费合成版：

```text
current_active_snapshot_resolved:
  base_snapshot_id:
  active_patch_ids: []
  resolved_version_id:
  resolved_fields_complete: true | false
  forbidden_missing_fields: []
  consumed_by_asset_stage: true | false
  consumed_by_storyboard_stage: true | false
  consumed_by_video_prompt_stage: true | false
  resolved_status: PASS | FAIL
```

硬规则：

- 下游不得只消费 patch。
- 下游不得只消费旧 snapshot。
- 必须消费 `current_active_snapshot_resolved`。
- 若 resolved 合成版缺少基准快照已有字段，QC 必须 FAIL。
- 每个 `prompt_id` 必须登记自己消费的 `base_snapshot_id`、`active_patch_ids` 与 `resolved_version_id`。

## 角色音色参考规则

### 启用阈值

角色是否需要音色参考由生产数据中心的视频任务映射统计决定：

```text
character_video_segment_count_from_production_data_center = 统计 required_characters / source_dialogues / assigned_video_task_id 中该角色出现的视频任务数量
```

规则：

- `character_video_segment_count_from_production_data_center >= 2` → `voice_reference_required: true`
- `< 2` → `voice_reference_required: false`，只写自然声音表演描述

### 首次音色建立弹窗

当 `voice_reference_required: true` 且 `voice_reference_status != ready` 时，必须用弹窗询问：

```text
A. 先生成首段视频，之后从首段视频中分离并剪辑角色台词音色（推荐）
B. 上传该角色音频音色文件
C. 后期配音 / speech 负责该角色台词（当前保留缺口，后续可优化）
```

当前用户确认的执行策略：

- 默认优先 A，即视频生成时使用 Seedance 原生音频。
- 选择 A 时，首段视频 prompt 仍必须写音色描述词；生成后提取该角色 5-10 秒台词音频作为后续音色参考。
- 选择 B 时，用户上传音频后分析为自然语言音色描述词。
- 选择 C 时，当前仍允许视频 prompt 写逐字台词与音色描述，保留未来 speech/后期配音优化缺口；必须在数据中心标记 `speech_post_dub_gap: true`，避免误判为已彻底解决重复声音风险。

### 角色音色字段

```text
character_voice_reference_map:
  - character_id:
    character_name:
    character_video_segment_count_from_production_data_center:
    voice_reference_required: true | false
    voice_reference_source: first_generated_video_extraction | user_uploaded_audio | speech_post_dub_gap | not_required | pending
    voice_reference_audio_path: pending | <path> | not_required
    voice_description_text: <自然语言音色描述词>
    voice_reference_status: pending | ready | not_required | failed
    first_voice_seed_video_task_id:
    voice_reference_clip_duration_required: 5-10s
    applies_to_dialogue_ids: []
    applies_to_video_task_ids: []
```

音色描述词必须是自然语言，包含性别年龄感、音高、厚薄、明暗、气息、颗粒感、共鸣、语速情绪、叙事风格。不得机械写参数。

## 中文片段镜号格式

最终视频提示词默认采用：

```text
第 <片段序号> 段视频片段完整提示词
[画面美学风格]：<继承 global_style_lock、tone_profile_lock、cinematography_profile>
[环境光影]：<场景时间、天气、季节、光源、情绪光影>
[人物站位]：<从 space_truth_id 和 scene_direction_lock 继承>
[内容概述]：<本片段剧情事件>
[情绪氛围]：<情绪曲线与冲突强度>
[衔接参考首帧]：<上一段尾势或本段开场>
[要求]：<180度轴线、视线匹配、物理真实、模式质感>
镜号：<连续镜号> | 场次：<时间/地点> | @<场景名> | <片段内时间段> | <景别> | <运镜> | ( @<角色名> <站位/姿态> ) <动作 + 物理细节 + 自然微表情 + 环境互动> | 台词 & 音效：<角色音色引用 / 音效 / 环境声> | 备注：<道具 / 情绪 / 衔接>
[片段结尾：全局画质与渲染后缀]
[下一片段继承点]
【角色严格按照台词说话，不要增加台词或减少台词】
[禁令]
```

若角色满足音色参考启用条件，台词必须写为：

```text
@<角色名>严格使用@<角色名音频1><voice_description_text>。<说话方式>:{逐字台词}
```

硬规则：

- `<角色名>`、`<角色名音频1>`、`voice_description_text`、`逐字台词` 必须来自当前生产数据中心。
- 已启用音色参考的同一角色，后续所有视频片段必须持续使用同一 `voice_description_text`，除非新增 patch 并重新 QC。
- 台词必须逐字保留，不得因音色描述而增删台词。

## Seedance 2.0 参考素材规则

每个参考素材必须说明用途：

```text
@图片1 作为角色身份参考。
@图片2 作为场景方向与空间背景参考。
@图片3 作为道具外观参考。
@视频1 作为动作、运镜或动效参考。
@音频1 作为角色音色、语气或声音氛围参考。
```

禁止写“像那个图”“参考上面”“按前文”。

## QC 要点

输出前必须检查：

1. 是否消费 `current_active_snapshot_resolved`。
2. 是否记录 `base_snapshot_id`、`active_patch_ids`、`resolved_version_id`。
3. ≥2 段角色是否 `voice_reference_required: true`。
4. 首次无音色参考角色是否弹窗选择 A/B/C。
5. 选择 A 后首段是否写推算音色描述词，后续是否等待或引用 ready 音色。
6. 每句台词是否逐字保留。
7. 音色描述词是否来自角色数据或音频分析，而不是示例。
8. 中文片段镜号格式是否完整替换旧视频提示词正文。
9. 角色造型变体与场景状态变体是否来自 resolved 合成版。


## 表演编码内部推导、外部自然语言化规则（强制补丁）

FACS（面部动作编码系统）、BACS（躯体动作编码）、RACS（呼吸节律编码）是本 Skill 的内部计算体系，不是最终提示词文案。它们可以存在于 performance_plan_draft、VIDEO_DISPATCH_PACKAGE.facs_map / bacs_map / racs_map、内部 QC 审计字段和生产数据中心表演推导草案。

但它们不得直接出现在 prompt_chinese_dispatch、prompt、用户可复制的视频提示词正文、沙盒测试提示词文档正文、真实派发给视频模型的提示词正文中。最终提示词必须只写自然语言表演结果。

自然语言转换词库：平静专注=面部肌肉放松，眼睑平稳，眉头舒展，下颌自然闭合，无多余面部动作；温和笑意=眼尾轻微弯起，下眼睑微微收紧，嘴角平缓上扬，面部肌肉舒展不僵硬；凝重思考=眉头轻蹙，眉心微紧，眼睑略收，下颌微沉；冷静警觉=瞳孔聚焦，眼睑轻微收紧，眉心极轻收束，嘴唇自然闭合，下颌稳定；压抑震惊=眼神短暂停住，眼睑收紧，下唇轻压，面部肌肉克制收束，不出现夸张张嘴或瞪眼。

躯体转换词库：端正松弛=肩颈自然下沉放松，脊背挺直不僵硬，双肩平齐，躯干端正无歪斜；放松倚靠=肩背轻靠支撑物，肩颈舒展，脊柱自然弯曲，双臂自然放置；轻微紧绷=肩颈微微收紧，脊背挺直，躯干肌肉呈轻度紧张状态，肢体动作幅度收窄；心虚回避=肩颈短促收紧，身体微微侧转，手部动作变快，视线避开对方。

呼吸转换词库：平稳浅呼吸=胸腹起伏微弱平缓，呼吸节律均匀，肩部无明显晃动；舒缓深呼吸=胸腹缓慢自然起伏，吸气时胸腔平稳扩张，呼气时平缓回落；急促浅呼吸=胸腹快速小幅起伏，呼吸频率加快，肩部伴随轻微联动；短促屏息=呼吸突然停顿半拍，胸口细微收住，肩部静止，随后恢复浅呼吸；压住长呼气=先短暂停顿，再缓慢呼出，胸腔轻微回落，声音或动作随之变冷静。

QC 若发现最终 prompt 出现 FACS、BACS、RACS、AU，必须判定 FAIL_PERFORMANCE_NATURALIZATION。


## 每镜音色描述展开规则（强制补丁）

每个镜号内，某角色首次发生画外音（VO）、内心独白（OS）或说出口台词之前，必须写不少于3句完整音色描述句。三句必须覆盖：

1. 音高与厚薄：例如“音色清亮偏柔，厚度轻薄但不虚。”
2. 气息与共鸣：例如“气息克制，胸腔共鸣浅，尾音轻轻落下。”
3. 语速与情绪控制：例如“语速平缓清晰，情绪压在声音底部，不提高音量。”

格式示例：

```text
台词与音效：@宋知 音色清亮偏柔，厚度轻薄但不虚。气息克制，胸腔共鸣浅，尾音轻轻落下。语速平缓清晰，情绪压在声音底部，不提高音量。宋知画外音（VO）：{台词}
```

同一镜号内同一角色连续说第二句台词，可以不重复三句音色；但跨镜号必须重新写三句。禁止写“同上”“延续前句音色”“保持前述音色”。

若角色满足音色参考启用条件但音频路径仍为 pending，也必须写三句自然语言音色描述；不得因缺少真实音频而省略音色。

QC 若发现任一镜号内角色首次发声前音色描述少于3句，标记 FAIL_VOICE_DESCRIPTION_TOO_SHORT。


## v4 台词发声格式补丁

每个镜号里，角色发声格式必须同时满足 v3 每镜三句音色与 v4 台词类型格式：

1. 画外音（VO）：@角色 + 三句音色描述 + 角色画外音（VO）：{dispatch_text}
2. 内心独白（OS）：@角色 + 三句音色描述 + 角色内心独白（OS）：{dispatch_text}
3. 角色说出口台词：@角色 + 情绪 / 动作 / 语气 + 说：{dispatch_text}

角色说出口台词也可以在同一“台词与音效”段前面先写三句音色描述；但台词本体必须仍为“@角色<情绪/动作/语气>说”。

错误示例：宋知：{出轨？}
正确示例：@宋知错愕地低声说：{出轨？}

若最终提示词出现“角色名：{台词}”且该句不是对白表展示层，而是真实 prompt 派发层，则标记 FAIL_SPOKEN_DIALOGUE_AT_EMOTION_MISSING。
