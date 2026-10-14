# 短剧视频提示词流程

## 目标

把分镜表转成可执行的视频生成任务。视频提示词必须继承 `production_visual_mode`，并与角色 / 场景 / 道具资产模式保持一致。

## 提示词语言硬规则

1. 视频提示词、`prompt_chinese_dispatch`、`prompt_chinese_review`、`prompt`、VIDEO_DISPATCH_PACKAGE 中的可见提示词正文默认必须使用中文。
2. 禁止为了“模型更好理解”把镜头、表演、动作、光影、参考图说明、声音说明、禁令主体写成英文；不得输出中英并列提示词。
3. 用户可见视频提示词文档实行“极限全中文”：字段名、段落标题、镜头正文、声音说明、负面提示、任务包展示层与审阅层都必须中文化；不得出现英文提示词正文或英文禁止词列表。
4. 用户可见视频文档中唯一允许保留的非中文内容：模型名、必要编号、版本号、项目链路 ID、文件路径，以及用户明确要求保留的非中文台词或入画文字。英文参数、英文枚举值、机器 token、英文禁止词只允许存在于内部派单映射层，不得混入用户可见视频提示词正文。
5. 若台词或入画文字本身是用户指定的非中文内容，必须逐字保留；除此之外的动作、表演、镜头、光影、参考图说明、负面提示仍必须使用中文。
6. 历史结构词必须改成中文等价词：`Native audio` 输出为“原生音频”，`Original request` 输出为“原始需求”，`Negative Prompt` 输出为“负面提示”。

## award-winning-performance-prompt融合读取规则

进入任何视频提示词冻结、派单或改写之前，必须读取并消费 `references/actor-performance-voice-integration.md`。视频提示词正文默认采用中文片段镜号格式，不再以旧逐秒段落作为主格式；若需要逐秒动作，可写在镜号行的片段内时间段中。

视频提示词必须消费：

```text
current_active_snapshot_resolved
base_snapshot_id
active_patch_ids
resolved_version_id
character_voice_reference_map
character_look_variant_plan
scene_state_variant_plan
```

若当前 video_task_id 对应的角色造型变体、场景状态变体或角色音色计划未在合成版中出现，不得冻结提示词。

## 生成前检查

每个镜头必须具备：

* 画幅比例。
* 时长。
* 模型。
* 首帧或参考图。
* 角色身份参考。
* 场景方向参考图。
* 场景方向锁：`scene_view_orientation` + `camera_background_lock`。
* 动作与表演。
* 镜头运动。
* 声音归属。
* 表演推导模式：`manual` 或 `auto`，必须来自启动弹窗。
* 语义 6 字段：台词文本、动作提示、场景上下文、人物关系、冲突强度、人物设定。
* 情绪状态坐标：Valence / Arousal 与起承转合情绪曲线。
* FACS / BACS / RACS 推导摘要。
* 4 个校准系数：性格、关系距离、景别适配、调性。
* 最终中文派发 prompt 与全中文审阅版。

## 前置数据依赖硬规则

进入任何视频提示词冻结、派单或改写之前，必须先具备并消费以下上游数据，缺一项即不得冻结：

- `production_visual_mode`
- `global_style_preset_id`
- `global_style_lock`
- `tone_profile_preset_id`
- `tone_profile_lock`
- `style_tone_lock_status`
- `source_script_range`
- `source_dialogue_ids`
- `source_asset_ids`
- `source_scene_id`
- `space_truth_id`（如涉及多人、追逐、争吵、证据揭露或位移）
- `required_character_asset_ids` / `required_scene_asset_ids` / `required_prop_asset_ids`
- `reference_image_paths_expected` / `reference_image_paths_actual`
- `scene_direction_lock`（包含 scene_view_asset_id、scene_view_orientation、camera_background_lock）
- `storyboard_order_composition_action_data`
- `cross_video_continuity_ref`（如存在相邻视频任务）
- `audio_owner` 与 `verbatim_dialogues`
- `current_active_snapshot_resolved`、`base_snapshot_id`、`active_patch_ids`、`resolved_version_id`
- `character_voice_reference_map`
- `character_look_variant_plan` 与当前 video_task_id 匹配的 `look_variant_id`
- `scene_state_variant_plan` 与当前 video_task_id 匹配的 `scene_state_variant_id`
- `model` / `aspect_ratio` / `duration`

若任何一项由上游未登记、未写回、状态非 PASS / ACTIVE / frozen、数量不一致或路径不一致，则 `reference_lock_status` 或 `status` 不得标记为 PASS / frozen / dispatched，必须回到资产、分镜或后期上游阶段补齐后再继续。

## 生产视觉模式继承

```text
production_visual_mode: cinematic_realistic | top_chinese_3d_animation_cg
```

