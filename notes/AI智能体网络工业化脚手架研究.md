# AI 智能体网络工业化脚手架（Scaffold）研究

> **一句话总结**：参考无线通信网治理体系，围绕 Token 智能计量计费、CPU+GPU 可扩展部署架构、安全合规治理和分布式智能体服务框架四大方向，构建支持 Scaling Law 持续扩展、可赋能千行百业的 AI 智能体网络工业化脚手架（Scaffold）体系。

---

## 简介

随着大模型技术的快速发展，人类社会正从信息化、数字化迈向"智能化"时代。在这一进程中，大模型通过 Scaling Law（扩展定律）不断提升智能能力，但其产业落地不仅需要训练更强大的模型，更需要一套可扩展、可治理、可迭代的工业化基础设施——我们称之为**智能体网络脚手架（Scaffold）**。当前业界对智能体的应用仍停留在小规模、碎片化的阶段，缺乏类似无线通信网络那样可演进、可管理的完整体系。本研究旨在通过系统性架构设计，为智能体网络的规模化部署与治理提供参考框架，最终推动 AI 从"实验室能力"转化为"社会基础设施"，实现千行百业的智能化转型。

---

## 一、研究背景

大模型的迅猛发展，为我们提供了信息化、数字化之外的"智能化"选项。计算机不再仅仅完成指定的数据处理和传输工作，而是利用 AI 大模型，针对非确定性任务自主完成带有决策和执行过程的信息处理工作。目前大模型的发展离不开 Scaling Law，即模型的智能能力（自主处理信息的能力）正比于其训练时数据集容量、训练算力强度以及模型参数规模。大模型在提供智能化服务时，目前业界基本采用 Token（词元）计量的方法来管理其服务能力。随着大模型能力的快速提高，其可以完成的任务越来越多。但就像移动通信网络一样，这种智能化能否有效计量计费以保障其合理性，能否有效扩展服务更多需求，能否有效管理以确认其安全性，以及能否结合生态使其赋能千行百业，都是我们在 Scaling Law（训练模型）之外需要考虑利用模型的事情。

由于大模型的迭代速度超过当年互联网普及时的迭代速度，目前业界研究的重点仍停留在模型的训练和直接推理，其核心基础架构是 GPU。今年以来，随着 OpenClaw 等智能体的快速普及，人们越来越多地使用大模型来驱动智能体操作各种工具，完成编程、办公、文档处理、视频生成等任务，并催生了 AI 短剧、AI 科研、AI 小程序等新兴领域。智能体的部署是在 CPU 之上的逻辑处理，其运行环境需要与现有的信息化、数字化和工具体系相融合。而大模型可以通过"现场编程"为智能体"造工具"，从而极大地拓展了 CPU+GPU 基础架构的应用范围和集成需求。我们注意到，目前支持这种应用的基础架构——脚手架（Scaffold），还处在小规模应用阶段，尚无类似无线通信网体系的可扩展、可迭代、可管理和可治理的完整体系，亟需对其"工业化"可扩展参考架构进行研究。

---

## 二、研究目标

参考无线通信网的构建和治理体系，从 Token 智能计量计费、CPU+GPU 智能网络部署参考架构、智能体网络安全合规治理，以及松散耦合的分布式智能体网络服务框架与数据基盘集成体系等方向开展研究，使智能体网络在部署时不仅能符合 Scaling Law 的智能扩充，还能随着任务范围扩大集成千行百业应用，并支持智能运营商建立网络部、技术部、安全部以及数据部等类似的治理机构。

---

## 三、研究方向

### 方向一：Token 的智能计量与计费体系研究

#### 研究挑战

当前大模型服务普遍采用基于 GPU 硬件成本的 Token 数量计费方式，即按输入和输出 Token 的数量乘以单价结算。这种纯成本驱动的定价逻辑存在根本性缺陷：不同模型解决同一问题的"智能效用"差异巨大，高智能模型可能用 300 万 Token 完成的任务，低智能模型可能需要 5000 万 Token 仍无法成功；用户在简单任务上使用高成本模型会造成过度支付，在复杂任务上使用未达阈值的低成本模型则导致任务无法完成并反复浪费 Token。现有体系仅有供给侧的成本信号，缺乏需求侧的智能效用信号，无法回答"什么模型适合什么任务"这一核心问题。

