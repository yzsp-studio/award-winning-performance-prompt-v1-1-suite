# 短剧全流程 QC 清单

## 故事 QC

  一句话钩子是否清楚。
  主角欲望是否明确。
  对手压力是否足够。
  每集是否有开场钩子。
  每集是否有结尾钩子。
  反转是否由前文信息支撑。
  爽点是否按节奏分布，而不是集中在最后。

## 视觉模式 QC

  是否已通过启动弹窗、用户明示或授权词确定 `production_visual_mode`。
  `production_visual_mode` 是否写回生产数据中心。
  角色、场景、道具资产与视频提示词是否使用同一个 `production_visual_mode`。
  若为 3D 动画 CG 模式，是否真实读取 `references/animation character converter.md`。
  若为 3D 动画 CG 模式，最终角色资产提示词是否完成真人风险词替换。

## 提示词语言 QC

  角色资产、场景资产、道具资产、分镜、关键帧、视频提示词、VIDEO_DISPATCH_PACKAGE、沙盒测试提示词文档的可见提示词正文是否默认使用中文。
  是否没有为了“模型更好理解”把提示词主体写成英文，且没有输出中英并列提示词正文。
  用户可见文档是否实行“极限全中文”：字段名、段落标题、描述正文、负面提示、任务包展示层与审阅层均已中文化。
  非中文内容是否只限于模型名、必要编号、版本号、项目链路 ID、文件路径，以及用户明确要求保留的非中文台词或入画文字；英文参数、英文枚举值、机器 token、英文禁止词是否只存在于内部派单映射层，未混入用户可见提示词正文。
  台词和用户指定入画文字是否逐字保留原语言；台词之外的动作、表演、镜头、光影、参考图说明、负面提示是否仍为中文。
  历史结构词是否已改成中文等价词：`Negative Prompt` → “负面提示”，`Native audio` → “原生音频”，`Original request` → “原始需求”，`front view / side view / back view` → “正面视图 / 侧面视图 / 背面视图”。
  若沙盒模式不生成真实资产或视频，画布上的完整提示词文档是否同样遵守中文提示词规则。

## 风格配置与影调配置 QC

  是否在确定 `production_visual_mode` 后立刻读取 `references/style tone presets.md`，并完成第二层弹窗选择或用户授权默认。
  生产数据中心是否完整写回 `global_style_preset_id`、`global_style_lock`、`tone_profile_preset_id`、`tone_profile_lock`、`style_tone_lock_status`。
  `style_tone_lock_status` 只有在完整风格配置正文与完整影调配置正文均已写回时才允许标记 PASS。
  3D 动画 CG 模式不得选择 `STYLE REAL *` 或 `TONE REAL *`；写实真人模式不得选择 `STYLE ANIM CG *` 或 `TONE ANIM CG *`。
  角色资产、场景资产、道具资产提示词是否完整展示 `global_style_lock` 与 `tone_profile_lock` 正文，不得只写预设 ID。
  视频提示词与 `VIDEO_DISPATCH_PACKAGE` 是否完整展示 `global_style_lock` 与 `tone_profile_lock` 正文，不得首段完整后续写“同上 / 按前文”。
  写实真人模式是否保留并允许真人皮肤、面部毛孔、真实摄影、ARRI、Cooke 等真人摄影词，不得被动画规则误删。
  3D 动画 CG 模式是否禁止真人词、photorealistic、metahuman、skin pores、真实皮肤毛孔、真人摄影等风险词。
  若任一资产或视频提示词缺少完整风格锁 / 影调锁，必须标记 `FAIL_STYLE_TONE_INHERITANCE` 并回到对应阶段补齐。

## 人物 QC

  主角所有被下游引用的角色是否有稳定外观锚点；不得只检查主角。
  主要所有被下游引用的角色是否都有 `face_structure_3t5e`、`character_name_aliases`、`canonical_identity_label` 与 `identity_anchor`，并按上庭 / 中庭 / 下庭 / 五眼 / 整体骨相写清。
  剧本没有明确三庭五眼时，是否已根据人物人设合理补齐并标记来源。
  角色关系是否能一句话说清。
  每个主要角色是否有欲望和秘密。
  对白风格是否区分角色。
  状态变化是否有剧情原因。

## 剧本 QC

  是否有场次编号。
  每场是否有地点、时间、人物。
  动作是否可拍。
  对白是否过长或解释过多。
  情绪是否通过动作和反应体现。
  结尾是否停在悬念点。

## 全量前置快照 QC

  剧本标准化后、资产阶段前是否已建立 `full_preproduction_snapshot`。
  快照是否包含 scene_table、dialogue_table、video_task_mapping、character_identity_table、character_look_variant_plan、scene_state_variant_plan、prop_usage_plan、voice_reference_plan、audio_owner_plan、reference_asset_plan、performance_plan_draft、chinese_shot_prompt_draft、qc_expectation_plan。
  后续变化是否只通过 `preproduction_patch` 写入，而不是直接覆盖基准快照。
  是否生成 `current_active_snapshot_resolved`。
  下游资产、分镜、视频提示词是否消费 `current_active_snapshot_resolved`，而不是只消费旧 snapshot 或 patch。
  若合成版缺少基准快照已有字段，是否标记 `FAIL_RESOLVED_SNAPSHOT_INCOMPLETE` 并阻断下游。
  每个 prompt 是否登记 `base_snapshot_id`、`active_patch_ids` 与 `resolved_version_id`。

