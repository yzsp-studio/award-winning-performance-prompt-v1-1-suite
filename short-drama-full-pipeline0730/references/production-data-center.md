# 生产数据中心

## 目标

建立 short-drama-full-pipeline 的统一母体数据中心，用来承接剧本、资产、空间、分镜、提示词、音频和后期信息，避免上下游断链。

## 数据中心名称

每个项目至少建立一个生产数据中心：

```text
短剧生产数据中心 — [项目名]
```

如果项目较长，可按集或段落拆分：

```text
短剧生产数据中心 — [项目名][集数][段落编号][场景名]
```

## 必填字段

```text
production_chain_id: short-drama-full-pipeline
production_chain_name: 神笔制作
workflow_source: user_skill_locked
fallback_allowed: false
local_skill_root: expanduser("~/Movies/Hub/skills/short-drama-full-pipeline")
project_name: <项目名>
project_type: <短剧 / 动态漫 / 微电影 / 宣传片等>
production_visual_mode: cinematic_realistic | top_chinese_3d_animation_cg
production_visual_mode_source: chosen_by_user_popup | inferred_from_user_text | user_authorized_agent_choice
global_style_preset_id: <STYLE-REAL-01 | STYLE-ANIM-CG-01 | 扩展预设ID>
global_style_preset_name: <风格预设名称>
global_style_lock: <从 references/style-tone-presets.md 继承的完整风格配置正文>
tone_profile_preset_id: <TONE-REAL-01 | TONE-ANIM-CG-01 | 扩展预设ID>
tone_profile_preset_name: <影调预设名称>
tone_profile_lock: <从 references/style-tone-presets.md 继承的完整影调配置正文>
style_tone_selection_source: chosen_by_user_popup | user_authorized_default | restored_from_project_data_center
style_tone_lock_status: PASS | FAIL | pending
output_ratio: <最终视频比例>
output_duration_plan: <总时长 / 单集时长 / 每任务时长>
```

`production_visual_mode` 是全链路硬锁。角色资产、场景资产、道具资产、视频提示词和 QC 必须保持一致，不得同一项目内混用真人资产与 3D 动画 CG 资产。

`global_style_lock` 与 `tone_profile_lock` 是第二层全局锁，必须来自 `references/style-tone-presets.md`。选择完成后，资产阶段、分镜阶段、视频提示词阶段、QC 阶段必须完整继承，不得只写预设 ID。任何阶段缺少完整风格锁或完整影调锁时，`style_tone_lock_status` 不得标记 PASS。

## 上游源信息

记录用户提供的所有源材料：

- original_request：用户原始需求。
- script_source：剧本 / 大纲 / 灵感来源。
- reference_assets：用户提供的图片、视频、音频、文档。
- user_constraints：用户明确要求与禁止事项。
- auto_inferred_context：agent 自动补全的上下文，必须写明依据和置信度。

## 剧本版本与写回登记

每次由本 Skill 优化、改写或新写的剧本，都必须登记为生产数据中心中的一个剧本版本，禁止只在聊天中输出剧本文本而不写回。

```text
script_version_id: <稳定编号，如 SCRIPT-OPT-V01 / E01-E03-SCRIPT-V01>
script_operation: optimize_existing | rewrite_existing | write_new | standardize_for_production
script_source_ref: <原剧本 / 上一版剧本 / 用户新输入路径或节点>
script_output_ref: <优化后剧本文档路径或节点>
scene_table_ref: <场次表位置>
dialogue_table_ref: <对白表位置>
character_face_structure_3t5e_ref: <角色三庭五眼结构表位置>
asset_extraction_input_ref: <资产抽取输入表位置>
video_task_mapping_ref: <视频任务映射表位置>
status: ACTIVE | DEPRECATED | PENDING | FAIL
replacement_of: <如有>
```

只有 `status: ACTIVE` 的剧本版本可以作为资产阶段、分镜阶段、视频提示词阶段的上游输入。若优化后的剧本没有写回 `scene_id`、`dialogue_id`、`required_characters`、`required_scene`、`required_props`、`face_structure_3t5e` 和视频任务映射，则 `stage_status.script: FAIL`，不得继续进入资产阶段。

## 剧本与对白表

每句对白都必须登记：

```text
dialogue_id: <稳定编号>
speaker: <角色名>
text: <原始台词，逐字保留>
source_scene: <场次或段落>
assigned_video_task_id: <所属视频任务>
preservation: verbatim_required | optional | user_authorized_change
```