- 写实真人模式：视频开头为“生成<实际段数>段连贯的超写实电影质感剧情视频：”。
- 3D 动画 CG 模式：视频开头为“生成<实际段数>段连贯的国漫顶级3D动画CG电影质感剧情视频：”。
- 3D 动画 CG 模式下，不得在视频 prompt 中写 real human、photorealistic、真人摄影、真人皮肤、毛孔等词；角色描述必须沿用动画 CG 角色资产参考图。
- 写实真人模式必须同时继承 `STYLE-REAL-*` 与 `TONE-REAL-*`，并完整展开 `global_style_lock` 与 `tone_profile_lock` 正文，允许且要求保留真人皮肤、毛孔、ARRI、Cooke 等真人摄影词。
- 3D 动画 CG 模式必须同时继承 `STYLE-ANIM-CG-*` 与 `TONE-ANIM-CG-*`，并完整展开 `global_style_lock` 与 `tone_profile_lock` 正文，禁止混入写实真人风格 / 影调预设。

## 摄影方案矩阵依赖硬规则

进入任何视频提示词冻结、改写、反推或派发前，必须读取并消费神笔制作内部文件 `references/cinematography-profiles.md`。该文件是本 Skill 内部 reference，不是外部 Skill。

每个视频任务必须从 `cinematography-profiles.md` 的 10 套院线电影级摄影方案中选择 1 套，并写入：

```text
cinematography_profile_id: <01-10>
cinematography_profile_name: <方案名>
cinematography_profile_selection_reason: <题材 + 情绪 + 场景空间匹配理由>
cinematography_profile: <可派发摄影参数>
```

## 视频提示词表演推导模式

### 启动弹窗：手动调整 / 自动调整

每次进入视频提示词冻结、改写、反推或派发前，必须先用弹窗询问本次采用哪种模式。没有用户选择，不得冻结最终提示词。

```text
问题：本次视频提示词表演推导模式？
A. 手动调整（推荐给高风险 / 高精度任务）：每个关键参数、每个创作决定都通过弹窗让我选择。
B. 自动调整（推荐给效率优先任务）：agent 从上级制作链路数据、剧本台词和分镜数据中自动推导，使用推荐选择直接生成，并在任务包中记录 chosen_by_agent。
```

### 自动调整

自动调整不跳过推导。agent 必须从上游制作链路数据和剧本台词推导所有参数，使用推荐值直接写入提示词，并在 VIDEO_DISPATCH_PACKAGE 中记录：

```text
performance_adjustment_mode: auto
selection_policy: chosen_by_agent
manual_confirmation_required: false
```

## 四层表演推导链

视频提示词中的表演细节必须从剧本与上游数据推导，不得凭空堆砌。推导链为：

```text
文本语义 → 情绪状态 → 生理反应 → 外显动作
```

底层支撑三个专业体系：

1. FACS（面部动作编码系统）：管脸，包括眼、眉、眼睑、鼻翼、嘴唇、下颌、面部肌肉 AU。
2. BACS（躯体微反应编码系统）：管身体，包括肩颈、胸腔、脊柱、手指、重心、步态、身体收缩或舒展。
3. RACS（呼吸节律编码系统）：管呼吸，包括屏息、浅快呼吸、哽咽吸气、鼻息、呼气长度、胸式或腹式呼吸。

## 场景方向锁定硬规则

视频提示词必须继承资产阶段的场景方向锁：

```text
scene_direction_lock:
  scene_view_asset_id: <场景方向资产编号>
  scene_view_orientation: front | reverse | left | right | top | keylight
  camera_background_lock: <使用该场景图时全部镜头必须遵循的背景机位方向>
  scene_view_ref_image_path: <真实路径>
```

规则：

- 使用正面场景图：本视频任务所有镜头必须遵循正面背景机位；可写正面机位、过肩正面、前景遮挡正面背景、浅景深前景实背景虚，但不得写成反向背景。
- 使用反向场景图：本视频任务所有镜头必须遵循反向背景机位。
- 使用左侧 / 右侧场景图：本视频任务所有镜头必须遵循对应侧向背景机位。
- 使用俯视 / 鸟瞰场景图：只用于空间理解或用户授权的舞台定位，不作为普通人物表演背景。
- 使用关键机位光影图：只用于对应关键机位，不得泛化。

若一个视频任务内需要多个背景方向，必须在上游拆成多个 `scene_view_asset_id` 或多个 video_task，不得用单张方向图硬写其它方向镜头。

## 空间坐标自然语言规则

视频提示词中的 `stage_map_coordinate_data_actual` 不再使用 `[x,y]` 数字坐标格式，也不写色块、箭头、形状编码、坐标网格。必须写成自然语言：

```text
stage_map_coordinate_data_actual:
  coordinate_system_description: 100×100 顶视空间理解，以自然语言表达，不输出数字坐标。
  characters_position_natural_language:
    - 角色A位于画面左侧约三成区域，靠近前景，面向画面中央的角色B。
  props_position_natural_language:
    - 道具P01位于画面中央偏前的桌案上，角色A右手可触及。
  eyeline_map:
    - 角色A视线指向画面右后方入口。
  movement_paths:
    - 角色B从画面右后方入口走向画面中央，停在角色A前方半步距离。
```

不得写“红色圆形”“蓝色方块”“箭头”“[15,30]”“xy: [15,30]”“坐标网格”。

## 单镜提示词结构

