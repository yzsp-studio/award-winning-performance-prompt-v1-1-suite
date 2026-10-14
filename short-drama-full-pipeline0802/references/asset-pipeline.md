# 短剧资产拆解流程

## 目标

把剧本转成可生成、可复用、可追踪的视觉资产清单。资产阶段必须服从启动弹窗选择的 `production_visual_mode`：

```text
cinematic_realistic = 写实真人风格
top_chinese_3d_animation_cg = 3D 动画 CG 风格
```

## 资产阶段总原则

1. 角色资产支持双模式：写实真人模式 / 3D 动画 CG 模式。
2. 场景资产不再生成六视图 / 六分区 / 六宫格合成图，改为按视频任务需要的视角方向单独生成。
3. 道具资产不再生成九宫格 / 自动网格 / 多道具合并图，改为按道具单独生成。
4. 舞台定位图和黑白分镜图默认不推荐生成，是否生成由分镜阶段弹窗决定。
5. 所有资产提示词必须保留 `模型：image2`，分类型使用画质 / 清晰度参数。
6. 所有角色、场景、道具资产提示词必须完整继承 `global_style_lock` 与 `tone_profile_lock`。风格配置与影调配置来自 `references/style-tone-presets.md`，不得只写预设 ID。
7. 所有用户可见资产提示词文档实行“极限全中文”：字段名、段落标题、描述正文、负面提示均必须中文化；不得为了模型理解把角色、场景、道具描述主体写成英文；不得输出中英并列提示词。
8. 用户可见资产文档中唯一允许保留的非中文内容：模型名（如 image2）、必要编号、版本号、项目链路 ID、文件路径，以及用户明确要求保留的非中文台词或入画文字。英文参数、英文枚举值、机器 token、英文禁止词只允许存在于内部派单映射层，不得混入用户可见资产提示词正文。
9. 历史模板中的英文结构词必须改写为中文等价词：`Negative Prompt` 输出为“负面提示”，`front view / side view / back view` 输出为“正面视图 / 侧面视图 / 背面视图”，`Native audio` 不得出现在资产提示词中。负面提示用户可见层必须全部中文化。
10. 资产提示词完整合同：每个需要生成的角色、场景、道具都必须输出一段可复制、可独立派单的完整提示词块，不得只写表格行，不得只写“同上 / 参考前文 / 按首个角色 / 继承上文”。后续任一资产的字段数量、段落结构、风格锁展开、影调锁展开、负面提示、连续性禁令和细节密度不得低于第一个资产。
11. 逐资产矩阵验收：生成资产提示词文档后，必须建立角色 / 场景 / 道具逐项验收矩阵，逐个检查模型、比例、清晰度、画质、视觉模式、全局风格锁、影调配置锁、核心描述、布局要求、继承字段、负面提示、连续性禁令、下游用途。任一格缺失即 `FAIL_ASSET_PROMPT_COMPLETENESS_MATRIX`，不得进入真实生图或下游分镜。
12. 全链路完整扩容：资产提示词、分镜任务、关键帧任务、视频任务包、声音任务包、后期任务包都必须独立展开当前任务所需信息；不得用“同上”“按前面”“参考上文”承接关键字段；不得为了节省篇幅压缩后续任务。

## 角色资产字段

* character_id：稳定编号，如 C01。
* 角色名：中文名。
* 剧情功能：主角、反派、盟友、情感对象、关键证人、群像框选人物。
* 年龄段：写实真人模式可登记真实可视化年龄；3D 动画 CG 模式必须转成阶段型动画角色资产语言。
* 外观锚点：发型、三庭五眼五官气质、身形、服装风格、标志物。
* 状态变化：日常、宴会、受伤、崩溃、胜利、伪装等。
* 首次出现：集数和场次。
* 复用频率：高 / 中 / 低。
* 需要资产：角色资产参考图、服装三视图、表情组、服装变化、状态变化。

## 场景资产字段

* scene_id：如 SCE01。
* scene_name：场景名。
* scene_view_orientation：正面 / 反向 / 左侧 / 右侧 / 俯视 / 鸟瞰 / 关键机位光影。
* scene_view_asset_id：场景方向资产稳定编号，例如 SCE01-FRONT、SCE01-REVERSE。
* scene_view_ref_image_path：该方向单张场景资产图路径或 pending。
* camera_background_lock：使用该图时，视频提示词中所有镜头必须遵循该方向作为背景机位。
* 剧情功能：压迫、告白、争吵、揭露、追逐。
* 空间结构：入口、桌椅、窗、走廊、楼梯、关键道具位置。
* 氛围：冷、暖、压抑、奢华、破败、危险。
* 复用频率：固定主场景优先做高质量参考图。
* 需要角度：由视频任务计划决定，不再一次性合成六视图。

## 道具资产字段

* prop_id：如 P01。
* prop_name：道具名。
* plot_function：证据、身份、威胁、情感信物、权力凭证。
* appearance_count：该道具在当前制作范围内出现次数。
* text_symbol_risk：是否含文字、符号、印章、数字、乱码、图样、准确标记。
* animation_precision_risk：是否需要非常准确的动效，例如数字变化、乱码变化、印章盖印、字迹浮现、纸条展开。
* prop_asset_required：true / false。
* prop_asset_reason：appearance_count_ge_2 / single_use_text_symbol_risk / animation_precision_risk / skipped_single_use_no_text。
* prop_ref_image_path：单道具资产图路径或 pending。
* prop_animation_reference：需要动效参考视频时登记路径或 pending。
* prop_animation_reference_filename_required：`道具动效参考-<prop_id>-<道具名>.mp4`。
* prop_animation_description：动效变化简述。

## image2 资产派单参数

| 资产类型 | 模型 | 比例 | 清晰度 | 画质 |
|---|---|---|---|---|
| 角色资产 | image2 | 16:9 | 2K | 高 |
| 场景资产 | image2 | 16:9 | 2K | 高 |
| 道具资产 | image2 | 16:9 | 2K | 高 |

高清增强策略：资产基础生成统一使用“画质：高、清晰度：2K、比例：16:9”。资产图生成后，若当前运行环境或画布提供“高清增强 / 分辨率提升 / upscale”功能，必须自动执行高清增强至 4K，并把增强后路径写回资产池；若当前 agent 无法调用该功能，必须明确提示用户在画布中对对应资产执行高清增强至 4K，不得假装已经增强完成。

## 角色造型变体与场景状态变体资产生成

资产阶段必须消费 `current_active_snapshot_resolved` 中的 `character_look_variant_plan` 与 `scene_state_variant_plan`，不得临场重算或跳过。

### 角色造型变体资产

每个 `asset_required: true` 的 `look_variant_id` 都必须生成或登记一张对应人物资产图。人物资产图仍使用左 50% 面部身份锁定区 + 右 50% 服装三视图布局，但右侧三视图必须对应该 `look_variant_id` 的服装、妆造、发型、发饰、年龄阶段、伤损、武器和贴身道具。

