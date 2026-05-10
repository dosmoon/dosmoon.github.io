---
title: Token Processor 调查报告
description: 围绕 Token 原语的专用智能加速器产业调查——产品形态、架构路径、玩家、风险与时间线。
---

> **版本**:v1.0 调查版
> **截稿**:2026年5月10日
> **范围**:聚焦"以Token为原语的专用智能加速器",涵盖产品形态、架构路径、产业格局、风险与时间线

---

## 摘要

过去六个月发生了三件事,把Token Processor从"实验性概念"推到了"产业主战场":

1. **2025年12月24日,NVIDIA以约200亿美元收购Groq的IP和资产**——AI硬件史上规模最大的一笔交易,7倍于Groq收购前估值。截至2026年4月,Groq 3 LPU处于早期访问预览阶段,需通过NVIDIA企业项目注册。
2. **2026年3月16日 GTC 2026上,Groq 3 LPU正式发布**,以SRAM替代HBM,实现150 TB/s内存带宽,约为Rubin GPU 22 TB/s的7倍。NVIDIA推出**异构架构**:Rubin GPU负责Prefill,Groq LPU负责Decode。
3. **多家纯Token Processor厂商完成大额融资**——Etched(5亿美元,50亿估值)、Taalas(1.69亿美元)、Positron(2.3亿美元)、SambaNova(3.5亿美元)、Cerebras准备2026年Q2 IPO目标266亿美元。

**核心判断**:Token Processor不是"GPU的小修正",而是**计算从通用张量到Token原语的范式迁移**。决定胜负的不再是峰值FLOPS,而是**单位Token的成本与延迟**(Cost/Token、Time-to-First-Token、Tokens/Second/Watt)。

---

## 一、概念边界:什么算"Token Processor"

调研中我把Token Processor定义为**同时满足以下三条**的加速器:

1. **以Token为基本数据单元**(而非通用张量),硬件架构围绕自回归生成或Transformer算子优化
2. **打破冯·诺依曼架构的内存-计算分离**——以片上SRAM、CIM、忆阻器或硬编码权重消除HBM搬运瓶颈
3. **软件层极薄**——编译器静态映射,运行时几乎不做调度决策(确定性执行)

按这个定义,严格的Token Processor目前包括:Groq LPU、Etched Sohu、Taalas HC1、IBM NorthPole、Tesla AI5(部分特征)、SambaNova SN系列、Cerebras WSE系列、Positron Atlas/Asimov、Tenstorrent Blackhole、d-Matrix。

**不算的**:NVIDIA Rubin GPU(仍是通用张量,但其LPX rack内嵌了Groq LPU,所以**Rubin平台整体**是混合架构),AMD MI400,Google TPU(TPU部分符合,但Google未公开足够细节)。

---

## 二、主要玩家:产品现状

### 2.1 Groq 3 LPU(NVIDIA旗下)

NVIDIA-Groq事件是整个领域的风向标。

- **架构**:将传统HBM替换为直接集成在芯片上的SRAM,内存带宽达到每秒150太字节。单芯片500 MB片上SRAM,带宽相当于H100 SXM(3.35 TB/s HBM3)的约45倍。
- **定位**:只做一件事——自回归Token生成。无法训练模型,无法以有竞争力的速度运行Prefill,无视觉/视频生成用途。
- **执行模型**:在LPU架构中,计算和数据移动以固定大小向量(320字节)为基本单元;每个LPU有96个互联链路、112 Gbps速率,聚合双向带宽约2.5 TB/s。
- **部署单元**:Groq 3 LPX平台是包含128个LPU的服务器机架(部分文档为256个,数据存在不一致)。
- **产业意义**:NVIDIA在GTC 2026推出**Vera Rubin + LPX**异构架构,为解码繁重的工作负载提供高达35倍每兆瓦推理吞吐量提升,但NVIDIA建议LPU仅占数据中心总容量约25%。
- **时间线**:Groq 3将于2026年下半年出货。

