# 短剧声音与后期流程

## 目标

把已生成的镜头、对白、旁白、音乐和音效组织成可交付成片，保证节奏、声音层级、画幅和连续性稳定。

## 声音资产规划

### 台词

- 现场同期感台词：可交给支持原生音频的视频模型生成。
- 稳定对白或旁白：交给 speech 生成。
- 多角色对白：拆分 speaker，保留角色名、情绪、语速、停顿。

### 音乐

- BGM 通常按整集或整段生成一次。
- 不要每个镜头单独生成 BGM。
- 主题曲、片尾曲、角色曲属于 music 任务。
- 音乐长度由模型决定，后期按实际时长剪辑适配。

### 音效

- 环境声：雨声、脚步、门响、玻璃碰撞、宴会厅人声底噪。
- 动作声：摔合同、手机震动、刹车、戒指落地。
- 情绪声：呼吸、哽咽、轻笑、倒吸气。

## 唯一 owner 规则

同一类声音只能交给一个生成方：

- 同一句台词：不能同时交给 video 原生音频和 speech。
- 同一段 BGM：不能按镜头重复生成。
- 同一段环境声：若视频原生音频已生成，则后期只做混合，不重复造声。

## 角色音色与后期配音缺口

神笔制作当前默认优先让视频生成阶段使用 Seedance 原生音频完成角色台词，并在视频 prompt 中写入角色音色描述。若用户在首次音色建立弹窗中选择“后期配音 / speech”，当前作为功能缺口保留：

```text
speech_post_dub_gap: true
voice_reference_source: speech_post_dub_gap
```

在该缺口修复前，仍允许视频 prompt 写逐字台词与角色音色描述，但后期阶段必须在剪辑计划中标记潜在重复声音风险，不得把该分支误判为已完成稳定 speech 配音链路。后续若用户专门优化 speech 后期配音功能，再将该缺口改为正式分支。

## 剪辑计划字段

- clip_id：对应镜头编号。
- video_path：视频片段路径。
- duration：实际时长。
- audio_owner：video / speech / music / editing。
- dialogue_path：独立台词音频路径，如有。
- bgm_path：整集或整段 BGM 路径，如有。
- transition：硬切、淡入淡出、音频先入、动作匹配切。
- cross_video_continuity_ref：上一视频尾势与下一视频起势映射，如 `EP01-VT01 14-15秒 -> EP01-VT02 1-2秒`。
- qc_note：需要注意的连续性问题。

## 合成顺序

1. 按分镜顺序排列视频片段。
2. 统一画幅和分辨率。
3. 放入对白或旁白。
4. 放入 BGM，并在对白出现时压低。
5. 放入必要音效。
6. 检查片头片尾和镜头节奏。
7. 导出成片。

## 混音优先级

1. 对白清晰度最高。
2. 关键音效服务剧情信息。
3. BGM 服务情绪，不压过对白。
4. 环境声只做空间真实感，不抢主声。

## 成片检查

- 画幅是否统一。
- 镜头顺序是否符合剧本因果。
- 主角服装、发型、道具是否连续。
- 台词是否对得上角色。
- BGM 是否突然断裂。
- 情绪爆点是否留有反应时间。
- 成片时长是否偏离计划超过 20%。

## 返工策略

- 节奏拖：缩短过渡镜头，保留爆点前后的反应镜头。
- 声音乱：先静音 BGM，只保留对白，再逐层加回。
- 情绪弱：增加特写反应镜头或延长关键停顿。
- 空间乱：回到分镜和舞台定位，重新排序镜头。

## 后期映射硬规则

后期阶段不得只拿一堆视频和音频做拼接，必须消费生产数据中心中的 `video_task_id`、`prompt_id`、`dialogue_id` 和资产路径映射。

每条剪辑轨道必须登记：

```text
edit_item_id
video_task_id
prompt_id
shot_id 或 panel_id
video_path
video_duration_actual
source_dialogue_ids
dialogue_audio_paths
bgm_path
sfx_paths
audio_owner
lip_sync_required: true | false
transition
cross_video_continuity_ref
continuity_notes
status: ready | missing_input | needs_fix | assembled
```

若 `video_path`、必需对白音频、必需 BGM 或 `source_dialogue_ids` 缺失，不得进入最终合成。

## 对白音频绑定硬规则

- 每条独立 speech 音频必须绑定 `dialogue_id` 或 `dialogue_id` 范围。
- 口型同步必须绑定同一 `dialogue_id`，不得用相似台词替代。
- 如果视频原生音频已经包含某句对白，后期不得再叠加同句 speech，除非明确替换原声并记录原因。
- 若发现最终音频台词与 `verbatim_required` 原文不一致，必须回到 speech 或 video 阶段重做，不得靠剪辑掩盖。

## 成片写回硬规则

文件命名规则：视频生成结果、剪辑中间件与最终成片在创建时必须采用中文精简命名，避免长串英文、无语义编号或临时代号；如果上游文件名已固定，则沿用其中文短名语义，不额外增加冗长后缀。

导出成片后必须写回生产数据中心：

```text
final_output_id
project_name
episode_id 或 segment_id
final_video_path
source_edit_items
source_video_task_ids
source_prompt_ids
source_dialogue_ids
final_duration_actual
output_ratio
mix_notes
qc_status: pending | PASS | FAIL
```

成片只能由 `status: assembled` 的 edit item 合成。任何 `missing_input` 或 `needs_fix` 不得被跳过当作 PASS。