角色核心身份锚点不得因造型变体改变。允许变化的只有：服装、妆造、妆感、发型、发饰、伤损、年龄阶段表现、武器、贴身道具、天气/季节造成的湿污或破损。

必须登记：

```text
character_variant_asset:
  asset_id:
  character_id:
  look_variant_id:
  look_variant_name:
  inherited_identity_anchor:
  inherited_face_structure_3t5e:
  costume:
  makeup_design:
  makeup_texture:
  hairstyle:
  hair_accessories:
  visible_age_stage:
  damage_or_weathering:
  carried_weapon:
  carried_body_prop:
  applicable_scene_ids: []
  applicable_video_task_ids: []
  asset_path: pending | <path>
  status: ACTIVE | PENDING | FAIL | DEPRECATED
```

### 场景状态变体资产

每个 `variant_asset_required: true` 的 `scene_state_variant_id` 必须按需要的方向生成对应场景状态资产图。用户已确认：季节、天气、日/夜、受损、新增固定道具、剧情状态或光源状态每次变化都新图。

必须登记：

```text
scene_state_variant_asset:
  asset_id:
  scene_id:
  scene_state_variant_id:
  scene_view_orientation:
  scene_view_asset_id:
  season_state:
  weather_state:
  time_of_day_state:
  damage_state:
  added_fixed_props: []
  removed_fixed_props: []
  lighting_state:
  camera_background_lock:
  applicable_video_task_ids: []
  asset_path: pending | <path>
  status: ACTIVE | PENDING | FAIL | DEPRECATED
```

视频提示词阶段只允许使用与当前 `video_task_id` 匹配的角色造型变体资产和场景状态变体资产，不得用默认图替代。

## A3 资产门硬规则

资产阶段必须先完成 A3 资产门，再允许进入分镜或视频提示词阶段。A3 资产门包括：

1. `A3-CHARACTER`：主要角色身份资产可追踪。
2. `A3-SCENE`：关键场景方向资产可追踪。
3. `A3-PROP`：关键道具资产可追踪，或明确登记跳过原因。

每个资产必须写入生产数据中心资产池：

```text
asset_id: <稳定编号>
asset_type: character | scene_view | prop | lighting | role_highlight_video | stage_map | storyboard_data | storyboard_image_optional
asset_name: <名称>
asset_path: <真实路径或 pending>
reference_role: <身份 / 场景方向 / 道具 / 声音 / 分镜数据>
production_visual_mode: cinematic_realistic | top_chinese_3d_animation_cg
global_style_preset_id: <继承生产数据中心>
global_style_lock: <完整风格配置正文，来自 references/style-tone-presets.md>
tone_profile_preset_id: <继承生产数据中心>
tone_profile_lock: <完整影调配置正文，来自 references/style-tone-presets.md>
style_tone_inheritance_status: PASS | FAIL
source_scene_ids: []
source_dialogue_ids: []
used_by_video_tasks: []
status: ACTIVE | DEPRECATED | PENDING | FAIL | SKIPPED
replacement_of: <如有>
```

只有 `status: ACTIVE` 且 `asset_path` 非空的资产，才能进入下游参考图清单。`PENDING`、`FAIL`、空路径、临时描述都不得作为视频参考图。道具若被判定为不需要出图，必须登记 `status: SKIPPED` 与 `prop_asset_reason: skipped_single_use_no_text`。

## 角色资产加硬字段

每个主要角色必须补齐：

```text
character_id
character_name
character_name_aliases: []
canonical_identity_label
identity_anchor: <脸型 / 五官 / 发型 / 体型 / 气质 / 标志物>
face_structure_3t5e: <从生产数据中心继承的三庭五眼结构，不得为空>
costume_anchor: <主服装与可变服装边界>
state_variants: [日常, 受伤, 崩溃, 胜利等]
character_ref_image_path: <真实路径或 pending>
role_highlight_video_path: <真实路径或 not_required / pending>
first_scene_id
reuse_level: high | mid | low
continuity_forbidden_changes: []
production_visual_mode: cinematic_realistic | top_chinese_3d_animation_cg
character_asset_prompt_source: realistic_prompt | animation_converter
```

身份锚点不得被状态变化改写。服装、妆发、伤痕、血迹、泥灰可以变化，但脸、体型、核心气质和标志物不能漂移。`face_structure_3t5e` 必须从剧本阶段和生产数据中心继承；若上游没有该字段，资产阶段不得临场跳过，必须回到剧本 / 人物设定阶段补齐后再继续。

## 角色资产参考图提示词格式加硬规则

角色资产参考图必须作为 A3-CHARACTER 资产链路的一部分生成和登记。生成完成后仍必须写回生产数据中心资产池，且只有 `status: ACTIVE`、`asset_path` 非空的角色资产才能进入下游分镜、关键帧和视频提示词参考图清单。

### 固定画面布局（双模式共用）

角色资产图必须采用单张 16:9 综合参考图布局：

```text
画面布局：左 50% 为面部身份锁定区，右 50% 为服装结构锁定区。
左 50%：面部角色设定展示 / 正面观察视角 / 面部朝向正前方 / 默认无表情展示姿态。
右 50%：同一角色、同一体型、同一气质、同一套服装的水平 1x3 服装三视图：正面、侧面、背面。
正面、侧面视图：颈部以下无头 body-only 服装结构展示，仅显示颈部以下身体和完整服装结构；服装必须从颈部完整覆盖至脚部，无头部和脸部；双手双脚完整可见，脚底下方留白。
背面视图：保留完整头部，须呈现后脑发型轮廓、颈部、背面服装轮廓、完整身体至脚部；双手双脚完整可见，脚底下方留白。
三视图必须为同一角色、同一体型、同一套服装，禁止画成三个不同的人。
```

### 写实真人角色资产派单

```text
模型：image2
比例：16:9
清晰度：2K
画质：高
production_visual_mode: cinematic_realistic
global_style_preset_id: <继承生产数据中心>
global_style_lock: <完整风格配置正文，来自 references/style-tone-presets.md>
tone_profile_preset_id: <继承生产数据中心>
tone_profile_lock: <完整影调配置正文，来自 references/style-tone-presets.md>
style_tone_inheritance_status: PASS

生成图片：写实真人电影资产参考图，不是海报，平光、无重阴影。
统一纯中灰色背景 #7c7c7c，无文字、无标签、无水印、无字幕、无任何 UI 元素。

角色：<从 character_id / character_name / character_name_aliases / canonical_identity_label / identity_anchor / face_structure_3t5e / costume_anchor / state_variants / 剧本人物设定提取的角色身份、年龄段、性别、时代、视觉气质、状态、服装；不得套用其它角色示例。所有角色必须使用同一细节标准，不得主角详细、配角简略。>

三庭五眼面部结构：
上庭：<额头、发际线、额面比例与气质。>
中庭：<眉眼、鼻梁、颧骨、面中结构与人物处境。>
下庭：<人中、唇形、下颌、下巴比例与年龄 / 情绪。>
五眼：<眼距、眼长、眉眼比例、眼神气质。>
整体骨相：<脸型、骨骼感、软组织状态、真实人类自然不完美。>
```