从成本推导角度看，Token 的定价基于 GPU 推理成本。以 NVIDIA H200 为例，云上单机时价约 $60/小时，若模型输出吞吐上限为 800 Token/秒，则每百万 Token 输出成本约为 $20.83。厂商在此基础上叠加利润、运行成本摊销和研发成本摊销形成最终售价。类似 OpenRouter、硅基流动等"Token 工厂"以批发方式从原厂采购或自行部署开源模型 Serving，以接近成本价策略对外销售。然而，这种纯成本定价忽视了 AI 服务的核心属性——**智能效用**，即单位 Token 实际解决用户问题的能力。

#### 研究内容

本方向需要引入**"任务智能计算法"**（Task Intelligence-Based Pricing），根据模型在特定任务上的实际表现来定价 Token，而非仅根据硬件成本。具体研究内容包括：

1. **三维度需求分级框架**：建立问题难度分类（金级/银级/铜级 Token）、工具体系分类（文本/多模态/感知/专业工具）和运行体系分类（速度/合规/隐私/SLA）的立体分级体系，遵循"先解决能不能干，再看干活的成本，并考虑干活的风险"的决策逻辑。

2. **五维度 Benchmark 分类标准**：在编程（项目级/任务级/作业级）、生成报告（论文级/报告级/工作级）、运维操作（企业级/项目级/个人级）、专业操作（核心系统/工作系统/个人操作）和创新操作（创新级/工作级）五个领域建立分级评估标准。

3. **Benchmark 输出维度**：从阈值达标（Pass/Fail，判定模型是否具备解决该类任务的基本能力）、效率指标（Token 消耗量、Token 效率比、时间消耗、迭代次数）和非功能需求评分（模型安全性、内置工具丰富度、推理效率、上下文长度、Agentic 适配性）三个维度输出评估结果。

4. **生态价值机制**：建立用户按需选择、模型工厂精准 Serving、模型提供方定向迭代的正向循环，让 Benchmark 丰富度推动工具链完善，工具链完善又反哺 Benchmark 扩展，最终从"卖 Token"转向"交付解决问题的能力"。

---

### 方向二：CPU+GPU 智能网络部署参考架构研究

#### 研究挑战

在传统的纯 GPU、无状态的模型 Serving 体系基础上，需要结合智能体工具需求和可扩展需求，研究 CPU+GPU 可以随着 Scaling Law 同步扩展的智能体部署参考架构。当前的核心矛盾在于：简单复制 5000 个虚机造就 5000 个"数字员工"的扩展方式，在 CPU 端实现很快，但会对 GPU 端造成巨大的 Serving 压力，引起排队、资源等待甚至传输冲突。如何在云计算基础上建立全国乃至全球合理分布的逻辑处理集成智能驱动的集群，同时解决智能体工具组装的灵活性与安全性矛盾，以及扩展速度与治理能力同步进化的问题，是本方向的核心挑战。

#### 研究内容

本方向分为三个子方向：

1. **可扩展的智能体服务框架研究**：利用云计算基础概念，研究如何建立全国乃至全球合理分布的逻辑处理集成智能驱动的集群，既满足智能体网络架构的基础要求，又响应 Scaling Law 带来的物理扩展需求。重点解决 GPU 端 Serving 压力、排队和资源冲突问题，探索算力中心、算力网络及其数据传输和多模态处理协作能力的映射机制。

2. **可组装的智能体服务研究**：研究如何根据用户的任务特点和大模型的治理水平，针对不同的可扩展任务，为智能体提供"乐高式"的工具组合能力与 Harness 调用管理能力，并在很短时间内完成组合与迭代。重点解决工具范围失控导致的"越狱"风险与工具过少限制能力之间的矛盾，探索超越 MicroVM 的组装体系在云计算不同分支上的融合与创新。

