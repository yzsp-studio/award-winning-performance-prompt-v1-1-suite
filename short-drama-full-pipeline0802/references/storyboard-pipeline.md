# 短剧分镜与舞台定位

## 总原则

多人戏先定空间，再定镜头。不要让角色在不同镜头中左右关系随机变化。

本文件不再默认生成舞台定位图或黑白分镜图。默认只产出数据：空间真值、镜头表、分镜数据、跨视频连续性和视频提示词所需的构图 / 动作 / 运镜字段。

## 分镜阶段启动弹窗（强制）

进入分镜阶段前，必须用 `question` 工具询问用户是否生成以下可视化辅助图。两个选项都不推荐：

```text
问题 1：是否生成舞台定位图？
A. 不生成，只写空间真值与 100×100 自然语言坐标描述（推荐）
B. 生成舞台定位图，仅作为制作参考，不进入最终画面

问题 2：是否生成黑白分镜图？
A. 不生成，只写分镜数据并融合进视频提示词（推荐）
B. 生成黑白分镜图，仅作为制作参考；如要进入视频参考图必须再次确认
```

若用户选择不生成，仍必须写完整空间真值与分镜数据。若用户选择生成，仍不得在最终视频画面中生成坐标网格、色块、箭头、形状编码、文字标注、框线、UI、黑白线稿、白底、草图线条或分镜质感。

## 场景方向锁定

分镜阶段必须继承生产数据中心中的：

```text
scene_view_orientation_required
scene_view_asset_id
scene_view_ref_image_path
camera_background_lock
```

每个镜头的机位、构图和角色调度必须遵循当前场景资产方向：

- 正面图：镜头以正面为背景机位，不得写成反向背景。
- 反向图：镜头以反向为背景机位。
- 左侧图：镜头以左侧为背景机位。
- 右侧图：镜头以右侧为背景机位。
- 俯视 / 鸟瞰图：只用于空间理解或用户授权的舞台定位，不得当作普通背景镜头。
- 关键机位光影图：只用于对应关键机位，不得泛化到其它方向。

如果视频任务的镜头方案需要多个背景方向，必须在资产阶段生成多个 `scene_view_asset_id`，不得用一张方向图硬改成其它方向。

## 空间真值字段

空间真值必须用 100×100 顶视逻辑，但输出给视频提示词时使用自然语言，不使用 `[x,y]` 数字坐标格式。

```text
space_truth_id: <稳定编号>
video_task_id
scene_id
scene_view_asset_id
scene_view_orientation
camera_background_lock
coordinate_system_description: 100x100_top_view_natural_language
characters_position_natural_language:
  - character_id
    character_name
    position: <例如：画面左侧约 30% 区域，靠近前景>
    facing: <看向谁 / 哪个方向 / 哪个道具>
    screen_position_lock: <左 / 中 / 右 / 前景 / 后景>
props_position_natural_language:
  - prop_id
    prop_name
    position: <例如：画面中央偏前的桌案上>
    owner_or_surface: <手中 / 桌上 / 地上 / 门边>
entry_exit_points: []
eyeline_map: []
movement_paths: []
```

若无法确定空间关系，必须停在空间真值阶段补齐，不得直接进入关键帧或视频提示词。

## 舞台定位字段

即使不生成舞台定位图，也必须记录：

* 场景编号。
* 场景方向资产编号。
* 场景方向锁。
* 角色位置：用 100×100 自然语言描述，如“画面左前约三成位置”“右后门口”“桌案旁”。
* 角色朝向：看向谁或看向哪个道具。
* 关键道具位置：桌面、门边、地上、手中。
* 运动路径：谁走向谁，谁后退，谁挡住出口。
* 视线关系：谁看见证据，谁避开视线。

## 分镜表字段

* shot_id：镜头编号。
* episode_scene：所属集和场次。
* duration：预计秒数。
* shot_size：远景、全景、中景、近景、特写、大特写。
* camera_angle：平视、俯视、仰视、过肩、主观。
* camera_move：固定、缓推、拉远、横移、跟拍、手持。
* camera_background_lock：继承场景方向资产。
* subject：画面主体。
* action：可拍动作。
* performance：细微眼神、微表情、身体反应。
* spatial_note：角色在画面中的位置关系。
* audio：台词、环境声、音乐情绪。
* refs：需要的角色、场景方向图、道具参考图。

## 短剧常用镜头组合

### 羞辱场

1. 中景展示压迫者靠近。
2. 主角近景承受压力。
3. 道具特写制造羞辱动作。
4. 围观者反应。
5. 主角眼神变化，埋反击。

### 身份揭露

1. 众人嘲笑或质疑。
2. 关键人物入场。
3. 手机 / 合同 / 证据特写。
4. 对手表情崩塌。
5. 主角稳定站在画面中心。

### 甜宠保护

1. 主角陷入危险或尴尬。
2. 另一角色进入画面挡住压力。
3. 两人短暂对视。
4. 对手被压制。
5. 留下暧昧反应。