## 角色造型变体与场景状态变体 QC

  是否在剧本标准化后计算 `character_look_variant_plan`。
  每个被下游引用角色是否登记服装、妆造、妆感、发型、发饰、年龄阶段、伤损、武器、贴身道具、适用场次、适用视频任务、换装理由和 `character_has_time_to_change`。
  角色没有现实时间换装时，是否延续上一套造型，只通过损伤、雨湿、脏污等状态变化处理。
  武器和贴身道具若与角色长期绑定，是否进入人物资产图变体。
  是否在剧本标准化后计算 `scene_state_variant_plan`。
  同一场景只要季节、天气、日/夜、受损、新增固定道具、剧情状态或光源状态变化，是否生成新场景状态资产图。
  视频提示词是否使用与当前 video_task_id 匹配的 `look_variant_id` 和 `scene_state_variant_id`，不得用默认图替代。

## 角色音色参考 QC

  是否从生产数据中心视频任务映射统计 `character_video_segment_count_from_production_data_center`。
  出现在 ≥2 段视频的角色是否 `voice_reference_required: true`。
  首次缺少音色参考时是否弹窗提供 A 首段视频后提取音色、B 上传角色音频、C 后期配音 / speech 缺口保留。
  选择 A 时，首段视频 prompt 是否写入推算音色描述词；首段生成后是否计划提取 5 10 秒角色台词音频。
  已启用音色参考的角色，后续所有视频是否持续使用同一 `voice_description_text`，除非通过 patch 更新。
  镜号台词是否使用 `@<角色名>严格使用@<角色名音频1><voice_description_text>。<说话方式>:{逐字台词}` 格式。
  台词是否逐字保留，未因加入音色描述而增删。
  若选择后期配音 / speech，是否标记 `speech_post_dub_gap: true`，不得误判为稳定 speech 链路已完成。

## 资产 QC

  角色、场景、道具是否都被编号。
  跨集复用资产是否优先生成。
  关键道具是否有特写需求。
  角色身份锚点是否写清楚。
  角色资产提示词是否消费生产数据中心中的 `face_structure_3t5e`，而不是临场泛化重写。
  所有被下游引用的角色是否使用同一三庭五眼标准；群像人物不得比主角简略。
  双魂共体、改名、伪装身份是否写入 `character_name_aliases` 与 `canonical_identity_label`。
  角色资产提示词是否逐项消费 `identity_anchor`、完整 `face_structure_3t5e`、`costume_anchor`、`state_variants`、`source_scene_ids`、`source_dialogue_ids`、`used_by_video_tasks`。
  角色资产图是否符合布局：左 50% 为面部角色设定展示 / 正面观察视角 / 面部朝向正前方 / 默认无表情展示姿态；右 50% 为横向 1x3 服装三视图；正面、侧面视图为颈部以下无头 body only；背面视图保留完整头部和后脑发型轮廓；三视图不得画成三个不同的人。
  角色资产 prompt 是否原样保留 `模型：image2`、`比例：16:9`、`清晰度：2K`、`画质：高`；资产图生成后是否自动执行高清增强至 4K，若当前 agent 无法调用高清增强，是否明确提示用户在画布中执行。
  角色资产 prompt 是否完整继承 `global_style_lock` 与 `tone_profile_lock` 正文，并登记 `style_tone_inheritance_status: PASS`。
  人物资产若提示词继承不完整或角色资产图布局不合格，是否标记为 `FAIL_INHERITANCE_PROMPT` 或 `DEPRECATED_NOT_FOR_DOWNSTREAM`，并从下游参考图清单移除。
  资产提示词文档是否执行“逐资产矩阵验收”：每个角色、场景、道具都必须逐项通过模型、比例、清晰度、画质、视觉模式、全局风格锁、影调配置锁、核心描述、布局 / 方向 / 单物规则、继承字段、负面提示、连续性禁令、下游用途。
  是否存在“第一个资产完整、后续资产简化”的结构漂移；若任何后续角色 / 场景 / 道具的字段数量、段落结构、风格锁展开、负面提示或细节密度低于首个同类资产，必须标记 `FAIL_ASSET_PROMPT_COMPLETENESS_MATRIX`，回到资产提示词阶段重写。
  全链路任务包是否独立展开当前任务所需信息；资产提示词、分镜任务、关键帧任务、视频任务包、声音任务包、后期任务包均不得使用“同上 / 按前文 / 参考上文 / 按首个角色”承接关键字段。

## 3D 动画 CG 角色资产专项 QC

仅当 `production_visual_mode: top_chinese_3d_animation_cg` 时执行：

  是否使用 `references/animation character converter.md` 将真人描述转换为 3D 动画 CG 角色资产提示词。
  是否包含 `production_visual_mode: top_chinese_3d_animation_cg`。
  是否包含 `animation_quality_bar: porcelain_SSS_skin + soft_bloom_glow + Octane_render + flawless_CG_shading`。
  是否锁定国漫顶级 3D 动画 CG 电影质感、高调透气柔光、柔和漫射无重阴影、干净白色或浅灰色棚拍背景。
  是否把“肖像、特写、正脸特写、直视镜头、镜头、模特、人像、写实、真实、真实皮肤、皮肤毛孔、卧蚕、双眼皮、唇峰、唇纹、肤色、清冷妆容”等风险词替换为 3D 动画角色资产术语。
  是否删除真人年龄数字，只保留年龄阶段型动画角色资产语言。
  是否没有职业介绍、阶层介绍、人物人设介绍，而是改成可视化角色资产锚点。
  是否没有出现 real human、photorealistic、metahuman、skin pores、真人、写实真人、真人摄影、真人肖像、真人皮肤、真实毛孔、人像摄影、影楼写真。
  “负面提示”是否包含真人写实压制和文字抑制。