3. **可扩展与可管理的集成保障研究**：研究企业在使用智能体时，如何既让其自主完成数据相关工作，又防止其跨越数据治理域造成风险。通过网络、数据中心、传输控制等多方向管理智能体自主工作和可扩展的范围，并建立结合 Scaling Law 的智能快速迭代管理体系，确保扩展速度与治理能力的同步进化。

---

### 方向三：智能体网络安全合规治理体系研究

#### 研究挑战

面向大模型的安全研究是当前业界的重点。在智能体网络中，安全治理不仅仅需要考虑恶意攻击，还需要考虑大模型的"内在幻觉"对自主智能体决策的影响。具体挑战包括：大模型采集的外部数据和内部数据的可靠性、时效性、完整性校验；企业内部数据在利用大模型时如何保证其可控性；以及针对不同智能体应用的安全等级适配能力。作为智能体运营商，连接企业应用和模型提供方时，如何保障信息的安全传输，并为双方提供可信的数据治理体系，是当前大模型应用的核心难题。此外，智能体网络与云计算、通讯网络是集成关系，跨网络边界的安全治理也是必须面对的挑战。

#### 研究内容

本方向重点研究以下四个层面：

1. **数据安全与隐私治理**：研究如何通过扩展算法去除原始数据中的个人隐私，通过"隐空间"转换屏蔽信息原始内容，通过信息量化和对抗网络以"近似法"处理信息，使智能体网络的治理比肩无线通信网和云计算的能力，从而扩大 Scaling Law 的赋能范围。

2. **跨网络边界安全治理**：研究智能体网络与云计算、通讯网络集成关系下的跨网络边界安全治理机制，包括不同治理域之间的数据传输安全、认证与授权管理、以及安全策略的统一编排。

3. **模型幻觉与决策可靠性**：假设模型存在幻觉，研究通过多个模型的混合决策，融合和激发可解释、可证伪及可形式化描述的智能过程，构建智能体网络的必要研究底座。重点研究多模型共识机制、决策可追溯性和可审计性。

4. **安全等级适配体系**：研究针对不同智能体应用场景（如个人助理、企业运维、核心系统操作）的安全等级划分与适配机制，建立动态安全评估与风险预警体系。

---

### 方向四：智能体网络服务框架与数据基盘集成体系研究

#### 研究挑战

当前智能体网络的服务框架仅停留在小规模原型阶段，缺乏面向用户和集成伙伴的、从 Scaling Law 到可扩展智能业务的完整参考架构和服务体系。挑战包括：如何实现物理和逻辑分布以保障业务连续性和管理有效性；如何将现有面向个人的 Client/Server 型大模型应用转化为具有服务中间形态的互联网型智能应用；如何将机器人具身智能与 Scaling Law 融合，实现 Robot-as-a-Service；以及如何解决现有智能体数据格式和处理方式不一致的问题，建立语义数据基盘。

#### 研究内容

本方向分为四个子方向：

1. **智能体构建的服务框架研究**：研究面向用户和集成伙伴的、从 Scaling Law 到可扩展智能业务构建的参考架构和服务体系。具体包括从个性化的 Skill 体系，到能力集成的 Harness 体系，到基础 Scaffold 体系的构建服务，以及数据基盘（Data Substrate）的集成，探索在语义集成的松散耦合体系下完成上述组件的快速组装与迭代。

2. **分布式智能体服务研究**：研究如何通过物理和逻辑的分布保障智能体网络服务的业务连续性和管理有效性。重点探索不同大模型算力中心、算力网络及其数据传输和多模态处理协作能力的映射机制，推动现有大模型应用从面向个人的 Client/Server 型向具有服务中间形态的互联网型智能应用转化。

3. **从智能体网络到具身智能的映射研究**：研究机器人具身智能与大模型 Scaling Law 的融合路径。重点探索 Robot-as-a-Service（RaaS）云部署产业模式，即用户租赁机器人、机器人从智能体网络下载 Skill、智能体网络利用分布式服务能力提供端到边的实时智能支持，推动物理智能体到信息智能体到大模型的应用体系落地。

