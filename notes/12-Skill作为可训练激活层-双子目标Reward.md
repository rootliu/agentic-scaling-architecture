# 12 — Skill 作为可训练激活层：双子目标 Reward 与 skill 的强化学习式蒸馏

> **来源**: 2026-07-14 研究讨论，读 [精读 - 2605.23904](精读%20-%202605.23904.md)（SkillOpt: Executive Strategy for Self-Evolving Agent Skills, Microsoft+SJTU, 2026-05）后的融合输入。承 [10-Skill-as-Code与确定性固化](10-Skill-as-Code%E4%B8%8E%E7%A1%AE%E5%AE%9A%E6%80%A7%E5%9B%BA%E5%8C%96.md)（skill 稳定后固化为 code）与 [08-模型原生计算架构-体系结构视角](08-%E6%A8%A1%E5%9E%8B%E5%8E%9F%E7%94%9F%E8%AE%A1%E7%AE%97%E6%9E%B6%E6%9E%84-%E4%BD%93%E7%B3%BB%E7%BB%93%E6%9E%84%E8%A7%86%E8%A7%92.md) §2（N0 概率控制面）。
> **类型**: 论文核心理论扩展 —— 给「skill 从哪来、怎么迭代出来」补上训练机制；10 号回答"稳定后固化为 code"，本文回答"**固化之前，skill 是怎么被训练出来的**"。
> **状态**: 草稿 v0.1
> **定位**: SkillOpt 证明了"skill = frozen agent 的外部可训练状态"这一范式，并把 DL 优化器纪律（learning rate / validation gate / meta update）搬进文本空间。但它用**单一 scalar reward** $r(s)\in[0,1]$ 训练——这正是它自己在 Limitations 承认的最大约束（"most applicable when the task has automatic verifiers … open-ended domains may require stronger evaluation"）。本文的 delta：**把 scalar reward 分解为「结果子域 × 过程子目标」双维 reward**，解决自然语言 goal 的打分粒度难题，并把它接入我们的 ⟨S,H,X⟩ / N0 架构。

---

## 0. 一句话总纲

> 对复杂的、用户直接使用的 agent，可以把它看成**一个权重固定（frozen）的大模型的、前端可编辑的"激活层"**——这层就是 skill：⟨goal，输出格式要求，工具集与数据源列表，调用与反思检查标准，正例与反例⟩。**它逻辑上属于大模型可被训练的部分**，只是训练发生在文本空间而非权重空间。训练 agent = 训练这个 skill = 一个针对 goal 给 reward 的**强化学习式迭代**。核心难点：goal 用自然语言描述，直接给 reward 在**粒度**上困难、需人工判断强制收敛。本文的解法：把 reward 拆成**两个子目标维度**——**(1) 结果子目标**（对齐格式化输出的各子域，如数字/内容总结，各子域配独立标注 benchmark 打分）；**(2) 过程子目标**（是否调用了正确工具/数据、是否做了正确逻辑分析、是否达到进入下一步的标准）。每个 mini-batch 同时算两维子目标 reward 并据此调整 skill。**由此 skill 必须是模型总结的、不能人工生成**；随梯度收敛、变化不大的子目标可被 code 化固化（接 [10-Skill-as-Code与确定性固化](10-Skill-as-Code%E4%B8%8E%E7%A1%AE%E5%AE%9A%E6%80%A7%E5%9B%BA%E5%8C%96.md)）。复杂 agent 的调教因此可**由不同子 agent 分头调教组成，或由分结果子域的 benchmark 分别指导**。

---

## 1. 定位一致性：SkillOpt 的范式 ↔ 我们的架构

SkillOpt 的核心 thesis 与本架构**天然同构**，先把两套语言对齐（这是 related-work 对齐，非本文 novelty）：