## 场景资产 QC

  场景资产是否为单张方向资产图，而不是场景六视图 / 六分区 / 六宫格 / 拼贴图。
  每张场景资产是否写回 `scene_view_asset_id`、`scene_view_orientation`、`scene_view_ref_image_path`、`camera_background_lock`。
  场景资产是否写回并在提示词中消费 `scene_era_profile`、`scene_atmosphere_profile`、`scene_art_direction_profile`、`project_visual_tone`。
  场景资产图中是否没有人物、群演、画面文字、标签、水印、字幕、UI、颜色框、数字、stable_id。
  场景资产 prompt 骨架是否保持 `模型：image2`、`比例：16:9`、`清晰度：2K`、`画质：高`；资产图生成后是否自动执行高清增强至 4K，若当前 agent 无法调用高清增强，是否明确提示用户在画布中执行。
  场景资产 prompt 是否完整继承 `global_style_lock` 与 `tone_profile_lock` 正文，并登记 `style_tone_inheritance_status: PASS`。
  视频任务需要正面图时是否生成正面图；需要反向图时是否生成反向图；不得用一张方向图冒充其它方向。

## 道具资产 QC

  每个道具是否登记 `appearance_count`。
  出现 ≥2 次的道具是否强制生成资产图。
  出现 1 次但含文字 / 符号 / 印章 / 数字 / 乱码 / 图样 / 准确标记的道具是否强制生成资产图。
  出现 1 次且无文字 / 符号风险的道具若未生成，是否登记 `prop_asset_reason: skipped_single_use_no_text`。
  需要准确动画效果的道具是否登记 `animation_precision_risk: true`。
  需要准确动画效果的道具是否已用弹窗提醒用户提供参考视频，并记录命名规则 `道具动效参考 <prop_id> <道具名>.mp4`。
  道具资产图是否为单个道具资产图，而不是九宫格、自动网格、多道具合并图或拼贴图。
  道具资产 prompt 骨架是否保持 `模型：image2`、`比例：16:9`、`清晰度：2K`、`画质：高`；资产图生成后是否自动执行高清增强至 4K，若当前 agent 无法调用高清增强，是否明确提示用户在画布中执行。
  道具资产 prompt 是否完整继承 `global_style_lock` 与 `tone_profile_lock` 正文，并登记 `style_tone_inheritance_status: PASS`。
  道具图是否没有颜色框、数字编号、道具名标签、prop_id、字幕、UI、水印。

## 分镜 QC

  多人场景是否先锁定站位。
  舞台定位图是否经过弹窗询问；默认是否不推荐生成。
  黑白分镜图是否经过弹窗询问；默认是否不推荐生成。
  即使不生成舞台定位图，是否仍写回 `space_truth_id`、`scene_view_asset_id`、`scene_view_orientation`、`camera_background_lock`、角色位置自然语言、道具位置自然语言、视线关系和运动路径。
  空间描述是否使用 100×100 顶视逻辑的自然语言，而不是 `[x,y]` 数字坐标格式。
  是否没有使用色块、箭头、形状编码、九色框、坐标网格等视觉标记描述。
  黑白分镜数据是否保留景别、机位、运镜、构图、动作起止、转场 / 动作尾势，并融合进视频提示词分段动作、镜头和转场描述中；默认不得生成制作黑白分镜图，也不得把黑白分镜图路径写入视频提示词参考图清单。
  相邻视频任务是否存在 `cross_video_continuity_map`。
  连续镜头是否避免重复景别。
  重要情绪是否有反应镜头。
  信息揭露是否有证据画面。
  镜头是否能转成关键帧。

## 视频提示词 QC

  是否写明 model、比例、时长。
  是否真实读取并消费 `references/actor performance voice integration.md`。
  是否采用中文片段镜号格式作为默认正式 prompt 结构。
  是否登记并消费 `base_snapshot_id`、`active_patch_ids`、`resolved_version_id`、`current_active_snapshot_resolved_status`。
  是否传入必要参考图。
  是否继承 `production_visual_mode`。
  是否完整继承并展开 `global_style_lock` 与 `tone_profile_lock` 正文，且 `style_tone_lock_status: PASS`。
  是否继承 `scene_direction_lock_actual`，包含 `scene_view_asset_id`、`scene_view_orientation`、`camera_background_lock`。
  若使用正面场景图，所有镜头是否遵循正面背景机位；若使用反向场景图，是否遵循反向背景机位；其它方向同理。
  是否继承空间真值中的角色位置、道具位置、空间站位、视线关系和运动路径，并以自然语言写出。
  是否为每张参考图写明用途说明、引用边界和禁止继承字段。
  是否锁定角色身份。
  是否写出动作链。
  写实真人模式下，视频 prompt 开头是否使用“生成<实际段数>段连贯的超写实电影质感剧情视频:”。
  3D 动画 CG 模式下，视频 prompt 开头是否使用“生成<实际段数>段连贯的国漫顶级3D动画CG电影质感剧情视频:”。
  每个时间段是否保持同等引用密度、表演细节粒度、景别运镜和参考图边界说明；不得第一段详细、后续压缩简略。
  是否写出镜头运动。
  是否明确声音归属。
  是否避免字幕和画面文字。
  是否没有出现“场景六视图、六宫格、道具九宫格、颜色框逐色说明”等旧规则残留。
  是否没有把舞台定位图或黑白分镜图默认传入 `reference_image_paths_actual`；若传入，是否有用户明确授权。