4. **松散耦合的数据基盘研究**：研究从语义数据基盘入手，协助运营商构建不同企业数据处理流水线，使数据物尽其用的同时围绕智能输出进行优选，完成从数据基盘到智能体耦合的快速、松散和可扩展拓展。重点研究数据处理过程、Embedding 融合、语义信息熵稳定性管理，以及"Aha Moment"类型的多领域信息激发机制。

---

## 四、总结与展望

总而言之，我们希望通过上述系列研究，使运营商在构建智能体网络时，不仅仅是物理地将不同的 GPU 集群连在一起，而是能够结合模型 Scaling Law，形成类似于无线通信网络的可演进的智能驱动框架，以完成 AI 赋能千行百业，提升社会总体生产率，推动基于 Transformer 智能的行业 Transformation。

这套工业化脚手架（Scaffold）体系的核心价值在于：将模型训练时代的 Scaling Law 从"实验室能力"转化为"社会基础设施"——通过可计量的智能效用、可扩展的部署架构、可治理的安全合规和可耦合的服务框架，让 AI 智能体网络像通信网络一样成为支撑社会运转的底层能力，最终推动整个人类社会的智能化转型。

---

## 附录：研究内容总表

| 大方向 | 子方向 | 研究挑战 | 核心研究内容 |
|--------|--------|----------|-------------|
| **方向一：Token 智能计量与计费** | 三维度需求分级框架 | 纯成本定价忽视智能效用差异，用户面临"过度支付"或"任务失败"的两难 | 建立问题难度（金/银/铜级）、工具体系（文本/多模态/感知/专业）、运行体系（速度/合规/隐私/SLA）的立体分级体系 |
| | 五维度 Benchmark 分类 | 缺乏面向应用的标准化模型评估体系，用户无法精准选型 | 在编程、生成报告、运维操作、专业操作、创新操作五个领域建立分级评估标准 |
| | Benchmark 输出维度 | 现有 Benchmark 无法衡量 Token 效率和任务完成质量 | 从阈值达标（Pass/Fail）、效率指标（Token 效率比、时间消耗、迭代次数）和非功能需求评分（安全性、工具丰富度、Agentic 适配性）三个维度输出评估 |
| | 生态价值机制 | 市场缺乏正向激励，模型厂商陷入同质化价格战 | 建立用户-模型工厂-提供方的飞轮效应，推动从"卖 Token"到"交付解决问题能力"的转变 |
| **方向二：CPU+GPU 智能部署架构** | 可扩展的智能体服务框架 | 简单复制虚机导致 GPU 端 Serving 压力、排队和资源冲突 | 研究全国/全球分布的逻辑处理集成智能驱动集群，响应 Scaling Law 的物理扩展需求 |
| | 可组装的智能体服务 | 工具范围失控导致"越狱"，工具过少又限制能力 | 研究"乐高式"工具组合、Harness 调用管理，超越 MicroVM 的组装体系 |
| | 可扩展与可管理的集成 | 智能体自主工作易跨越数据治理域造成风险 | 通过网络、数据中心、传输控制等多方向管理，实现扩展与治理同步进化 |
| **方向三：安全合规治理体系** | 数据安全与隐私治理 | 原始数据隐私泄露风险，信息原始内容需要屏蔽 | 研究扩展算法去隐私、"隐空间"转换、信息量化和对抗网络的"近似法"处理 |
| | 跨网络边界安全治理 | 智能体网络与云计算、通讯网络集成带来的边界安全挑战 | 研究跨网络边界的安全传输、认证授权、安全策略统一编排 |
| | 模型幻觉与决策可靠性 | 大模型"内在幻觉"影响自主智能体决策 | 研究多模型混合决策、可解释/可证伪/可形式化的智能过程 |
| | 安全等级适配体系 | 不同智能体场景需要差异化的安全等级 | 研究个人助理、企业运维、核心系统操作的安全等级划分与动态适配 |
| **方向四：服务框架与数据基盘** | 智能体构建的服务框架 | 缺乏面向用户和集成伙伴的完整参考架构 | 研究 Skill 体系、Harness 体系、Scaffold 构建服务、数据基盘集成的语义松散耦合体系 |
| | 分布式智能体服务 | 需要保障业务连续性和管理有效性 | 研究算力中心、算力网络协作能力的映射，推动 Client/Server 向互联网型智能应用转化 |
| | 具身智能映射 | 机器人具身智能与 Scaling Law 尚未融合 | 研究 Robot-as-a-Service（RaaS）模式，物理智能体-信息智能体-大模型的应用体系 |
| | 松散耦合的数据基盘 | 智能体数据格式不一致，缺乏面向企业/机器人/互联网侧的数据处理支持 | 研究语义数据基盘、企业数据处理流水线、Embedding 融合、语义信息熵管理、"Aha Moment"多领域信息激发 |