### 悬疑发现

1. 环境空镜建立危险感。
2. 手部翻找。
3. 证据特写。
4. 背后声响。
5. 主角回头，切断在悬念点。

## 分镜节奏

* 情绪爆点前用更短镜头加速。
* 重要反应给近景或特写。
* 信息揭露必须有证据画面，不只靠对白。
* 同一场景连续镜头避免重复景别和角度。
* 同一视频任务内的镜头方向必须服从 `camera_background_lock`。

## 角色数量锁

每个分镜镜头必须记录角色数量锁：

```text
character_count_expected: <数字>
characters_visible: [character_id]
characters_offscreen: [character_id]
extras_policy: none | allowed_background_only | required
```

不得在视频提示词阶段临时增加或删除主要角色。群众演员只能按 `extras_policy` 出现，不得替代主要角色。

## 黑白分镜数据规则

默认不生成制作黑白分镜图，但每个 `video_task_id` 仍必须产出 `storyboard_order_composition_action_data`。每个 Panel / shot 必须登记：

```text
panel_id 或 shot_id
video_task_id
source_scene_id
source_dialogue_ids
scene_view_asset_id
scene_view_orientation
camera_background_lock
shot_size
camera_angle
camera_move
characters_visible
character_count_expected
space_truth_id
required_asset_ids
reference_image_paths_expected
action_start
action_end
panel_transition_to_next
```

Panel 9 到下一任务 Panel 1 的衔接必须记录：角色位置、动作尾势、视线方向和未完成台词 / 声音。不得让相邻视频任务在空间和动作上断裂。

跨视频任务衔接必须显式写成 `cross_video_continuity_map`，不能只在上一段 Panel 9 内写一句“为下一段做尾势”。

```text
cross_video_continuity_map:
  from_video_task_id: <上一视频任务>
  from_panel_id: <上一任务尾部 panel_id>
  from_time_range: <如 14-15秒>
  to_video_task_id: <下一视频任务>
  to_panel_id: <下一任务开头 panel_id>
  to_time_range: <如 1-2秒>
  inherited_action_tail: <上一段动作尾势>
  inherited_eyeline: <上一段视线 / 失焦 / 转头等>
  inherited_audio_tail: <上一段未完成台词 / 呼吸 / 环境声>
  new_scene_opening_state: <下一段承接后的起始画面>
  continuity_status: PASS | FAIL
```

缺少 `cross_video_continuity_map` 时，相邻视频任务不得进入最终视频提示词冻结。

## 分镜到视频提示词交接硬规则

每个镜头或 Panel 交给视频提示词阶段前，必须提供：

```text
shot_id 或 panel_id
video_task_id
source_scene_id
source_dialogue_ids
space_truth_id
required_asset_ids
reference_image_paths_expected
scene_direction_lock:
  scene_view_asset_id
  scene_view_orientation
  camera_background_lock
character_count_expected
audio_owner_plan
cross_video_continuity_map: <若存在上一 / 下一 video_task_id 必填>
prompt_source_fields_ready: true | false
```

如果 `prompt_source_fields_ready` 不是 true，或 `reference_image_paths_expected` 为空但该镜头需要角色 / 场景 / 道具参考，则禁止进入视频提示词阶段。若引用场景方向图但缺少 `scene_direction_lock`，同样禁止进入视频提示词阶段。

## 舞台定位图 prompt 骨架（仅用户授权生成时）

```text
生成图片：标准 90 度垂直俯视舞台定位图 / 鸟瞰正交平面图，仅作为制作参考。

space_truth_id: <稳定编号>
video_task_id: <视频任务编号>
source_scene_id: <场次编号>
scene_view_asset_id: <场景方向资产编号>
scene_view_orientation: <场景方向>
camera_background_lock: <背景机位方向锁>
coordinate_system_description: 100x100_top_view_natural_language
characters_position_natural_language: <完整展开>
props_position_natural_language: <完整展开>
entry_exit_points: []
eyeline_map: []
movement_paths: []
character_count_expected: <数字>
characters_visible: [<character_id>]
extras_policy: none | allowed_background_only | required

画面要求：若用户授权生成，只生成干净俯视制作图。不得使用九色选框、色块、箭头、形状编码、格线、数字坐标、文字标签、stable_id、说明文字、水印、字幕或 UI。若需要说明，只写在数据层，不写入图中。

下游引用规则：默认不作为视频参考图传入。若用户再次明确授权作为视频参考图，只允许用于空间站位和运动路径理解，最终视频不得生成坐标网格、色块、箭头、文字标注、框线或 UI。
```

## 黑白分镜图 prompt 骨架（仅用户授权生成时）

