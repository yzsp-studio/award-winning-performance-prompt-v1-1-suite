# 院线电影级摄影方案矩阵

## 目标

为神笔制作的视频提示词阶段提供内部摄影方案矩阵。所有影视作品任务，无论是短剧、中剧、长剧、短片、微短片、微电影、网大或电影，都按题材类型、情绪调性、场景空间匹配院线电影级摄影方案。

本文件是神笔制作内部 reference，不是外部 Skill。视频提示词阶段必须读取本文件，并把选定的摄影方案写入 `VIDEO_DISPATCH_PACKAGE.cinematography_profile`、`prompt_english_dispatch` 开头的 `Cinematography profile:`，以及每个逐秒 / 短分段的局部镜头与光影细节。

## 使用硬规则

1. 自动模式下，按“题材类型 + 情绪调性 + 场景空间”匹配最合适方案，并记录 `selection_policy: chosen_by_agent`。
2. 手动模式下，先给出推荐方案，再用弹窗让用户选择或改选。
3. 开头 `Cinematography profile:` 负责统一整段视频的院线影像风格。
4. 每个逐秒 / 短分段仍必须写本段镜头参数、景别、机位、光源方向、景深、环境互动和人物面部受光状态。
5. 不得只在开头写摄影方案而省略分段细节；也不得只写分段细节而省略开头统一 `Cinematography profile:`。
6. 方案名只作为内部匹配标签；最终英文 prompt 中写可派发摄影参数，不写研究过程。

## 自动匹配优先级

1. 题材类型：古装、复仇、警匪、犯罪、悬疑、青春、家庭、科幻、动作、历史、作者电影等。
2. 情绪调性：压迫、暗黑、明亮、温柔、克制、史诗、惊悚、浪漫、现实主义等。
3. 场景空间：灵堂、宫殿、街巷、都市夜景、家庭室内、校园、荒野、战场、审讯室、舞台化空间等。
4. 若多套方案同时匹配，优先选择更贴合“情绪调性 + 场景空间”的方案，而不是只看题材关键词。

## 10 套摄影方案

### 01 好莱坞史诗商业大片方案

适用题材：科幻、动作、战争、冒险、灾难、超级英雄、宏大世界观。

自动匹配关键词：科幻、战争、动作、灾难、冒险、未来、末日、太空、怪兽、史诗、大场面。

可派发摄影参数：

```text
Cinematography profile: hyper-real cinematic blockbuster quality, ARRI ALEXA 65, Panavision / ARRI Master Anamorphic lenses, Rec 709 color space, high dynamic range theatrical contrast, EI 800, 180-degree shutter, 24fps.
```

美学说明：大画幅、宽银幕、强纵深、清晰动作调度、高完成度商业视觉、强光比但主体清晰。适合需要“大片感”、宏大空间和清楚动作线的任务。

### 02 好莱坞奥斯卡剧情片方案

适用题材：人物剧情、传记、现实主义、家庭、社会议题、法庭、成长。

自动匹配关键词：传记、家庭、社会议题、现实主义、人物弧光、奥斯卡、克制表演、法庭、伦理。

可派发摄影参数：

```text
Cinematography profile: prestige drama cinema quality, ARRI Alexa Mini LF, Zeiss Supreme Prime / Cooke S4 lenses, Rec.709 color space, EI 800, 180-degree shutter, 24fps, restrained naturalistic contrast.
```

美学说明：重视演员表情、肤色真实、室内自然光、低饱和、浅景深克制，不追求炫技。适合文戏、人物心理、现实主义剧情。

### 03 好莱坞新黑色惊悚方案

适用题材：犯罪、悬疑、惊悚、侦探、都市夜戏、心理压迫。

自动匹配关键词：犯罪、悬疑、黑色电影、夜景、追查、阴谋、审讯、霓虹、都市压迫。

可派发摄影参数：