* 任务类型：图生视频或文生视频。
* model：指定模型。
* aspect_ratio：与项目一致。
* duration：按镜头节奏设置。
* reference_image_paths：首帧、角色、场景方向图、道具。
* production_visual_mode：继承项目模式。
* scene_direction_lock：场景方向资产 + 背景机位锁。
* 画面描述：主体、场景、动作。
* 表演描述：必须由四层推导链生成。内部可使用 FACS / BACS / RACS 计算，但最终用户可见提示词、prompt_chinese_dispatch、沙盒提示词和真实派发 prompt 必须全部转换为自然语言面部、躯体、呼吸描述，不得直接出现 FACS / BACS / RACS 或 AU 编码字样。
* 镜头描述：每段都必须写景别、机位、运镜、焦段 / T 值或浅景深倾向、景别适配系数；机位必须服从 `camera_background_lock`。
* 光影描述：必须采用双层结构；开头集中写从 `cinematography-profiles.md` 选定的 `Cinematography profile:`，每个逐秒 / 短分段再写本段镜头参数、光源方向、环境反光 / 阴影 / 动态光、景深和人物面部稳定性。
* 声音描述：如果使用原生音频，写明台词、环境声、音乐风格；如果声音外部生成，写“无原生对白”。
* 输出语言：最终派发 prompt 必须直接用中文；台词和用户指定的入画文字必须逐字保留原语言。
* 原始需求：带上用户原始需求或已消解后的自包含需求。

## 声音分工规则

同一类声音只交给一个 owner：

* 视频模型原生音频：适合短单镜、现场对白、环境声一体生成。
* speech：适合旁白、稳定台词、多角色配音。
* music：适合 BGM、主题曲、片尾曲。
* editing：只负责合成、混音、口型同步、拼接。

不要同时让视频模型生成台词，又让 speech 生成同一句台词。不要每个镜头都生成一段新 BGM；整支片子的 BGM 通常生成一次，再剪辑适配。

## reference count lock

视频提示词阶段必须执行参考图数量锁。每个 `prompt_id` 必须登记：

```text
prompt_id
video_task_id
shot_id 或 panel_id
reference_image_paths_expected: []
reference_image_paths_actual: []
reference_count_expected: <数字>
reference_count_actual: <数字>
reference_roles_expected: [character, scene_view, prop, first_frame, stage_map_optional, storyboard_image_optional]
storyboard_data_expected: storyboard_order_composition_action_data
reference_roles_actual: []
missing_reference_paths: []
extra_reference_paths: []
scene_direction_lock_expected: <scene_view_asset_id + scene_view_orientation + camera_background_lock>
scene_direction_lock_actual: <scene_view_asset_id + scene_view_orientation + camera_background_lock>
reference_lock_status: PASS | FAIL
```

硬规则：

- `reference_count_expected` 必须等于上游分镜 / 资产包要求的数量。
- `reference_count_actual` 必须等于实际派单传入数量。
- 少传、乱序、错角色、错场景方向、错道具、用非 ACTIVE 资产替代，都必须 `reference_lock_status: FAIL`。
- 引用场景图时，必须同时继承 `scene_direction_lock`，用于说明该场景参考图的背景机位方向。
- 引用道具图时，只说明单个道具用途，不得逐色说明，不得提九宫格。
- FAIL 时不得派发视频生成任务，必须回到资产或分镜阶段修复。

## VIDEO_DISPATCH_PACKAGE

每个视频任务必须把最终派发内容冻结为可复制的任务包，不得只写“按上文”“参考分镜”“同前”。`global_style_lock` 与 `tone_profile_lock` 必须完整展示配置正文，不得只写预设 ID、不得只在首个任务完整展示后续省略。

```text
[VIDEO_DISPATCH_PACKAGE]
prompt_id:
video_task_id:
base_snapshot_id:
active_patch_ids:
resolved_version_id:
current_active_snapshot_resolved_status:
source_scene_id:
source_dialogue_ids:
production_visual_mode:
global_style_preset_id:
global_style_preset_name:
global_style_lock:
tone_profile_preset_id:
tone_profile_preset_name:
tone_profile_lock:
style_tone_lock_status:
verbatim_dialogues:
  - dialogue_id:
    speaker:
    text: <逐字台词>
    preservation:
required_character_asset_ids:
required_character_look_variant_ids:
required_scene_asset_ids:
required_scene_state_variant_ids:
required_prop_asset_ids:
character_voice_reference_map:
reference_image_paths_actual:
reference_roles_actual:
scene_direction_lock_actual:
  scene_view_asset_id:
  scene_view_orientation:
  camera_background_lock:
  scene_view_ref_image_path:
stage_map_reference_actual: optional_not_recommended | skipped_by_user | path
stage_map_coordinate_data_actual: <100×100 自然语言空间描述，不使用 [x,y] 数字坐标，不写色块箭头>
storyboard_order_composition_action_data_actual: <景别、机位、运镜、构图、动作起止、转场 / 动作尾势；数据继承，不作为参考图路径；必须融合进正式视频 prompt>
cross_video_continuity_ref:
shot_or_panel_id:
character_count_expected:
model:
aspect_ratio:
duration:
generate_audio:
audio_owner:
performance_adjustment_mode: manual | auto
selection_policy: chosen_by_user | chosen_by_agent
manual_confirmation_required: true | false
semantic_input_fields:
subtext_coefficient:
emotion_state:
emotion_curve:
facs_map:
bacs_map:
racs_map:
calibration_coefficients:
cinematography_profile_id:
cinematography_profile_name:
cinematography_profile_selection_reason:
cinematography_profile:
prompt_chinese_dispatch:
prompt_chinese_review:
prompt:
[/VIDEO_DISPATCH_PACKAGE]
```

