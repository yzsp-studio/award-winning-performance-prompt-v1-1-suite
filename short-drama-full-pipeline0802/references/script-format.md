# 短剧剧本格式

## 场次格式

每场按以下字段输出：

* 场次编号：如 E01-S03。
* 时代：朝代、王朝、近现代、纪元、地质年代、当代、年代。
* 场景：地点。
* 时间：日/夜/清晨/傍晚。
* 人物：出场角色。
* 剧情功能：冲突、揭露、反转、过渡、情绪兑现。
* 动作：可被拍摄的行为。
* 对白：角色实际说出口的话。
* 情绪：表演方向。
* 镜头备注：只写必要镜头，不抢分镜阶段工作。

## 标准剧本文体

示例：

场次：E01-S01  豪门宴会厅  夜
人物：林晚、顾沉、宾客
剧情功能：主角被羞辱，隐藏身份埋钩子。
动作：林晚端着酒杯站在人群边缘，宾客故意撞开她，红酒泼在礼服上。
对白：
宾客：你这种人，也配来顾家的宴会？
林晚：我只是来拿回属于我的东西。
情绪：林晚克制，顾沉冷眼观察。
镜头备注：先用近景压迫，再切顾沉反应。

## 对白原则

1. 每句对白必须推动关系、信息或情绪。
2. 避免解释世界观，优先让冲突暴露信息。
3. 短剧对白要短、狠、易懂。
4. 角色说话方式要区分：主角克制，对手尖锐，盟友直接，长辈压迫。
5. 重要信息不要一次说完，分散到多个钩子。

## 动作原则

动作必须可视化：

* 不写“她很伤心”，写“她握紧杯脚，指节发白”。
* 不写“他很愤怒”，写“他把合同摔到桌面，纸页滑到她脚边”。
* 不写“众人震惊”，写“宴会厅短暂安静，几只酒杯停在半空”。

## 单集结构模板

* 开场 0-5 秒：钩子动作或爆点台词。
* 5-25 秒：交代当集冲突。
* 25-45 秒：冲突升级，主角受压或反击。
* 45-60 秒：反转或悬念。

## 改写已有剧本

当用户给已有剧本时：

1. 保留用户核心设定和剧情事实。
2. 修正不可拍、过长、解释性台词；对于用户原剧本中的台词，除非存在错别字、明显病句、标点缺失或其他会导致台词明显错误的情况，否则不得删除、缩减、概括或简化。
3. 增加场次编号和镜头可执行动作。
4. 检查每集是否有开场钩子和结尾钩子。
5. 输出“改写版剧本”与“修改理由摘要”。

## 生产数据中心继承硬规则

剧本阶段必须消费故事阶段写回的数据中心，不得只根据聊天摘要重写。每次由本 Skill 优化、改写或新写的剧本，都必须同步写入或更新生产数据中心；禁止只输出剧本文本但不写回数据中心。

进入剧本阶段前必须读取并继承：

```text
project_name
project_type
original_request
script_source
user_constraints
main_conflict
main_characters
visual_promise
episode_ranges
```

剧本写回生产数据中心时，至少必须更新：

```text
script_version_id: <优化版 / 标准生产版 / 新写版稳定编号>
script_source_ref: <原剧本 / 上一版剧本 / 用户新输入>
scene_table_ref: <本次写入的场次表>
dialogue_table_ref: <本次写入的对白表>
character_face_structure_3t5e_ref: <所有被下游引用角色的三庭五眼结构表，含主角 / 配角 / 管家 / 婆子 / 老仆 / 侍卫 / 群像框选人物>
asset_extraction_input_ref: <资产抽取输入表>
video_task_mapping_ref: <视频任务映射表>
stage_status.script: PASS | FAIL | pending
```

缺少以上任一写回对象时，剧本阶段不得进入资产阶段。

每个场次必须写入稳定编号，并能被资产、分镜、视频任务追踪：

```text
episode_id: E01
scene_id: E01-S01
story_source_id: <来自故事阶段>
scene_function: <冲突 / 揭露 / 反转 / 过渡 / 情绪兑现>
required_characters: [角色名]
required_scene: <场景名>
required_props: [道具名]
dialogue_ids: [D001, D002]
asset_need_hint: <角色 / 场景 / 道具 / 状态变化>
video_task_hint: <建议拆分的视频任务范围>
```

## 对白保真锁

所有实际说出口的对白必须进入生产数据中心的对白表。每句对白必须有稳定 `dialogue_id`：

```text
dialogue_id: D001
speaker: <角色名>
text: <原始台词，逐字保留>
source_scene: <scene_id>
assigned_video_task_id: pending
preservation: verbatim_required | optional | user_authorized_change
```

硬规则：

- 用户原剧本中的关键对白默认 `verbatim_required`。
- `verbatim_required` 的对白不得删减、概括、换人、沉默化、旁白化或改写。
- 视频任务切分只能拆分承载对白，不能以时长为由压缩对白。
- 风险替代只允许替代高风险视觉动作，不允许替代对白文本。
- 若需要修改用户原台词，必须把原台词与修改版同时保留，并把 `preservation` 改为 `user_authorized_change`，不得覆盖原文。

## 角色三庭五眼数据链硬规则