```text
仅用户明确授权生成制作黑白分镜图时生成图片：黑白分镜制作图，服务视频任务 <video_task_id>；默认只产出下游继承数据，不生成该图片。

video_task_id: <视频任务编号>
source_scene_id: <场次编号>
source_dialogue_ids: [<对白ID>]
space_truth_id: <空间真值编号>
required_character_asset_ids: [<角色资产ID>]
required_scene_asset_ids: [<场景方向资产ID>]
required_prop_asset_ids: [<道具资产ID>]
reference_image_paths_expected: [<角色 / 场景方向 / 道具路径>]
scene_direction_lock: <必须展开>

画面规格：单张黑白分镜制作图，仅用于镜头顺序、构图、动作调度和角色位置。不得使用九色框、宫格边框、颜色编号、stable_id、水印、字幕或 UI；不得被解释为最终视频画面。

下游说明：默认不生成制作黑白分镜图，也默认不把黑白分镜图路径传入视频提示词参考图。视频提示词只继承 `storyboard_order_composition_action_data`，包含 shot_size、camera_angle、camera_move、characters_visible、action_start、action_end、panel_transition_to_next 和构图 / 动作调度说明。这些字段必须融合进正式 prompt 的分段动作、镜头、构图、运镜和转场描述中。
```

## 输出要求

输出分镜表时，优先让每个镜头都可直接进入关键帧生成。不要写抽象词，如“气氛紧张”，要写具体画面，如“走廊灯闪烁，主角停在半开的病房门前”。

## 景别优先级与剧本视觉备注降权（资产 v5 补丁）

分镜阶段必须遵循 Skill 景别优先级，高于剧本中的视觉备注。默认优先使用大特写、特写、近景、中景，以及前景对焦加背景高虚化，用来强化人物微表情、手部动作、证据点和压迫感。

远景、全景、大远景只允许在以下情况使用：建立空间、交代人物与环境关系不可缺少、战争/灾害/大场面、群众规模、地理动线或剧情强烈需要。否则即使剧本写了全景、远景、大远景，也必须改写为中景以下景别。

每个分镜表必须新增 shot_scale_decision_reason，记录为什么使用当前景别；若使用远景/全景/大远景，必须写 strong_story_need。没有 strong_story_need 的远景/全景/大远景标记 FAIL_SHOT_SCALE_PRIORITY_OVERRIDE。


### 双模式强制适用与剧本视觉备注降权

本景别规则同时适用于 `cinematic_realistic` 写实真人模式与 `top_chinese_3d_animation_cg` 3D 动画 CG 模式。3D 动画 CG 不因为是动画就自动放宽为全景、远景或大远景。剧本中的视觉备注只作为剧情理解和信息点来源，不作为镜头执行优先级。

执行顺序固定为：先理解剧情功能 → 再按 Skill 景别优先级选择大特写 / 特写 / 近景 / 中景 / 前景对焦 + 背景高虚化 → 最后检查剧本视觉备注是否需要被降权或改写。若剧本写全景、远景、大远景，但没有建立空间、人物环境关系不可缺少、战争灾害大场面、群众规模、地理动线或强剧情必要性，必须改为中景以下，并写入 `rewrite_from_script_visual_note: true`。

## 空间建模 v6：3列×3景深分区空间真值（当前正式方案）

本节为当前正式空间真值可见层。旧 `100×100_top_view_natural_language` 仅作为后备缺口能力保留，本轮正式生产不加载、不输出；后续迭代空间系统时必须提醒用户是否重新启用或升级 100×100 后备能力。

### 固定分区规则

```text
[参考素材空间规则]：@<主场景基准图> 为全镜头空间基准图；
画面横向分为左列、中列、右列 3 大列，每列内可补充“偏左、居中、偏右”；
纵向按景深分为前景层、中景层、背景层 3 大层，每层内可补充“前段、中段、后段”；
所有人物、道具位置统一以“大列 + 列内方位 + 大层 + 层内区段”格式描述；
中列居中、中景层中段为主体核心区；
禁止在最终视频提示词可见层使用精确米数、精确坐标刻度、100×100 坐标或 [x,y]。
```

### 分镜空间字段

每个分镜镜头必须新增：

```text
reference_base: @<主场景基准图或对应机位补充图>
spatial_partition_anchor:
  core_subject:
  horizontal_column: 左列 | 中列 | 右列
  column_inner_position: 偏左 | 居中 | 偏右
  depth_layer: 前景层 | 中景层 | 背景层
  depth_inner_section: 前段 | 中段 | 后段
  anchor_state: 保持 | 进入 | 离开 | 转移
  anchor_reason: 主体表演 | 道具证据 | 视线焦点 | 空间衔接 | 运镜稳定
reference_layer_type: main_scene_base | camera_supplement
requires_camera_supplement: true | false
```

### 镜头切换补图判断

分镜阶段必须先判断每个镜头是否仍由主场景基准图覆盖。若只是同视角景别变化、小幅运镜或主体在原分区内微调，则 `requires_camera_supplement: false`。若发生视角跳变、区域切换、反打、俯视、越轴风险或主基准图无法支撑的背景变化，则 `requires_camera_supplement: true`，并必须回到资产阶段补齐对应机位补充图后再继续。