`prompt` 字段必须展开当前镜头所需全部信息，不能依赖聊天历史、上一个镜头或外部解释。若使用舞台定位图或黑白分镜图，必须说明它们仅为用户授权的制作参考；默认不生成、不传入。

## 提示词映射写回硬规则

每个最终提示词必须写回生产数据中心的提示词映射：

```text
prompt_id
video_task_id
source_script_range
source_dialogue_ids
source_asset_ids
global_style_preset_id
global_style_lock
tone_profile_preset_id
tone_profile_lock
style_tone_lock_status
source_stage_map: optional_not_recommended | skipped_by_user | path
source_stage_map_coordinates: natural_language_100x100_space_description
source_storyboard_image: optional_not_recommended | skipped_by_user | path
source_storyboard_data: storyboard_order_composition_action_data
scene_direction_lock_actual
reference_image_paths_expected
reference_image_paths_actual
audio_owner
verbatim_lock: true | false
status: frozen | dispatched | needs_fix
```

只有 `status: frozen` 且 `reference_lock_status: PASS` 的提示词可以派发。派发后改为 `dispatched`，不得在未记录变更的情况下临场改写。

## 中文片段镜号格式视频提示词骨架

当视频任务需要把角色参考、场景方向图、场景状态变体图、角色造型变体图、道具参考等多类参考图共同传入时，`prompt` 不得只写剧情概要，必须在提示词开头逐项说明每张参考图的用途、引用边界和禁止继承内容。参考图说明必须来自生产数据中心资产池、`current_active_snapshot_resolved`、`scene_direction_lock`、`space_truth_id`、自然语言空间描述和 `reference_image_paths_actual`，不得临场编造。

正式 prompt 默认使用中文片段镜号格式：

```text
第 <片段序号> 段视频片段完整提示词
[画面美学风格]：<完整继承 global_style_lock、tone_profile_lock、cinematography_profile>
[环境光影]：<继承 scene_state_variant_id 的时间、天气、季节、受损、光源状态>
[人物站位]：<继承 space_truth_id 与 100×100 自然语言空间描述>
[内容概述]：<本片段剧情事件>
[情绪氛围]：<情绪曲线、冲突强度、人物关系>
[衔接参考首帧]：<cross_video_continuity_ref 或开场状态>
[要求]：<180度轴线、视线匹配、物理真实、production_visual_mode 质感要求>
镜号：<连续镜号> | 场次：<时间/地点> | @<场景名> | <片段内时间段> | <景别> | <运镜> | ( @<角色名> <站位/姿态 + look_variant_id> ) <动作、物理细节、自然微表情、环境互动> | 台词 & 音效：<若启用音色参考，写 @<角色名>严格使用@<角色名音频1><voice_description_text>。<说话方式>:{逐字台词}> | 备注：<道具 / 情绪 / 衔接>
[片段结尾：全局画质与渲染后缀]
[下一片段继承点]
【角色严格按照台词说话，不要增加台词或减少台词】
[禁令]
```

旧逐秒 / 短分段规则只作为镜号行内部动作密度要求，不再替代中文片段镜号主格式。

`prompt_chinese_dispatch` / `prompt` 字段必须直接用中文创作并按固定结构展开，不得先写英文稿再翻译。`prompt_chinese_review` 必须在 `prompt_chinese_dispatch` 完成后，由其完整整理成中文审阅版，不得摘要、删减、合并、改写结构或只保留重点。

若因历史兼容需要保留旧分段结构，固定结构如下；但正式冻结版仍必须以中文片段镜号格式为主，旧结构只能作为内部展开密度参考：

1. **视频开场行**：
   - 写实真人模式：`生成<实际段数>段连贯的超写实电影质感剧情视频：`
   - 3D 动画 CG 模式：`生成<实际段数>段连贯的国漫顶级3D动画CG电影质感剧情视频：`
