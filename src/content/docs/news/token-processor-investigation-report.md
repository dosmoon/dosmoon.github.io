---
title: "Token Processor: Industry Investigation Report"
description: Industry investigation on specialized accelerators built around Tokens as the primitive — product status, architecture paths, players, risks, and timeline.
---

> **Version**: v1.0 (English edition)
> **Cutoff**: May 10, 2026
> **Scope**: Focused on "specialized intelligent accelerators with Tokens as their primitive" — covering product status, architectural paths, industry landscape, risks, and timeline

---

## Executive Summary

Three things in the past six months have pushed Token Processors from "experimental concept" to "main industrial battlefield":

1. **On December 24, 2025, NVIDIA acquired Groq's IP and assets for approximately $20B** — the largest deal in AI hardware history, at 7× Groq's pre-acquisition valuation. As of April 2026, the Groq 3 LPU is in early-access preview, requiring registration through NVIDIA's enterprise program.
2. **At GTC 2026 on March 16, 2026, the Groq 3 LPU was officially unveiled**, replacing HBM with SRAM and achieving 150 TB/s memory bandwidth — roughly 7× the 22 TB/s of the Rubin GPU. NVIDIA introduced a **heterogeneous architecture**: Rubin GPU handles Prefill, Groq LPU handles Decode.
3. **Multiple pure-play Token Processor vendors closed major rounds** — Etched ($500M, $5B valuation), Taalas ($169M), Positron ($230M), SambaNova ($350M), and Cerebras is preparing a Q2 2026 IPO targeting $26.6B.

**Core judgment**: the Token Processor isn't a "minor correction to the GPU" — it's a **paradigm shift in compute, from general tensors to Token primitives**. Winners will no longer be decided by peak FLOPS, but by **cost and latency per Token** (Cost/Token, Time-to-First-Token, Tokens/Second/Watt).

---

## I. Defining the Boundary: What Counts as a "Token Processor"

For this investigation, a Token Processor must satisfy **all three** of the following:

1. **Token as the basic data unit** (rather than general tensors), with hardware architecture optimized around autoregressive generation or Transformer operators
2. **Breaks the von Neumann separation of memory and compute** — through on-chip SRAM, CIM, memristors, or hardcoded weights, eliminating the HBM-movement bottleneck
3. **Extremely thin software layer** — compiler does static mapping, runtime makes virtually no scheduling decisions (deterministic execution)

By this definition, strict Token Processors today include: Groq LPU, Etched Sohu, Taalas HC1, IBM NorthPole, Tesla AI5 (partially), SambaNova SN series, Cerebras WSE series, Positron Atlas/Asimov, Tenstorrent Blackhole, and d-Matrix.

**Excluded**: NVIDIA Rubin GPU (still general tensor, but its LPX rack embeds Groq LPU, so the **Rubin platform as a whole** is a hybrid architecture), AMD MI400, Google TPU (TPU partially qualifies, but Google has not disclosed enough detail).

---

## II. Major Players: Product Status

### 2.1 Groq 3 LPU (now under NVIDIA)

The NVIDIA-Groq event is the bellwether for the entire field.

- **Architecture**: replaces traditional HBM with SRAM integrated directly on the processor, achieving 150 terabytes per second of memory bandwidth. Each chip has 500 MB of on-chip SRAM, with bandwidth roughly 45× the H100 SXM (3.35 TB/s HBM3).
- **Positioning**: does one thing — autoregressive token generation. Cannot train models, cannot run Prefill at competitive speeds, has no use for vision or video generation.
- **Execution model**: in the LPU architecture, compute and data movement operate on fixed-size vectors (320 bytes); each LPU has 96 interconnect links at 112 Gbps, with aggregate bidirectional bandwidth of about 2.5 TB/s.
- **Deployment unit**: the Groq 3 LPX platform is a server rack containing 128 LPUs (some documents say 256 — sources are inconsistent).
- **Industry significance**: at GTC 2026, NVIDIA introduced the **Vera Rubin + LPX** heterogeneous architecture, delivering up to 35× higher inference throughput per megawatt for decode-heavy workloads, but recommends LPUs occupy only ~25% of total data center capacity.
- **Timeline**: Groq 3 ships in H2 2026.