## 后期 QC

  镜头顺序是否符合因果。
  音量是否以对白清晰为第一优先。
  BGM 是否压过台词。
  画幅是否统一。
  成片时长是否偏离计划超过 20%。



### 双模式资产状态与景别专项 QC（v5 加硬）

  `3D 动画 CG 角色变体完整提示词模板（v5 防压缩专用）` 是否已用于 `production_visual_mode: top_chinese_3d_animation_cg` 的所有 look_variant；若 3D CG 后续变体只写继承、同一身份、沿用基础模型，标记 `FAIL_ASSET_VARIANT_PROMPT_COMPRESSION`。
  场景状态变体是否使用完整模板，逐项写明 `scene_state_variant_id`、`base_scene_asset_ref`、`before_state`、`after_state`、`change_trigger`、`continuity_keep`、`continuity_change`、`scene_architecture_period_lock`、`scene_view_orientation`、`camera_background_lock`；若只写“夜雨版 / 破损版 / 继承原场景”，标记 `FAIL_ASSET_VARIANT_PROMPT_COMPRESSION`。
  道具状态变体是否使用完整模板或完整登记状态绑定，逐项写明 `shared_prop_visual_anchor`、`body_attachment_position`、`scene_placement_position`、`handling_state`、`before_state`、`after_state`、`continuity_keep`、`continuity_change`、`independent_asset_required` 与原因；若身体状态和放置状态的同一道具外观锚点不一致，标记 `FAIL_PROP_STATE_ANCHOR_DRIFT`。
  同一人物、场景、道具在不同状态中，服装、破损、血迹、灰尘、湿痕、新增固定道具、器物文字或材质变化是否有剧情推进标注 `change_trigger`；若无，标记 `FAIL_STATE_CHANGE_TRIGGER_MISSING`。
  景别规则是否同时作用于 `cinematic_realistic` 与 `top_chinese_3d_animation_cg`；3D 动画 CG 不得默认放宽使用全景、远景、大远景。
  剧本视觉备注是否已降权为剧情理解材料；若剧本写全景、远景、大远景但没有 `strong_story_need: true`，分镜与最终 prompt 是否已改写为大特写、特写、近景、中景或前景对焦 + 背景高虚化，并登记 `rewrite_from_script_visual_note: true`。



### 空间建模 v6 专项 QC：参考图分层与 3×3 空间锚定

  是否已将 `active_spatial_language` 设为 `three_column_three_depth_partition`，并将 100×100 标记为 `reserved_not_loaded`；若最终视频提示词仍输出 100×100 坐标、[x,y] 或精确刻度，标记 `FAIL_SPATIAL_PARTITION_FORMAT`。
  每个场景是否有 1 张 `main_scene_base_ref`；若没有主场景基准图，标记 `FAIL_MAIN_SCENE_BASE_MISSING`。
  单场景是否最多 1 张主场景基准图 + 3 张机位补充图；若超过，标记 `FAIL_REFERENCE_OVER_LIMIT`，必须拆分场景或重排镜头。
  大角度机位跳变、正反打、侧面切换、俯视、区域切换、越轴风险是否在资产阶段预先计算并生成机位补充图；若视频提示词阶段才发现缺图，标记 `FAIL_CAMERA_SUPPLEMENT_ASSET_MISSING`。
  [参考素材使用规则] 是否明确角色图、主场景基准图、机位补充图、道具图的用途和禁止继承边界；若没有职责边界，标记 `FAIL_REFERENCE_ROLE_BOUNDARY_MISSING`。
  [参考素材空间规则] 是否使用左列 / 中列 / 右列 + 前景层 / 中景层 / 背景层；人物和道具是否用“大列 + 列内方位 + 大层 + 层内区段”描述。
  [人物站位] 是否只定义一次全局站位，镜号级是否只锚定当前核心主体；若每镜重复冗余全局站位或缺少核心主体锚定，标记 `FAIL_SPATIAL_ANCHOR_MISSING`。
  每个镜号是否在“场次”之后包含“参考基准”和“空间锚定”；缺任一项，标记 `FAIL_SHOT_SPATIAL_BASE_MISSING`。
  机位补充图是否只用于对应机位透视与物体相对布局，未覆盖主场景基准图的光影、材质、色调和统一气氛。

## 统一失败路由矩阵（所有 FAIL_* 强制执行）

任何 FAIL_* 状态都不得口头忽略、不得直接进入下游、不得用“先这样 / 后面再补 / 模型会理解 / 为了效率压缩”绕过。处理方式固定为：定位最近 producer 阶段 → 保留已通过字段 → 只补齐失败字段 → 重新执行对应 QC → PASS 后才允许冻结或派发。

