# 13 — 数据子系统落地：Data Wiki / Theme Wiki / IR 中间关系层

> **来源**: 2026-07-17 研究讨论。承 [06-数据平面四组成架构](06-%E6%95%B0%E6%8D%AE%E5%B9%B3%E9%9D%A2%E5%9B%9B%E7%BB%84%E6%88%90%E6%9E%B6%E6%9E%84.md)（$D_1$–$D_4$ 形式化）与 [12-Skill作为可训练激活层-双子目标Reward](12-Skill%E4%BD%9C%E4%B8%BA%E5%8F%AF%E8%AE%AD%E7%BB%83%E6%BF%80%E6%B4%BB%E5%B1%82-%E5%8F%8C%E5%AD%90%E7%9B%AE%E6%A0%87Reward.md)（σ_out 结果子域、双子目标 reward）。
> **类型**: 论文核心理论扩展 —— 把 06 号的 $D_2$（语义摘要平面）与 $D_3$（治理 memory）落地为**两个具名 wiki + 一个中间关系层**，并把它们与 12 号的 σ_out 结果子域缝合成完整的"数据→产出"闭环。
> **状态**: 草稿 v0.1
> **定位**: 06 号回答"数据子系统四组成是什么"（偏形式化）；本文回答"**这四组成在工程上落成什么系统、彼此怎么松耦合对接**"。核心手段：把 $D_2$ 具名为 **Data Wiki**（数据是什么），把 $D_3$ 的"复用产出物"半分离出一个新的 **Theme Wiki**（产出是什么），中间插一层 **IR（Intermediate Relation）** 做 5W+1H 描述 + semantic join，是 06 号"$D_2$/$D_3$ 松耦合"论断的具体实现。

---

## 0. 一句话总纲

> 数据侧要回答"这数据是什么"，产出侧要回答"这份产出该长什么样"，中间要有一层回答"这次任务该用哪份数据配哪种产出"——这三件事**不能揉在一起**，否则数据语义和产出格式会互相污染、无法独立复用。**Data Wiki**（承 $D_2$）由 agent 读取数据源、产出自然语言总结+格式+关键词+关联关系（外键）；复杂报表则**人机协同**构建规范（来源/频率/维护/时效性），并用人常备报表做**还原式 reflection** 校验总结质量。**Theme Wiki**（承 $D_3$ 的产出侧）收录被 skill 验证过的可复用输出物（报表/图表/PPT/分析报告/数据模型程序……），来自 σ_out 各结果子域固化后的产物。两个 wiki 通过一层**中间关系 IR**（≈ ETL 的 data view，但是 agent-native、松耦合）对接：给定一个 theme，IR 找到它对应的数据源集合，除 semantic join 外还必须显式携带 **5W+1H**（When 时效性、Where 使用范围、Who 数据拥有者及授权、What 数据语义、Why 数据集成逻辑即 semantic join 的理由、How 物理访问方式）。三者合起来把 $D_2$（数据语义）与 $D_3$（数据使用）之间原本隐式的耦合，改造成一个**显式、可审计、可复用的中间层**。

---

## 1. 三组件与已有记号的映射