**Judgment**: NVIDIA has explicitly defined "Token" as the AI factory's core commodity. The LPU isn't replacing the GPU — it's **forming a production line with the GPU**. This is the industry's signature event: it simultaneously (a) validates the direction of specialized Token Processors, (b) eliminates Groq as an independent challenger, and (c) leaves all other players the window of "doing the kind NVIDIA can't buy".

### 2.2 Etched Sohu (independent Transformer ASIC)

One of the most aggressive "specialization-first" players.

- **Architecture**: builds Transformer computation — multi-head attention QKV projection, softmax, output projection, feed-forward network with GELU/SiLU activation, and layer normalization — as dedicated hardware blocks rather than programmable compute units. Data flows through a fixed pipeline of hardwired operations; the chip doesn't execute instructions in the traditional sense.
- **Process**: TSMC 4nm, 144GB HBM3E, reticle-limit die (~800mm²).
- **Performance**: an 8-Sohu server reportedly replaces ~160 NVIDIA H100s, generating ~500,000 tokens/sec on Llama 70B.
- **Funding**: Stripes and Peter Thiel led a $500M round, total funding $620M, $5B valuation.
- **Risks**: not shipping to customers as of March 2026, more than 20 months after announcement; no independent benchmarks, all performance claims self-reported; can only run Transformers — if architecture shifts (SSM, hybrid architectures), the hardware becomes a permanent liability.

**Judgment**: Sohu represents the extreme bet of "transformer is the new x86". If Transformers remain mainstream for the next 5–10 years, Sohu is one of the strongest decode engines available; if a paradigm shift happens, Sohu goes to zero.

### 2.3 Taalas HC1 (model burned into silicon)

The **most radical design** in the investigation, and possibly the most dangerous bet.

- **Core idea**: rather than building malleable compute engines so companies can keep tweaking models, Taalas hardwires the trained AI inference weights directly into the chip's transistors.
- **Architectural innovation**: uses a mask ROM recall fabric where weight storage and the corresponding multiply for a single weight are implemented in a single transistor (i.e., "store 4 bits + multiply, all in one transistor"). This physically eliminates the memory wall.
- **Performance**: a single HC1 running Llama 3.1 8B generates 16,000–17,000 tokens per second; an NVIDIA H100 serves a single user at ~150 tokens/sec. That's **~100× single-user throughput**.
- **Efficiency claim**: 1000× improvement in efficiency (performance-per-watt and performance-per-dollar) versus conventional chips (self-reported, not independently verified).
- **Process**: TSMC 6nm (N6), die ~815mm², ~53 billion transistors.
- **Roadmap**: by summer 2026, plans to bake a 20B-parameter Llama 3.1 model into HC chips; by year-end, a frontier-class LLM running across multiple HC cards under HC2 architecture.
- **Funding**: $169M raised in early 2026, more than $200M cumulative. Founder Ljubisa Bajic is the founder of Tenstorrent.
- **Fatal constraint**: weights are non-rewritable — the chip is the model. A firmware upgrade requires a new chip. The cadence of GPT-4 → GPT-5, Llama 2 → 3 → 3.1, etc., creates very high residual-value risk for hardcoded models.

**Judgment**: Taalas pushes "software infinitely cheap, hardware as the moat" to the extreme — if models eventually stabilize, why not simply turn them into base material? But this is also the biggest possible bet on "model stability". Plausible for automotive ECUs, industrial controllers, and specific offline inference products; nearly impossible for general cloud inference.

### 2.4 Tesla AI5 / Dojo 3 (Musk's vertical integration)