| FAIL 状态 | 最近 producer 阶段 | 必须修复内容 | 下游阻断 |
|   |   |   |   |
| FAIL_SPATIAL_POLICY_MISSING | 生产数据中心 / 空间策略初始化 | 补齐 spatial_control_policy，确认 active_spatial_language=three_column_three_depth_partition，backup_100x100_policy=reserved_not_loaded | 阻断资产拆解 / 分镜 / 视频冻结 |
| FAIL_SPATIAL_PARTITION_FORMAT | 分镜阶段 / 视频提示词阶段 | 删除 100×100 坐标、[x,y]、精确刻度，改用左列 / 中列 / 右列 + 前景层 / 中景层 / 背景层及细化区段 | 阻断分镜冻结 / 视频冻结 |
| FAIL_MAIN_SCENE_BASE_MISSING | 场景资产阶段 | 为当前场景补生成或补登记 1 张 main_scene_base_ref，并写清 reference_role、use_for、do_not_use_for | 阻断分镜 / 视频冻结 |
| FAIL_CAMERA_SUPPLEMENT_ASSET_MISSING | 场景资产阶段 / 分镜阶段 | 为正反打、侧面、俯视、区域切换、越轴风险等镜头补生成对应 camera_supplement_ref，或回到分镜拆分 / 重排机位 | 阻断视频冻结 / 派发 |
| FAIL_REFERENCE_OVER_LIMIT | 资产拆解 / 分镜阶段 | 单场景参考图限制为 1 主场景基准图 + 最多 3 机位补充图；超限时拆分场景或重排镜头 | 阻断资产冻结 / 视频冻结 |
| FAIL_REFERENCE_ROLE_BOUNDARY_MISSING | 资产拆解 / 视频提示词阶段 | 补齐角色图、主场景基准图、机位补充图、道具图的 use_for 与 do_not_use_for，防止参考职责互相覆盖 | 阻断视频冻结 / 派发 |
| FAIL_SPATIAL_ANCHOR_MISSING | 分镜阶段 / 视频提示词阶段 | 补齐全局一次性 [人物站位] 与镜号级核心主体空间锚定，使用 3×3 分区语言 | 阻断视频冻结 / 派发 |
| FAIL_SHOT_SPATIAL_BASE_MISSING | 视频提示词阶段 | 在每个镜号“场次”之后补写“参考基准：@...”与“空间锚定：@...” | 阻断视频冻结 / 派发 |
| FAIL_STYLE_TONE_INHERITANCE | 风格影调选择 / 资产提示词 / 视频提示词 | 补齐 global_style_lock 与 tone_profile_lock 完整正文，不能只写 ID | 阻断资产生成 / 视频冻结 |
| FAIL_RESOLVED_SNAPSHOT_INCOMPLETE | 生产数据中心 / full_preproduction_snapshot | 重新合成 current_active_snapshot_resolved，补回基准快照字段 | 阻断资产 / 分镜 / 视频 |
| FAIL_ASSET_PROMPT_COMPLETENESS_MATRIX | 资产提示词阶段 | 按逐资产矩阵重写缺字段资产，后续资产细节密度不得低于首个同类资产 | 阻断真实生图 / 分镜 |
| FAIL_ASSET_VARIANT_PROMPT_COMPRESSION | 角色变体资产提示词阶段 | 后续 look_variant 必须完整展开身份锚点、三庭五眼、体型气质、服装锚点、状态链、时代职务锁、负面提示 | 阻断角色变体资产生成 |
| FAIL_PERIOD_STATUS_LOCK_MISSING | 剧本标准化 / 生产数据中心 / 资产拆解 | 补齐 era_dynasty_lock、period_region_lock、official_rank_role_lock、costume_regulation_lock、prop_period_lock、scene_architecture_period_lock | 阻断历史 / 古装 / 年代资产派单 |
| FAIL_INHERITANCE_PROMPT | 角色资产提示词阶段 | 补齐角色别名、同一身份主键、identity_anchor、face_structure_3t5e、costume_anchor、source_scene_ids、used_by_video_tasks | 阻断下游参考图使用 |
| FAIL_ANIMATION_CONVERTER_QC | 3D 动画 CG 角色转换阶段 | 重新读取 animation character converter.md，替换真人风险词，删除真人年龄数字和职业介绍式文字 | 阻断 3D CG 角色资产派单 |
| FAIL_SCENE_DIRECTION_LOCK | 场景方向资产阶段 | 补生成正确 scene_view_orientation 的单张方向资产，写回 camera_background_lock | 阻断分镜 / 视频 |
| FAIL_PROP_SINGLE_ASSET_RULE | 道具资产阶段 | 按出现次数、文字符号风险、读屏 / 证据 / 特写 / 动效风险补单道具资产或登记跳过原因 | 阻断引用该道具的视频任务 |
| FAIL_PROMPT_AT_REFERENCE_MISSING | 视频提示词 / 资产池引用映射 | 补齐画面出现的人物、场景、道具 @引用与 reference_image_paths_actual | 阻断视频冻结 / 派发 |
| FAIL_UNUSED_REFERENCE_ASSET | 视频提示词参考图清单 | 移除当前镜号未出现、未触碰、未读屏、未作为背景 / 证据使用的参考图 | 阻断视频冻结 / 派发 |
| FAIL_VOICE_DESCRIPTION_TOO_SHORT | 声音表演 / 视频提示词阶段 | 每镜号内角色首次 VO/OS/台词前补足三句音色描述 | 阻断视频冻结 / 派发 |
| FAIL_UNCONDITIONAL_AUXILIARY_BAN | 视频提示词禁令段 | 未启用舞台定位图 / 黑白分镜图时删除对应辅助图禁令；启用时才条件化保留 | 阻断视频冻结 |
| FAIL_VIDEO_PROMPT_V3_COMPLETENESS | 视频提示词阶段 | 补 [要求] 固定句、[画面] 固定块、15 秒拆分、天气光线、@引用、音色描述、条件化禁令、完整展开 | 阻断视频冻结 / 派发 |
| FAIL_SCENE_REQUIREMENT_PREFIX_MISSING | 视频提示词 [要求] 段 | 在 [要求] 第一句补“@<场景方向资产名>为背景保持<方向>机位” | 阻断视频冻结 / 派发 |
| FAIL_UNIQUE_CHARACTER_BAN_MISSING | 视频提示词 [禁令] 段 | 在 [禁令] 首句补唯一人物 / 禁止分身固定句 | 阻断视频冻结 / 派发 |
| FAIL_SPOKEN_DIALOGUE_AT_EMOTION_MISSING | 视频提示词台词层 | 把说出口台词改为“@角色 + 情绪 / 动作 / 语气 + 说：{逐字台词}” | 阻断视频冻结 / 派发 |
| FAIL_SHOT_REMARK_MISSING | 分镜 / 视频提示词镜号 | 每个镜号补“备注：剧情功能 / 情绪功能 / 证据点 / 衔接功能” | 阻断视频冻结 / 派发 |
| FAIL_VIDEO_PROMPT_V4_REGRESSION | 视频提示词阶段 | 核查 v4 五项：场景机位前缀、唯一人物禁令、@情绪说、每镜备注、读音映射 | 阻断视频冻结 / 派发 |
| FAIL_PROP_STATE_ANCHOR_DRIFT | 道具状态变体 / 角色资产 / 单独道具资产 | 统一同一道具在身体状态、手持状态、放置状态、独立道具图中的 shared_prop_visual_anchor，核心外观描述必须逐字一致 | 阻断角色资产 / 道具资产 / 视频冻结 |
| FAIL_STATE_CHANGE_TRIGGER_MISSING | 角色 / 场景 / 道具状态变体计划 | 补齐 before_state、after_state、change_trigger、continuity_keep、continuity_change，并说明剧情推进原因 | 阻断资产变体生成 / 分镜冻结 |
| FAIL_SHOT_SCALE_PRIORITY_OVERRIDE | 分镜阶段 / 视频提示词阶段 | 按 Skill 景别优先级重排；远景 / 全景 / 大远景必须写 strong_story_need | 阻断分镜冻结 / 视频冻结 |