2. **全局风格锁**：第二段必须写 `全局风格锁：<从 references/style-tone-presets.md 继承的 global_style_lock 完整正文>`，不得只写 `global_style_preset_id`，不得在后续镜头写“同上”。
3. **影调配置锁**：第三段必须写 `影调配置锁：<从 references/style-tone-presets.md 继承的 tone_profile_lock 完整正文>`，不得只写 `tone_profile_preset_id`，不得在后续镜头省略。
4. **统一摄影参数**：第四段必须写 `统一摄影参数：<来自 cinematography-profiles.md 的可派发摄影参数正文>`。
5. **参考图用途声明**：逐项说明 `@角色.png`、`@场景方向图.png`、`@道具.png` 的用途。场景图必须说明 `scene_view_orientation` 与 `camera_background_lock`，例如“用 @灵堂-正面.png 作为场景正面背景参考，本视频所有镜头必须遵循正面背景机位”。道具图只说明单个道具外观，不得逐色说明，不得提九宫格。
6. **表演推导声明**：用中文写入本镜头表演推导结果，必须融合 `semantic_input_fields`、`subtext_coefficient`、`emotion_curve`、`FACS / BACS / RACS` 和 4 个校准系数。
7. **逐秒或短分段剧情动作**：默认按 1-1.5 秒高密度短分段组织；每段必须直接使用 `@资产路径` 引用主体与道具，并保留自然语言空间位置与 `cross_video_continuity_ref`。每段必须写完整：镜头景别、机位、运镜、焦段 / T 值或浅景深倾向、角色位置、手部 / 眼神 / 肩颈 / 重心 / 呼吸 / 肌肉反应、显式 FACS 面部动作、显式 BACS 躯体微反应、显式 RACS 呼吸节律、道具动作、光源方向、环境反光 / 阴影 / 动态光、环境物互动、声音触发点、段尾静止时间。镜头机位必须服从 `camera_background_lock`。
8. **原生音频固定结尾块**：逐秒段落之后必须写“原生音频：”块。若 `generate_audio: on`，该块必须逐字写出人物对白原文、环境音、音效、是否有 BGM，并明确不重复生成 speech / music。
9. **最终禁止项结尾块**：最后一段必须明确最终视频不得出现字幕、标题卡、花字、参考图标签、UI、水印、舞台坐标网格、色块、箭头、黑白分镜质感、草图线条、分镜边框或白底分镜背景。3D 动画 CG 模式还必须禁止 real human、photorealistic、metahuman、skin pores、真人摄影、真人皮肤质感。

### prompt 示例骨架

```text
生成 <实际段数> 段连贯的<按 production_visual_mode 填写>剧情视频：

全局风格锁：<完整展开 global_style_lock 正文；写实真人模式继承 STYLE-REAL-*，3D 动画 CG 模式继承 STYLE-ANIM-CG-*；不得只写预设 ID，不得写同上>。

影调配置锁：<完整展开 tone_profile_lock 正文；写实真人模式继承 TONE-REAL-*，3D 动画 CG 模式继承 TONE-ANIM-CG-*；不得只写预设 ID，不得省略>。

统一摄影参数：<从 cinematography-profiles.md 选定的摄影参数>。

用 @<main_character_reference>.png 作为 <character_name> 的身份参考。
用 @<scene_view_reference>.png 作为 <scene_name> 的 <scene_view_orientation> 场景背景参考；本视频所有镜头必须遵循 <camera_background_lock>，不得临场改变为其它方向。
用 @<prop_reference>.png 作为 <prop_name> 道具外观参考。

空间与调度：以 100×100 顶视空间理解，但用自然语言表达。<角色A> 位于画面左侧约三成区域，面向画面中央；<道具P01> 位于画面中央偏前的桌案上；<角色B> 从画面右后方入口走向中央。不得在最终视频中生成任何坐标网格、色块、箭头或标注。

表演推导：根据 semantic_input_fields、subtext_coefficient、emotion_curve、FACS、BACS、RACS 和 calibration_coefficients 推导表演细节。不要把它孤立成分析报告；下面每个时间段都必须显式带上 FACS / BACS / RACS、镜头设计、光影、环境互动和声音触发点。

0-1.5 秒：<机位必须服从 camera_background_lock + 直接 @character / @prop 路径引用 + 自然语言空间位置 + FACS + BACS + RACS + 光源方向 + 环境物互动 + 声音触发点>。
1.5-3 秒：<保持同等密度，不得写同上>。
3-4.5 秒：<保持同等密度，不得压缩>。
按真实剧情节奏继续以 1-1.5 秒高密度短分段展开。

原生音频：<逐字对白、环境音、道具音、呼吸声、静默停顿和 BGM 策略>。

最终视频不得生成字幕、标题卡、花字、参考图标签、UI、水印、舞台坐标网格、色块、箭头、黑白分镜质感、草图线条、分镜边框或白底分镜背景。若 production_visual_mode 为 top_chinese_3d_animation_cg，最终视频不得生成 real human、photorealistic、metahuman、skin pores、真人摄影、真人皮肤质感。
```

## 台词派发硬规则

- `verbatim_required` 的对白必须逐字进入 `verbatim_dialogues`。
- 如果视频模型原生音频负责台词，prompt 中的台词必须逐字写出。
- 如果 speech 负责台词，视频 prompt 必须写“无原生对白”，并保留对应 `dialogue_id` 给后期合成。
- 不得为了镜头时长删台词；应拆分 `video_task_id` 或改由 speech 承载。
- 风险替代只处理危险动作和画面，不得替换、弱化或删除对白。

## 禁止事项

* 不主动生成字幕、标题卡、花字。
* 不把参考图描述成必须逐像素复制。
* 不在单镜里塞太多动作。
* 不改变已锁定的角色身份。
* 不让同一角色在同场景里左右关系乱跳。
* 不使用场景正面图写反向背景机位。
* 不提场景六视图、六宫格、道具九宫格、颜色框逐色说明。
* 不在默认流程中传入舞台定位图或黑白分镜图，除非用户明确授权。


## 用户可见视频提示词模板 v2（强制补丁）