写实真人模式可使用真实人类面部特征和自然生理不完美，但仍不得让角色资产变成海报、写真、广告图、多套服装或多人合影。


### 写实真人角色变体完整提示词模板（v5 防压缩专用）

每个 look_variant_id 必须完整输出，不得只写“完整继承 / 同一身份 / 继承上版”。后续变体可以用 source_identity_asset_ref 引用基础角色资产图，但文本仍必须完整展开。

```text
模型：image2
比例：16:9
清晰度：2K
画质：高
production_visual_mode: cinematic_realistic
global_style_preset_id: <继承生产数据中心>
global_style_lock: <完整风格配置正文，不得只写预设 ID>
tone_profile_preset_id: <继承生产数据中心>
tone_profile_lock: <完整影调配置正文，不得只写预设 ID>
style_tone_inheritance_status: PASS
asset_id: <角色变体资产编号>
character_id: <角色稳定编号>
character_name: <角色名>
character_name_aliases: [<别名 / 身份称呼 / 伪装名，如无写 none>]
canonical_identity_label: <同一身体 / 同一人物身份主键>
source_identity_asset_ref: <基础角色资产图路径或 @基础角色资产名；基础变体写 none>
look_variant_id: <造型变体编号>
look_variant_name: <造型变体名>
applicable_scene_ids: [<适用场次>]
applicable_video_task_ids: [<适用视频任务>]
era_dynasty_lock: <朝代 / 年代 / 历史时期；现代戏写现代城市年代语境>
period_region_lock: <地域制度 / 城市 / 县府 / 宫廷 / 战时或平时制度>
official_rank_role_lock: <职位 / 职务 / 官阶 / 社会身份>
costume_regulation_lock: <服饰制度 / 官服等级 / 常服 / 礼服 / 战后状态 / 禁止错代服饰>
prop_period_lock: <随身器物年代 / 材质 / 制式；如无写 none>
生成图片：写实真人电影资产参考图，不是海报，不是写真，不是广告图。单张 16:9 综合角色资产图，平光、无重阴影，统一纯中灰色背景 #7c7c7c，无文字、无标签、无水印、无字幕、无 UI。
画面布局：左 50% 为面部身份锁定区；右 50% 为服装结构锁定区。左侧为同一角色面部设定展示，正面观察视角，面部朝向正前方，默认无表情。右侧为同一角色、同一体型、同一气质、同一套服装的水平 1x3 服装三视图：正面、侧面、背面。正面和侧面视图为颈部以下无头 body-only；背面视图保留完整头部与后脑发型轮廓。
角色身份锚点：<脸型、骨相、眉眼、鼻梁、颧骨、嘴唇、下颌、发型、体型、身高体态、气质、标志物；必须完整展开。>
三庭五眼面部结构：
上庭：<额头、发际线、额面比例、皱纹 / 疲态等。>
中庭：<眉形、眼型、眼距、鼻梁、鼻头、颧骨、面中起伏、法令或泪沟状态等。>
下庭：<人中、唇形、嘴角、下颌线、下巴比例、咬肌 / 软组织状态等。>
五眼：<眼距、眼长、左右眼平衡、眉眼间距、眼神气质。>
整体骨相：<脸型、头脸比例、真实人类自然不完美、年龄阶段可视特征。>
体型气质：<肩宽、颈肩关系、体态、身材比例、身份带来的身体状态。>
服装锚点：<完整服装、配饰、材质、纹理、磨损、湿痕、血迹、灰尘、破损位置；如有随身道具，使用 shared_prop_visual_anchor 的逐字描述。>
状态变化链：before_state: <变化前状态>; after_state: <本变体状态>; change_trigger: <剧情触发原因>; continuity_keep: <不变的脸、骨相、体型、气质、服饰制度、共享道具锚点>; continuity_change: <允许改变的服装、妆发、湿痕、灰尘、破损、伤损、疲惫、血迹等>
连续性禁令：不得改变角色脸型、五官比例、三庭五眼、体型、核心气质、身份主键；不得把该角色画成另一个人；不得把右侧三视图画成不同人物；不得把 source_identity_asset_ref 仅当风格参考而丢失身份。
负面提示：海报感、广告大片、影楼写真、过度磨皮、AI 网红脸、霸总短剧海报、浓重阴影、多人合影、三个人脸不一致、服装三视图漂移、截脚、畸形手、畸形脚、多指、少指、融合手指、画面文字、字幕、水印、标签、签名、边框、UI。
```

### 3D 动画 CG 角色资产派单

进入本模式前必须读取 `references/animation-character-converter.md`。上游若已经有真人版本角色描述提示词，必须先用该转换器转为 3D 动画 CG 角色资产术语，再派 image2。

```text
模型：image2
比例：16:9
清晰度：2K
画质：高
production_visual_mode: top_chinese_3d_animation_cg
global_style_preset_id: <继承生产数据中心>
global_style_lock: <完整风格配置正文，来自 references/style-tone-presets.md>
tone_profile_preset_id: <继承生产数据中心>
tone_profile_lock: <完整影调配置正文，来自 references/style-tone-presets.md>
style_tone_inheritance_status: PASS
animation_quality_bar: porcelain_SSS_skin + soft_bloom_glow + Octane_render + flawless_CG_shading
animation_negative_lock: real_human_photorealistic_metahuman_skin_pores_forbidden

生成图片：国漫顶级3D动画CG电影角色资产参考图，不是海报。角色设定参考图，16:9 横图。东方仙侠顶级3D动画渲染，国产顶级影视CG质感，商业级电影渲染，高纯度无瑕CG材质，高调透气柔光，柔和漫射无重阴影，干净白色或浅灰色棚拍背景，色彩透亮低饱和。

左侧 50%：同一角色的面部角色设定展示，正面观察视角，面部朝向正前方，默认无表情展示姿态。必须清晰呈现东方动画角色骨相设计、三庭五眼结构、眼睑结构层次、下眼睑柔和结构设计、水晶玻璃质感CG眼球、精细睫毛模型结构、CG唇部轮廓结构、默认闭合嘴型、CG毛发shader光泽、CG角色陶瓷化SSS皮肤shader、无真实皮肤纹理、纯CG表面材质。

右侧 50%：同一角色的水平 1x3 服装三视图。正面视图与侧面视图为颈部以下无头 body-only 服装结构展示，背面视图保留完整头部与后脑发型轮廓。三视图必须是同一角色、同一体型、同一比例、同一服装、同一材质，不得生成三个不同角色。

角色资产描述：<把待转换角色设定中的脸型、五官、发型、服装、状态、标志物、气质全部转成 3D 动画 CG 角色资产术语；不得写职业介绍、阶层介绍、真人年龄数字、真人肖像词。>

负面提示：真人实拍感、照片级写实、数字人质感、真实皮肤毛孔、真人摄影、真人肖像、真实皮肤、影楼写真、画面文字、字母、字幕、水印、标签、注释、签名、边框、画面裁切、圆眼卡通感、眼距过宽、大眼卡通感、幼态 Q 版、婴儿脸、塑料娃娃感、嘴唇过度油亮、嘴唇过度磨皮、颅顶过低、假睫毛感、医美式眼睑、韩式网游脸、手办质感、玩具材质、多人合影、多套服装、截脚、畸形手、畸形脚、多指、少指、融合手指。
```