返工时只修复 FAIL 对应缺口，不得把已完整通过的资产提示词、视频提示词、生产数据中心字段批量压缩或重写成短版。

## 返工策略

1. 偏离人物：回到角色资产表，强化身份锚点。
2. 3D 动画 CG 模式下真人化：回到 `animation character converter.md` 重新转换提示词。
3. 剧情无聊：回到故事结构，增加压迫、误会、证据或反转。
4. 镜头单调：回到分镜表，增加反应、道具特写、视角变化。
5. 视频动作不稳：拆短动作链，减少单镜动作数量。
6. 场景方向错误：回到资产阶段补生成正确方向的场景资产图。
7. 道具文字 / 符号错误：回到道具资产阶段补生成道具单图；若涉及精确动效，要求用户提供参考视频。
8. 声音混乱：重新指定唯一 audio owner。

## LOCAL_CHAIN_AUDIT 最终验收

QC 阶段必须把 `LOCAL_CHAIN_AUDIT` 作为最终验收主表，而不是只检查观感。必须确认：

```text
production_chain_id: short drama full pipeline
production_chain_name: 神笔制作
workflow_source: user_skill_locked
fallback_allowed: false
local_skill_root: expanduser("~/Movies/Hub/skills/short drama full pipeline")
template_source: <本地 reference 绝对路径>
link_status: PASS
```

以下任一项为否，QC 必须 FAIL：

  是否真实读取本地 `SKILL.md` 与当前阶段 reference。
  是否没有走线上通用制作链路。
  是否没有把其它 Skill / workflow 当作主模板。
  是否没有 light dispatch 跳过本地阶段。
  是否每个阶段都有 `template_source`。
  是否每个阶段都写回生产数据中心。
  是否确定并写回 `production_visual_mode`。

## 数据链验收硬规则

QC 必须逐项检查数据链：

```text
visual_mode  > story  > script  > assets  > storyboard  > video_prompt  > post  > final_output
```

每个最终成片或最终提示词必须能追溯：

  `original_request`
  `production_visual_mode`
  `story_source_id`
  `scene_id`
  `dialogue_id`
  `asset_id`
  `scene_view_asset_id`
  `scene_view_orientation`
  `space_truth_id`
  `shot_id` 或 `panel_id`
  `prompt_id`
  `video_task_id`
  `edit_item_id`
  `final_output_id`