| SkillOpt 语言 | 本架构语言（⟨S,H,X⟩ / N0） | 备注 |
|---|---|---|
| skill = frozen agent 的 external trainable state | **skill = frozen 大模型的可编辑激活层**（本文 §0 定位） | 用户输入的核心比喻，与 SkillOpt Abstract "external state of a frozen agent" 逐字对应 |
| skill document = parameter | skill $s=\langle\text{desc},\sigma^{in},\sigma^{out},c\rangle$（[01-C5](01-C5-%E5%8F%8C%E6%89%A9%E5%B1%95%E8%A7%A3%E8%80%A6%E5%BD%A2%E5%BC%8F%E5%8C%96%E4%B8%8E%E5%91%BD%E9%A2%98.md)） | S 层规格就是"参数" |
| optimizer model（独立 frontier 模型） | Harness 维护子系统 $M$ 的一项能力（[03-Harness](03-Harness-System-SubAgents%E6%B8%85%E5%8D%95.md) E） | "谁来训 skill" = Harness 职责 |
| trajectory → bounded edit（DL 优化器纪律） | H 契约面上的 skill 迭代；learning rate=编辑预算、gate=留出验证 | 本架构 P8/P9 治理记忆收敛的具体算法 |
| best_skill.md（零推理成本部署） | S 层被推进 X 的 context（[01-C5](01-C5-%E5%8F%8C%E6%89%A9%E5%B1%95%E8%A7%A3%E8%80%A6%E5%BD%A2%E5%BC%8F%E5%8C%96%E4%B8%8E%E5%91%BD%E9%A2%98.md) 逻辑扩展 𝒯↑） | 部署即"激活层写入 context" |

> **一句话**：SkillOpt 给了「skill 可训练」这条主张一个**可运行的优化器骨架**；本架构此前只有 P8/P9（治理记忆随沉淀降熵）的**定性**主张。二者对接后，P8/P9 获得了 SkillOpt 式的**可操作训练回路**。但 SkillOpt 的 reward 是 scalar——这是它的骨架里最薄的一环，也是本文要补的地方（§3）。

---

## 2. 激活层的六要素：skill 的完整可训练状态

把 §0 的"可编辑激活层"展开为可训练的六要素（对齐 SkillOpt 对 skill 内容的描述"procedures, domain heuristics, tool policies, output constraints, failure modes"，并补齐我们 [研究原则-外部记忆即Skill基础] 的九件套）：

| 激活层要素 | 形式化符号 | SkillOpt 对应 | 是否随训练变 |
|---|---|---|---|
| **目标 goal** | $g$（自然语言） | domain/task 描述 | 固定（训练目标） |
| **输出格式要求** | $\sigma^{out}$（结构化子域） | output constraints | 缓变，→ 结果子目标锚点（§3.1） |
| **工具集列表** | $\tau(s)$ | tool policies | 缓变，闭合后可 code 化（[10-Skill-as-Code与确定性固化](10-Skill-as-Code%E4%B8%8E%E7%A1%AE%E5%AE%9A%E6%80%A7%E5%9B%BA%E5%8C%96.md)） |
| **数据源列表** | $\mathcal{D}(s)$ | （SkillOpt 未显式，我们补） | 缓变，接数据面 D₃（[06-数据平面四组成架构](06-%E6%95%B0%E6%8D%AE%E5%B9%B3%E9%9D%A2%E5%9B%9B%E7%BB%84%E6%88%90%E6%9E%B6%E6%9E%84.md)） |
| **调用与反思检查标准** | $c$（判据/验证规则） | verifier feedback / failure modes | **主训练对象**，→ 过程子目标（§3.2） |
| **正例 / 反例** | $E^+, E^-$ | success/failure minibatch | 训练产物：成功保留、失败纠正 |