| 新组件 | 承接的旧记号 | 差异/新增点 |
|---|---|---|
| **Data Wiki** | $D_2$（off-policy 语义总结平面 $\Sigma$） | 06 号只定义了 $\Sigma=\langle\text{schema}^*,\text{content-profile},\text{latent-fields},\text{rels}\rangle$ 四段；本文把它**具名化为一个可浏览、可增量维护的 wiki**，并新增第五段——**复杂报表的人机协同构建 + reflection 校验**（06 号未覆盖，是本文的主要 delta） |
| **Theme Wiki** | $D_3$（数据治理 memory）的**产出侧分身** | 06 号的 $D_3$ 讲"如何用数据最好"（data-usage skill）；本文把"用数据产出了什么、且被验证复用"这部分**独立出一个新 wiki**——它的内容来自 [12-Skill作为可训练激活层-双子目标Reward](12-Skill%E4%BD%9C%E4%B8%BA%E5%8F%AF%E8%AE%AD%E7%BB%83%E6%BF%80%E6%B4%BB%E5%B1%82-%E5%8F%8C%E5%AD%90%E7%9B%AE%E6%A0%87Reward.md) §3.1 的 **σ_out 结果子域**（报表/图表/PPT/分析报告/数据模型程序……各是一类子域），经双子目标 Reward 验证收敛后才登记 |
| **IR（Intermediate Relation）** | 06 号 §3.2 的 $H$ 契约映射 $H:\mathcal{I}\xrightarrow{\text{consult }D_3,D_4}\text{plan}\xrightarrow{D_1,D_2}\mathcal{E}$ 中"plan"这一步 | 06 号只说"consult $D_3,D_4$ 生成 plan"，未定义 plan 的内部结构；本文把这个 plan **实体化**为 IR：一个 theme → 数据源集合的映射，**必须显式携带 5W+1H**，是 06 号"$D_2$/$D_3$ 松耦合"的具体机制 |

> **为什么要拆成两个 wiki 而不是一个**：Data Wiki 回答"数据本身是什么"，与任何具体产出无关，理应能被**任意** theme 复用；Theme Wiki 回答"某类产出该长什么样"，与具体数据源无关（同一份 PPT 模板可能配不同季度的数据）。**把二者放进同一个 wiki 会让数据语义随产出需求漂移、或让产出格式绑死在某个数据源上**——这正是 06 号"$D_2$ 与 $D_3$ 平面分离"论断在产出侧的延伸，二者的正交性靠 IR 这层显式关系保持。

---

## 2. Data Wiki：$D_2$ 的落地实现

### 2.1 常规数据源：agent 全自动构建

对结构较规整、可编程访问的数据源（数据库表、API、日志），agent（$D_2$ 的独立 off-policy loop $\mathcal{L}_2$）自动执行：

$$\text{src} \xrightarrow{\ \text{read}\ } \langle\ \underbrace{\text{summary}_{\text{NL}}}_{\text{自然语言总结}},\ \underbrace{\sigma}_{\text{格式}},\ \underbrace{\kappa}_{\text{关键词}},\ \underbrace{\text{FK}}_{\text{关联关系/外键}}\ \rangle = \Sigma(\text{src})$$

这是对 06 号 $\Sigma$ 四段（schema*/content-profile/latent-fields/rels）的**具体展开**：`summary_NL` ≈ content-profile 的自然语言化，`σ` ≈ schema*，`κ` 是新增的检索锚点（供 semantic join 命中），`FK` ≈ rels 但显式化为"外键"这个工程概念——即跨数据源的**领域知识图谱式关联**（06 号 §1 第 4 类信息）。

### 2.2 复杂报表：人机协同构建 + 还原式 reflection

复杂报表（多 sheet、隐藏公式、口径随部门/时间漂移的 Excel/BI 报表）**不适合 agent 单方面产出格式说明**——06 号 §1 已指出"人定义会截断，但 agent 单方面猜测又会失真"。解法是**人机协同**：

1. **人机协同构建规范**：与人一起明确该报表的**来源**（哪个系统/谁导出）、**频率**（日/周/月）、**维护**（谁负责、怎么改）、**时效性**（口径何时变过），这正是 06 号 $D_4$（lifetime 体系）在单份报表粒度上的具体落地，而不是重新发明；
2. **记录人常用报表作为参照物**：把人在日常工作中**实际使用**的报表（而非任意样例）记为 ground-truth 参照；
3. **还原式 reflection**：agent 尝试**部分还原**参照报表中的表格（给定总结反推能否重建原表结构/数值),用还原成功率作为 Data Wiki 总结质量的验证信号。

