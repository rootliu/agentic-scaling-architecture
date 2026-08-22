# 数据平面：LLM 抽取 vs 人为 schema 的信息保真边界

> **来源**: 2026-08-21 用户命题验证（"LLM 本身是优秀知识压缩器"——对比对象从 BM25 修正为"人为 schema / 传统特征工程"）
> **类型**: 论证与证据链（evidence brief / 边界分析）
> **状态**: 初稿 v0.1
> **定位**: 为 [[06-数据平面四组成架构]] 的 D₂（off-policy 语义总结、"避免人为截断"）提供外部证据背书与**三条边界修正**；把"schema-on-write 的损失类型"从直觉升级为可引用、可证伪的结论
> **关联**: [[06-数据平面四组成架构]] | [[08-数据层修订-三阶记忆子架构]] | [[05-控制面与数据面正交切分]] | [[Harness-Memory-子系统-显隐双轨设计]] | [[02-2026相关论文清单]]

---

## 0. 一句话结论

**方向对，但有边界。** "人为 schema / 传统特征工程"是真正的**有损压缩**——它是 schema-on-write，事先把信息硬塞进一个固定的、低容量的码本，码本之外的信息写丢即不可逆；而 LLM 提取是一个从海量数据学到的、内容自适应的有损编码器。因此**在"同码率下谁保留更多信息"这一问上，LLM 显著优于人为 schema**，特征工程文献给出干净证据。但"优于 schema"既不等于"无损"，也不等于"优于人类专家"，更不等于"损失可审计"——这三条限定必须同时写进结论。

---

## 1. 对照的修正：为什么必须是"人为 schema / 特征工程"

上一版把 BM25 放进来是概念错位：BM25 是稀疏检索索引，它只重排原文、不重写信息，本质上不是压缩器，和"LLM 有损压缩"比量纲不对。

而**人为 schema 和传统特征工程确实在丢信息**：LLM-FE 原文直接把传统自动化特征工程的瓶颈描述为"依赖预定义变换、固定手工搜索空间"；MedFeat 也说人工特征"受限于固定算子模板"。所以"LLM 抽取 vs 人为 schema"才是真正在比两个有损压缩器的信息容量，这次诉求成立。

**这两个对照物为什么能被归到同一类**：

| 对照物 | 丢弃机制 | 损失的可知性 |
|---|---|---|
| 人为 schema（schema-on-write / ETL） | 事先定死字段/口径，码本之外丢弃 | 已知、可审计（你精确知道丢了哪些字段） |
| 传统特征工程（TF-IDF / 手工算子 / 预定义搜索空间） | 低维固定投影 | 已知、可审计 |
| LLM 抽取（summarization / feature extraction） | 学习到的、内容自适应的有损编码 | **未知、随机（你不知道丢了什么、甚至可能被改错）** |

---

## 2. 证据链：LLM 特征 > 人为 schema / 预定义特征工程

| 证据 | 对照对象 | 结果 |
|---|---|---|
| LLM-FE（Virginia Tech, arXiv:2503.14434） | 传统 AutoFE（预定义算子 + 固定搜索空间） | 分类/回归基准全面胜出，最低 mean rank |
| FeatEHR-LLM（EPFL, arXiv:2604.22534） | 纯手工 / 转换式的 EHR 特征工程 | 8 个 ICU 任务中 7 个取得最高 AUROC，最高 +6pp |
| MedFeat（牛津+微软, arXiv:2603.02221） | 固定算子模板（AutoFeat / OpenFE 等） | 稳定提升，且能生成跨分布鲁棒、有临床意义的特征 |

**信息论解释**：人为 schema 是"低维固定投影"，其互信息上限 $I(X; Z)$ 被一个事先定死的低容量码本卡死；LLM 的码本是从数据分布学出来的，同码率下能逼近更高的 $I(X; Z)$。这直接印证 [[06-数据平面四组成架构]] 里 D₂ 的命题——"避免人为截断"有外部证据支撑。

---

## 3. 三条边界（缺一不可）

### 3.1 "优于 schema" ≠ "优于不压缩"

能保留原文 + 检索（BM25/dense 检索 + raw chunk）时，损失恒为 0，永远优于任何有损压缩。2606.29251 也强调压缩"只有在其能保留原文本所支持的决策时才可用"。所以 LLM 的优势只成立于"上下文预算强制要求压缩"这个前提之下。