**判断**:NVIDIA把"Token"明确定为AI工厂的核心商品,LPU不是替代GPU,而是**与GPU组成生产线**。这是整个行业的标志性事件——它同时(a)验证了专用Token Processor的方向、(b)消灭了Groq作为独立挑战者的地位、(c)给所有其他玩家留下了"做NVIDIA买不动的那一类"的窗口。

### 2.2 Etched Sohu(独立Transformer ASIC)

最激进的"专用化优先"玩家之一。

- **架构**:将Transformer计算——多头注意力的QKV投影、softmax、输出投影、含GELU/SiLU激活的前馈网络、层归一化——构建为专用硬件块,而非可编程计算单元。数据流经固定的硬连线操作流水线,芯片不执行传统意义上的指令。
- **工艺**:基于TSMC 4nm工艺,144GB HBM3E,Reticle极限尺寸die(约800 mm²)。
- **性能**:8个Sohu芯片的服务器号称可替代约160片NVIDIA H100,在Llama 70B上实现约50万 tokens/秒。
- **融资**:Stripes和Peter Thiel领投5亿美元,总融资6.2亿美元,估值50亿美元。
- **风险**:截至2026年3月尚未向客户出货,距宣布超过20个月;无独立基准测试,所有性能宣称为自报;只能跑Transformer,若架构发生根本性变化(如SSM、混合架构),硬件即变成永久性资产负债。

**判断**:Sohu代表"transformer is the new x86"的极端押注。如果Transformer未来5-10年仍是主流,Sohu就是最强的Decode引擎之一;如果范式迁移,Sohu归零。

### 2.3 Taalas HC1(把模型烧进硅)

调研中**最激进的设计**,可能也是最危险的赌博。

- **核心理念**:不再让计算引擎可塑以便公司不断调整模型,而是把训练完成的AI推理权重直接编码到芯片的晶体管中。
- **架构创新**:使用mask ROM召回结构,将一个权重存储和与之相关的乘法全部用单个晶体管实现(即"四位存储+乘法,1个晶体管搞定")。这从物理上消除了内存墙。
- **性能**:单颗HC1运行Llama 3.1 8B,每秒生成16,000-17,000个tokens;NVIDIA H100对单用户约150 tokens/秒。即**约100倍单用户Throughput**。
- **效率宣称**:与传统芯片相比,效率(性能/瓦、性能/美元)提升1000倍(自报,未独立验证)。
- **工艺**:TSMC 6nm工艺(N6),die约815 mm²,约530亿晶体管。
- **路线图**:2026年夏季前将20亿参数Llama 3.1模型烧入HC芯片;年底用第二代HC2架构跨多卡运行前沿级LLM。
- **融资**:2026年初融资1.69亿美元,累计超2亿美元。创始人是Tenstorrent前创始人Ljubisa Bajic。
- **致命约束**:权重不可重写,芯片即模型;固件升级需要新芯片。GPT-4被GPT-5取代、Llama 2→3→3.1的迭代节奏,使硬编码模型的残值风险极高。

**判断**:Taalas把"软件无限廉价、硬件即护城河"推到极限——既然模型最终会稳定,不如直接把它做成基础材料。但这也是赌"模型稳定"的最大赌注。在汽车ECU、工业控制器、特定的离线推理产品上可能成立;在通用云端推理几乎不可能成立。

### 2.4 Tesla AI5 / Dojo 3(Musk的垂直整合)

- **AI5进展**:2026年4月15日Tesla taped out AI5。12个DRAM模块,16GB/模块,合计192GB LPDDR5X存储。
- **性能定位**:Musk称AI5单SoC约Hopper级,双SoC约Blackwell级(自报)。
- **路线**:9个月设计周期目标,AI6 Tape-out目标2026年12月,AI7已在规划中。
- **量产**:大批量生产预计2027年中期,由TSMC亚利桑那厂和Samsung德州厂双源供应。
- **Terafab**:2026年3月Tesla和SpaceX宣布在Austin建设250亿美元的Terafab项目;4月Intel加入负责制造和封装。
- **Dojo 3**:作为下一代训练超算,与AI5/AI6并行开发。