> **与 [12-Skill作为可训练激活层-双子目标Reward](12-Skill%E4%BD%9C%E4%B8%BA%E5%8F%AF%E8%AE%AD%E7%BB%83%E6%BF%80%E6%B4%BB%E5%B1%82-%E5%8F%8C%E5%AD%90%E7%9B%AE%E6%A0%87Reward.md) 的结构对应**：还原式 reflection 本质是给 Data Wiki 的总结过程装了一个**局部 r_proc**——不是验证"总结格式对不对"（那是 r_out 的事），而是验证"总结有没有正确捕捉到能重建原表的信息"，即**过程/内容正确性**。这把 12 号的双子目标框架从"产出验证"复用到了"数据理解验证"，是 Data Wiki 与 Skill 训练机制的一个隐藏同构点。

### 2.3 命题 P16（拟）· 还原式 reflection 是摘要充分性的可操作判据

> 06 号 P8（语义摘要充分性）主张 $\Sigma$ 是"lossy-but-sufficient"的充分统计量，但**没给出可操作的验证手段**。本文给出一个具体判据：**若 agent 能从 $\Sigma(\text{src})$ 出发、结合参照报表的结构描述，还原出参照报表的关键数值/结构，则 $\Sigma$ 对该 use case 是充分的**；还原失败的字段即是 $\Sigma$ 的信息损失点，可直接定位需要补充总结的方向。

**可证伪**：对 $N$ 份人常用报表，比较 (a) 用 $\Sigma$ + reflection 还原的准确率，(b) 直接读原始报表的准确率。P16 预期 (a) 随 $\Sigma$ 迭代逐步逼近 (b)；若长期有固定差距 → $\Sigma$ 的 schema 设计有系统性缺口。

---

## 3. Theme Wiki：$D_3$ 产出侧的具体登记表

### 3.1 内容来源：σ_out 各结果子域

Theme Wiki 收录的不是"数据"，而是**验证过的输出物**——直接对应 [12-Skill作为可训练激活层-双子目标Reward](12-Skill%E4%BD%9C%E4%B8%BA%E5%8F%AF%E8%AE%AD%E7%BB%83%E6%BF%80%E6%B4%BB%E5%B1%82-%E5%8F%8C%E5%AD%90%E7%9B%AE%E6%A0%87Reward.md) §3.1 里 σ_out 沿输出格式拆出的各子域，只是这里的子域粒度是"产出**类型**"而不是"字段类型"：

$$\sigma^{out}_{\text{theme}} \in \{\text{报表},\ \text{图表},\ \text{PPT},\ \text{数据分析报告},\ \text{数据模型程序},\ \dots\}$$

每一类产出经 skill 的双子目标 Reward（$r_{\text{out}}$ 对齐该产出类型的格式规范、$r_{\text{proc}}$ 校验生成过程用对了工具/数据）验证收敛后，才作为**可复用模板/组件**登记进 Theme Wiki——这正是 12 号 §4.2「收敛后变化不大的子目标可 code 化固化」在产出侧的实例：一份验证稳定的 PPT 模板/报表结构，本身就是一个可被复制的 skill-as-code 产物。

### 3.2 与 Data Wiki 的对称性

| | Data Wiki | Theme Wiki |
|---|---|---|
| 回答的问题 | 这数据是什么 | 这类产出该长什么样 |
| 承接记号 | $D_2$ | $D_3$ 产出侧 |
| 验证机制 | 还原式 reflection（§2.3 P16） | 双子目标 Reward（12 号 P15） |
| 复用粒度 | 数据源级（一个 src 一条 $\Sigma$ 记录） | 产出类型级（一个 theme 的 σ_out 子域一条模板） |
| 独立性 | 与任何具体产出无关 | 与任何具体数据源无关 |

---

## 4. IR（Intermediate Relation）：两个 wiki 之间的中间关系层

### 4.1 定位：不是 ETL 的 data view，是 agent-native 的松耦合契约