- **AI5 progress**: Tesla taped out AI5 on April 15, 2026. 12 DRAM modules at 16GB each, totaling 192GB LPDDR5X.
- **Performance positioning**: Musk claims AI5 single SoC ≈ Hopper-class, dual SoC ≈ Blackwell-class (self-reported).
- **Roadmap**: 9-month design cycle target. AI6 tape-out targeted for December 2026; AI7 already in planning.
- **Production**: volume production expected mid-2027, dual-sourced from TSMC's Arizona facility and Samsung's Texas plant.
- **Terafab**: in March 2026, Tesla and SpaceX announced a $25B Terafab project in Austin; Intel joined as manufacturing and packaging partner in April.
- **Dojo 3**: in development as the next-generation training supercomputer in parallel with AI5/AI6.

**Judgment**: Tesla's path differs from other Token Processor vendors — it's **application-driven** (FSD + Optimus + Robotaxi), not directly selling chips. AI5 partially qualifies as a Token Processor (custom ISA, unified SRAM, compiler static mapping), but is more accurately described as a "vertically integrated agentic compute platform". Terafab is a variable worth watching closely — the first time a single industrial system has tried to take the entire AI supply chain (design–manufacturing–packaging–application) in-house.

### 2.5 NVIDIA Vera Rubin Platform (GPU + LPU hybrid)

The Rubin GPU itself isn't a Token Processor, but the **Vera Rubin platform as a whole** is the largest hybrid architecture attempt at present.

- **Rubin GPU**: TSMC 3nm, multi-chip module design, 336B transistors total, 224 streaming multiprocessors, 6th-gen Tensor cores supporting FP4/FP6/FP8 etc.
- **Platform scale**: includes seven chips and five rack-scale systems; at the rack level provides 5× inference performance, 10× lower cost per token, 10× higher inference throughput per watt.
- **Hybrid division**: for trillion-parameter models, NVIDIA's reference allocates 25% of compute to LPX and 75% to Rubin GPUs — Groq 3 LPUs run feed-forward layers, attention stays on Rubin.
- **Key 2026 GTC decision**: the Rubin CPX announced at AI Infra Summit in September 2025 was removed from NVIDIA's roadmap at GTC 2026, replaced by the Groq 3 LPX Rack — equivalent to NVIDIA abandoning a self-developed Decode-specialized GPU and adopting the Groq solution directly.

**Judgment**: NVIDIA has set out the most likely mainstream paradigm for the next 3–5 years — **GPU for Prefill, LPU for Decode**, switched seamlessly via Dynamo orchestration. This "layered heterogeneity" approach assigns workloads with different lifecycles and latency characteristics to the most suitable hardware, instead of one-size-fits-all.

### 2.6 Cerebras WSE-3 (wafer-scale beast, IPO incoming)

- **Form**: third-generation wafer-scale chip (WSE-3), about 57× the size of NVIDIA H100, 4 trillion transistors, 900,000 compute cores, 44GB on-chip SRAM, 21 PB/s bandwidth.
- **Pivot**: Cerebras has aggressively pivoted to inference.
- **Major contract**: in January 2026, signed a 750-megawatt compute contract with OpenAI through 2028, valued at over $10B.
- **IPO**: $1B raised in January 2026 at a $23B valuation; targeting Q2 2026 IPO at $26.6B.
- **Architectural limits**: no off-chip memory interface; large models must be partitioned across multiple WSEs; architecture targets strong single-user TPS, which may limit efficiency in multi-user enterprise environments.

**Judgment**: Cerebras is **the largest independent Token Processor player** after Groq's NVIDIA acquisition. The OpenAI contract essentially locks in two years of cash flow, but high customer concentration (G42 was 87% of 2024 revenue) is a structural risk.

### 2.7 SambaNova SN50 (reconfigurable dataflow)

- **New chip**: SN50 launched February 24, 2026, claiming 5× compute per accelerator versus the prior SN40L.
- **Architecture**: SN40L is a Reconfigurable Dataflow Unit (RDU) with a three-tier memory hierarchy.
- **Strategic moves**: in April 2026, partnered with Intel on a heterogeneous AI inference systems blueprint; Intel also participated in SambaNova's $350M funding round.

**Judgment**: SambaNova represents the "FPGA-like runtime reconfiguration" path. Strength: a single system can run a large variety of models, well-suited for enterprise Agentic scenarios. Weakness: complex software stack; the ecosystem lags NVIDIA's.