规则：

- `verbatim_required` 的对白不得删减、概括、换人、沉默化或改写。
- 如果视频任务承载不了完整对白，必须拆分任务，不得压缩对白。
- 只有用户明确授权或剧本明示中断，才允许不完整说出。

## 视频任务映射

把剧情拆成可生产的视频任务，但不得删减剧情和台词：

```text
video_task_id: EP01-VT01
narrative_range: <剧情范围>
duration_target: 10-15 秒或用户指定
source_dialogues: [dialogue_id]
required_characters: []
required_scene_assets: []
required_prop_assets: []
scene_view_orientation_required: front | reverse | left | right | top | keylight
stage_map_ref: optional_not_recommended | path | skipped_by_user
storyboard_image_ref: optional_not_recommended | path | skipped_by_user
storyboard_data_ref: pending | path
final_prompt_ref: pending | path
status: pending | ready | generated | needs_fix
```

`scene_view_orientation_required` 是场景方向锁源头。场景资产阶段必须按该字段生成对应方向的单张场景图；视频提示词阶段必须以该方向作为背景机位。

## 角色面部身份结构表

主要角色必须在剧本 / 剧本优化阶段写入 `face_structure_3t5e`，并由生产数据中心统一登记。该字段用于把剧本人物设定继承到资产需求包、角色资产参考图、分镜身份锁定、关键帧和视频提示词。

```text
character_id: <稳定编号>
character_name: <角色名>
source_scene_ids: []
identity_anchor: <脸型 / 五官 / 发型 / 体型 / 气质 / 标志物>
face_structure_3t5e:
  source_basis: script_explicit | auto_inferred_from_character_design | user_provided_reference
  upper_third: <上庭：额头、发际线、额面比例与气质>
  middle_third: <中庭：眉眼、鼻梁、颧骨、面中结构与人物处境>
  lower_third: <下庭：人中、唇形、下颌、下巴比例与年龄 / 情绪>
  five_eye_ratio: <五眼：眼距、眼长、眉眼比例、眼神气质>
  bone_and_soft_tissue: <整体骨相、软组织、材质表现；3D 动画 CG 模式不得写真人皮肤或毛孔>
  temperament_mapping: <面部结构如何服务角色性格 / 剧情处境>
  forbidden_face_drift: <后续图像不得改变的脸型、骨相、眉眼、气质边界>
production_visual_mode_adaptation: cinematic_realistic | top_chinese_3d_animation_cg
status: ACTIVE | PENDING | FAIL
```

如果剧本原文没有明确三庭五眼描写，必须根据角色人设合理补齐并标记 `source_basis: auto_inferred_from_character_design`，不得留空。`face_structure_3t5e.status` 不是 `ACTIVE` 时，角色资产、分镜、关键帧和视频提示词阶段不得把该角色标记为身份锁定完成。

## 全量前置快照、差异补丁与当前合成版

剧本标准化后、资产阶段前，必须建立完整前置快照。该快照不是最终不可变 prompt，而是全链路生产母体数据的完整基准。

```text
full_preproduction_snapshot:
  snapshot_id: <稳定编号>
  snapshot_scope: episode | segment | video_task_group | full_project
  source_script_version_id:
  created_after_stage: script_standardized
  scene_table_ref:
  dialogue_table_ref:
  video_task_mapping_ref:
  character_identity_table_ref:
  character_look_variant_plan_ref:
  scene_state_variant_plan_ref:
  prop_usage_plan_ref:
  voice_reference_plan_ref:
  audio_owner_plan_ref:
  reference_asset_plan_ref:
  performance_plan_draft_ref:
  chinese_shot_prompt_draft_ref:
  qc_expectation_plan_ref:
  completeness_status: PASS | FAIL | pending
  status: ACTIVE | DEPRECATED | FAIL
```

后续若角色资产图、场景方向、道具参考、音色来源、audio_owner、镜头时长、角色造型变体或场景状态变体变化，必须新增差异补丁，不得直接覆盖初始快照：

```text
preproduction_patch:
  patch_id:
  target_snapshot_id:
  change_trigger: character_asset_changed | scene_direction_changed | prop_reference_changed | voice_source_changed | audio_owner_changed | duration_changed | character_look_variant_changed | scene_state_variant_changed | user_authorized_change | qc_fix
  changed_fields: []
  before_value_ref:
  after_value:
  affected_video_task_ids: []
  affected_prompt_ids: []
  patch_status: ACTIVE | DEPRECATED | FAIL
```