---

## 附表二：研究方向产出物 Spec 清单

> **说明**：以下 Spec 清单基于三层可扩展 Agentic Runtime 架构（Scaffold / Harness / Skill / Data）的已有研究，为每个研究方向列出可独立研究、可工程化落地的具体产出物。每个 Spec 均包含定义、接口、验证标准与可集成路径，可直接指导原型开发与 Benchmark 设计。

### 一、Scaffold 层产出物 Spec

| Spec 编号 | Spec 名称 | 对应研究方向 | 核心内容 | 关键指标 / 验证标准 |
|-----------|-----------|-------------|----------|-------------------|
| S-01 | **Agentic MicroVM Spec** | 方向二·可扩展的智能体服务框架 | microVM / container / WASM sandbox 的隔离执行单元定义：runtime_kind、image/snapshot、资源配额、syscall filter、冷启动与快照恢复 | escape rate < 0.01%；cold start < 500ms；snapshot restore < 100ms |
| S-02 | **Agentic Scaling Benchmark** | 方向一·Benchmark 输出维度 + 方向二·可扩展框架 | 面向 Agentic Runtime 的扩展性评估框架：subagent 并发上限、fork 延迟、KV cache 多租户调度、GPU Serving 排队模型 | TTFT p95 < 2s；并发扩展线性度 R² > 0.95；资源冲突率 < 1% |
| S-03 | **Token Efficiency Benchmark** | 方向一·Benchmark 输出维度 | 任务级 Token 效率评估：单位任务消耗的 Token 数、迭代次数、context 膨胀率、compact/recap 触发频率 | Token 效率比（任务完成度 / Token 消耗）> 基准模型 2x |
| S-04 | **Enterprise SSO / Identity Spec** | 方向三·跨网络边界安全治理 | OIDC / SAML 2.0 联合登录、SCIM 用户/组同步、RBAC/ABAC、租户隔离、JIT 授权、审计登录事件 | SSO 成功率 > 99.9%；token 刷新失败 < 0.1%；越权访问 = 0 |
| S-05 | **Cloud Integration Spec** | 方向二·可扩展与可管理的集成 | AWS/GCP/Azure 接入：Workload Identity（免静态密钥）、KMS/Secrets Manager、对象存储（S3/GCS/Blob）、VPC/PrivateLink、Bedrock/Vertex 模型端点 | 跨云延迟 < 50ms；密钥泄漏面 = 0；provider 故障切换 < 5s |
| S-06 | **Subagent Launch / Fork Spec** | 方向二·可扩展的智能体服务框架 | 启动/供给 subagent 运行时的完整接口：分配 CPU/隔离单元/serving 槽位、fork 可调度执行体、生命周期管理（create/pause/resume/snapshot/terminate） | subagent 冷启动 < 1s；资源占用可预测；并发上限可配置 |
| S-07 | **Security Policy Enforcement Spec** | 方向三·安全等级适配体系 | syscall filter、path/network policy、malware scan、prompt/tool boundary、data boundary 的统一下发与审计 | policy violation = 0（阻断模式）；audit completeness = 100% |
| S-08 | **Serving Capacity Scheduling Spec** | 方向二·可扩展的智能体服务框架 | 模型端点、KV cache、batching、speculative decoding、多租户调度、背压与优先级 | tokens/s 利用率 > 80%；p95 latency < 3s；cost per task 可预测 |