**判断**:Tesla路径与其他Token Processor厂商不同——它是**应用驱动**(FSD + Optimus + Robotaxi),不直接对外卖芯片。AI5部分符合Token Processor定义(自定义指令集、统一SRAM、编译器静态映射),但更准确的描述是"垂直整合的智能体计算平台"。Terafab是值得密切跟踪的变量——这是单一工业体系第一次试图把AI的整个供应链(设计-制造-封装-应用)收回手里。

### 2.5 NVIDIA Vera Rubin平台(GPU + LPU混合)

虽然Rubin GPU本身不是Token Processor,但**Vera Rubin整个平台**是当前最大的混合架构尝试。

- **Rubin GPU**:TSMC 3nm,多芯片模组设计,总晶体管3360亿,224个流式多处理器,第六代Tensor核支持FP4/FP6/FP8等。
- **平台规模**:Vera Rubin平台包含七个芯片、五种机架级系统;在机架级提供5倍推理性能、10倍每Token成本下降、10倍每瓦推理吞吐。
- **混合分工**:对万亿参数模型,NVIDIA参考分配为25%算力给LPX、75%给Rubin GPU,Groq 3 LPU运行前馈层、注意力留在Rubin。
- **2026年GTC关键决策**:2025年9月在AI Infra Summit宣布的Rubin CPX已从NVIDIA路线图移除,被Groq 3 LPX机架取代——这一替换很关键,等于NVIDIA放弃自研Decode专用GPU,直接采纳Groq方案。

**判断**:NVIDIA给出了未来3-5年最可能成为主流的范式——**Prefill用GPU、Decode用LPU**,通过Dynamo orchestration无缝切换。这种"分层异构"思路把不同生命周期、不同延迟特性的负载分给最适合的硬件,而非一刀切。

### 2.6 Cerebras WSE-3(晶圆级巨兽,准备IPO)

- **形态**:第三代晶圆级芯片(WSE-3),约57倍于NVIDIA H100,4万亿晶体管、90万计算核、44GB片上SRAM、21 PB/s带宽。
- **定位变化**:Cerebras已强力转向推理。
- **重磅合同**:2026年1月与OpenAI签署750兆瓦算力合同(到2028年),价值超过100亿美元。
- **IPO**:2026年1月以230亿估值募集10亿美元,目标266亿美元市值的Q2 2026 IPO。
- **架构限制**:无片外内存接口,大模型需跨多颗WSE分区;架构定位强单用户TPS,可能限制多用户企业环境效率。

**判断**:Cerebras是Groq被NVIDIA收购后**最大的独立Token Processor选手**。OpenAI的合同基本锁定了其未来两年的现金流,但客户高度集中(2024年G42一家占87%营收)是结构性风险。

### 2.7 SambaNova SN50(可重构数据流)

- **新一代芯片**:2026年2月24日发布SN50,宣称比上一代SN40L提供5倍每加速器算力。
- **架构**:SN40L为可重构数据流单元(RDU),三层内存层级。
- **战略动向**:2026年4月与Intel联合开发用于AI推理的异构系统蓝图,Intel还参与了SambaNova 3.5亿美元融资。

**判断**:SambaNova是"FPGA-like运行时重构"路径的代表。优势是单系统能跑大量不同模型,适合企业Agentic场景;劣势是软件栈复杂,生态不如NVIDIA。

### 2.8 Positron Atlas/Asimov(高内存推理)