### 3D 动画 CG 角色变体完整提示词模板（v5 防压缩专用）

本模板专用于 `production_visual_mode: top_chinese_3d_animation_cg`，与写实真人角色变体模板同等级。每个 3D CG `look_variant_id` 都必须完整输出，不得只写“完整继承 / 同一身份 / 继承上版 / 沿用基础模型”。后续变体可以用 `source_identity_asset_ref` 引用基础 3D CG 角色资产图作为面部身份、骨相、体型和 CG 材质基础，但文本仍必须完整展开，并且必须经过 `references/animation-character-converter.md` 的 3D CG 术语转换。

```text
模型：image2
比例：16:9
清晰度：2K
画质：高
production_visual_mode: top_chinese_3d_animation_cg
global_style_preset_id: <继承生产数据中心>
global_style_lock: <完整风格配置正文，必须为 STYLE-ANIM-CG-*，不得只写预设 ID>
tone_profile_preset_id: <继承生产数据中心>
tone_profile_lock: <完整影调配置正文，必须为 TONE-ANIM-CG-*，不得只写预设 ID>
style_tone_inheritance_status: PASS
animation_quality_bar: porcelain_SSS_skin + soft_bloom_glow + Octane_render + flawless_CG_shading
animation_negative_lock: real_human_photorealistic_metahuman_skin_pores_forbidden
animation_converter_source: references/animation-character-converter.md
animation_converter_qc_status: PASS

asset_id: <角色变体资产编号，例如 C01-LV02>
character_id: <角色稳定编号>
character_name: <角色名>
character_name_aliases: [<剧情中所有别名 / 身份称呼 / 伪装名，如无写 none>]
canonical_identity_label: <同一身体 / 同一人物身份主键>
source_identity_asset_ref: <基础 3D CG 角色资产图路径或 @基础角色资产名；基础变体写 none>
look_variant_id: <造型变体编号>
look_variant_name: <造型变体名，如“夜雨湿痕常服”“战损官服”“宴会礼服”>
applicable_scene_ids: [<适用场次>]
applicable_video_task_ids: [<适用视频任务>]

era_dynasty_lock: <朝代 / 年代 / 历史时期；现代戏写现代城市年代语境>
period_region_lock: <地域制度 / 城市 / 县府 / 宫廷 / 战时或平时制度>
official_rank_role_lock: <职位 / 职务 / 官阶 / 社会身份；3D CG 中改写为可视化身份阶层与服饰等级，不写职业介绍段落>
costume_regulation_lock: <服饰制度 / 官服等级 / 常服 / 礼服 / 战后状态 / 禁止错代服饰>
prop_period_lock: <随身器物年代 / 材质 / 制式；如无写 none>

生成图片：国漫顶级 3D 动画 CG 电影角色变体资产参考图，不是真人实拍，不是照片，不是海报。单张 16:9 综合角色资产图，高调透气柔光，柔和漫射无重阴影，干净白色或浅灰色棚拍背景，无文字、无标签、无水印、无字幕、无 UI。

画面布局：左 50% 为面部身份锁定区；右 50% 为服装结构锁定区。左侧为同一角色的面部角色设定展示，正面观察视角，面部朝向正前方，默认无表情展示姿态。右侧为同一角色、同一体型、同一比例、同一气质、同一套服装的水平 1x3 服装三视图：正面、侧面、背面。正面和侧面视图为颈部以下无头 body-only 服装结构展示；背面视图保留完整头部与后脑发型轮廓。三视图必须是同一个 3D CG 角色，不得生成三个不同角色。

3D CG 角色身份锚点：<东方动画角色脸型、骨相设计、眉眼结构、鼻梁结构、颧骨结构、CG 唇部轮廓、下颌线、CG 毛发 shader、体型比例、身高体态、气质、标志物；必须完整展开，不得写“继承上版”。>

三庭五眼面部结构（3D CG 术语）：
上庭：<额头体块、发际线形状、额面比例、CG 角色年龄阶段可视特征。>
中庭：<眉形、眼睑结构层次、下眼睑柔和结构设计、眼距、鼻梁、鼻头、颧骨、面中体块。>
下庭：<人中结构、CG 唇部轮廓结构、嘴角、下颌线、下巴比例、面部软组织的 CG 体块感。>
五眼：<眼距、眼长、左右眼平衡、眉眼间距、水晶玻璃质感 CG 眼球与眼神气质。>
整体骨相与材质：<东方美型 3D 角色骨相、陶瓷化 SSS 皮肤 shader、柔和 bloom、无真实皮肤毛孔、无真人皮肤纹理。>

体型气质：<肩宽、颈肩关系、体态、身材比例、角色身份带来的站姿气质，全部使用 3D CG 角色资产语言。>
服装锚点：<本 look_variant 的完整服装、发饰、配饰、材质、纹理、磨损、湿痕、血迹、灰尘、破损位置；如有随身道具，使用 shared_prop_visual_anchor 的逐字描述，并转换为 3D CG 材质语言。>
状态变化链：before_state: <变化前状态>; after_state: <本变体状态>; change_trigger: <剧情触发原因>; continuity_keep: <必须保持不变的脸、骨相、体型、气质、CG 材质标准、服饰制度、共享道具锚点>; continuity_change: <允许改变的服装、妆发、湿痕、灰尘、破损、伤损、疲惫、血迹等>

连续性禁令：不得改变角色脸型、五官比例、三庭五眼、体型、核心气质、身份主键；不得把该角色画成另一个 3D CG 角色；不得把右侧三视图画成不同人物；不得出现真人实拍感、照片级写实、数字人皮肤毛孔、真人摄影、真人肖像；不得把 source_identity_asset_ref 仅当风格参考而丢失身份。
负面提示：真人实拍感、照片级写实、数字人质感、真实皮肤毛孔、真人摄影、真人肖像、真实皮肤、影楼写真、画面文字、字母、字幕、水印、标签、注释、签名、边框、圆眼卡通感、大眼卡通感、幼态 Q 版、塑料娃娃感、多人合影、三个人脸不一致、服装三视图漂移、截脚、畸形手、畸形脚、多指、少指、融合手指。
```

### 3D 动画 CG 输出前 QC