### 二、Harness 层产出物 Spec

| Spec 编号 | Spec 名称 | 对应研究方向 | 核心内容 | 关键指标 / 验证标准 |
|-----------|-----------|-------------|----------|-------------------|
| H-01 | **Capability Registry Spec** | 方向四·智能体构建的服务框架 | 工具、数据接口、sub-agent、Scaffold 能力、模型能力的统一注册与发现：CapabilityCapsule 的 intent / contract / implementation / validation / lifecycle | 注册延迟 < 100ms；发现准确率 > 99%；版本兼容性可检测 |
| H-02 | **Tool Synthesis (Live Coding) Spec** | 方向二·可组装的智能体服务 | 当缺少能力时，LLM 当场生成代码工具 → sandbox 测试 → validation evidence → 注册为 capsule 的完整闭环（T8 → T3 结晶路径） | 生成工具成功率 > 80%；sandbox 验证通过率 > 95%；结晶后复用率 > 60% |
| H-03 | **Code Generation for Skills Stable** | 方向四·智能体构建的服务框架 | 面向交付物的代码生成：Read/Grep/Glob 检索 → Edit/Write 改写 → Bash 跑测试/lint → diff/patch → 迭代修复（对标 Claude Code + SWE-agent ACI） | 代码生成任务成功率 > 70%；测试通过率 > 90%；patch 可应用率 > 95% |
| H-04 | **OCR SaaS Spec** | 方向四·智能体构建的服务框架 | 微调 OCR 小模型作为 T2 定制模型工具：文档解析、表格提取、图像 OCR、layout parser，集成到 CapabilityCapsule 的 model_ref + served_on | OCR 准确率 > 98%（印刷体）/ > 90%（手写体）；latency < 2s/页 |
| H-05 | **Orchestration Eight Primitives Spec** | 方向四·智能体构建的服务框架 | O1–O8 编排原语的形式化定义与接口：tool 选择、shots 构造、output format、plan、live coding、reflection、model 选择、token 分发 | 每原语的决策延迟 < 500ms；plan 成功率 > 85%；token 预算遵守率 = 100% |
| H-06 | **Human-in-the-Loop (Elicitation) Spec** | 方向三·模型幻觉与决策可靠性 | 运行中向人追问/澄清/确认/审批/打分的结构化工具（T7）：schema 定义、超时兜底、审批留痕、闭环回 T3 正例 | 用户响应率 > 80%；审批留痕完整性 = 100%；正例闭环转化率 > 50% |
| H-07 | **Context Assembly & Token Budget Spec** | 方向一·Token 智能计量 | task state、memory、shots、tool docs、data summary、output format 的按需组装 + context 预算切分 + KV 预留与背压 | context 组装延迟 < 200ms；token 预算超限 = 0；KV 预留命中率 > 90% |
| H-08 | **Data Bridge (D1/D2/D3/D4) Spec** | 方向四·松散耦合的数据基盘 | Harness 与数据子系统的统一桥接：D1 查询、D2 semantic join、D3 governance memory 咨询、D4 时效校验 | 取数延迟 < 1s；semantic join 准确率 > 95%；时效校验覆盖率 = 100% |

### 三、Skill 层产出物 Spec