所有下游只允许消费当前合成版：

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

若合成版缺少基准快照已有字段，`resolved_status` 必须为 FAIL，不得进入下游。

## 角色造型变体计划

同一角色在长期多集、单集或单个视频中可能因剧情逻辑需要多套人物资产图。剧本标准化后必须计算：

```text
character_look_variant_plan:
  character_id:
  character_name:
  look_variant_id: <如 C01-LV01>
  look_variant_name: <日常 / 夜宴 / 战损 / 雨中 / 十年后等>
  costume: <服装>
  makeup_design: <妆造>
  makeup_texture: <妆感>
  hairstyle: <发型>
  hair_accessories: <发饰>
  visible_age_stage: <年龄阶段或年龄变化>
  damage_or_weathering: <伤痕 / 血迹 / 泥水 / 雨湿 / 疲惫等>
  carried_weapon: <贴身武器，可与人物资产图绑定 | none>
  carried_body_prop: <贴身道具，可与人物资产图绑定 | none>
  applicable_scene_ids: []
  applicable_video_task_ids: []
  change_reason: scene_change | weather_change | season_change | day_night_change | identity_state_change | damage_state_change | age_time_skip | weapon_change | body_prop_change | plot_required_disguise
  character_has_time_to_change: true | false | uncertain
  continuity_forbidden_changes: []
  asset_required: true | false
  character_asset_id: pending | <asset_id>
  status: planned | ACTIVE | DEPRECATED | FAIL
```

逻辑规则：

- 不得每场无脑生成新造型；必须根据剧情时间线、天气季节、场景环境、身份状态和角色是否有现实时间换装来判断。
- 若角色没有时间换装，只能延续上一套造型，并通过损伤、雨湿、脏污等状态变化处理。
- 武器和贴身道具若与角色身体长期绑定，应进入人物资产图变体，而不是临场口头描述。
- 所有被视频任务使用的角色造型变体必须进入 `full_preproduction_snapshot` 与 `current_active_snapshot_resolved`。

## 场景状态变体计划

同一场景只要剧情中出现季节、天气、日/夜、受损、新增固定道具、剧情状态或光源状态变化，就必须计算并生成对应场景状态资产图。

```text
scene_state_variant_plan:
  scene_id:
  scene_name:
  scene_state_variant_id: <如 SCE01-SV01>
  scene_state_variant_name: <日间晴天 / 夜雨 / 战后破损 / 新增灵位等>
  season_state: <春 / 夏 / 秋 / 冬 / 不适用>
  weather_state: <晴 / 雨 / 雪 / 雾 / 风沙 / 不适用>
  time_of_day_state: day | night | dawn | dusk | interior_lamp | candlelight
  damage_state: intact | damaged | burned | flooded | battle_aftermath | other
  added_fixed_props: []
  removed_fixed_props: []
  lighting_state: <主要光源与情绪光影>
  applicable_scene_ids: []
  applicable_video_task_ids: []
  required_scene_view_orientations: []
  scene_view_asset_ids: []
  variant_asset_required: true | false
  status: planned | ACTIVE | DEPRECATED | FAIL
```

规则：

- 用户已确认：每次季节、天气、日/夜、受损、新增固定道具、剧情状态或光源状态变化，都生成新场景状态资产图。
- 场景状态变体仍必须服从 `scene_view_orientation` 和 `camera_background_lock`。
- 视频提示词不得用旧场景状态图临场硬写新天气、新季节、新破损或新增固定道具。

## 角色音色参考计划

角色音色参考由视频任务映射统计驱动：

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
    speech_post_dub_gap: true | false