提示词发给 image2 之前必须检查：

- 是否还出现 real human / photorealistic / metahuman / skin pores / 真人 / 写实真人 / 真人摄影 / 真人肖像 / 真人皮肤 / 真实毛孔。
- 是否还出现真实岁数数字。
- 是否出现职业介绍、阶层介绍、人物人设介绍，而不是角色资产可视化锚点。
- 是否把“正脸特写 / 直视镜头 / 肖像 / 人像 / 真实皮肤 / 卧蚕 / 双眼皮 / 唇峰 / 肤色”等风险词替换为 3D 动画角色资产术语。
- 是否保留角色核心设定，不得把人物改成另一个角色。

## 场景方向单图资产硬规则

关键场景或复用场景必须按下游视频提示词需要的方向生成单张场景资产图。禁止输出六视图 / 六分区 / 六宫格合成图。

### 场景资产登记字段

```text
scene_id
scene_name
scene_view_asset_id: <scene_id>-FRONT | REVERSE | LEFT | RIGHT | TOP | KEYLIGHT
scene_view_orientation: front | reverse | left | right | top | keylight
scene_view_display_name: 正面 / 反向 / 左侧 / 右侧 / 俯视 / 关键机位光影
scene_view_ref_image_path: <真实路径或 pending>
scene_view_source_video_tasks: []
camera_background_lock: <使用该场景图时所有镜头必须遵循的背景机位方向>
scene_era_profile
scene_atmosphere_profile
scene_art_direction_profile
project_visual_tone
entrance_exit_map
fixed_prop_positions
usable_shot_angles
status: ACTIVE | PENDING | FAIL
```

### 场景资产 prompt 骨架

```text
模型：image2
比例：16:9
清晰度：2K
画质：高
production_visual_mode: <继承项目模式>
global_style_preset_id: <继承生产数据中心>
global_style_lock: <完整风格配置正文，来自 references/style-tone-presets.md>
tone_profile_preset_id: <继承生产数据中心>
tone_profile_lock: <完整影调配置正文，来自 references/style-tone-presets.md>
style_tone_inheritance_status: PASS

生成图片：<按 production_visual_mode 写“写实真人电影场景资产参考图”或“国漫顶级3D动画CG电影场景资产参考图”>，不是海报。单张场景方向资产图，不是六视图，不是宫格图，不是拼贴图。

scene_id: <场景稳定编号>
scene_name: <场景名>
scene_view_asset_id: <方向资产编号>
scene_view_orientation: <front / reverse / left / right / top / keylight>
source_scene_ids: [<来自剧本的 scene_id>]
used_by_video_tasks: [<后续 video_task_id>]
scene_era_profile: <朝代 / 时代 / 制式，必须来自项目设定或生产数据中心>
scene_atmosphere_profile: <压迫 / 冷清 / 温情 / 危险等，必须来自剧情功能与场次情绪>
scene_art_direction_profile: <建筑、材质、陈设、门窗、家具、地面、墙面、器物体系>
project_visual_tone: <项目总视觉基调>
light_time_variants:
  primary_time: <夜 / 清晨 / 日间 / 黄昏 / 室内烛光等>
  key_light_source: <窗光 / 烛火 / 天光 / 门外冷光等>
  shadow_direction: <主要阴影方向>
  mood_light: <压迫 / 冷清 / 权力感 / 危险等>
entrance_exit_map: <入口、出口、门、窗、走廊、楼梯等>
fixed_prop_positions: <灵位、桌案、屏风、椅、账箱等固定道具位置>
usable_shot_angles: <只允许与 scene_view_orientation 一致的镜头方向>

画面要求：单张 16:9 场景资产图，只呈现 scene_view_orientation 对应方向的完整空间，不得做六分区，不得合成多张，不得出现人物、群演、画面文字、标签、水印、字幕、UI、颜色框、数字、stable_id。

下游方向锁定：后续视频提示词使用本图时，所有镜头都必须遵循 scene_view_orientation 作为背景机位；不得临场改成其它方向。
```

## 道具单图资产硬规则

道具资产必须先做使用次数和文字 / 符号风险判断，再决定是否生成。

### 道具生成判定

```text
appearance_count >= 2 -> prop_asset_required: true
appearance_count == 1 and text_symbol_risk == true -> prop_asset_required: true
appearance_count == 1 and animation_precision_risk == true -> prop_asset_required: true + prop_animation_reference_required: true
appearance_count == 1 and text_symbol_risk == false and animation_precision_risk == false -> prop_asset_required: false, prop_asset_reason: skipped_single_use_no_text
```

### 道具动效参考视频提醒

如果 `animation_precision_risk: true`，必须用弹窗提醒用户：

```text
该道具需要非常准确的动画效果。请在视频派单前提供参考视频，并命名为：道具动效参考-<prop_id>-<道具名>.mp4。该参考视频将在对应视频任务中作为该道具动画效果参考使用。
```

### 道具资产 prompt 骨架

```text
模型：image2
比例：16:9
清晰度：2K
画质：高
production_visual_mode: <继承项目模式>
global_style_preset_id: <继承生产数据中心>
global_style_lock: <完整风格配置正文，来自 references/style-tone-presets.md>
tone_profile_preset_id: <继承生产数据中心>
tone_profile_lock: <完整影调配置正文，来自 references/style-tone-presets.md>
style_tone_inheritance_status: PASS

生成图片：<按 production_visual_mode 写“写实真人电影道具资产参考图”或“国漫顶级3D动画CG电影道具资产参考图”>，不是海报。单个道具资产图，不是九宫格，不是自动网格，不是多道具合并图，不是拼贴图。

prop_id: <道具稳定编号>
prop_name: <道具名>
plot_function: <证据 / 身份 / 威胁 / 情感信物 / 权力凭证>
appearance_count: <出现次数>
prop_asset_reason: <appearance_count_ge_2 / single_use_text_symbol_risk / animation_precision_risk>
first_scene_id: <首次出现场次>
owner_character_id: <持有人或关联角色>
used_by_video_tasks: [<后续 video_task_id>]
closeup_required: true | false
text_or_marking_lock: <道具上的关键文字、印章、暗纹、划痕、磨损、血迹等，如无则写 none>
material_anchor: <纸张 / 金属 / 玉 / 木 / 布 / 药包 / 印泥等材质>
size_and_handling: <手持尺寸、桌面尺寸、佩戴方式、开合方式等>
continuity_forbidden_changes: [<不可改变的形状、材质、文字、破损位置>]
prop_animation_reference_required: true | false
prop_animation_reference_filename_required: <如需，写“道具动效参考-<prop_id>-<道具名>.mp4”>

画面要求：单个道具居中展示，16:9 横图，干净背景，无人物、无手部、无场景干扰、无多道具拼接、无宫格、无颜色框、无数字编号、无道具名标签、无 prop_id、无字幕、无 UI、无水印。若道具有文字 / 印章 / 符号，必须清晰呈现并保持与 text_or_marking_lock 一致。
```