任何 ID 缺失、断链、重复指向错误对象或只写“同上 / 见上文 / 参考前面”，均为 FAIL。

## 参考图验收硬规则

必须检查每个视频提示词：

```text
reference_image_paths_expected
reference_image_paths_actual
reference_count_expected
reference_count_actual
reference_roles_expected
reference_roles_actual
missing_reference_paths
extra_reference_paths
reference_lock_status
scene_direction_lock_expected
scene_direction_lock_actual
```

QC PASS 条件：

  expected 与 actual 数量一致。
  expected 与 actual 角色一致。
  expected 与 actual 场景方向一致。
  expected 与 actual 道具一致。
  所有路径均来自生产数据中心中 `ACTIVE` 资产。
  `stage_map_path` 与 `storyboard_image_path` 默认不进入 `reference_image_paths_actual`；若进入，必须有用户明确授权。
  不存在用错误角色 / 错误场景方向 / 错误道具替代。

否则必须回到资产阶段或分镜阶段补齐。

## 台词保真验收硬规则

必须逐句检查 `verbatim_required` 台词：

```text
dialogue_id
source_text
final_prompt_text
final_audio_text
final_video_text_or_native_audio_plan
match_status: EXACT | AUTHORIZED_CHANGE | FAIL
```

QC PASS 条件：

  `verbatim_required` 台词在 prompt 或 speech 文本中逐字出现。
  没有因视频任务切分而删除对白。
  没有把角色台词转给错误角色。
  没有把对白改成旁白、沉默、概述或字幕。
  风险替代没有改写对白。

若不满足，必须回到剧本、视频提示词或 speech 阶段修复。

## 角色与空间验收硬规则

必须检查：

  `character_count_expected` 是否等于实际主要应出现角色数量，含主角、配角、群演和群像人物。
  `characters_visible` 是否与分镜一致。
  主要被下游引用的角色是否被遗漏、替换、新增或被错误合并。
  同一角色身份锚点是否跨镜一致。
  `face_structure_3t5e` 是否从剧本 / 生产数据中心继承到资产需求包、角色资产提示词和下游参考图说明。
  `space_truth_id` 是否贯穿对应镜头。
  角色左右、前后、朝向、视线关系是否连续。
  `camera_background_lock` 是否贯穿对应镜头。
  Panel 9 到下一任务 Panel 1 是否存在动作尾势与空间衔接。

角色数量漂移或空间漂移不得靠后期剪辑掩盖，必须回到分镜或视频生成阶段修复。

## 链路冻结验收硬规则

当提示词或任务包进入 `status: frozen` 后：

  不得临场改写 prompt。
  不得替换参考图路径。
  不得改变模型、比例、时长、声音 owner，除非记录变更原因并重新执行 `LOCAL_CHAIN_AUDIT`。
  不得用“优化”“压缩”“更适合模型”等理由删减用户 Skill 中已有规则或删减台词 / 参考图 / 数据字段。

QC 只允许判定 PASS / FAIL / needs_fix。若 FAIL，必须回到最近 producer 阶段补齐，不得直接向下游硬推。

## 视频提示词模板 v2 专项 QC（强制补丁）

  最终用户可见提示词与派发 prompt 是否按固定顺序输出：开场行 → [电影质感] → [画面美学风格] → [环境光影] → [人物站位] → [内容概述] → [情绪氛围] → [衔接参考首帧] → [参考素材] → [要求] → 镜号 → [画面] → [片段结尾] → 台词保真禁令 → [禁令]。
  [电影质感] 是否紧跟开场行，并使用 cinematography_profile_visual_dispatch，不得只粘贴 24fps、180 度快门、EI 等偏物理参数。
  3D 动画 CG 模式下，摄影描述是否转换为“自然电影感运动模糊、窄空间近景构图、温润定焦镜头、电影级景深、克制自然明暗层次”等可见效果。
  写实真人模式下，摄影机 / 镜头参数是否中文化为可见效果描述，例如 ARRI Alexa Mini LF 摄影机质感、库克镜头暖调柔和高光光晕、电影级景深、柔和焦外虚化、自然镜头呼吸感。
  最终 prompt、prompt_chinese_dispatch、沙盒提示词中是否没有出现 FACS、BACS、RACS、AU 编码字样；如出现，标记 FAIL_PERFORMANCE_NATURALIZATION。
  内部任务包是否允许保留 FACS/BACS/RACS 推导字段，并已转换为自然语言表演描述。
  镜号场次是否使用“凌晨、清晨、早晨、中午、下午、傍晚、夜晚、深夜”等高权重时段词，而不是单字“夜”。
  天气与光线是否根据室内 / 室外 / 半室外写清，例如“夜晚 / 室外小雨窗外雨景”“下午 / 窗外阴天室内柔和天光”。
  所有 VO 是否写为“画外音（VO）”，所有 OS 是否写为“内心独白（OS）”。
  [参考素材] 与 reference_image_paths_actual 是否只包含镜号中实际出现、触碰、读屏或使用的素材；镜号未提及的道具不得生成、不得传入。
  每个 video_task_id 是否写入 duration_calculation，并根据台词字数、语速、表演留白、空镜、动作复杂度和摄影方案节奏系数计算推荐时长。
  是否没有为了固定 10 15 秒而压缩台词、加快语速或牺牲表演留白。
  若计算时长超过模型舒适时长，是否拆分为多个 video_task_id，而不是删减对白。