> **关键洞察（与 SkillOpt 的 success/failure minibatch 对偶）**：SkillOpt 已经在做"失败 minibatch 提纠正规则、成功 minibatch 保留有效行为"——这**正是我们的 $E^-$（反例，给剪枝先验）/ $E^+$（正例，给最优锚点）二分**，也印证 [研究原则-Zotero批注提炼] 的"正例求最优、负例求多样"。SkillOpt 把它落成了 minibatch 反思机制。**本文的增量是给这个反思一个"沿两维子目标"的结构，而不是让优化器凭一个 scalar 自由发挥。**

---

## 3. 核心 delta：双子目标 Reward —— 破解自然语言 goal 的打分粒度难题

### 3.0 问题：scalar reward 对自然语言 goal 粒度不够

SkillOpt 的 forward pass 产出 $(τ(s), r(s))$，$r(s)\in[0,1]$ 是**一个标量**（来自 benchmark 的 exact-match / hard score）。它 Limitations 明写：这只在"有自动 verifier / exact-match / 可执行检查"时最有效；**开放域 goal（成功是主观的、多维的、判断代价高）需要更强的人工或模型评估**。

根因：**goal 是自然语言，reward 是标量，中间隔着一次有损投影**。一个标量既无法告诉优化器"错在结果还是错在过程"，也无法在多子域任务上分别归因 → 只能靠人工判断强制收敛。

### 3.1 结果子目标（Outcome Subgoals）：按 $\sigma^{out}$ 子域分别打分

把"结果对不对"从一个标量拆成**沿输出格式 $\sigma^{out}$ 的各子域**分别打分：

- $\sigma^{out}$ 通常是结构化的（如"数字 + 内容总结 + 引用列表"）。**每个子域配一套独立的标注 benchmark**：数字子域 → 数值精确匹配 / 容差；内容总结子域 → 摘要质量 benchmark（ROUGE / LLM-judge rubric）；引用子域 → 检索命中率。
- 结果子目标 reward = 各子域 reward 的加权：
$$r_{\text{out}}(s) = \sum_{d\in\text{子域}(\sigma^{out})} w_d \cdot r_d\big(\text{output}_d,\; \text{benchmark}_d\big)$$
- **把过程输出与格式化子域结果做比较**即得每个 $r_d$。这样优化器拿到的不再是"0.463"，而是"数字子域 0.9 / 总结子域 0.4 / 引用子域 0.7"——**归因立刻变清晰**，reflection minibatch 能定位"错在总结子域"。

### 3.2 过程子目标（Process Subgoals）：达到结果的过程是否正确

只看结果无法回答"蒙对的"和"对的"区别，也无法在长程任务里及早纠偏。过程子目标评估**达到结果子目标的过程**：

- **是否调用了正确的工具 / 数据源**：$\mathbb{1}[\tau_{\text{used}} \subseteq \tau_{\text{correct}}]$、数据源是否命中 $\mathcal{D}(s)$；
- **是否进行了正确的逻辑分析**：中间推理步骤是否满足 $c$ 里的判据；
- **是否达到进入下一步的标准**：每个 step 的 gate 是否通过（接 [09-并行度与局部性协同设计](09-%E5%B9%B6%E8%A1%8C%E5%BA%A6%E4%B8%8E%E5%B1%80%E9%83%A8%E6%80%A7%E5%8D%8F%E5%90%8C%E8%AE%BE%E8%AE%A1.md) 的 step-level 局部性）。

$$r_{\text{proc}}(s) = \frac{1}{|\text{steps}|}\sum_{k}\mathbb{1}[\text{step}_k \text{ 满足工具/数据/逻辑/进阶判据}]$$

> **过程子目标的作用是加快 skill 迭代方向的一致性**：结果 reward 是稀疏的、滞后的（长程任务末端才出现）；过程 reward 是稠密的、即时的。用过程子目标约束方向，可以让 skill 更新不至于在"结果偶然对了但过程是错的"轨迹上收敛——这正是 SkillOpt 的 rejected-edit buffer 想防的"plausible but harmful"编辑，本文给它一个**过程维的即时信号**而非只靠留出集事后 gate。

### 3.3 合成 reward 与 mini-batch 更新