### 2.8 Positron Atlas / Asimov (high-memory inference)

- **Current product**: first-gen Atlas, fabricated by Intel in the US, claims roughly 3× compute per watt versus NVIDIA H100.
- **Next-gen**: Asimov supports 2TB memory per accelerator, 8TB per Titan system, over 100TB at rack-scale. Tape-out October 2026, production early 2027.
- **Funding**: closed $230M Series B in February 2026, valuation over $1B.
- **Customers**: Cloudflare, Jump Trading, etc.

**Judgment**: Positron's differentiation is **extreme memory capacity** — making "long context + multi-agent concurrency" the core scenario. If Asimov ships on schedule in early 2027, it will be one of the few Token Processors with both capacity and bandwidth advantages.

### 2.9 Tenstorrent Blackhole (open-source RISC-V path)

- **Progress**: Galaxy Blackhole entered volume production. 6nm tensor processor, GDDR6 RAM, direct-attach Ethernet, air-cooled.
- **Performance**: 308 tokens/sec/user on DeepSeek, with a roadmap to 500 TSU at $6/million output tokens; record video generation (Prodia 2.4-second generation of a 2.2-second video).

**Judgment**: Tenstorrent bets on RISC-V + open-source software stack to compete head-on with NVIDIA on ecosystem. Technically solid; commercially dependent on whether large customers can use "open-source security" as a justification to cross the migration cost.

### 2.10 IBM NorthPole (neuromorphic school)

- **Architecture**: eliminates off-chip memory, intertwines compute and memory on chip, externally appearing as an active memory chip.
- **Performance**: on ResNet-50, vs. 12nm GPU, 25× higher frames/watt energy efficiency, 5× higher frames/transistor space efficiency, 22× lower latency.
- **LLM capability**: a 16-card NorthPole setup runs the 3B-parameter Granite LLM, mapping 14 transformer layers per card.

**Judgment**: NorthPole is still a research prototype, but its theoretical significance is large — it proves a design that **completely eliminates the von Neumann bottleneck** can reach industrial-grade accuracy. IBM's next step is larger-scale multi-card systems.

### 2.11 d-Matrix (SRAM density path)

- **Path**: bets that data center customers will want a variety of inference processors, and that winning systems will combine different silicon and fit into existing data centers.
- **View**: d-Matrix CEO says NVIDIA's announcement validates the importance of SRAM-based architectures for large-scale inference, and that d-Matrix has pushed SRAM density furthest.
- **Progress**: $275M raised in November 2025, acquired GigaIO's data center business.

### 2.12 Compute-in-Memory / Memristors (the underlying physics path)

Significant progress in academia and early commercialization:

- **Foundation**: RRAM/memristor crossbar arrays already achieve MAC energy of 30–150 fJ/MAC; fully monolithic RRAM-CMOS chips work.
- **Transformer acceleration**: a March 2026 paper proposed a variation-aware memristor analog accelerator for Vision Transformers, using 2048-level memristor precision.
- **Commercialization paths**: Mythic, IBM (NorthPole), TSMC's SLC-MLC hybrid ReRAM CIM, etc. Reported energy efficiency up to 251 TOPS/W.

**Judgment**: CIM is the **physical foundation that can actually deliver 10–1000× efficiency leaps**, but process yield, analog noise, and ecosystem are all still in research stages. First data-center-scale commercial deployments expected 2028–2030.

### 2.13 Unconventional AI (a more radical path)

Worth mentioning separately — it represents the "everything above isn't radical enough" school:

- Naveen Rao, former Senior VP of AI at Databricks, founded Unconventional AI. Confirmed a $475M seed round in early 2026, led by a16z and Lightspeed.
- His view: Groq, D-Matrix, Cerebras may be well positioned in today's market, but they are still optimizing within the same digital computing paradigm. Unconventional AI is pursuing hardware that exploits the physical behavior of silicon itself, with neural networks redesigned to match.
- He has acknowledged the effort could take five years or more to bear fruit.