- **现产品**:第一代Atlas由Intel在美国制造,声称达到NVIDIA H100 GPU三倍每瓦算力。
- **下一代**:Asimov支持每加速器2TB内存、每Titan系统8TB内存,机架级超过100TB;2026年10月tape-out,2027年初量产。
- **融资**:2026年2月完成2.3亿美元B轮,估值超10亿美元。
- **客户**:Cloudflare、Jump Trading等。

**判断**:Positron的差异化是**极端的内存容量**——把"长上下文+多智能体并发"作为核心场景。如果Asimov能在2027年初按时落地,会是少数同时具备容量和带宽优势的Token Processor。

### 2.9 Tenstorrent Blackhole(开源RISC-V路径)

- **进展**:Galaxy Blackhole进入量产,6nm Tensor处理器,GDDR6 RAM,Direct-Attach以太网,空冷。
- **性能**:DeepSeek模型每用户每秒308 tokens,目标到达500 TSU、6美元/百万输出tokens;视频生成创纪录(Prodia 2.4秒生成2.2秒视频)。

**判断**:Tenstorrent押注RISC-V + 开源软件栈,与NVIDIA正面竞争生态。技术上稳健,商业上依赖大客户能否以"开源安全感"为由跨过迁移成本。

### 2.10 IBM NorthPole(神经形态学派)

- **架构**:取消片外内存,在芯片上交织计算与内存,对外表现为active memory chip。
- **性能**:在ResNet-50上,相比12nm GPU,实现25倍每瓦帧数能效、5倍每晶体管帧数空间效率、22倍延迟优势。
- **LLM能力**:在16卡NorthPole设置上运行30亿参数Granite LLM,每张卡映射14个transformer层。

**判断**:NorthPole仍是研究原型,但理论意义大——它证明了**完全消除冯·诺依曼瓶颈**的设计可以做到工业级精度。IBM的下一步是更大规模的多卡系统。

### 2.11 d-Matrix(SRAM密度路径)

- **路线**:押注数据中心客户会需要多种推理处理器,获胜系统将组合不同硅片并适配现有数据中心。
- **观点**:d-Matrix CEO称"NVIDIA的发布验证了SRAM架构对大规模推理的重要性,而d-Matrix在SRAM密度上推得最远"。
- **进展**:2025年11月融资2.75亿美元,收购了GigaIO数据中心业务。

### 2.12 Compute-in-Memory / 忆阻器(底层物理路径)

学术界和早期产业化进展显著:

- **基础**:RRAM/忆阻器交叉阵列已实现30-150 fJ/MAC的MAC能效,完全单片RRAM-CMOS芯片可工作。
- **Transformer加速**:2026年3月发表的工作提出考虑变异(variation-aware)的忆阻器模拟Vision Transformer加速器,使用2048级忆阻器精度。
- **产业化路径**:Mythic、IBM(NorthPole)、台积电的SLC-MLC混合ReRAM CIM等。报告了251 TOPS/W的能效。

**判断**:CIM是**真正能实现10-1000倍能效跃迁的物理基础**,但工艺良率、模拟噪声、生态都还在研究阶段。预计2028-2030年看到首批数据中心级商用。

### 2.13 Unconventional AI(更激进的路径)

值得单独提及——它代表"以上所有都不够激进"的派别:

- 前Databricks AI高级副总裁Naveen Rao创立Unconventional AI,2026年初确认完成4.75亿美元种子轮,a16z和Lightspeed领投。
- 他的观点:Groq、D-Matrix、Cerebras虽在当前市场定位良好,但仍在同一数字计算范式内优化;Unconventional AI追求的路径是构建利用硅本身物理行为的新硬件,并重新设计与之匹配的神经网络。
- 他承认这一努力可能需要五年以上才能见效。

**判断**:这是Token Processor"下一代"的前哨。如果当前所有玩家做的是"软件→Token专用硬件"的迁移,Unconventional AI做的是"网络架构与物理器件协同设计"——更接近忆阻器+学习算法的联合优化。值得密切跟踪。