```text
Cinematography profile: neo-noir thriller cinema quality, ARRI Alexa Mini LF, Panavision anamorphic lenses, Rec.709 color space, EI 1280, 180-degree shutter, 24fps, deep shadow contrast with controlled neon highlights.
```

美学说明：高反差、局部实用光源、冷暖对比、霓虹、深阴影、前景遮挡、浅景深压迫。适合犯罪、悬疑、都市惊悚和审讯空间。

### 04 中国大陆历史史诗 / 古装仪式方案

适用题材：古装、权谋、战争、历史、朝堂、仪式、家国、史诗。

自动匹配关键词：古装、朝堂、战争、仪式、权谋、家国、历史、宫殿、大场面、礼制。

可派发摄影参数：

```text
Cinematography profile: Chinese theatrical historical epic quality, ARRI ALEXA 65, ARRI Master Anamorphic lenses, Rec 709 color space, ARRI 709 look, EI 800, 180-degree shutter, 24fps, controlled ceremonial contrast.
```

美学说明：对称构图、仪式感、色彩秩序、纵深空间、大场面调度、服化道质感。适合古装正剧、权谋、战争、史诗和高规格礼制场面。

### 05 中国大陆 / 港台东方暗黑复仇方案

适用题材：复仇、灵堂、宅斗、权谋、武侠、黑帮、雨夜、压迫空间。

自动匹配关键词：复仇、灵堂、宅斗、暗黑、雨夜、武侠、黑帮、压迫、背叛、审判、烛火、白幡。

可派发摄影参数：

```text
Cinematography profile: East Asian dark revenge cinema quality, ARRI ALEXA 65, anamorphic prime lenses, Rec 709 color space, low-key theatrical contrast, EI 800, 180-degree shutter, 24fps, candlelight and shadow-driven image design.
```

美学说明：低调光、烛火、雨夜、深阴影、前景遮挡、近景压迫、冷暖冲突。适合古装复仇、灵堂压迫、宅斗翻盘、暗黑武侠、黑帮审判类场景。

### 06 香港都市警匪 / 黑帮夜景方案

适用题材：警匪、卧底、追车、枪战、黑帮、都市压迫、夜景。

自动匹配关键词：警匪、卧底、黑帮、审讯、天台、街巷、霓虹、追车、港片、雨夜都市。

可派发摄影参数：

```text
Cinematography profile: Hong Kong urban crime cinema quality, ARRI Alexa Mini LF, anamorphic lenses, Rec.709 color space, EI 1000, 180-degree shutter, 24fps, wet neon night contrast and fast handheld urban tension.
```

美学说明：霓虹、湿地反光、夜色、手持、快速调度、狭窄空间、都市压迫。适合警匪黑帮、现代动作、街巷追逐、天台对峙。

### 07 台湾青春 / 家庭生活流方案

适用题材：青春、家庭、校园、成长、城市孤独、亲情、生活流。

自动匹配关键词：青春、家庭、校园、成长、夏天、生活流、亲情、城市、温柔、遗憾、暗恋。

可派发摄影参数：

```text
Cinematography profile: Taiwanese naturalistic coming-of-age cinema quality, ARRI Alexa Mini LF, Cooke S4 lenses, Rec.709 color space, EI 400, 180-degree shutter, 24fps, soft natural daylight and gentle skin-tone rendering.
```

美学说明：自然光、柔和肤色、生活细节、低侵入镜头、青春遗憾感、空气感。适合情感短剧、青春、家庭、校园、亲情和轻现实题材。

### 08 日本物哀家庭 / 日常生活方案

适用题材：家庭、日常、离别、青春、治愈、物哀、低冲突心理戏。

自动匹配关键词：家庭、日常、物哀、离别、安静、饭桌、街道、青春、温柔、克制、生活细节。

可派发摄影参数：

```text
Cinematography profile: Japanese quiet realist cinema quality, ARRI Alexa Mini LF, Zeiss Supreme Prime lenses, Rec.709 color space, EI 800, 180-degree shutter, 24fps, restrained natural light and low-saturation soft contrast.
```