$$r(s) = \alpha \cdot r_{\text{out}}(s) + \beta \cdot r_{\text{proc}}(s)$$

**每个 mini-batch 同时计算两维子目标 reward**，据此调整 skill（沿用 SkillOpt 的 bounded edit + validation gate，但 gate 现在是**双维**的：结果子域回归任一子域、或过程一致性下降，都可触发 reject）。

> 这把 SkillOpt 的单标量 gate 升级为**结构化 gate**：不仅"总分是否更高"，而是"哪个子域升了、哪个过程指标退了"——rejected-edit buffer 因此能记录**带维度的负反馈**（"这次编辑升了数字子域但砸了总结子域"），比 SkillOpt 的无维度 buffer 信息量高一个量级。

### 3.4 用户示例的处理：大模型协助拆解 + 确定评测计算法

用户给出的 few-shot 正/反例（$E^+, E^-$）不是直接塞进 context，而是：

1. **大模型协助解析拆解**：把用户示例拆成 $\sigma^{out}$ 的子域标注 + 过程 step 的正确性标注 → 自动构造 §3.1 的分子域 benchmark 雏形；
2. **确定每个子域的评测计算方法**：数字子域用容差匹配、总结子域用哪个 rubric、过程用哪些 gate —— 由优化器模型提议、人确认。

这样人只需**审"评测方法"这一次**，之后每个 mini-batch 的 reward 由确定的评测法自动算 —— 把"人工判断强制收敛"从**每轮**降到**一次**（呼应 [08-模型原生计算架构-体系结构视角](08-%E6%A8%A1%E5%9E%8B%E5%8E%9F%E7%94%9F%E8%AE%A1%E7%AE%97%E6%9E%B6%E6%9E%84-%E4%BD%93%E7%B3%BB%E7%BB%93%E6%9E%84%E8%A7%86%E8%A7%92.md) §6 协作悖论：把委派率抬高的抓手）。

---

## 4. 推论：skill 必须模型总结、且收敛后可 code 化

### 4.1 skill 必须是模型总结的，不能人工生成

这是双子目标训练的**直接推论**，也与 SkillOpt 的实证一致（它的 SkillOpt 全面击败 human-skill / one-shot LLM-skill baseline）：

- skill 是"针对 goal 的双维 reward"迭代出来的**梯度产物**——人工写的 skill 没经过这个回路，无法保证在结果子域 + 过程一致性上是最优的；
- 人只提供 **goal + 示例 + 确认评测方法**（§3.4），**skill 本体由优化器模型从轨迹总结**。这把 [研究原则-外部记忆即Skill基础] 的"HITL 是 skill 生成器"精化为"**HITL 是 reward 评测法的确认者，优化器模型是 skill 的生成器**"。

### 4.2 收敛后的子目标可被 code 化 → 接 10 号

随梯度收敛，**变化不大的子目标**（无论结果子域的评测逻辑，还是过程判据）说明其操作空间已闭合 → 满足 [10-Skill-as-Code与确定性固化](10-Skill-as-Code%E4%B8%8E%E7%A1%AE%E5%AE%9A%E6%80%A7%E5%9B%BA%E5%8C%96.md) 的可固化度 $\kappa$ 阈值 → **可被编码以确定其输出逻辑**。

> **这条把 10 号和 12 号缝合成一个完整生命周期**：
> $$\underbrace{\text{双子目标 RL 迭代}}_{\text{本文 §3}} \xrightarrow{\ \text{子目标收敛}\ } \underbrace{\kappa \uparrow \text{ 达阈}}_{\text{10 号 §1}} \xrightarrow{\ \text{固化}\ } \underbrace{s^{\text{code}}\ (\text{确定执行体})}_{\text{10 号 §2 N0 三分}}$$
> 即：**skill 先在文本空间被"训练"（本文），稳定的部分再"编译"为 code（10 号）**——训练与编译是 skill 生命周期的两个阶段，都归 Harness 维护子系统 $M$。