传统 ETL 里，一个 report/theme 对应的数据源关系是**写死在 pipeline 代码里**的（改数据源要改 ETL job）。IR 层的设计目标恰恰是**反过来**：给定一个 theme，IR 是一份**显式、可审计、可独立更新**的关系记录，声明"这个 theme 的数据源集合是什么、为什么是这些、怎么访问"——数据源变了只改 IR 记录，不改 theme 的产出逻辑；产出格式变了只改 Theme Wiki 条目，不改 IR。这就是题目里"**松散耦合的过程**"的具体机制。

### 4.2 形式化

$$\text{IR}: \text{theme} \mapsto \langle\ \underbrace{\{\Sigma(\text{src}_i)\}_{i}}_{\text{semantic join 命中集}},\ \underbrace{\text{5W1H}}_{\text{显式关系描述}}\ \rangle$$

**5W+1H 六要素**（本文核心新增，是对 06 号 $D_2/D_3/D_4$ 三者信息的**重组**，而非新增信息类别——见 §4.3 对照表）：

| 要素 | 内容 | 对应 06 号已有记号 |
|---|---|---|
| **When**（时效性） | 该数据在这个 theme 下的有效期、更新频率 | $D_4$ lifetime 体系（时新性） |
| **Where**（使用范围） | 内网 / 外网 / 互联网数据——访问域边界 | $D_4$ NFR 里隐含、本文显式化为独立维度 |
| **Who**（数据拥有者及授权） | 谁拥有这份数据、当前 agent/theme 是否被授权 | 06 号 §1 第 5 类 NFR（安全/授权范围） |
| **What**（数据语义） | 这份数据本身的字段/业务口径含义 | $D_2$ 的 $\Sigma$（summary_NL / σ / κ，见 §2.1） |
| **Why**（数据集成逻辑） | 为什么这些数据源该被联到一起——即 semantic join 背后的理由 | 06 号 §1 第 4 类跨数据语义联系（领域知识图谱式关联）+ $D_3$ 的"哪些数据可被其它数据补充" |
| **How**（物理访问方式） | 数据库 / lakehouse / JSON / Harness 里的某个工具——物理协议 | $D_1$ 的 $q=\langle\text{src},\text{scope},\text{time},\text{proj}\rangle$ 里隐含的访问方式，本文显式化为独立维度 |

> **关键澄清**：5W+1H 不是绕开 semantic join 的另一条路，而是**semantic join 结果之上必须附带的元信息**——semantic join 解决"哪些 $\Sigma$ 该被检索出来"（What/命中集本身），5W+1H 解决"这次命中**在当下 theme 里是否可用、可信、怎么落地访问**"。少了 5W+1H，semantic join 命中的数据可能过期（少 When）、越权（少 Who）、或者取不到（少 How）。

### 4.3 IR 与 $H$ 契约映射的关系（回填 06 号 §3.2）

06 号给出 $H:\mathcal{I}\xrightarrow{\text{consult }D_3,D_4}\text{plan}\xrightarrow{D_1,D_2}\mathcal{E}$，本文把中间的"plan"具体化：

$$H:\ \mathcal{I}\ \xrightarrow{\ \text{IR}(\text{theme})\ }\ \langle\{\Sigma\}, \text{5W1H}\rangle\ \xrightarrow{\ D_1\ }\ \mathcal{E}$$

即：意图 $\mathcal{I}$ 先确定 theme（来自 Theme Wiki 匹配到的产出类型），theme 经 IR 查到数据源命中集 + 5W1H，H 据此校验（时效/授权/访问方式是否满足）后再调 $D_1$ 取实际数据、组装成可执行单元 $\mathcal{E}$。**IR 因此是 $D_2$（Data Wiki）与 $D_3$ 产出侧（Theme Wiki）之间唯一的显式耦合点**，其余部分保持正交独立——两个 wiki 各自可以独立扩充、独立验证、独立版本演进，互不干扰。

---

## 5. 命题扩展（P17 拟）

### 命题 P17（IR 松耦合 / IR Decoupling）