## 视频提示词 v3 防漏字段专项 QC（最高优先级补丁）

  [要求] 是否逐字包含：严格遵守180度轴线与视线匹配原则，严防越轴跳切。画面干净又高级；画面里前中远景递进关系分明。极具影视写实感与物理细节真实感。
  每个提示词是否包含 [画面] 固定块；写实真人模式是否使用“8K写实、人物皮肤纹理清晰”版本；3D 动画 CG 模式是否使用“8K级精细CG渲染、CG角色材质细节清晰、无真实皮肤纹理”版本。
  当前 model_duration_cap_seconds 是否为 15；任何 video_task_id 的 final_duration_seconds 是否 ≤ 15。
  recommended_duration_seconds > 15 时是否拆分 video_task_id；是否没有通过提高语速、删台词、压缩留白来硬塞。
  每个 video_task_id 是否有 weather_light_context，并在 [环境光影] 与每个镜号场次中落地；是否没有只写“室内暖光”而缺少外部天气 / 光线来源。
  画面描述中出现的人物、场景、道具是否全部 @引用；画外音（VO）、内心独白（OS）和逐字台词内部名称是否正确标记为例外。
  镜号中出现的道具是否全部有对应资产；含文字 / 符号 / 数字 / 消息 / 书名 / 项目名 / 备注的道具是否即使只出现一次也生成单道具资产。
  每个镜号内某角色首次画外音（VO）、内心独白（OS）或说台词前，是否有不少于3句完整音色描述；是否禁止“同上 / 延续前句 / 保持前述音色”。
  用户未启用舞台定位图时，[禁令] 是否没有写舞台坐标网格、色块、箭头、形状编码、坐标标注。
  用户未启用黑白分镜图时，[禁令] 是否没有写黑白分镜质感、草图线条、分镜边框、白底分镜背景。
  是否每个 video_task_id 都独立完整展开全部字段，没有首段完整、后续压缩简化。

任一不通过，对应状态必须标记 FAIL_VIDEO_PROMPT_V3_COMPLETENESS，不得冻结或派发。


## 视频提示词 v4 回归防护 QC（最高优先级补丁）

  [要求] 第一句是否为“@<场景方向资产名>为背景保持<方向>机位，严格遵守180度轴线与视线匹配原则...”格式。若缺失，标记 FAIL_SCENE_REQUIREMENT_PREFIX_MISSING。
  [禁令] 是否以“视频全程严禁出现外形、着装、配饰完全相同的两个人;杜绝双胞胎或分身效果，确保同一时刻画面中该人物唯一”开头。若缺失，标记 FAIL_UNIQUE_CHARACTER_BAN_MISSING。
  所有非画外音（VO）、非内心独白（OS）的说出口台词，是否写为“@角色 + 情绪 / 动作 / 语气 + 说：{dispatch_text}”。若出现“角色名：{台词}”，标记 FAIL_SPOKEN_DIALOGUE_AT_EMOTION_MISSING。
  每个镜号是否有独立“备注：”。若缺失，标记 FAIL_SHOT_REMARK_MISSING。
  每句派发台词是否有 dialogue_pronunciation_rewrite_map；无替换也必须标记 no_rewrite_needed。
  多音字 / 生僻字替换是否只作用于 dispatch_text，未覆盖 source_text。
  替换优先级是否按：剧本剧情描述 ＞ 文字词语用法正确性 ＞ 日常常用读音 ＞ 姓名字多用文字读音。
  若上述任一失败，video_prompt_v4_regression_status 必须为 FAIL_VIDEO_PROMPT_V4_REGRESSION，不得冻结或派发。


## 资产 v5 与景别优先级 QC（最高优先级补丁）

  每个角色 look_variant 提示词是否完整展开身份锚点、别名、同一身份主键、三庭五眼、体型气质、服装锚点、状态变化、时代朝代职位锁、连续性禁令和负面提示；是否没有用“完整继承 / 同一身份 / 继承上版”替代关键字段。若失败，标记 FAIL_ASSET_VARIANT_PROMPT_COMPRESSION。
  后续角色变体是否引用 source_identity_asset_ref，并说明只修改允许变化字段，同时完整展开三庭五眼。
  period_world_lock 是否完整：era_dynasty_lock、period_region_lock、official_rank_role_lock、costume_regulation_lock、prop_period_lock、scene_architecture_period_lock。若缺失，标记 FAIL_PERIOD_STATUS_LOCK_MISSING。
  角色、场景、道具是否都有 state_variant_chain，含 before_state、after_state、change_trigger、continuity_keep、continuity_change。
  prop_state_variant_plan 是否状态绑定优先，且没有无脑每状态出图；独立状态资产是否只用于外观本体变化、文字证据特写、破损沾灰湿痕明显、剧情反转或读屏状态。
  shared_prop_visual_anchor 是否在角色资产与单独道具资产中逐字一致。
  分镜和视频是否默认优先大特写、特写、近景、中景，以及前景对焦加背景高虚化。
  远景、全景、大远景是否有 strong_story_need；若无，标记 FAIL_SHOT_SCALE_PRIORITY_OVERRIDE。
  剧本视觉备注是否没有覆盖 Skill 景别和资产规则。