美学说明：极简、安静、自然光、留白、固定镜头、低饱和、细微表情。适合家庭、青春、生活流、内心戏和低冲突心理变化。

### 09 韩国类型片 / 阶层寓言 / 复仇惊悚方案

适用题材：犯罪、复仇、惊悚、阶层、悬疑、心理压迫、黑色喜剧。

自动匹配关键词：韩国、复仇、犯罪、阶层、地下室、豪宅、雨夜、悬疑、反转、压迫、类型片。

可派发摄影参数：

```text
Cinematography profile: Korean high-control genre cinema quality, ARRI Alexa Mini LF, Cooke S4 / anamorphic lenses, Rec.709 color space, EI 800, 180-degree shutter, 24fps, precise spatial contrast and controlled cold-warm separation.
```

美学说明：空间阶层、精准构图、冷暖分区、类型节奏、强情绪推进。适合复仇、犯罪、悬疑、阶层寓言、黑色喜剧和高控制类型片。

### 10 欧洲作者电影 / 历史文学方案

适用题材：作者电影、社会议题、历史文学、心理、家庭、欧洲现实主义。

自动匹配关键词：作者电影、社会议题、历史、文学、贵族、阶级、欧洲、心理、现实主义、长镜头、自然主义。

可派发摄影参数：

```text
Cinematography profile: European arthouse theatrical cinema quality, ARRI Alexa Mini LF, Leica Summilux-C / Zeiss Supreme Prime lenses, Rec.709 color space, EI 800, 180-degree shutter, 24fps, naturalistic contrast with painterly composition.
```

美学说明：自然主义、长镜头倾向、构图克制、人物心理、历史空间、文学质感。适合法国作者电影、英国历史文学、意大利现实 / 史诗和欧洲社会议题。

## 匹配输出格式

选定方案后，在 `VIDEO_DISPATCH_PACKAGE` 中写：

```text
cinematography_profile_id: <01-10>
cinematography_profile_name: <方案名>
cinematography_profile_selection_reason: <题材 + 情绪 + 场景空间匹配理由>
cinematography_profile: <可派发摄影参数>
```

在 `prompt_english_dispatch` 开头写：

```text
Cinematography profile: <可派发摄影参数正文>
```

在每个逐秒 / 短分段里继续写本段局部摄影细节。


## 用户可见摄影视觉描述层（强制补丁）

本文件允许保留摄影机、镜头、帧率、快门、感光度等专业审计参数，作为内部 cinematography_profile_audit_params。但写入用户可见提示词、prompt_chinese_dispatch、沙盒提示词与真实派发 prompt 时，必须优先使用 cinematography_profile_visual_dispatch。

转换原则：24fps、180-degree shutter、180 度快门转换为“自然电影感运动模糊”；EI 800 / EI 1280 等曝光感光参数转换为“暗部层次稳定、主体面部清晰、弱光不过曝不死黑”；spatial contrast / controlled contrast 转换为“前中远景递进关系分明、空间层次清楚”；close interior pressure / spatial pressure 转换为“窄空间近景构图，营造轻微压迫感”；prestige drama cinema quality 转换为“大师级人物剧情片摄影质感”。

写实真人模式可保留摄影机与镜头型号，但必须中文化并连接画面效果：例如“ARRI Alexa Mini LF 摄影机质感，库克镜头暖调柔和高光光晕，50mm 定焦 f/2.8，3200K 暖色温，电影级景深，柔和焦外虚化，自然镜头呼吸感，弱光戏剧化对比”。3D 动画 CG 模式使用虚拟摄影语言，不应把帧率、快门、感光度作为风格锚点，应写“虚拟大画幅摄影机、温润定焦镜头、自然电影感运动模糊、电影级景深、克制自然的室内明暗层次”。