---

## 5. 推论：复杂 agent 的调教可分解

双子目标结构天然支持**分而治之**，回答"一个复杂的、用户直接用的 agent 怎么调教"：

- **按子 agent 分头调教**：不同子 agent 负责 goal 的不同子任务，各自用自己的双子目标 reward 独立训练 skill，再组合（接 [09-并行度与局部性协同设计](09-%E5%B9%B6%E8%A1%8C%E5%BA%A6%E4%B8%8E%E5%B1%80%E9%83%A8%E6%80%A7%E5%8D%8F%E5%90%8C%E8%AE%BE%E8%AE%A1.md) 的并行度 + [05-控制面与数据面正交切分](05-%E6%8E%A7%E5%88%B6%E9%9D%A2%E4%B8%8E%E6%95%B0%E6%8D%AE%E9%9D%A2%E6%AD%A3%E4%BA%A4%E5%88%87%E5%88%86.md) 的正交切分）；
- **按分结果子域的 benchmark 指导**：同一 agent 的不同 $\sigma^{out}$ 子域各由其标注 benchmark 分别指导迭代（§3.1）。

> 这恰好补上 SkillOpt 的 Limitation 之三："SkillOpt 只训**一个** portable skill，异构域可能需要 many disjoint procedures。"本文的分解式调教给了那个缺口一个结构化答案：**异构 = 多子域 benchmark × 多子 agent**，每个仍是一个紧凑 skill，但组合覆盖异构域。

---

## 6. 形式化与命题（拟 N9 / P15）

沿用 [01-C5-双扩展解耦形式化与命题](01-C5-%E5%8F%8C%E6%89%A9%E5%B1%95%E8%A7%A3%E8%80%A6%E5%BD%A2%E5%BC%8F%E5%8C%96%E4%B8%8E%E5%91%BD%E9%A2%98.md) 记号，引入：

- **子目标分解算子** $\Pi$：把自然语言 goal $g$ 投影为 $\{r_d\}_{d}$（结果子域集）+ $r_{\text{proc}}$（过程一致性）。
- **归因清晰度** $\text{Attr}(r)$：reward 对"错在哪个子域/哪个 step"的可归因程度。

### 命题 P15（子目标分解的收敛加速 / Subgoal-Decomposed Convergence）— 本文主命题

> **在自然语言 goal 下，双维子目标 reward（结果子域 × 过程一致性）比单一 scalar reward 有更高的归因清晰度，因而在同等 rollout 预算下 skill 迭代方向更一致、收敛更快、且更少依赖人工判断。** 形式化：
> $$\text{Attr}(r_{\text{out}}\oplus r_{\text{proc}}) \gg \text{Attr}(r_{\text{scalar}}),\qquad \mathbb{E}[\text{steps-to-converge} \mid \text{双维}] < \mathbb{E}[\cdot \mid \text{scalar}]$$

**可证伪**：取一个多子域任务（如 OfficeQA 类：数字+总结+引用），复现 SkillOpt 两种配置——(a) 原单 scalar gate；(b) 本文双子目标 gate。比较：① 收敛所需 epoch/编辑数；② 最终各子域分；③ 人工干预次数。P15 预期 (b) 更快收敛、子域更均衡、人工更少；若 (b)≈(a) → 子目标分解无增益，goal 的 scalar 投影损失可忽略，P15 被证伪。

### 命题 N9（拟）· 过程 reward 的即时纠偏

> **稠密的过程子目标 reward 能在长程任务中比稀疏结果 reward 更早剪掉错误轨迹方向，等价于给 SkillOpt 的 rejected-edit buffer 提供带维度的即时负反馈。**

**可证伪**：长程任务上，比较"仅结果 reward"vs"结果+过程 reward"的中途纠偏率（错误轨迹被识别的平均 step 位置）。预期后者显著更早；若无差异 → 过程信号冗余于结果信号。