---

## 三、五条架构路径的现状对比

按上文分类,把2026年5月各路径的成熟度归纳:

| 路径 | 代表 | 成熟度 | 商业进度 |
|---|---|---|---|
| **Token Streaming + 大SRAM** | Groq、Cerebras、d-Matrix、Positron | 已商用 | NVIDIA-Groq、OpenAI-Cerebras等大单已签 |
| **可重构数据流(FPGA-like)** | SambaNova、Tenstorrent | 已商用 | 中等规模部署,与Intel/AMD合作 |
| **Compute-in-Memory(数字)** | IBM NorthPole | 研究原型 | 多卡LLM Demo已实现,2027年系统级落地 |
| **CIM + 忆阻器(模拟)** | Mythic、学术界 | 边缘/研究 | 数据中心级未商用 |
| **硬编码权重(model-on-silicon)** | Taalas、(部分Etched) | 演示级 | 2026年首批客户验证 |
| **垂直整合(自研全栈)** | Tesla AI5、Google TPU | 自用为主 | 不直接对外销售 |
| **混合GPU + LPU** | NVIDIA Vera Rubin | 即将商用 | 2026年下半年出货 |

---

## 四、共同的产业逻辑

调研多家公司后,**七个共性**清晰浮现:

### 1. 以推理为唯一目标
几乎所有Token Processor明确放弃训练。原因:2023年推理占AI算力约三分之一,2025年增至一半,2026年将代表总AI算力支出的约三分之二。训练一次,推理数十亿次——这是个量级问题,不是偏好问题。

### 2. 内存墙成为第一物理约束
所有架构创新都在攻击同一个问题:权重必须搬运到计算单元。三种路径并存:把权重塞进片上SRAM(Groq/Cerebras)、用CIM在内存里直接算(IBM/Mythic)、把权重直接物理化(Taalas)。

### 3. 确定性执行替代动态调度
GPU的核心灵活性——动态调度、缓存、分支预测——在自回归推理里都是噪音源。Token Processor普遍用**编译器静态映射 + 确定性数据通路**,把运行时不确定性降到接近零。

### 4. 单位Token成本成为唯一指标
不再比较TFLOPS、TOPS、HBM容量。GPT-4级别推理在2022年底约20美元/百万tokens,目前约0.40美元/百万tokens——这是规模与专用化共同作用的结果,**两年内成本下降50倍**。

### 5. Prefill/Decode 解耦成为标准架构
NVIDIA的官方推荐(Rubin负责Prefill、LPU负责Decode)正在成为行业最佳实践。vLLM、SGLang、NVIDIA Dynamo均已支持解耦推理。这意味着未来数据中心将是异构的,而非单一加速器。

### 6. 4nm/6nm已经够用,3nm争夺训练
Token Processor普遍选择**成熟工艺**(TSMC 4nm、6nm、12nm),理由是良率、成本、可获得性。NorthPole即在12nm下击败先进工艺GPU。这是产业逻辑:推理芯片不需要追最先进节点。3nm被留给训练。

### 7. 资本和并购指向终局
2025-2026的并购/融资规模($20B Groq、$5.5B Celestial AI、$10B+ OpenAI-Cerebras合同、$300B+ 2026年hyperscaler资本支出)说明:**这是基础设施级别的押注,不是产品级别的竞争**。业内分析师预测Intel可能收购SambaNova、AMD可能收购Cerebras。

---

## 五、关键不确定性

任何投资或架构决策必须考虑这五个变量:

### 5.1 模型范式风险
所有Token Processor都建立在"Transformer是稳定架构"的假设上。如果state-space models、混合架构、liquid neural networks或其他范式在2027-2029崛起,**Sohu和Taalas首当其冲**。Groq/Cerebras的SRAM架构相对灵活,但仍需重新优化编译器。