## 链路继承与阻断

角色、场景、道具资产生成后，必须登记：

```text
asset_id
asset_type: character | scene_view | prop
asset_name
asset_path
reference_role
production_visual_mode
global_style_preset_id
global_style_lock
tone_profile_preset_id
tone_profile_lock
style_tone_inheritance_status
source_scene_ids
source_dialogue_ids
used_by_video_tasks
status
```

若角色资产图缺少真实路径、未按左 50% 面部角色设定展示 + 右 50% 水平 1x3 服装三视图生成、未消费生产数据中心中的 `face_structure_3t5e`、三庭五眼身份描述缺失、未登记 `character_name_aliases` / `canonical_identity_label` 导致双魂 / 改名 / 伪装身份混乱、服装三视图漂移、三视图被画成三个不同的人、或 `production_visual_mode` 与项目不一致，则 `asset_gate_status: FAIL`，不得进入分镜、关键帧或视频提示词阶段。

若角色、场景或道具资产提示词缺少完整 `global_style_lock`、完整 `tone_profile_lock`，或仅写预设 ID 而未展开配置正文，则 `asset_gate_status: FAIL_STYLE_TONE_INHERITANCE`，不得进入分镜、关键帧或视频提示词阶段。

若 3D 动画 CG 模式下角色提示词仍含真人风险词，则 `asset_gate_status: FAIL_ANIMATION_CONVERTER_QC`。

若场景资产被生成成六视图、六分区、宫格、拼贴图，或缺少 `scene_view_orientation`、`camera_background_lock`，则 `asset_gate_status: FAIL_SCENE_DIRECTION_LOCK`。

若道具资产被生成成九宫格、自动网格、多道具合并图，或未按出现次数判断是否生成，则 `asset_gate_status: FAIL_PROP_SINGLE_ASSET_RULE`。

## 输出模板

输出内容必须包含四部分：

1. 角色资产表、场景方向资产表、道具资产表：每行写清楚是否需要生成参考图，以及它服务哪些集数 / 镜头。
2. 角色资产完整提示词块：每个需要生成的角色 / 造型变体各输出一段完整提示词，必须能脱离上下文单独复制派单。不得只让第一个角色完整，后续角色简写。
3. 场景资产完整提示词块：每个需要生成的场景方向资产各输出一段完整提示词，必须能脱离上下文单独复制派单。
4. 道具资产完整提示词块：每个需要生成的道具各输出一段完整提示词，必须能脱离上下文单独复制派单。

输出末尾必须附“逐资产矩阵验收”。验收矩阵逐行列出每个资产编号，并检查：模型、比例、清晰度、画质、视觉模式、全局风格锁、影调配置锁、核心描述、布局 / 方向 / 单物规则、继承字段、负面提示、连续性禁令、下游用途。任一项不通过，必须先重写资产提示词，不得进入真实生图。

文件命名规则：角色、场景、道具、舞台定位图等生成资产在创建时就必须采用中文精简命名，尽量用可读短名，不使用长串英文、无语义代号或临时拼接名；角色建议“角色名-状态名”，场景建议“场景名-方向”，道具建议“道具名-材质或状态”。

## 视频提示词 v3 道具生成与 @引用联动补丁

资产阶段不得只按道具出现次数粗略判断。只要道具满足以下任一条件，必须生成单道具资产图并进入资产池：

1. 出现次数 ≥ 2。
2. 出现 1 次但有文字、符号、数字、备注、消息、书名、项目名、印章、logo式图样、准确标记。
3. 出现 1 次但将在镜号中被 @引用、被触碰、被读屏、作为证据点、作为情感信物、作为剧情反转信息。
4. 出现 1 次但需要特写或读屏时间。
5. 出现 1 次但有动效精度风险。

如果视频提示词镜号中出现 @道具，则该道具必须已在资产池中登记为 ACTIVE 或 PENDING_FOR_SANDBOX；若没有道具资产，资产阶段必须补生成提示词。

如果某道具没有在任何镜号中出现、没有被角色触碰、没有读屏、不是证据点，且不含文字 / 符号风险，可以跳过并登记 skipped_single_use_no_text。

带文字道具提示词必须锁定 text_or_marking_lock，并在视频任务中预留 1.5-2.5 秒读屏或证据识别时间。


## 资产 v5：变体完整性、时代职务锁与共享道具锚点（最高优先级补丁）

### 角色变体资产完整展开
每个 character_variant_asset / look_variant_id 必须输出一段可独立派单的完整提示词。不得只写“完整继承 C01-LV01”“同一姚怀祥身份”“鬓白与眉心忧思纹完全继承”等短语来替代身份字段。

每个角色变体提示词必须完整包含：production_visual_mode、资产编号、角色名、角色别名、同一身份主键、source_identity_asset_ref（首个基础变体可为 none）、适用场次、适用视频任务、时代朝代锁、职位职务锁、服饰制度锁、生成图片类型、画面布局、角色描述、三庭五眼面部结构、体型气质、服装锚点、状态变化、连续性禁令、负面提示。

后续变体必须写：以 @<原始角色资产图> 作为面部身份、骨相、体型、气质基础，仅修改 <本变体允许变化字段>。但即便引用原图，也必须完整重写三庭五眼与身份锚点，不能只写继承。

### 强制时代职务锁
资产拆解时必须从剧本提取并登记：

```text
era_dynasty_lock: <朝代 / 年代 / 历史时期>
period_region_lock: <地域制度 / 城市 / 县府 / 战时或平时制度>
official_rank_role_lock: <职位 / 职务 / 官阶 / 社会身份>
costume_regulation_lock: <服饰制度 / 官服等级 / 常服 / 战后状态 / 禁止错代服饰>
prop_period_lock: <器物年代 / 材质 / 制式 / 禁止现代错置>
scene_architecture_period_lock: <建筑年代 / 空间制度 / 陈设制度>
```

角色、场景、道具提示词必须完整消费这些字段。历史剧、古装、年代戏中，缺任一字段不得进入资产派单。

### 三类状态变体链
角色、场景、道具的状态变化必须结构化：

```text
state_variant_chain:
  variant_id:
  base_identity_or_asset_ref:
  before_state:
  after_state:
  change_trigger:
  continuity_keep:
  continuity_change:
  applicable_scene_ids:
  applicable_video_task_ids:
  asset_required_reason:
  prompt_must_expand_full_fields: true
```

角色变化包括服装、官帽/发饰、灰尘、湿痕、炮灰、破损、伤损、光线状态、疲惫程度。场景变化包括日夜、天气、烟尘、战后破损、新增固定道具。道具变化包括持握、佩戴、取下、放置、收纳、沾灰、破损、读屏、证据特写。

### 道具状态绑定与共享道具锚点
建立 prop_state_variant_plan，但不得无脑每个状态都出图。默认状态绑定优先：