> **数据源集合的变更（Data Wiki 侧）与产出格式的变更（Theme Wiki 侧）互不传播，只要 IR 记录同步更新。** 形式化：设 $\text{IR}_t(\text{theme})$ 为 $t$ 时刻的中间关系记录，
> $$\text{src 变更} \Rightarrow \Delta\Sigma,\quad \text{theme 产出格式变更} \Rightarrow \Delta\sigma^{out}_{\text{theme}}$$
> 若两者独立变更后仅需更新 $\text{IR}_{t+1}(\text{theme})$ 而不需同时改 Data Wiki 与 Theme Wiki 的内部结构，则 P17 成立。

**可证伪**：模拟场景——(a) 只换数据源（如 ERP 系统迁移）、(b) 只换产出格式（如报表模板换季）。测两种变更各自波及的改动范围。P17 预期改动只落在 IR 记录本身；若改动扩散进 Data Wiki 的 $\Sigma$ schema 或 Theme Wiki 的模板结构，则耦合并未真正解开。

> **与 [01-C5-双扩展解耦形式化与命题](01-C5-%E5%8F%8C%E6%89%A9%E5%B1%95%E8%A7%A3%E8%80%A6%E5%BD%A2%E5%BC%8F%E5%8C%96%E4%B8%8E%E5%91%BD%E9%A2%98.md) P2（契约充分性）的对齐**：P2 说良定义契约 $H$ 使 $S$ 与 $X$ 无直接依赖；P17 是 P2 在**数据/产出双 wiki 场景下的实例**——IR 就是这里的"契约层"，Data Wiki ≈ $X$（物理侧资源），Theme Wiki ≈ $S$（逻辑侧规格），IR 承担 $H$ 的翻译职能。

---

## 6. 对主线 / novelty 的影响

1. **N10（拟）· Data Wiki 的人机协同 + 还原式 reflection**：给 06 号 $D_2$ 补上"复杂报表不能靠 agent 单方面猜"的现实约束,并给出一个可操作的验证手段（P16），是 P8（摘要充分性）从"理论主张"到"可执行判据"的落地。
2. **N11（拟）· Theme Wiki 作为 σ_out 结果子域的复用登记表**：把 12 号的 skill 训练产出（验证收敛的结果子域）与数据侧的 $D_3$ 治理 memory 首次在**产出侧**打通，回应"复杂 agent 的产出可由分结果子域的 benchmark 分别指导"这一论断的具体存储形态。
3. **N12（拟）· IR 中间关系层 + 5W1H**：把 06 号 $H$ 契约映射里含糊的"plan"步骤**实体化**为可审计的中间关系记录，5W1H 六要素是对 06 号已有信息（$D_1$ 访问方式、$D_2$ 语义、$D_3$ 集成逻辑、$D_4$ lifetime+NFR）的**首次统一重组**，而非新增信息源——novelty 在于"重组为显式记录"这个工程动作本身，使 Data Wiki 与 Theme Wiki 的正交性可审计、可验证（P17）。

---

## 7. 文献支撑与划界（防 reviewer "已有人做过"）

| 主张 | 支撑/对标 | 我们的 delta |
|---|---|---|
| off-policy 语义总结（$D_2$） | 06 号已有 N1，对标 CoeusBI/Pneuma/Octopus/EasyTUS | 本文新增"复杂报表人机协同 + 还原式 reflection"，是这些工作都没做的**验证手段** |
| 数据使用即 skill（$D_3$） | 06 号已有 N2 | 本文把"产出物"这一半从 $D_3$ 独立出 Theme Wiki，与数据侧显式解耦 |
| ETL data view / 物化视图 | 经典数据仓库工程 | 传统 view 是**写死的 pipeline**；IR 是**可独立审计更新的关系记录**，且强制携带 5W1H 而非只有 join 逻辑 |
| Semantic join | 06 号 $\bowtie_\text{sem}$ | IR 把 semantic join 的命中结果**包装**进一个更完整的 5W1H 记录，而非替代它 |