```

≥2 段视频出现的角色必须启用音色参考流程。默认优先首段视频生成后提取角色 5-10 秒台词音频；用户也可上传角色音频。若选择后期配音 / speech，当前作为功能缺口保留，仍允许视频 prompt 写逐字台词和音色描述，但必须标记 `speech_post_dub_gap: true`。

## 资产池

所有资产必须进入资产池登记：

```text
asset_id: <稳定编号>
asset_type: character | scene_view | prop | lighting | role_highlight_video | stage_map | storyboard_data | storyboard_image_optional
asset_name: <名称>
asset_path: <真实路径或 pending>
reference_role: character_identity | scene_environment_direction | prop_identity | stage_blocking_optional | storyboard_composition_data | storyboard_image_optional
production_visual_mode: cinematic_realistic | top_chinese_3d_animation_cg
global_style_preset_id: <继承项目风格预设ID>
tone_profile_preset_id: <继承项目影调预设ID>
global_style_lock_consumed: true | false
tone_profile_lock_consumed: true | false
style_tone_inheritance_status: PASS | FAIL
status: ACTIVE | DEPRECATED | PENDING | FAIL | SKIPPED
used_by_video_tasks: []
replacement_of: <如有>
```

只有 `ACTIVE` 且 `asset_path` 非空的资产可以进入下游参考图清单。`SKIPPED` 只允许用于被明确判定为无需生成图像的道具。

## 场景方向资产字段

场景资产不再登记 `scene_six_view_path`，改为登记单张方向资产集：

```text
scene_id: <场景稳定编号>
scene_name: <场景名>
scene_view_set:
  - scene_view_asset_id: <scene_id>-FRONT | REVERSE | LEFT | RIGHT | TOP | KEYLIGHT
    scene_view_orientation: front | reverse | left | right | top | keylight
    scene_view_display_name: 正面 | 反向 | 左侧 | 右侧 | 俯视 | 关键机位光影
    scene_view_ref_image_path: <真实路径或 pending>
    scene_view_source_video_tasks: []
    camera_background_lock: <使用该场景图时所有镜头必须遵循的背景机位方向>
    scene_era_profile: <朝代 / 时代 / 制式>
    scene_atmosphere_profile: <剧情氛围与情绪功能>
    scene_art_direction_profile: <建筑 / 材质 / 陈设 / 美术体系>
    project_visual_tone: <项目总视觉基调>
    entrance_exit_map: <入口出口与动线>
    fixed_prop_positions: <固定道具位置>
    usable_shot_angles: <与 scene_view_orientation 一致的镜头方向>
    visual_inheritance_status: PASS | FAIL
```

方向继承规则：

```text
video_task.scene_view_orientation_required -> scene_view_asset_id -> scene_view_ref_image_path -> prompt.reference_image_paths_expected -> prompt.reference_image_paths_actual -> prompt.scene_direction_lock_actual
```

若视频任务需要正面场景图，则该视频任务所有镜头必须以正面为背景机位；若需要反向图，则所有镜头必须以反向为背景机位。禁止视频提示词临场把正面图当反向背景使用。

## 角色资产提示词继承完整性

角色资产为 `character` 时，除 `face_structure_3t5e` 外，还必须登记提示词继承完整性：

```text
character_asset_prompt_inheritance:
  character_id: <稳定编号>
  production_visual_mode: cinematic_realistic | top_chinese_3d_animation_cg
  character_asset_prompt_source: realistic_prompt | animation_converter
  identity_anchor_consumed: true | false
  face_structure_3t5e_consumed: true | false
  costume_anchor_consumed: true | false
  state_variants_consumed: true | false
  source_scene_ids_consumed: true | false
  source_dialogue_ids_consumed: true | false
  used_by_video_tasks_consumed: true | false
  prompt_block_complete: true | false
  prompt_field_count_parity_status: PASS | FAIL
  prompt_detail_density_parity_status: PASS | FAIL
  prompt_forbidden_shorthand_status: PASS | FAIL
  asset_quality: 高
  asset_clarity_base: 2K
  asset_upscale_target: 4K
  upscale_status: pending | done | manual_required | not_available
  animation_converter_qc_status: PASS | FAIL | not_required
  inheritance_status: PASS | FAIL_INHERITANCE_PROMPT | FAIL_ANIMATION_CONVERTER_QC | FAIL_ASSET_PROMPT_COMPLETENESS_MATRIX