```text
prop_state_variant_plan:
  prop_id:
  shared_prop_visual_anchor:
  state_id:
  state_name:
  bound_character_id:
  body_attachment_position:
  scene_placement_position:
  handling_state: 持握 | 佩戴 | 收纳 | 放置 | 取下 | 展开 | 读屏 | 证据特写
  before_state:
  after_state:
  continuity_keep:
  continuity_change:
  independent_asset_required: true | false
  independent_asset_reason:
```

只有外观本体明显变化、文字/证据/特写风险、破损/沾灰/湿痕明显、剧情反转状态或读屏状态，才生成独立道具状态资产。

同一道具出现在角色资产和单独道具资产中时，shared_prop_visual_anchor 必须逐字一致。角色资产提示词中关于该道具的描述，不得与单独道具提示词冲突。


### 场景状态变体完整提示词模板（v5 防压缩专用，双模式共用）

每个 `scene_state_variant_id` 只要被判定需要出图，就必须输出一段完整场景状态变体提示词。不得只写“同一场景夜雨版 / 继承原场景 / 增加破损 / 按前景别”。场景状态变体必须完整说明哪些结构保持、哪些状态变化、变化由哪段剧情触发，并继续服从 `scene_view_orientation` 与 `camera_background_lock`。

```text
模型：image2
比例：16:9
清晰度：2K
画质：高
production_visual_mode: <cinematic_realistic | top_chinese_3d_animation_cg，继承项目模式>
global_style_preset_id: <继承生产数据中心>
global_style_lock: <完整风格配置正文，不得只写预设 ID>
tone_profile_preset_id: <继承生产数据中心>
tone_profile_lock: <完整影调配置正文，不得只写预设 ID>
style_tone_inheritance_status: PASS

scene_id: <场景稳定编号>
scene_name: <场景名>
scene_state_variant_id: <场景状态变体编号>
scene_state_variant_name: <日间晴天 / 夜雨 / 战后破损 / 新增固定道具等>
base_scene_asset_ref: <基础场景方向资产路径或 @基础场景资产名；基础状态写 none>
source_scene_ids: [<剧本场次>]
used_by_video_tasks: [<后续 video_task_id>]
scene_view_asset_id: <方向资产编号>
scene_view_orientation: <front / reverse / left / right / top / keylight>
camera_background_lock: <使用该图时所有镜头必须遵循的背景机位方向>

era_dynasty_lock: <朝代 / 年代 / 历史时期>
period_region_lock: <地域制度 / 城市 / 县府 / 宫廷 / 战时或平时制度>
scene_architecture_period_lock: <建筑年代 / 空间制度 / 陈设制度 / 禁止错代建筑>
prop_period_lock: <固定道具与陈设器物年代 / 材质 / 制式>

before_state: <变化前场景状态>
after_state: <本场景状态变体>
change_trigger: <剧情推进触发原因>
continuity_keep: <必须保持的空间结构、入口出口、墙体、窗、门、固定家具、时代制式、主体材质、场景方向>
continuity_change: <允许改变的天气、日夜、季节、烟尘、破损、积水、血迹、灰尘、新增固定道具、移除固定道具、光源状态>

生成图片：<按 production_visual_mode 写“写实真人电影场景状态资产参考图”或“国漫顶级 3D 动画 CG 电影场景状态资产参考图”>。单张 16:9 场景状态方向资产图，不是六视图，不是宫格图，不是拼贴图。

画面要求：只呈现 scene_view_orientation 对应方向的完整空间；完整体现 after_state；保留 continuity_keep 中的空间骨架和时代制式；准确表现 continuity_change 中的剧情状态变化。不得出现人物、群演、画面文字、标签、水印、字幕、UI、颜色框、数字、stable_id。

下游方向锁定：后续视频提示词使用本图时，所有镜头都必须遵循 scene_view_orientation 作为背景机位；不得把旧场景状态图临场硬写成新天气、新日夜、新破损或新增固定道具。
```

### 道具状态变体完整提示词模板（v5 防压缩专用，双模式共用）

每个 `prop_state_variant_plan` 必须先判断是否需要独立道具状态资产。默认状态绑定优先；如果不出独立图，也必须在数据中心完整登记状态绑定、身体位置、放置位置和一致性保持。若独立出图，则必须按本模板完整输出，不得只写“同一道具放桌上版 / 继承手持版 / 沾血版”。

```text
模型：image2
比例：16:9
清晰度：2K
画质：高
production_visual_mode: <cinematic_realistic | top_chinese_3d_animation_cg，继承项目模式>
global_style_preset_id: <继承生产数据中心>
global_style_lock: <完整风格配置正文，不得只写预设 ID>
tone_profile_preset_id: <继承生产数据中心>
tone_profile_lock: <完整影调配置正文，不得只写预设 ID>
style_tone_inheritance_status: PASS

prop_id: <道具稳定编号>
prop_name: <道具名>
prop_state_id: <道具状态编号>
prop_state_name: <佩戴 / 手持 / 放置 / 取下 / 展开 / 读屏 / 破损 / 沾血 / 雨湿等>
shared_prop_visual_anchor: <同一道具核心外观锚点，必须与角色资产、单独道具资产、视频提示词逐字一致>
base_prop_asset_ref: <基础道具资产路径或 @基础道具资产名；基础状态写 none>
owner_character_id: <持有人或关联角色>
bound_character_id: <绑定角色，如无写 none>
body_attachment_position: <戴在身上 / 握在右手 / 腰间 / 胸前 / 袖中 / none>
scene_placement_position: <桌上 / 地上 / 门边 / 椅旁 / 证据袋中 / none>
handling_state: 持握 | 佩戴 | 收纳 | 放置 | 取下 | 展开 | 读屏 | 证据特写
source_scene_ids: [<剧本场次>]
used_by_video_tasks: [<后续 video_task_id>]

prop_period_lock: <器物年代 / 材质 / 制式 / 禁止现代错置>
text_or_marking_lock: <道具上的关键文字、印章、暗纹、划痕、磨损、血迹等，如无写 none>
material_anchor: <纸张 / 金属 / 玉 / 木 / 布 / 药包 / 印泥等材质>
size_and_handling: <手持尺寸、佩戴方式、开合方式、放置方式>

before_state: <变化前道具状态>
after_state: <本状态变体>
change_trigger: <剧情推进触发原因>
continuity_keep: <必须保持的形状、比例、材质、文字、符号、纹样、破损基准、shared_prop_visual_anchor>
continuity_change: <允许改变的位置、持握方式、展开/收起、沾灰、湿痕、血迹、破损、读屏角度等>
independent_asset_required: true | false
independent_asset_reason: <外观本体明显变化 / 文字证据特写 / 破损沾灰湿痕明显 / 剧情反转 / 读屏状态 / not_required_state_binding_only>

生成图片：<按 production_visual_mode 写“写实真人电影道具状态资产参考图”或“国漫顶级 3D 动画 CG 电影道具状态资产参考图”>。单个道具居中展示，16:9 横图，干净背景。

画面要求：完整呈现 after_state，同时保持 shared_prop_visual_anchor 与 continuity_keep。无人物、无手部、无场景干扰、无多道具拼接、无宫格、无颜色框、无数字编号、无道具名标签、无 prop_id、无字幕、无 UI、无水印。若道具有文字 / 印章 / 符号，必须清晰呈现并保持与 text_or_marking_lock 一致。
```