本节覆盖旧版提示词骨架中不利于模型遵循的写法。旧规则若与本节冲突，以本节为准。

### 固定段落顺序
最终 prompt_chinese_dispatch、prompt、沙盒提示词和真实派发提示词必须按以下顺序展开：开场行 → [电影质感] → [画面美学风格] → [环境光影] → [人物站位] → [内容概述] → [情绪氛围] → [衔接参考首帧] → [参考素材] → [要求] → 镜号行 → [画面] → [片段结尾] → 【角色严格按照台词说话，不要增加台词或减少台词】 → [禁令]。

### [电影质感] 必填
[电影质感] 必须紧跟开场行，是模型风格锚定第一段。3D 动画 CG 模式优先写可见视觉效果，例如“大师级人物剧情片摄影质感，虚拟大画幅摄影机，温润定焦镜头，低饱和自然对比，自然电影感运动模糊，克制自然的室内明暗层次，窄空间近景构图，营造轻微压迫感，重视面部微表情、手部动作和人物情绪细节”。写实真人模式允许摄影机 / 镜头型号，但必须中文化为画面效果，例如“ARRI Alexa Mini LF 摄影机质感，库克镜头暖调柔和高光光晕，50mm 定焦 f/2.8，3200K 暖色温，电影级景深，柔和焦外虚化，自然镜头呼吸感，弱光戏剧化对比”。

### FACS / BACS / RACS 自然语言化输出
FACS / BACS / RACS 只允许保留在内部推导字段中。最终 prompt、prompt_chinese_dispatch、用户可复制提示词和沙盒提示词中禁止出现 FACS、BACS、RACS、AU 编码等字样，必须转换成自然语言：平静专注=面部肌肉放松，眼睑平稳，眉头舒展，下颌自然闭合；端正松弛=肩颈自然下沉放松，脊背挺直不僵硬，双肩平齐；平稳浅呼吸=胸腹起伏微弱平缓，呼吸节律均匀，肩部无明显晃动。

### 时间段与天气词汇规则
镜号中的场次不得只写单字“夜”。必须写高权重时段词：凌晨、清晨、早晨、中午、下午、傍晚、夜晚、深夜。天气必须按场景写入，例如室内小雨写“窗外小雨、窗外细雨、室外小雨室内暖光、玻璃外飘着小雨”；阴天室内写“窗外阴天、室外阴云室内柔和天光”；晴天室内写“窗外晴天、阳光透窗、室外晴天室内柔光”。

### VO / OS 写法
所有 VO 必须写为“画外音（VO）”。所有 OS 必须写为“内心独白（OS）”。人物说出口的台词沿用角色名 + 说话方式 + {逐字台词}。

### 参考素材裁剪规则
[参考素材] 与 reference_image_paths_actual 只允许包含当前视频任务和镜号实际用到的角色、场景、道具、动作或音频参考。镜号中没有提及、画面中不会出现、不会被角色触碰或不会作为信息点展示的道具，不得生成资产图，不得写入参考素材，不得传入视频模型。

## 视频时长与镜号数量科学计算（强制补丁）
不得先固定 10-15 秒再塞台词。每个 video_task_id 必须先计算 duration_calculation，再冻结 duration 与镜号数量。duration_calculation 必须包含：source_dialogue_ids、spoken_text_breakdown、silent_performance_beats、empty_shot_or_prop_reading_time、action_complexity_time、cinematography_pacing_profile_id、pacing_multiplier、subtotal_seconds_before_multiplier、total_seconds_after_multiplier、recommended_duration_seconds、recommended_shot_count、shot_duration_distribution、split_required、split_reason。
语速基准：普通短剧清晰语速每秒 4-5 个中文字；克制文戏、低声质问、压抑旁白每秒 3-4 个中文字；情绪迟疑、哽咽、儿童、喘息明显每秒 2.5-3.5 个中文字。关键对白前后保留 0.4-1.2 秒表演留白；证据揭露、读屏、抬眸、屏息、转身、抢夺等关键节拍保留 1-3 秒；文字道具读屏至少 1.5-2.5 秒；连续动作 2-4 秒。人物剧情片 / 家庭生活流 / 物哀日常节奏系数 1.15-1.35；暗黑复仇 / 悬疑惊悚 / 阶层类型片 1.05-1.25；动作 / 警匪 / 追逐 0.85-1.10；史诗 / 仪式 / 大场面 1.20-1.50。若计算总时长超过模型舒适时长，必须拆成多个 video_task_id；禁止删台词、压缩台词、让人物高速说话或牺牲表演留白。


## 视频提示词模板 v3 防漏字段与防压缩规则（最高优先级补丁）

本节优先级高于本文件所有旧模板。任何视频提示词、沙盒视频提示词、prompt_chinese_dispatch、真实派发 prompt 均必须执行。

### [要求] 固定句强制写入
每个视频提示词的 [要求] 段必须逐字包含：严格遵守180度轴线与视线匹配原则，严防越轴跳切。画面干净又高级；画面里前中远景递进关系分明。极具影视写实感与物理细节真实感。
该固定句不能被概括、改写、压缩、移动到 QC 或任务包字段中；必须出现在最终可复制提示词正文。