**Judgment**: this is the outpost of "next-generation" Token Processors. If everyone today is migrating from "software → Token-specialized hardware", Unconventional AI is doing co-design between network architecture and physical devices — closer to joint optimization of memristors and learning algorithms. Worth watching closely.

---

## III. Comparing the Five Architectural Paths Today

Summarizing the maturity of each path as of May 2026:

| Path | Representative | Maturity | Commercial progress |
|---|---|---|---|
| **Token Streaming + large SRAM** | Groq, Cerebras, d-Matrix, Positron | Commercial | NVIDIA-Groq, OpenAI-Cerebras and other major contracts signed |
| **Reconfigurable dataflow (FPGA-like)** | SambaNova, Tenstorrent | Commercial | Mid-scale deployment, partnerships with Intel/AMD |
| **Compute-in-Memory (digital)** | IBM NorthPole | Research prototype | Multi-card LLM demos achieved, system-level rollout 2027 |
| **CIM + memristor (analog)** | Mythic, academia | Edge / research | Not commercialized at data-center scale |
| **Hardcoded weights (model-on-silicon)** | Taalas, (partially Etched) | Demo level | First customer validations in 2026 |
| **Vertical integration (full self-developed)** | Tesla AI5, Google TPU | Internal use | Not sold externally |
| **Hybrid GPU + LPU** | NVIDIA Vera Rubin | About to ship | Shipping H2 2026 |

---

## IV. Common Industrial Logic

After investigating the players, **seven commonalities** clearly emerge:

### 1. Inference as the sole goal
Almost all Token Processors explicitly give up training. Reason: in 2023 inference was about one-third of AI compute; in 2025 it's about half; in 2026 it will represent roughly two-thirds of total AI compute spend. Train once, inference billions of times — this is a question of magnitude, not preference.

### 2. The memory wall is the first physical constraint
All architectural innovations are attacking the same problem: weights have to move to compute. Three approaches coexist: pack weights into on-chip SRAM (Groq/Cerebras), compute in memory directly (IBM/Mythic), or physicalize the weights (Taalas).

### 3. Deterministic execution replaces dynamic scheduling
The GPU's core flexibility — dynamic scheduling, caching, branch prediction — are noise sources in autoregressive inference. Token Processors uniformly use **compiler static mapping + deterministic data paths**, reducing runtime uncertainty to nearly zero.

### 4. Cost-per-Token becomes the only metric
No longer comparing TFLOPS, TOPS, HBM capacity. GPT-4-class inference cost about $20 per million tokens in late 2022, currently about $0.40 per million tokens — the combined effect of scale and specialization, **a 50× cost reduction in two years**.

### 5. Prefill/Decode disaggregation becomes standard architecture
NVIDIA's official recommendation (Rubin handles Prefill, LPU handles Decode) is becoming industry best practice. vLLM, SGLang, and NVIDIA Dynamo all support disaggregated inference. This means future data centers will be heterogeneous, not single-accelerator.

### 6. 4nm/6nm is enough; 3nm is for training
Token Processors generally choose **mature processes** (TSMC 4nm, 6nm, 12nm), citing yield, cost, and availability. NorthPole at 12nm beats more advanced GPUs. This is industrial logic: inference chips don't need to chase the most advanced node. 3nm is left to training.

### 7. Capital and M&A signal an endgame
The scale of M&A and funding in 2025–2026 ($20B for Groq, $5.5B for Celestial AI, $10B+ OpenAI-Cerebras contract, $300B+ in 2026 hyperscaler capex) shows: **this is an infrastructure-level bet, not a product-level competition**. Industry analysts predict Intel may acquire SambaNova, AMD may acquire Cerebras.

---

## V. Key Uncertainties

Any investment or architectural decision must consider these five variables:

### 5.1 Model paradigm risk
All Token Processors rest on the assumption that "Transformer is a stable architecture". If state-space models, hybrid architectures, liquid neural networks, or other paradigms rise in 2027–2029, **Sohu and Taalas take the brunt**. Groq/Cerebras's SRAM architectures are relatively flexible, but still need compiler re-optimization.