剧本阶段或剧本优化阶段必须为所有被下游引用的角色建立可继承的面部身份字段 `face_structure_3t5e`。该字段服务于后续角色资产参考图、分镜身份锁定、关键帧与视频提示词，不得只停留在聊天描述中。主角、反派、配角、管家、婆子、老仆、侍卫、路人和群像人物只要拥有 `character_id`、进入角色资产、出现在分镜 / 视频提示词、或作为下游需要独立身份锁定的人物被引用，就必须按同一深度写入身份结构；禁止主角详细、配角或后续群像简略。

如果用户原剧本或人物小传已经包含明确外貌描写，必须从原文提取并结构化；如果原文没有明确三庭五眼描写，必须根据角色的年龄段、性别、身份阶层、性格、剧情功能、关系压力、状态变化和视觉承诺合理补齐，并标记为 `auto_inferred_from_character_design`，不得留空。

每个被下游引用的角色至少写入：

```text
character_id: <稳定编号或 pending>
character_name: <角色名>
character_name_aliases: [<曾用名 / 剧情后续名 / 双魂掌控名 / 伪装名>]
canonical_identity_label: <本制作链路使用的同一身份主键标签>
identity_anchor: <脸型 / 五官 / 发型 / 体型 / 气质 / 标志物>
face_structure_3t5e:
  source_basis: script_explicit | auto_inferred_from_character_design | user_provided_reference
  upper_third: <上庭：额头、发际线、额面比例与气质>
  middle_third: <中庭：眉眼、鼻梁、颧骨、面中结构与人物处境>
  lower_third: <下庭：人中、唇形、下颌、下巴比例与年龄 / 情绪>
  five_eye_ratio: <五眼：眼距、眼长、眉眼比例、眼神气质>
  bone_and_soft_tissue: <整体骨相、软组织、真实人类自然不完美>
  temperament_mapping: <这些面部结构如何服务角色性格 / 阶层 / 剧情处境>
  forbidden_face_drift: <后续图像不得改变的脸型、骨相、眉眼、气质边界>
```

`face_structure_3t5e`、`character_name_aliases`、`canonical_identity_label` 和 `identity_anchor` 必须写入生产数据中心和资产抽取输入表。缺少任一字段时，`stage_status.script` 不得标记 PASS；资产阶段不得自行跳过，只能回到剧本 / 人物设定阶段补齐。

双魂、改名、共用身体或伪装身份必须在剧本阶段先合并身份主键。例如“沈月 / 沈曦共用身体 / 沈曦月”必须登记为同一身体身份的 `canonical_identity_label`，并在 `character_name_aliases` 中同时保留剧情称呼、掌控状态和后续名字；下游只能改变表演状态、眼神控制者、台词归属和剧情称呼，不得生成多张互相冲突的脸。

## 剧本后全量前置与变体计算

剧本标准化完成后、进入资产阶段前，必须建立 `full_preproduction_snapshot`，并完成角色造型变体与场景状态变体计算。不得让资产阶段临时猜“要不要换衣服 / 要不要换发型 / 场景是否需要新天气版本”。

### 角色造型变体计算

每个被下游引用的角色都必须根据剧本时间线和场景逻辑计算 `character_look_variant_plan`：

- 场景更换是否要求不同服装。
- 天气、季节、日夜是否影响服装、妆感、发型、发饰或湿污状态。
- 角色在剧情中是否有现实时间换装；没有时间换装时，不得强行换成全新造型。
- 身份伪装、宴会、战斗、受伤、时间跳跃、年龄变化是否要求新人物资产图。
- 武器和贴身道具是否与人物长期绑定，是否应进入人物资产图。

必须登记服装、妆造、妆感、发型、发饰、年龄阶段、伤损、武器、贴身道具、适用场次、适用视频任务、换装理由和 `character_has_time_to_change`。

### 场景状态变体计算

每个场景都必须根据剧本变化计算 `scene_state_variant_plan`。用户已确认：同一场景只要季节、天气、日/夜、受损、新增固定道具、剧情状态或光源状态发生变化，就必须生成新场景状态资产图，不得用旧场景图临场硬写新状态。

必须登记季节、天气、日夜、受损状态、新增 / 移除固定道具、光源状态、适用场次、适用视频任务和需要的场景方向。

### 快照写回

角色造型变体计划、场景状态变体计划、音色参考计划、声音 owner 计划和视频任务映射必须一起写入 `full_preproduction_snapshot`。后续变化只允许通过 `preproduction_patch` 更新，并由 `current_active_snapshot_resolved` 供下游消费。

## 剧本到资产的交接硬规则

剧本完成后，必须产出资产抽取输入表、角色造型变体计划、场景状态变体计划和完整前置快照。不得让资产阶段重新猜角色、场景、道具、角色造型或场景状态。

每场至少交接：

```text
scene_id
required_characters
required_scene
required_props
state_changes
special_makeup_or_damage
character_face_structure_3t5e_refs: [character_id.face_structure_3t5e]
character_identity_alias_refs: [character_id.character_name_aliases + canonical_identity_label]
continuity_notes
```

缺少任一核心字段时，`stage_status.script` 不得标记 PASS。



## 历史时代、职位职务与视觉备注降权补丁

剧本标准化后必须提取 period_world_lock：era_dynasty_lock、period_region_lock、official_rank_role_lock、costume_regulation_lock、prop_period_lock、scene_architecture_period_lock。历史剧、古装、年代戏不得留空。

剧本中的视觉备注只作为剧情意图参考，不得覆盖 Skill 的资产、景别、场景方向和视频提示词规则。若剧本写全景、远景、大远景，分镜阶段必须按 Skill 景别优先级重新判断。