> **必须诚实标注的边界**：本文没有提出新的检索算法或新的数据集成技术，science delta 是**系统层面的关系重组与显式化**——把原本隐含在 06 号形式化里的"$D_2$/$D_3$ 如何对接"这一步，抽出来做成一个独立、可验证、可审计的中间层。这是工程架构贡献，需与"提出新算法"的论文划清。

---

## 8. 待验证 / 风险点

- [ ] **还原式 reflection 的成本**：对每份复杂报表都做还原测试，calls 数可能不小，需要评估是否只需抽样字段还原而非全表还原。
- [ ] **5W1H 六要素的完整性**：是否存在第七个必要维度（如"数据质量/置信度"）？需要在实际 theme 落地时观察是否有信息缺口。
- [ ] **IR 记录本身的维护成本**：谁负责在数据源或产出格式变更时同步更新 IR？可能需要一个专门的 IR 维护 sub-agent（呼应 [03-Harness-System-SubAgents清单](03-Harness-System-SubAgents%E6%B8%85%E5%8D%95.md) 的 $M$ 维护子系统）。
- [ ] **P17 的证伪场景设计**：需要构造真实的"只换数据源"和"只换产出格式"两类变更场景，工程量不小。
- [ ] **Theme Wiki 与 D3 的边界**：Theme Wiki 存"产出物模板"，$D_3$ 存"数据使用策略"，二者都可能涉及"某 theme 该怎么做"的经验——需要明确谁存"怎么用数据"、谁存"怎么呈现结果"，避免重复存储（呼应 06 号已有的 $D_3$/$\Omega$ 边界风险）。

---

## 9. 下一步

1. 把 §2.1 Data Wiki 的四段 $\Sigma$ 展开（summary_NL/σ/κ/FK）与 06 号原始 $\Sigma$ 四段（schema*/content-profile/latent-fields/rels）做逐项对照表，确认是展开而非冲突。
2. 把 IR 的 5W1H schema 落成一个最小可执行的记录格式（类比 06 号 §9 建议的 $\Sigma$ schema），供阶段 2 实验使用。
3. 设计还原式 reflection 的具体评测协议（抽样字段还原 vs 全表还原的成本/信度权衡）。
4. 把 P16/P17 回填进 [07-创新点总结](07-%E5%88%9B%E6%96%B0%E7%82%B9%E6%80%BB%E7%BB%93.md) 命题总表与 novelty 全表（N10–N12）。
5. 把本文 §4.3 的 $H$ 契约映射回填进 [06-数据平面四组成架构](06-%E6%95%B0%E6%8D%AE%E5%B9%B3%E9%9D%A2%E5%9B%9B%E7%BB%84%E6%88%90%E6%9E%B6%E6%9E%84.md) §3.2。

---

相关：[06-数据平面四组成架构](06-%E6%95%B0%E6%8D%AE%E5%B9%B3%E9%9D%A2%E5%9B%9B%E7%BB%84%E6%88%90%E6%9E%B6%E6%9E%84.md) · [12-Skill作为可训练激活层-双子目标Reward](12-Skill%E4%BD%9C%E4%B8%BA%E5%8F%AF%E8%AE%AD%E7%BB%83%E6%BF%80%E6%B4%BB%E5%B1%82-%E5%8F%8C%E5%AD%90%E7%9B%AE%E6%A0%87Reward.md) · [10-Skill-as-Code与确定性固化](10-Skill-as-Code%E4%B8%8E%E7%A1%AE%E5%AE%9A%E6%80%A7%E5%9B%BA%E5%8C%96.md) · [01-C5-双扩展解耦形式化与命题](01-C5-%E5%8F%8C%E6%89%A9%E5%B1%95%E8%A7%A3%E8%80%A6%E5%BD%A2%E5%BC%8F%E5%8C%96%E4%B8%8E%E5%91%BD%E9%A2%98.md) · [03-Harness-System-SubAgents清单](03-Harness-System-SubAgents%E6%B8%85%E5%8D%95.md) · [07-创新点总结](07-%E5%88%9B%E6%96%B0%E7%82%B9%E6%80%BB%E7%BB%93.md)