### [画面] 固定块强制写入，按视觉模式双版本
每个视频提示词必须包含 [画面] 段。
写实真人模式固定块：无水印，无字幕，无logo，无背景音乐。电影级光影，8K写实，人物皮肤纹理清晰，面部微表情舒展克制，无夸张神态；体态端正放松，肢体无僵直感；步态平稳协调；搭配眨眼、轻呼吸、手指微动等低幅度无意识小动作，真实肢体动作，电影质感，专业影视摄影。
3D 动画 CG 模式等价固定块：无水印，无字幕，无logo，无背景音乐。电影级光影，8K级精细CG渲染，CG角色材质细节清晰，陶瓷化SSS皮肤shader干净通透，无真实皮肤纹理，面部微表情舒展克制，无夸张神态；体态端正放松，肢体无僵直感；步态平稳协调；搭配眨眼、轻呼吸、手指微动等低幅度无意识小动作，真实肢体动作，电影质感，专业影视摄影。
3D 动画 CG 模式严禁直接写“人物皮肤纹理清晰”或“8K写实”作为最终画面块；必须使用上面的 CG 等价块，避免与3D模式禁令冲突。

### 单段视频 15 秒硬上限
当前视频模型单段上限为 15 秒。生产数据中心必须登记 model_duration_cap_seconds: 15。任何 duration_calculation 得出的 recommended_duration_seconds 若大于 15，必须拆分为多个 video_task_id，每个 video_task_id 的 duration ≤ 15 秒。禁止用提高语速、删减台词、压缩表演留白、合并镜号来硬塞进 15 秒。该规则预留未来缺口：当模型支持更长时，只允许通过修改 model_duration_cap_seconds 调整。

### 天气字段强制落地
每个 video_task_id 必须有 weather_light_context 字段，并在 [环境光影] 与每个镜号的 场次 中落地。禁止只写“室内暖光”而不写外部天气 / 光线来源。室内必须写类似“夜晚 / 窗外小雨室内暖光”“夜晚 / 窗外阴天室内暖光”“下午 / 窗外阴天室内柔和天光”；若剧本未给天气，agent 必须按场景情绪选择一个合理天气并登记 weather_light_context_source: chosen_by_agent。

### @引用强制规则
最终视频提示词中，只要画面动作、镜号描述、[人物站位]、[内容概述]、[参考素材]、[要求]、[画面]、[片段结尾] 提及具体人物、场景、道具，并且该人物 / 场景 / 道具在画面中可见、被触碰、被读屏、作为证据点或空间背景使用，就必须使用 @名称 引用。例：@宋知、@江咎、@江家客厅、@白衬衫口红印、@设计图纸、@匿名消息手机。
例外：如果人物、场景、道具名称只出现在画外音（VO）、内心独白（OS）或角色逐字台词内部，则不强制 @ 引用。
若镜号中提到道具但没有 @ 道具，标记 FAIL_PROMPT_AT_REFERENCE_MISSING。若 [参考素材] 列出道具但镜号未使用，标记 FAIL_UNUSED_REFERENCE_ASSET。

### 有文字 / 符号 / 读屏道具强制生成
任何道具只要出现可读文字、符号、数字、备注、消息、书名、图纸项目名、印章、logo式图样、准确标记，哪怕只出现一次，也必须生成单独道具资产并写入 reference_image_paths_actual；不能因为出现次数少跳过。若镜号要求读屏，必须预留 1.5-2.5 秒读屏时间，并 @引用对应道具。

### 每镜音色三句描述
每个镜号内，某角色首次发生画外音（VO）、内心独白（OS）或说出口台词之前，必须写不少于3句完整音色描述句。音色描述必须包含音高/厚薄、气息/共鸣、语速/情绪控制三个维度，且不能写“同上”“延续前句”“保持前述音色”。同一镜号内同一角色后续连续台词可不重复三句；跨镜号必须重新写。

### 条件化禁令
[禁令] 分为通用禁令与辅助图禁令。通用禁令始终写：最终视频不得生成字幕、标题卡、花字、参考图标签、UI、水印、logo、白底背景；不得改变角色身份、服装、站位关系和关键道具位置。
只有当 stage_map_reference_actual != skipped_by_user 时，才写舞台定位图相关禁令：不得出现舞台坐标网格、色块、箭头、形状编码、坐标标注。
只有当 storyboard_image_reference_actual != skipped_by_user 时，才写黑白分镜图相关禁令：不得出现黑白分镜质感、草图线条、分镜边框、白底分镜背景。
如果用户选择不制作舞台定位图和黑白分镜图，最终提示词不得写这些辅助图禁令。

### 防后续压缩与完整性矩阵
所有视频任务的提示词字段密度必须等同，不允许首段完整、后续段落压缩。每个 video_task_id 都必须独立完整写出 [电影质感]、[画面美学风格]、[环境光影]、[人物站位]、[内容概述]、[情绪氛围]、[衔接参考首帧]、[参考素材]、[要求]、镜号、[画面]、[片段结尾]、台词保真禁令、[禁令]、duration_calculation、reference_usage_statement_actual。不得使用“同上、按前文、延续上段、参考前面、保持一致”等承接关键字段。