```

## 道具资产字段

道具资产为 `prop` 时，先登记是否需要生成：

```text
prop_id: <稳定编号>
prop_name: <道具名>
appearance_count: <在当前制作范围内出现次数>
text_symbol_risk: true | false
animation_precision_risk: true | false
prop_asset_required: true | false
prop_asset_reason: appearance_count_ge_2 | single_use_text_symbol_risk | animation_precision_risk | skipped_single_use_no_text
prop_ref_image_path: <真实路径或 pending | not_required>
prop_animation_reference_required: true | false
prop_animation_reference_filename_required: 道具动效参考-<prop_id>-<道具名>.mp4 | not_required
prop_animation_reference: <真实路径或 pending | not_required>
prop_animation_description: <动效变化简述 | not_required>
used_by_video_tasks: []
status: ACTIVE | PENDING | FAIL | SKIPPED
```

道具资产不再登记 `prop_sheet_config`、`prop_marker_map`、颜色框、宫格行列、空格、box_order_number。每个道具独立一张参考图。

## 空间与分镜映射

每个 `video_task_id` 必须能追溯：

- 空间真值或舞台定位信息。
- 角色位置和朝向，用自然语言 100×100 空间描述，不使用 `[x,y]` 数字坐标格式。
- 道具位置和归属。
- 镜头 / Panel / 分镜表。
- Panel 9 到下一任务 Panel 1 的衔接信息，如适用。

```text
space_truth_id: <稳定编号>
coordinate_system_description: 100x100_top_view_natural_language
characters_position_natural_language:
  - character_id
    position: <例如：画面左侧约 30% 区域，靠近前景>
    facing: <看向谁 / 哪个方向 / 哪个道具>
    screen_position_lock: <左 / 中 / 右 / 前景 / 后景>
props_position_natural_language:
  - prop_id
    position: <例如：画面中央偏前的桌案上>
    owner_or_surface: <手中 / 桌上 / 地上 / 门边>
entry_exit_points: []
eyeline_map: []
movement_paths: []
```

## 提示词映射

每个最终视频提示词必须登记：

```text
prompt_id: <稳定编号>
video_task_id: <对应任务>
source_script_range: <剧本范围>
source_dialogue_ids: []
source_asset_ids: []
source_stage_map: optional_not_recommended | skipped_by_user | path
source_stage_map_coordinates: natural_language_100x100_space_description
source_storyboard_image: optional_not_recommended | skipped_by_user | path
source_storyboard_data: storyboard_order_composition_action_data
scene_direction_lock_actual:
  scene_view_asset_id
  scene_view_orientation
  camera_background_lock
reference_image_paths_expected: []
reference_image_paths_actual: []
audio_owner: video_native | speech | music | editing | mixed_with_rules
verbatim_lock: true | false
status: draft | frozen | dispatched | needs_fix
```

## 参考图继承矩阵

所有参考图必须从资产池或上游分镜资产进入下游：

```text
character_ref_image_path -> storyboard.refs -> prompt.reference_image_paths_expected -> prompt.reference_image_paths_actual
scene_view_ref_image_path + scene_direction_lock -> storyboard.refs -> prompt.reference_image_paths_expected -> prompt.reference_image_paths_actual
prop_ref_image_path -> storyboard.refs -> prompt.reference_image_paths_expected -> prompt.reference_image_paths_actual
stage_map_path -> prompt.reference_image_paths_expected -> prompt.reference_image_paths_actual（仅用户明确授权生成舞台定位图时）
storyboard_image_path -> prompt.reference_image_paths_expected -> prompt.reference_image_paths_actual（仅用户明确授权生成黑白分镜图时）
storyboard_order_composition_action_data -> prompt.source_storyboard_data（默认只进数据，不进图像参考）
```

下游不得直接使用未登记路径。若用户新上传参考图，必须先登记到资产池并说明 `reference_role`，再进入下游。

## 参考图用途说明与禁止继承字段

每个进入视频提示词阶段的参考图必须登记“用途说明”和“禁止继承字段”，并写入提示词包；不得只把路径列入 `reference_image_paths_actual`。

```text
reference_usage_statement:
  - path: <参考图路径>
    asset_id: <角色 / 场景方向 / 道具 / 舞台定位 / 分镜资产ID>
    reference_role: character_identity | scene_environment_direction | prop_identity | storyboard_composition_optional | stage_blocking_optional
    use_for: <身份 / 场景环境方向 / 道具外观 / 镜头顺序 / 构图 / 动作调度 / 空间站位>
    do_not_use_for: <画风 / 材质 / 人物外貌 / 服装纹理 / 分镜线稿 / UI 等>
    scene_direction_lock: <若为场景参考图，必须写 scene_view_orientation 与 camera_background_lock>
    final_frame_exclusion: <最终视频不得出现字幕、UI、水印、黑白线稿、宫格边框、白底、草图线条等>
    inheritance_status: PASS | FAIL