### 资产变体完整性 QC
若任一后续变体字段数量、段落结构、三庭五眼展开、时代职务锁、服装锚点、状态链、负面提示、连续性禁令低于基础变体，标记 FAIL_ASSET_VARIANT_PROMPT_COMPRESSION。

## 空间建模 v6：场景参考图分层预判与资产生成规则（最高优先级补丁）

本节为资产阶段新增规则，必须在视频提示词阶段之前完成。空间参考资产分为：主场景基准图、机位补充场景图、角色参考图、道具参考图。注意力分散的根源不是图多，而是职责混乱；因此每张参考图必须在资产阶段写明 `reference_role`、`use_for`、`do_not_use_for`。

### 单场景参考图上限

每个场景最多 4 张场景参考图：

1. 主场景基准图 1 张：作为全场景视觉宪法，统一空间结构、材质质感、光影色调、空间尺度和气氛。
2. 机位补充图最多 3 张：只在大角度机位跳变、正反打、侧面切换、俯视、区域切换、越轴风险或强剧情需要时生成。机位补充图只提供对应机位的视角透视与物体相对布局，不携带光影、材质、色调风格定义；这些仍继承主场景基准图。

若超过 3 张机位补充图仍无法覆盖镜头计划，必须回到分镜阶段拆分场景或重排镜头，不得继续堆参考图。

### 不需要补图的情况

只要机位轴线不变、只在同一视角内变化，不需要新增机位补充图：

- 景别切换：特写 → 中近景 → 中景等推拉变化。
- 小幅运镜：缓慢横移、轻微仰俯、变焦、轻推拉。
- 主体位置微调：人物在原机位的画面区块内移动。
- 前景 / 中景 / 背景层内的遮挡与景深变化。

### 必须补图的情况

以下情况必须在资产阶段预先生成机位补充场景图：

- 视角跳变：正面切侧面、正面切反打、平视切俯视。
- 区域切换：从主基准图的核心区域切到旁听席、被告席后方、审判席背后、走廊、门口等主基准图无法稳定延展的区域。
- 越轴风险：越过 180 度轴线、反向机位、视线匹配可能混乱的机位。
- 大角度机位变化：主基准图透视无法支撑的横向 / 纵深 / 俯视变化。

### 场景参考图分层登记字段

```text
scene_reference_layer_asset:
  scene_id:
  scene_name:
  main_scene_base_asset_id:
  main_scene_base_path: pending | <path>
  main_scene_base_use_for: 全场景空间结构 / 材质质感 / 光影色调 / 空间尺度 / 统一气氛
  camera_supplement_assets:
    - asset_id:
      camera_view_type: side | reverse | over_shoulder_reverse | top | region_switch | keylight | other
      asset_path: pending | <path>
      trigger_reason: view_axis_jump | reverse_angle | over_180_axis_risk | region_switch | top_down_required | strong_story_need
      use_for: 仅对应机位的视角透视与物体相对布局
      do_not_use_for: 光影色调 / 材质质感 / 全局美术风格
      linked_video_task_ids: []
      linked_shot_ids: []
  camera_supplement_count: 0 | 1 | 2 | 3
  over_limit_resolution: not_required | split_scene | reduce_camera_plan | ask_user
  status: PASS | FAIL_CAMERA_SUPPLEMENT_ASSET_MISSING | FAIL_REFERENCE_OVER_LIMIT
```

道具参考图仍按现有道具规则生成，但如果道具在视频提示词中承担空间锚点、读屏、证据特写、角色手持到放置状态切换，则必须生成或登记对应道具资产与状态绑定，不能只在视频提示词中口头描述。

### 空间 v6 资产任务包完整模板

以下模板为结构模板，不是剧情示例；所有字段必须由剧本、分镜计划或生产数据中心真实填写，不得写“同上 / 继承前文 / 暂略”。

```text
scene_reference_layer_asset:
  scene_id: <scene_id>
  scene_name: <scene_name>
  active_spatial_language: three_column_three_depth_partition
  backup_100x100_policy: reserved_not_loaded
  main_scene_base_ref:
    asset_id: <asset_id>
    asset_name: <中文资产名>
    asset_path: pending | <path>
    reference_role: main_scene_base
    use_for: 全场景空间结构 / 材质质感 / 光影色调 / 空间尺度 / 统一气氛
    do_not_use_for: 单个角色身份 / 单个道具细节 / 替代机位补充图
    linked_scene_ids: [<scene_id>]
    linked_video_task_ids: [<video_task_id>]
  camera_supplement_trigger_audit:
    - shot_id: <shot_id>
      trigger_type: none | view_axis_jump | reverse_angle | side_angle | top_down_required | region_switch | over_180_axis_risk | strong_story_need
      trigger_reason: <为什么主场景基准图不足或为什么不需要补图>
      required_camera_supplement_ref: none | <camera_supplement_asset_id>
      decision_status: PASS | FAIL_CAMERA_SUPPLEMENT_ASSET_MISSING | FAIL_REFERENCE_OVER_LIMIT
  camera_supplement_refs:
    - asset_id: <asset_id>
      asset_name: <中文资产名>
      asset_path: pending | <path>
      reference_role: camera_supplement
      camera_view_type: side | reverse | over_shoulder_reverse | top | region_switch | keylight | other
      use_for: 仅对应机位的视角透视与物体相对布局
      do_not_use_for: 光影色调 / 材质质感 / 全局美术风格 / 角色身份 / 道具细节
      linked_shot_ids: [<shot_id>]
      linked_video_task_ids: [<video_task_id>]
  prop_spatial_anchor_assets:
    - prop_id: <prop_id>
      prop_name: <道具名>
      asset_path: pending | <path>
      prop_spatial_function: none | subject_axis_anchor | table_axis_anchor | read_screen | evidence_closeup | hand_to_placement_transition | body_attachment
      binding_target: none | @<角色名> | @<桌案/审判席/门口/墙面等场景结构>
      spatial_partition_default: 横向：<大列+列内方位>；景深：<大层+层内区段>
      state_binding_required: true | false
      linked_shot_ids: [<shot_id>]
  reference_stack_status: PASS | FAIL_MAIN_SCENE_BASE_MISSING | FAIL_CAMERA_SUPPLEMENT_ASSET_MISSING | FAIL_REFERENCE_OVER_LIMIT | FAIL_REFERENCE_ROLE_BOUNDARY_MISSING
```