## 视频提示词模板 v4：场景机位、人物唯一性、台词情绪、备注与读音（最高优先级补丁）

本节优先级高于本文件所有旧模板。若旧模板示例与本节冲突，以本节为准。

### [要求] 场景方向前缀
[要求] 段必须以场景方向引用开头：

```text
[要求]：@<场景方向资产名>为背景保持<方向>机位，严格遵守180度轴线与视线匹配原则，严防越轴跳切。画面干净又高级；画面里前中远景递进关系分明。极具影视写实感与物理细节真实感。
```

例如：

```text
[要求]：@江家客厅-夜晚正面为背景保持正面机位，严格遵守180度轴线与视线匹配原则，严防越轴跳切。画面干净又高级；画面里前中远景递进关系分明。极具影视写实感与物理细节真实感。
```

不得只写“所有镜头遵循正面背景机位”而不在 [要求] 首句 @引用场景方向资产。

### [禁令] 人物唯一性固定首句
[禁令] 必须以人物唯一性禁令开头：

```text
[禁令]：视频全程严禁出现外形、着装、配饰完全相同的两个人;杜绝双胞胎或分身效果，确保同一时刻画面中该人物唯一，<继续写当前模式禁令与条件化辅助图禁令>。
```

3D 动画 CG 模式必须继续写：不得出现真人实拍感、数字人质感、真实皮肤毛孔、真人摄影、真人肖像、真实皮肤质感。
舞台定位图和黑白分镜图相关禁令仍按 v3 条件化规则执行；未启用时不得写。

### 说出口台词必须 @角色 + 情绪 / 动作 / 语气 + 说
所有非画外音（VO）、非内心独白（OS）的说出口台词，必须写为：

```text
@角色<情绪 / 动作 / 语气>说：{逐字台词}
```

示例：

```text
@宋知错愕地低声说：{出轨？}
@江咎强装镇定地低声辩解说：{老婆，你知道的应酬场合乱七八糟的，你别太敏感。}
```

禁止写成“宋知：{出轨？}”“江咎：{嗯。}”。画外音必须写“@角色 + 三句音色描述 + 角色画外音（VO）：{台词}”。内心独白必须写“@角色 + 三句音色描述 + 角色内心独白（OS）：{台词}”。

### 每镜备注强制保留
每个镜号行末尾必须有：

```text
| 备注：<剧情功能 / 情绪功能 / 证据点 / 衔接功能>
```

备注用于保留导演意图，不得省略，不得只在首镜写，不得合并进动作正文。若没有备注，标记 FAIL_SHOT_REMARK_MISSING。

### 多音字 / 生僻字派发替换规则
对白保真表保留原始文本；派发层可为了读音正确生成 dispatch_text。替换优先级：剧本剧情描述 ＞ 文字词语用法正确性 ＞ 日常常用读音 ＞ 姓名字多用文字读音。

每个替换必须写入：

```text
dialogue_pronunciation_rewrite_map:
  - dialogue_id:
    source_text:
    dispatch_text:
    changed_chars:
    rewrite_reason:
    priority_basis:
    preservation_status: source_preserved_dispatch_rewritten
```

禁止直接覆盖 source_text。若台词中没有多音 / 生僻 / 易错读字，则 dispatch_text = source_text，并标记 no_rewrite_needed。

### v4 回归防护
最终提示词必须通过：
- [要求] 场景方向 @前缀存在。
- [禁令] 人物唯一性首句存在。
- 所有说出口台词均为 @角色 + 情绪/动作/语气 + 说。
- 每个镜号都有备注。
- 多音字 / 生僻字有派发替换记录或 no_rewrite_needed。
任一失败，标记 FAIL_VIDEO_PROMPT_V4_REGRESSION，不得冻结或派发。


## 视频景别优先级与前景虚化规则（资产 v5 补丁）

视频提示词阶段必须继承分镜阶段的 shot_scale_decision_reason，并再次执行景别优先级检查。默认优先大特写、特写、近景、中景；优先使用前景对焦加背景高虚化、前景实背景虚、浅景深压迫构图来服务人物表演和证据点。

剧本中的全景、远景、大远景视觉备注不能直接覆盖 Skill 规则。只有 strong_story_need 为真时，才允许使用远景、全景、大远景。否则必须改写为中景以下景别，并记录 rewrite_from_script_visual_note: true。

若最终 prompt 出现远景、全景、大远景但没有 strong_story_need，标记 FAIL_SHOT_SCALE_PRIORITY_OVERRIDE，不得冻结或派发。


### 双模式强制适用与剧本视觉备注降权

本视频景别规则同时适用于 `cinematic_realistic` 写实真人模式与 `top_chinese_3d_animation_cg` 3D 动画 CG 模式。最终视频提示词不得因为 3D 动画 CG 风格而默认增加全景、远景、大远景。剧本视觉备注只作为剧情信息来源，不能覆盖 Skill 的镜头执行优先级。

最终 prompt 生成前必须逐镜检查：若镜号包含全景、远景、大远景，则必须存在 `strong_story_need: true` 与具体原因；否则必须改写为大特写、特写、近景、中景，或前景对焦加背景高虚化构图，并登记 `rewrite_from_script_visual_note: true`。