```

## 链路状态

每个阶段完成后更新：

```text
stage_status:
  visual_mode: PASS | FAIL | pending
  story: PASS | FAIL | pending
  script: PASS | FAIL | pending
  assets: PASS | FAIL | pending
  space: PASS | FAIL | pending
  storyboard: PASS | FAIL | pending
  prompt: PASS | FAIL | pending
  post: PASS | FAIL | pending
  qc: PASS | FAIL | pending
```

任何阶段不得把空值当作 PASS。

## 全链路继承矩阵

| 阶段 | 必须消费 | 必须写回 |
|---|---|---|
| visual_mode | original_request, user_constraints | production_visual_mode, production_visual_mode_source, stage_status.visual_mode |
| story | original_request, user_constraints, reference_assets, production_visual_mode | story_source_id, project card, main_conflict, episode_ranges, stage_status.story |
| script | story_source_id, project card, episode_ranges | script_version_id, script_output_ref, scene_id, dialogue_id, required_characters, required_scene, required_props, face_structure_3t5e, asset_extraction_input_ref, video_task_mapping_ref, stage_status.script |
| assets | current_active_snapshot_resolved, scene_id, required_characters, required_scene, required_props, face_structure_3t5e, character_look_variant_plan, scene_state_variant_plan, production_visual_mode | asset_id, asset_path, reference_role, ACTIVE/PENDING/SKIPPED status, required_reference_package, character_variant_asset, scene_state_variant_asset, character_asset_prompt inheritance, scene_view_ref_image_path, scene_view_orientation, prop_asset_required, stage_status.assets |
| storyboard | current_active_snapshot_resolved, video_task_id, scene_id, asset_id, dialogue_id, scene_view_orientation_required, scene_view_ref_image_path, look_variant_id, scene_state_variant_id | space_truth_id, shot_id/panel_id, reference_image_paths_expected, character_count_expected, scene_direction_lock, stage_status.storyboard |
| prompt | current_active_snapshot_resolved, base_snapshot_id, active_patch_ids, resolved_version_id, shot_id/panel_id, dialogue_id, asset_id, space_truth_id, scene_direction_lock, character_voice_reference_map, look_variant_id, scene_state_variant_id | prompt_id, VIDEO_DISPATCH_PACKAGE, reference_image_paths_actual, verbatim_lock, prompt_chinese_dispatch, status frozen/dispatched, stage_status.prompt |
| post | video_task_id, prompt_id, dialogue_id, video_path/audio_path | edit_item_id, final_output_id, source mappings, final_duration_actual, stage_status.post |
| qc | all ids and paths | qc_status, missing fields, return stage, stage_status.qc |

## 强制停止条件

出现以下任一情况，必须停止下游制作：

- `fallback_allowed` 不是 false。
- 当前阶段没有 `template_source`。
- required reference 没有真实读取。
- 未通过启动弹窗或明确上下文确定 `production_visual_mode`。
- `script_version_id`、`script_output_ref`、场次表、对白表、资产抽取输入表、视频任务映射、`full_preproduction_snapshot`、`character_look_variant_plan`、`scene_state_variant_plan` 或 `current_active_snapshot_resolved` 没有写回生产数据中心。
- `dialogue_id` 缺失或 `verbatim_required` 台词被改写。
- 主要角色缺少 `face_structure_3t5e`，或该字段未写入生产数据中心，或状态不是 `ACTIVE`。
- 3D 动画 CG 模式下角色提示词未经过 `animation-character-converter.md` 或仍含真人风险词。
- 场景参考图不是单张方向资产，或缺少 `scene_view_orientation` / `camera_background_lock`。
- 道具资产未按出现次数和文字 / 符号风险判定。
- expected reference path 与 actual reference path 数量或角色不一致。
- 主要角色数量与 `character_count_expected` 不一致。
- 资产状态不是 ACTIVE 却被下游使用。
- prompt 没有 `prompt_id` 或没有写回提示词映射。
- 后期素材没有绑定 `video_task_id` / `prompt_id` / `dialogue_id`。
- QC 发现断链但仍尝试继续生成。

## 视频提示词 v3 数据中心强制字段（补丁）

每个 video_task_mapping 必须新增并写回：

```text
model_duration_cap_seconds: 15
recommended_duration_seconds: <由 duration_calculation 得出>
final_duration_seconds: <= 15
split_required: true | false
split_from_video_task_id: <如由长任务拆分而来>
split_part_index: <第几段>
split_total_parts: <总段数>
weather_light_context: <时段 / 天气或外部光线 / 室内外组合>
weather_light_context_source: script_explicit | chosen_by_agent | user_confirmed
stage_map_reference_actual: skipped_by_user | path
storyboard_image_reference_actual: skipped_by_user | path
mandatory_requirements_block_status: PASS | FAIL
mandatory_picture_block_status: PASS | FAIL
at_reference_status: PASS | FAIL_PROMPT_AT_REFERENCE_MISSING | FAIL_UNUSED_REFERENCE_ASSET
voice_description_per_shot_status: PASS | FAIL_VOICE_DESCRIPTION_TOO_SHORT
conditional_ban_status: PASS | FAIL_UNCONDITIONAL_AUXILIARY_BAN
```

若 recommended_duration_seconds > model_duration_cap_seconds，必须拆分 video_task_id；不得把 final_duration_seconds 硬压到 15 秒。

每个 prompt 映射必须新增：

```text
duration_calculation_ref
weather_light_context
mandatory_requirements_block_actual
mandatory_picture_block_actual
reference_usage_statement_actual
at_mention_inventory_actual
voice_description_inventory_actual
conditional_ban_inventory_actual
```

`at_mention_inventory_actual` 必须逐项列出最终提示词中所有可见人物、场景、道具是否已 @引用；画外音（VO）、内心独白（OS）与逐字台词内部名称可标记 exempt_dialogue_text。


## 视频提示词 v4 数据字段补丁

每个 prompt 映射必须新增：

```text
scene_requirement_prefix_actual: <@场景方向资产为背景保持方向机位 + 180度轴线固定句>
scene_requirement_prefix_status: PASS | FAIL_SCENE_REQUIREMENT_PREFIX_MISSING
unique_character_ban_actual: <视频全程严禁出现外形、着装、配饰完全相同的两个人...>
unique_character_ban_status: PASS | FAIL_UNIQUE_CHARACTER_BAN_MISSING
spoken_dialogue_style_inventory:
  - dialogue_id:
    speaker:
    speech_type: 画外音（VO） | 内心独白（OS） | 角色对白
    final_prompt_text:
    format_status: PASS | FAIL_SPOKEN_DIALOGUE_AT_EMOTION_MISSING | FAIL_VO_OS_STYLE_MISSING