| Spec 编号 | Spec 名称 | 对应研究方向 | 核心内容 | 关键指标 / 验证标准 |
|-----------|-----------|-------------|----------|-------------------|
| X-01 | **Document Parsing Skill Spec** | 方向四·智能体构建的服务框架 | 文档解析 Skill：文件类型识别、抽取范围、引用格式、表格/图像策略、PDF/OCR/layout parser 协调、渐进式披露（L1/L2/L3） | 解析准确率 > 95%；表格保留率 > 90%；L1 注入 tokens < 100/skill |
| X-02 | **Code Generation Skill Spec** | 方向四·智能体构建的服务框架 | Code 生成 Skill：repo 边界、测试命令、风格约束、patch 格式、回滚策略、git 集成、verifier 闭环 | 代码生成任务成功率 > 70%；测试通过率 > 90%；patch 可应用率 > 95% |
| X-03 | **Git Management Skill Spec** | 方向四·智能体构建的服务框架 | Git 管理 Skill：branch 策略、diff/commit policy、PR rubric、冲突解决、review harness、audit trail | commit 合规率 = 100%；PR 评审通过率 > 80%；冲突自动解决率 > 60% |
| X-04 | **Data Report Generation Skill Spec** | 方向四·智能体构建的服务框架 | 数据报表生成 Skill：指标口径、时间范围、图表类型、交付格式（markdown/json/docx/xlsx）、数据源选择、刷新策略 | 报表准确率 > 99%；格式合规率 = 100%；数据新鲜度满足 SLA |
| X-05 | **Research Synthesis Skill Spec** | 方向四·智能体构建的服务框架 | 研究综述 Skill：source policy、检索范围、引用格式、novelty ledger、web search / PDF / note reading 协调 | 引用准确率 > 95%；novelty 检测率 > 80%；综述覆盖率 > 90% |
| X-06 | **System Skill (Memory Maintenance) Spec** | 方向三·模型幻觉与决策可靠性 | 系统 Skill：memory compaction、reflection、retrieval、writeback、GC、verification trigger 的触发条件与执行标准 | compaction 后信息保留率 > 95%；reflection 触发准确率 > 80%；GC 无泄漏 |
| X-07 | **Personalized Writing Skill Spec** | 方向四·智能体构建的服务框架 | 个性化写作 Skill：语气、结构偏好、术语表、禁用表达、style profile、domain memory、user preference 适配 | 风格匹配度 > 85%（人工评分）；术语一致性 = 100% |
| X-08 | **Skill Packaging & Distribution Spec** | 方向四·智能体构建的服务框架 | Skill 打包标准：SKILL.md 三级渐进披露（L1 元数据/L2 正文/L3 资源脚本）、目录结构、版本管理、兼容性声明 | 包体积 < 5MB；L1 加载时间 < 50ms；版本兼容性可检测 |

### 四、Data 层产出物 Spec

| Spec 编号 | Spec 名称 | 对应研究方向 | 核心内容 | 关键指标 / 验证标准 |
|-----------|-----------|-------------|----------|-------------------|
| D-01 | **5W1H+Which Fact Index Spec** | 方向四·松散耦合的数据基盘 | Tier 2 Index & Link 的 5W1H+Which 结构化事实定义：what/who/where/when/why/how/which 七维字段、时序约束、evidence_ref、supersedes 链 | fact 提取覆盖率 > 90%；时序查询准确率 > 95%；evidence_ref 可回指率 = 100% |
| D-02 | **Data Theme Spec** | 方向四·松散耦合的数据基盘 | Tier 3 Data Theme 的 5W1H 记录结构：theme_name/intent_type/output_spec、检索策略、关联逻辑、回退行为、复用/继承/演化/废弃机制 | Theme 匹配命中率 > 80%（同类 use case 重复 10 次后）；决策熵 ℋ 下降 > 50% |
| D-03 | **Off-Policy Indexing Cluster (OPIC) Spec** | 方向四·松散耦合的数据基盘 | 离线索引 agent 集群：observe → extract → link → write → 触发增量更新的完整 loop、专用 sub-agents（文档提取/schema 探查/关联推断/质量校验） | 索引延迟 < 5min（增量）；fact 质量评分 > 0.85；索引成本可控（每千页 < $0.5） |
| D-04 | **Lakehouse Integration Spec** | 方向四·松散耦合的数据基盘 | Raw Data 层与 Lakehouse 对接：Object Store（S3/OSS/GCS）、Table Format（Iceberg/Delta）、Catalog（Polaris/Hive）、Streaming Ingestion（Kafka/Flink） | 数据入湖延迟 < 1min；ACID 事务完整性 = 100%；Catalog 查询延迟 < 100ms |
| D-05 | **Semantic Summary Storage Spec** | 方向四·松散耦合的数据基盘 | D2 结构化摘要存储：SummaryEntry 的 claim/valid_from/valid_to/evidence_ref/supersedes/themes、结构化 DB 索引、MVCC 快照读、分级降冷（热层→冷层→归档） | 时点查询延迟 < 200ms；unverifiable 率 < 1%；降冷后 evidence_ref 保留率 = 100% |
| D-06 | **Data Usage Skill (D3) Spec** | 方向四·松散耦合的数据基盘 | 数据使用 Skill：usecase_id/intent_pattern/preferred_sources/semantic_join_plan/access_plan/evidence/governance 的完整定义与沉淀 | 数据源选择准确率 > 90%；join 成功率 > 85%；governance 合规率 = 100% |
| D-07 | **Data Lifetime & Freshness Spec** | 方向四·松散耦合的数据基盘 | D4 数据生命周期：freshness 阈值、业务口径版本、validity 窗口、NFR budget、retention policy、自动失效与刷新触发 | 时效告警延迟 < 1min；口径版本一致性 = 100%；retention 合规率 = 100% |
| D-08 | **Workspace (Ω) Artifact Spec** | 方向四·松散耦合的数据基盘 | Agent 工作区：RunTrace、IntermediateRelation、LLM Wiki、ArtifactManifest、ReflectionRecord 的最小对象定义与持久化 | artifact 完整性 = 100%；trace 可回放率 = 100%；wiki 查询延迟 < 100ms |