---

## 7. 对主线 / novelty 的影响

1. **N9（拟）· 双子目标 reward**：把"skill 可训练"（SkillOpt 已立）从**单 scalar** 升级为**结果子域 × 过程一致性双维**，正面回应 SkillOpt 自认的最大 Limitation（开放域/多维 goal 打分难）。对标空白：SkillOpt/GEPA/TextGrad 都用标量或单一偏好信号；**无人把 reward 沿"输出格式子域 + 过程判据"结构化分解并证明其加速归因**。
2. **P15（拟）· 子目标分解收敛加速**：一个可证伪的效率主张，且给"复杂 agent 分解调教"（§5）提供理论依据。
3. **skill 生命周期闭环**：本文（训练）+ [10-Skill-as-Code与确定性固化](10-Skill-as-Code%E4%B8%8E%E7%A1%AE%E5%AE%9A%E6%80%A7%E5%9B%BA%E5%8C%96.md)（编译）合成 **train → freeze-to-code** 两阶段生命周期，都归 Harness $M$。这是本架构相对 SkillOpt（只训、不编译）和 CodeAct（只执行 code、不训）的**组合 novelty**。
4. **HITL 定位精化**：从"HITL 是 skill 生成器"精化为"**HITL 是 reward 评测法的一次性确认者**"（§3.4），把人工判断从每轮降到一次——给 [08-模型原生计算架构-体系结构视角](08-%E6%A8%A1%E5%9E%8B%E5%8E%9F%E7%94%9F%E8%AE%A1%E7%AE%97%E6%9E%B6%E6%9E%84-%E4%BD%93%E7%B3%BB%E7%BB%93%E6%9E%84%E8%A7%86%E8%A7%92.md) 协作悖论一个具体的委派率抬升机制。

---

## 8. 文献支撑与划界（防 reviewer "已有人做过"）

| 主张 | 支撑文献 | 我们的 delta |
|---|---|---|
| skill = frozen agent 外部可训练状态；DL 优化器纪律（LR/gate/meta）搬进文本空间 | **SkillOpt (2605.23904)** | 我们采纳其骨架，但把**单 scalar reward** 换成**双子目标结构化 reward** |
| trajectory feedback 引导反射式 prompt 进化，胜过 RL | GEPA (2506.xxxx) | GEPA 优化 prompt/单信号；我们优化持久 skill + 双维 reward |
| success/failure minibatch 反思 | SkillOpt §3.3 | 我们给反思一个**沿两维子目标的结构**，而非凭 scalar 自由发挥 |
| reward 可验证环境 > PRM + 小数据 | [研究总览] 洞察 #8（AI 编码精读） | 我们主张**过程子目标 = PRM 的自然语言 agent 形态**，结果子目标 = ORM，二者互补而非取舍 |
| 正例求最优、负例求多样 | [研究原则-Zotero批注提炼] | SkillOpt 的 success/failure minibatch 是其实证；我们补双维归因 |

> **必须诚实标注的边界**：SkillOpt 已经做了"skill 可训练 + minibatch 反思 + validation gate + rejected buffer"。本文唯一的科学 delta 是：**(a) 把 scalar reward 分解为「结果子域 benchmark × 过程一致性」双维**，**(b) 证明该分解提升归因清晰度并加速收敛（P15）**，**(c) 把训练阶段与 10 号的 code 固化阶段缝成 skill 完整生命周期**。写 paper 必须与 "SkillOpt 已做单标量 skill 训练" 显式划清。

---

## 9. 待验证 / 风险点