### 5.2 软件生态护城河
NVIDIA真正的壁垒不是GPU,是CUDA。Groq 3整合到NVIDIA NIM推理软件栈,设计上让LPU成为默认选择——这是NVIDIA在Token Processor时代试图复制CUDA锁定。其他玩家面对**"快40%但要换工具链"**的困境,落地时的实际摩擦远大于纸面性能。

### 5.3 内存方案的押注
HBM4? GDDR6? 大容量SRAM? LPDDR5X? 物理嵌入?每条路径都有结构性Trade-off:
- HBM:容量大但带宽-成本-功耗都重
- SRAM:延迟最低但容量限制大模型
- 嵌入(Taalas):效率天花板最高但灵活性归零

### 5.4 NVIDIA的护栏
NVIDIA已经收编Groq,下一步的猎物可能是:Etched、d-Matrix、SambaNova。任何独立Token Processor厂商都面临"要么被收购、要么被边缘化"的二元前景。这压缩了创业空间,但放大了已上车玩家(Cerebras、Tenstorrent)的估值。

### 5.5 工艺执行风险
Tesla AI6已因Samsung 2nm良率问题滑落约六个月。Terafab从宣布到出片至少3年。任何Token Processor的**纸面性能**和**实际可获得算力**之间存在巨大的执行落差。

---

## 六、时间线推断

基于已公开的tape-out和量产时间:

| 时间 | 事件 |
|---|---|
| **2026 Q2** | Cerebras IPO目标;NVIDIA Rubin GPU出货开始 |
| **2026 H2** | Groq 3 LPU/LPX机架广泛上市;Etched Sohu计划首批出货 |
| **2026 Q4** | Tesla AI6 tape-out目标;Positron Asimov tape-out;Taalas HC2前沿LLM部署 |
| **2027 H1** | Tesla AI5量产;Positron Asimov量产 |
| **2027 H2** | Rubin Ultra发布;Tesla AI6量产;首批Terafab产能 |
| **2028+** | 大规模CIM商用;NVIDIA Feynman发布;轨道级Token Processor演示(SpaceXAI路径) |

---

## 七、结论与判断

**1. Token Processor已经从概念变成产业现实。** NVIDIA-Groq事件的意义不仅在于200亿美元的金额,更在于**GPU霸主主动承认通用架构在Decode阶段输给了专用架构**。这是产业拐点。

**2. 最确定的赢家是Cerebras和NVIDIA(LPX)。** Cerebras靠OpenAI 100亿美元合同+IPO锁定地位;NVIDIA靠Groq IP+Rubin平台锁定异构架构标准。其他玩家都在争剩下的市场。

**3. 最大的赌注在Taalas和Etched。** 如果Transformer未来5-10年仍是主流且稳定,这两家定义下一代Token Processor的能效天花板;如果范式变,它们归零。这是高赔率/高风险的押注。

**4. 真正的下一代尚未到来。** Unconventional AI、CIM忆阻器、模拟计算这些路径,代表的是**2030年之后的Token Processor**——届时可能根本不再叫"Processor",而是叫"智能材料"。

**5. Token经济学正在重塑数据中心。** 当Cost/Token在两年内下降50倍,继续下降到接近零的边际成本时,**AI能力将像电力一样成为公用事业**——这才是Token Processor真正的产业意义。

---

**参考路径**:本报告基于2025年12月至2026年5月的公开报道、官方公告、技术论文、分析师评论。所有性能数据均为各公司自报或第三方测试,**独立基准测试在多数情况下尚未发布**——任何决策都应在产品实际可获得后再次验证。

**下一步关注点**:
- AMD CDNA 5/MI400系列在Computex 2026的反应
- Etched Sohu首次独立基准
- Taalas HC2前沿模型实测
- Unconventional AI的技术路径披露
- Tesla Terafab的实际开工进度
- 中国厂商(华为昇腾、寒武纪、Moore Threads)在Token Processor路径上的对应动作