### 五、跨层集成与治理 Spec

| Spec 编号 | Spec 名称 | 对应研究方向 | 核心内容 | 关键指标 / 验证标准 |
|-----------|-----------|-------------|----------|-------------------|
| G-01 | **Agentic Runtime Integration Spec** | 方向四·智能体构建的服务框架 | 三层栈 ⟨Scaffold, Harness, Skill⟩ + 数据子系统 ℳ = ⟨Raw, Index, Theme⟩ 的集成接口：ExecutionSpec ↔ CapabilityCapsule ↔ SkillSpec ↔ DataUsageSkill 的调用链 | 端到端任务成功率 > 80%；跨层调用延迟 < 3s；错误传播可追溯 |
| G-02 | **Audit & Replay Spec** | 方向三·模型幻觉与决策可靠性 | 可审计执行：run trace、tool evidence、branch provenance、decision log、replayable evidence 的完整记录与回放 | trace 覆盖率 = 100%；replay 成功率 > 95%；audit log 不可篡改 |
| G-03 | **Policy Gate & Data Boundary Spec** | 方向三·安全等级适配体系 | 权限检查、auth isolation、capability attenuation、data boundary 的统一下发与执行：permission check → scope validation → network policy → data boundary enforcement | 越权访问阻断率 = 100%；policy 下发延迟 < 1s；data boundary 泄漏 = 0 |
| G-04 | **Multi-Tenant Resource Quota Spec** | 方向二·可扩展与可管理的集成 | 多租户资源配额：CPU/GPU/Token/Storage/Network 的租户级隔离、burst 控制、优先级抢占、公平调度 | 配额遵守率 = 100%；burst 响应 < 500ms；优先级抢占无饥饿 |
| G-05 | **Benchmark Automation Harness Spec** | 方向一·五维度 Benchmark 分类 | 五维度 Benchmark 的自动化执行框架：编程/生成报告/运维操作/专业操作/创新操作的分级评估、阈值达标/效率指标/非功能需求评分的自动采集 | Benchmark 执行自动化率 = 100%；评分一致性（人工 vs 自动）> 90% |

---

> **使用说明**：
> 1. 每个 Spec 可独立作为研究课题或工程原型立项，建议按 **S → H → X → D → G** 的依赖顺序推进。
> 2. Spec 编号中的字母前缀表示所属层级（S=Scaffold, H=Harness, X=Skill, D=Data, G=Governance/Integration），数字为层内序号。
> 3. "关键指标 / 验证标准"列提供了可量化的验收条件，可直接用于设计实验或撰写测试计划。
> 4. 本清单与 §4.1–§4.6 的详细 YAML 定义、§5.2 的编排八原语、以及 08-数据层修订-三阶记忆子架构 形成完整对照，建议联合阅读。