shot_remark_inventory:
  - shot_id:
    remark_text:
    status: PASS | FAIL_SHOT_REMARK_MISSING
dialogue_pronunciation_rewrite_map:
  - dialogue_id:
    source_text:
    dispatch_text:
    changed_chars:
    rewrite_reason:
    priority_basis:
    preservation_status: source_preserved_dispatch_rewritten | no_rewrite_needed
video_prompt_v4_regression_status: PASS | FAIL_VIDEO_PROMPT_V4_REGRESSION
```

原始 dialogue_table.text 永远保留剧本文本；多音字 / 生僻字替换只进入 dispatch_text，不得覆盖 source_text。


## 资产 v5 数据中心字段补丁

生产数据中心必须新增并贯穿以下字段：

```text
period_world_lock:
  era_dynasty_lock:
  period_region_lock:
  official_rank_role_lock:
  costume_regulation_lock:
  prop_period_lock:
  scene_architecture_period_lock:
  source_basis: script_explicit | inferred_from_context | user_confirmed
  status: PASS | FAIL_PERIOD_LOCK_MISSING

character_variant_prompt_completeness_matrix:
  character_id:
  look_variant_id:
  source_identity_asset_ref:
  identity_anchor_expanded: true | false
  face_structure_3t5e_expanded: true | false
  era_official_lock_consumed: true | false
  costume_state_expanded: true | false
  state_variant_chain_ref:
  prompt_density_equal_to_base: true | false
  status: PASS | FAIL_ASSET_VARIANT_PROMPT_COMPRESSION

prop_state_variant_plan:
  prop_id:
  shared_prop_visual_anchor:
  state_id:
  bound_character_id:
  body_attachment_position:
  scene_placement_position:
  handling_state:
  before_state:
  after_state:
  continuity_keep:
  continuity_change:
  independent_asset_required:
  independent_asset_reason:
  status:

state_variant_chain_ref:
  role: character | scene | prop
  variant_id:
  before_state:
  after_state:
  change_trigger:
  continuity_keep:
  continuity_change:
```

任何下游资产、分镜、视频提示词若消费角色 / 场景 / 道具，必须能追溯到 period_world_lock 与对应 state_variant_chain。