### 5.2 Software ecosystem moat
NVIDIA's real moat isn't the GPU — it's CUDA. Groq 3 integrates into NVIDIA's NIM inference software stack, designed by NVIDIA to make the LPU the default choice — this is NVIDIA trying to replicate CUDA lock-in for the Token Processor era. Other players face the **"40% faster but you have to switch toolchains"** dilemma; the practical friction at deployment far exceeds the on-paper performance.

### 5.3 Memory choice bet
HBM4? GDDR6? Large-capacity SRAM? LPDDR5X? Physical embedding? Every path has structural trade-offs:
- HBM: large capacity, but heavy on bandwidth-cost-power
- SRAM: lowest latency, but capacity limits big models
- Embedding (Taalas): highest efficiency ceiling, but flexibility goes to zero

### 5.4 NVIDIA's enclosure
NVIDIA has already absorbed Groq. Next prey could be Etched, d-Matrix, or SambaNova. Every independent Token Processor vendor faces a binary outcome: be acquired or be marginalized. This compresses the startup space but amplifies valuations of those already on board (Cerebras, Tenstorrent).

### 5.5 Process execution risk
Tesla AI6 has already slipped about six months due to Samsung 2nm yield issues. Terafab takes at least 3 years from announcement to first wafers. The gap between any Token Processor's **paper performance** and **actually available compute** is large.

---

## VI. Timeline Outlook

Inferred from publicly disclosed tape-out and production schedules:

| Time | Event |
|---|---|
| **2026 Q2** | Cerebras IPO target; NVIDIA Rubin GPU begins shipping |
| **2026 H2** | Groq 3 LPU/LPX rack widely available; Etched Sohu first shipments planned |
| **2026 Q4** | Tesla AI6 tape-out target; Positron Asimov tape-out; Taalas HC2 frontier LLM deployment |
| **2027 H1** | Tesla AI5 volume production; Positron Asimov production |
| **2027 H2** | Rubin Ultra launch; Tesla AI6 production; first Terafab capacity |
| **2028+** | Large-scale CIM commercialization; NVIDIA Feynman launch; orbital-grade Token Processor demos (the SpaceXAI path) |

---

## VII. Conclusions and Judgments

**1. Token Processors have moved from concept to industrial reality.** The significance of the NVIDIA-Groq event is not the $20B price tag but rather **the GPU king publicly admitting that the general-purpose architecture loses to specialized architectures in the Decode stage**. This is the industry's inflection point.

**2. The most certain winners are Cerebras and NVIDIA (LPX).** Cerebras locks its position with the $10B OpenAI contract + IPO; NVIDIA locks the heterogeneous-architecture standard via Groq IP + Rubin platform. Other players are competing for the rest of the market.

**3. The biggest bets are Taalas and Etched.** If Transformer remains mainstream and stable for the next 5–10 years, these two define the efficiency ceiling of next-generation Token Processors; if a paradigm shift happens, they go to zero. This is the high-payoff/high-risk bet.

**4. The true next generation is not yet here.** Unconventional AI, CIM memristors, analog computing — these paths represent the **post-2030 Token Processor** — by which point it may not be called a "Processor" at all, but rather "intelligent material".

**5. Token economics are reshaping the data center.** When Cost/Token drops 50× in two years and continues toward near-zero marginal cost, **AI capability becomes a public utility like electricity** — that is the Token Processor's true industrial significance.

---

**Reference path**: This report draws on public reporting, official announcements, technical papers, and analyst commentary from December 2025 through May 2026. All performance data are self-reported by the respective companies or third-party tested; **independent benchmarks have, in most cases, not yet been published** — any decision should be re-validated when products are actually available.

**Next focus points**:
- AMD CDNA 5 / MI400 series response at Computex 2026
- Etched Sohu first independent benchmarks
- Taalas HC2 frontier model real-world tests
- Disclosure of Unconventional AI's technical path
- Tesla Terafab actual construction progress
- The corresponding moves of Chinese vendors (Huawei Ascend, Cambricon, Moore Threads) on the Token Processor path