### 3.2 损失的"类型"不同，这是最关键的治理差异

人为 schema 丢信息是**已知且可审计的**；LLM 丢信息是**不透明且随机的**，且一条反证显示它随规模**变差**而非变好：

- **Size-Fidelity Paradox（arXiv:2602.09789）**：压缩器从 0.6B 放大到 90B，反而出现"知识覆盖"（用模型先验替换原文事实，如 blue-banded bee → honey bee）和"语义漂移"（Alice hit Bob → Bob hit Alice）。
- 也就是说：schema 只会"丢掉"，LLM 会"主动改错"，二者不是同一类风险。

### 3.3 "优于 schema" ≠ "优于人类专家"

- **Summarization is Not Dead Yet（arXiv:2606.08000）**：跨数据集、跨 5 个前沿模型评估显示，人类参考摘要在**信息量**和**忠实度**上仍占优，LLM 只在流利度/连贯性这类"形式维度"领先；原话是"表面流利不传导为信息保真"。
- **Human-LLM Collaborative FE（ICLR 2026, arXiv:2601.21060）**：人机协同特征工程显示"LLM 提案 + 人类筛选"比 LLM 单独更好（错误率再降 8.96–11.23%）。

最优解不是 LLM 单打，而是 **LLM + human-in-the-loop**。

---

## 4. 对架构的落点（回到 D₂）

三条可执行结论，直接约束 D₂ 的 off-policy 语义总结设计：

1. **默认路径 = raw retention + retrieval（0 损失基线）**；人为 schema 只降级为"索引/路由维度"（正是 5W1H+Which / [[Harness-Memory-子系统-显隐双轨设计]] 的七维本体）；LLM 只在上下文预算**强制压缩时**才作为压缩器启用。
2. **LLM 的损失不可审计 → 需在 Harness 侧加"保真审计"层**：对照 2606.29251 的"多候选压缩 + 分歧审计"（Agentic Context Compression），对 D₂ 产出的 $\Sigma$ 做异议检测后再注入 semantic join。
3. **警惕"越大越忠实"的误区**：$\Sigma$ 生产模型（$\Theta_2$）的规模要按保真需求选，而非越大越好（2602.09789 的 Size-Fidelity Paradox）。

**可证伪实验（直接对接 [[06-数据平面四组成架构]] 的 P8）**：三臂对比——(a) 裸 agent 在线发现；(b) 人工 schema/元数据；(c) off-policy $\Sigma$ + semantic join。测 precision/recall/last-mile 成功率与 token 成本。本证据链预期 **(c) precision 接近 (b)、coverage 接近 (a)**，且需增测第四臂 (d) LLM 抽取 + 人工筛选，验证 3.3 的"最优是 LLM + human-in-the-loop"。

---

## 5. 引用清单

- LLM-FE: Automated Feature Engineering for Tabular Data with LLMs as Evolutionary Optimizers. arXiv:2503.14434. https://arxiv.org/abs/2503.14434
- FeatEHR-LLM: Leveraging LLMs for Feature Engineering in Electronic Health Records. arXiv:2604.22534. https://arxiv.org/abs/2604.22534
- MedFeat: Model-Aware and Explainability-Driven Feature Engineering with LLMs for Clinical Tabular Prediction. arXiv:2603.02221. https://arxiv.org/abs/2603.02221
- Human-LLM Collaborative Feature Engineering for Tabular Learning. ICLR 2026. arXiv:2601.21060. https://arxiv.org/abs/2601.21060
- Summarization is Not Dead Yet. arXiv:2606.08000. https://arxiv.org/abs/2606.08000
- When Summaries Distort Decisions: Information Fidelity in LLM-Compressed Financial Analysis. arXiv:2606.29251. https://arxiv.org/abs/2606.29251
- When Less is More: The LLM Scaling Paradox in Context Compression. arXiv:2602.09789. https://arxiv.org/abs/2602.09789

---

相关：[[06-数据平面四组成架构]] · [[08-数据层修订-三阶记忆子架构]] · [[05-控制面与数据面正交切分]] · [[Harness-Memory-子系统-显隐双轨设计]] · [[02-2026相关论文清单]] · [[原始构想-用户原话]]