- [ ] **子域权重 $w_d$ 与 $\alpha/\beta$ 的确定**：是超参还是可学？过程 reward 权重过高可能过拟合"形式正确但结果错"的轨迹。
- [ ] **过程子目标的 verifier 从哪来**：过程判据本身也需要一个 verifier；若过程 verifier 不可靠，$r_{\text{proc}}$ 引入噪声。可能需要"过程 verifier 也用 skill 训练"的递归——注意别陷入无穷回归。
- [ ] **分子域 benchmark 的标注成本**：§3.1 需要每子域有标注 benchmark，比 SkillOpt 单 benchmark 成本高。§3.4 的"大模型协助拆解"是缓解手段，但拆解质量待验。
- [ ] **过程 reward 与结果 reward 冲突时的仲裁**：过程全对但结果错（工具/数据没问题但世界变了），或结果对但过程侥幸——谁优先？需定义仲裁规则。
- [ ] **P15 的实验依赖复现 SkillOpt**：需先跑通 SkillOpt 开源（aka.ms/SkillOpt），在其上改 gate 为双维——工程量不小。

---

## 10. 下一步

1. 精读 SkillOpt 附录的 optimizer prompt 模板与 hyperparameter 分析（§C / 表 2），确认双维 gate 的最小改动点。
2. 把 N9 / P15 回填进 [07-创新点总结](07-%E5%88%9B%E6%96%B0%E7%82%B9%E6%80%BB%E7%BB%93.md) novelty/命题总表。
3. 把 §4.2 的 train→freeze 生命周期接进 [10-Skill-as-Code与确定性固化](10-Skill-as-Code%E4%B8%8E%E7%A1%AE%E5%AE%9A%E6%80%A7%E5%9B%BA%E5%8C%96.md) §9，标为其上游阶段。
4. 把 §5 的分解式调教接进 [09-并行度与局部性协同设计](09-%E5%B9%B6%E8%A1%8C%E5%BA%A6%E4%B8%8E%E5%B1%80%E9%83%A8%E6%80%A7%E5%8D%8F%E5%90%8C%E8%AE%BE%E8%AE%A1.md)（多子 agent 并行训练）。
5. 将 SkillOpt 加入 [02-2026相关论文清单](02-2026%E7%9B%B8%E5%85%B3%E8%AE%BA%E6%96%87%E6%B8%85%E5%8D%95.md)，标为"skill 训练"主线的锚点论文。
6. 把"过程子目标 = PRM 的 agent 形态 / 结果子目标 = ORM"接进 [研究总览] 洞察 #8。

---

相关：[精读 - 2605.23904](精读%20-%202605.23904.md)（SkillOpt 原文精读） · [10-Skill-as-Code与确定性固化](10-Skill-as-Code%E4%B8%8E%E7%A1%AE%E5%AE%9A%E6%80%A7%E5%9B%BA%E5%8C%96.md) · [08-模型原生计算架构-体系结构视角](08-%E6%A8%A1%E5%9E%8B%E5%8E%9F%E7%94%9F%E8%AE%A1%E7%AE%97%E6%9E%B6%E6%9E%84-%E4%BD%93%E7%B3%BB%E7%BB%93%E6%9E%84%E8%A7%86%E8%A7%92.md) · [09-并行度与局部性协同设计](09-%E5%B9%B6%E8%A1%8C%E5%BA%A6%E4%B8%8E%E5%B1%80%E9%83%A8%E6%80%A7%E5%8D%8F%E5%90%8C%E8%AE%BE%E8%AE%A1.md) · [01-C5-双扩展解耦形式化与命题](01-C5-%E5%8F%8C%E6%89%A9%E5%B1%95%E8%A7%A3%E8%80%A6%E5%BD%A2%E5%BC%8F%E5%8C%96%E4%B8%8E%E5%91%BD%E9%A2%98.md) · [05-控制面与数据面正交切分](05-%E6%8E%A7%E5%88%B6%E9%9D%A2%E4%B8%8E%E6%95%B0%E6%8D%AE%E9%9D%A2%E6%AD%A3%E4%BA%A4%E5%88%87%E5%88%86.md) · [03-Harness-System-SubAgents清单](03-Harness-System-SubAgents%E6%B8%85%E5%8D%95.md)