每个视频任务必须同时写入 cinematography_profile_id、cinematography_profile_name、cinematography_profile_selection_reason、cinematography_profile_audit_params、cinematography_profile_visual_dispatch。最终 prompt 的 [电影质感] 只能消费 cinematography_profile_visual_dispatch，不得直接粘贴英文审计参数。

10 套方案视觉描述层：
01 好莱坞史诗商业大片方案：宏大商业大片电影质感，虚拟大画幅摄影机，宽银幕纵深构图，强动态范围与清晰动作调度，自然电影感运动模糊，主体始终清楚，远近层次开阔。
02 好莱坞奥斯卡剧情片方案：大师级人物剧情片摄影质感，虚拟大画幅摄影机，温润定焦镜头，低饱和自然对比，自然电影感运动模糊，克制自然的室内明暗层次，窄空间近景构图，营造轻微压迫感，重视面部微表情、手部动作和人物情绪细节。
03 好莱坞新黑色惊悚方案：新黑色惊悚电影质感，冷暖分离明显，深阴影与局部高光形成压迫，前景遮挡增强窥视感，自然电影感运动模糊，窄空间近景构图营造不安与心理压迫。
04 中国大陆历史史诗 / 古装仪式方案：中国历史史诗与仪式感电影质感，对称构图，纵深空间庄重，服化道层次清晰，自然电影感运动模糊，光影秩序稳定，画面具有礼制、权力和命运压迫。
05 中国大陆 / 港台东方暗黑复仇方案：东亚暗黑复仇电影质感，低调光影、烛火或雨夜反光、深阴影与高光边缘共同塑造压迫，窄空间近景构图营造审判感，自然电影感运动模糊。
06 香港都市警匪 / 黑帮夜景方案：香港都市犯罪电影质感，湿润霓虹夜色、快速手持张力、狭窄街巷纵深、自然电影感运动模糊，冷暖光交错。
07 台湾青春 / 家庭生活流方案：台湾自然主义青春与家庭生活流电影质感，柔和自然天光，低侵入镜头，轻微空气感，低饱和温柔对比，自然电影感运动模糊。
08 日本物哀家庭 / 日常生活方案：日本安静现实主义电影质感，固定镜头与留白构图，自然柔光，低饱和软对比，自然电影感运动模糊，细微表情与日常动作被温柔放大。
09 韩国类型片 / 阶层寓言 / 复仇惊悚方案：韩国高控制类型片电影质感，精准空间构图，冷暖分区清楚，前中远景递进关系分明，自然电影感运动模糊，情绪推进强。
10 欧洲作者电影 / 历史文学方案：欧洲作者电影与历史文学电影质感，自然主义对比，绘画感构图，克制长镜倾向，自然电影感运动模糊，人物与环境关系被清楚保留。


## 15秒上限与摄影节奏系数补丁

摄影方案只辅助时长计算，不得覆盖 model_duration_cap_seconds。当前默认 model_duration_cap_seconds: 15。

节奏系数建议：
- 01 史诗商业大片：1.20-1.50，若动作密集可拆多段。
- 02 人物剧情片：1.15-1.35，必须保留表演留白。
- 03 新黑色惊悚：1.05-1.25，保留压迫停顿与证据识别。
- 04 历史史诗仪式：1.20-1.50，仪式动作不可压缩。
- 05 东方暗黑复仇：1.10-1.30，审判停顿和眼神反应不可压缩。
- 06 都市警匪夜景：0.90-1.10，动作可快但台词不可超速。
- 07 青春家庭生活流：1.15-1.35，生活动作和情绪留白必须保留。
- 08 物哀日常：1.25-1.50，留白优先。
- 09 韩国类型片：1.05-1.25，空间压迫与反转停顿保留。
- 10 欧洲作者电影：1.30-1.60，长镜与沉默优先，通常需要拆分。

若节奏系数计算后超过 15 秒，必须拆分任务，不得降低系数来硬塞。
