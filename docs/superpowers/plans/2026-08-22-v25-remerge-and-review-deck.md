# v25 计划：两篇合回一篇 + 笔记单一事实源 + 架构评审 deck

> **日期**: 2026-08-22
> **决策来源**: 用户选定"合回一篇"，撤销 2026-08-05 的 v21/v22 拆分
> **前置输入**: 2026-08-22 仓库审查的 13 条发现（本文件 §1 全量登记并给出处置）
> **产物**: 本计划 + vault 笔记合并 + `academy/` 下的 v25 大纲 + 架构评审 PPTX

---

## 0. 决策记录（本轮由执行者代为判断，需要时可推翻）

用户明确选择"合回一篇"，并在被告知代价后确认。其余判断如下，均为落地所必需：

| # | 决策 | 理由 |
|---|---|---|
| D1 | 合并后单篇代号 **v25**，目标 **38–42 页** | v23 两篇合计 55 页，其中 8 图与契约解剖纯重复；去重后落在此区间 |
| D2 | **所有跨篇冲突一律以聚焦篇（Separability Study v23）的方法学为准** | 上一轮评审已判定 cluster-period 在方法学上明显更严谨 |
| D3 | 判决规则升为**四态**：`supported` / `falsified` / `conditional-engineering` / `inconclusive` | 企业篇独有的 conditional-engineering 是六合取 inconclusive 膨胀的唯一缓解；合并后应全局生效 |
| D4 | vault `Agentic-Runtime-参考架构/` 为**唯一权威**，repo `notes/` 降为镜像 | vault 侧含 v20–v22 评审、v0.2 综合稿、子系统设计，信息量显著更大 |
| D5 | 代价接受：**放弃 v22 作为独立可投测量协议论文的形态** | 用户已被告知并确认；合并后测量协议成为单篇的 §6–§8，仍完整保留 |
| D6 | PPT 用**中文**、16:9、复用 `site/pptx_build.py` 的构建风格 | 架构评审场景为中文；已有 pptx 机制与配色，不从零写 |

**本计划不做的事**：不执行最小可行实验（v22/v23 复核连续两轮标记的首要风险仍然存在，合并不改变这一点）；不改动 `site/` 下已发布的 HTML/图；不改 v23 及以前的 PDF 产物。

---

## 1. 13 条发现的处置对照

合并本身直接消灭 P0 全部四条 —— 这是选"合回一篇"的最大收益。

| # | 发现 | 合并后处置 |
|---|---|---|
| P0-1 | 两篇标题字面相同（`latex_to_preprint.py:29` 单一硬编码 `TITLE`，无 `--title`） | **自动消失**（只剩一篇）。仍给脚本加 `--title` 参数，避免将来再拆时复发 |
| P0-2 | 契约元组冲突：`separability:121` 用 `⟨I,O,G,A,B,V⟩`，`enterprise:219/482` 用 `⟨I,O,G,B,E,T⟩` | 全局统一为 **`⟨I,O,G,A,B,V⟩`**（D2）。`:482` 的字段级 walkthrough 需逐字段改写：原 `E`→`A`、原 `T`→`V` |
| P0-3 | 随机化单位矛盾：`enterprise:631` "one independent run" vs `separability:242` "not independent randomized units" | 以 **cluster-period** 为准（D2），删除 `enterprise:631` 的整句并改写该段 |
| P0-4 | 两篇零交叉引用 | **自动消失** |
| P1-5 | `conditional-engineering result` 只在企业篇（`:265/:267/:764`），聚焦篇三态判决无此降级档 | 升为**第四态**（D3），写入合并后的判决规则一节 |
| P1-6 | margin 推导规则不对称：`enterprise:636` 立了"每个 margin 须由具名决策推导并记录 owner"，但 `separability:250` 的 reset 哨兵 `±log(1.05)` / `-0.025` 是裸数字 | `:636` 的规则**全局适用**；为两个哨兵数字补领域论证，或标注为"占位待定，投稿前必须由具名决策替换" |
| P1-7 | `E(c,s)` 未声明是边际执法开销（全文无 `marginal` / `opportunity cost`） | 在 `E(c,s)` 定义处加一句显式声明：估计的是**边际运行时执法开销**；被拒行为改变后续轨迹的机会成本归入 `Q(c,s)` |
| P2-8 | 26 篇已下载 PDF 中 9 篇零引用，最危险的是 `2605.26112`（*From Model Scaling to System Scaling*，与 capability/capacity 双轴同问题域，vault 有专门笔记） | 优先补 `2605.26112`、`2607.13987`、`2605.22781`、`2605.18747` 四篇进 bib 与 novelty boundary；其余 5 篇（`2605.08715`/`2606.15376`/`2605.14892`/`2605.29790`/`2606.03698`/`2606.12835`）按相关度择要 |
| P2-9 | 聚焦篇 bib 仅 21 条，同期工作只引 4 篇 | 合并后取两篇 bib 并集（去重约 41 条）+ P2-8 新增 |
| P3-10 | 8 个 figure label 两篇全重复；55 页 | 合并为**单套 8 图**；目标页数见 D1 |
| P4-11 | 笔记三份副本漂移（repo `notes/` / vault 顶层 / vault 子目录），27 个同名文件 24 个不同；编号撞车（repo `13-DataWiki` vs vault `13-v20`） | 按 D4 合并，见 §2 |
| P4-12 | `notes/07-创新点总结.md` 仍 v0.1 / 2026-06-20，登记 P1–P17 + N0–N12，而论文已撤回 P2–P14 | 重写为 v25 版 novelty ledger，明确标注哪些命题已撤回/并入六义务 |
| P4-13 | `notes/02-2026相关论文清单.md` 说"7 篇已精读 + 9 篇"，实际 26 篇 PDF、企业篇已引 13 篇 2607 工作 | 按 `academy/papers/README.md` 与两篇 bib 的实际状态重建清单 |

---

## 2. Obsidian 笔记合并（本轮执行）

**权威**：`~/Documents/Obsidian Vault/Agentic-Runtime-参考架构/`（D4）

三份副本的现状：

| 位置 | 内容 | 处置 |
|---|---|---|
| vault `Agentic-Runtime-参考架构/` | 00–16 + 子系统设计 + v0.2 综合稿，共 40 个 md | **保留为权威** |
| vault 顶层 | 00–12 的旧副本（部分更短） | **删除重复项**，仅保留非本课题的独立笔记 |
| repo `notes/` | 27 个文件，另有 2 个 vault 没有的 | **先把独有内容并入权威，再降为镜像** |

repo 独有、必须并入的两份：

1. `13-DataWiki-ThemeWiki-IR中间关系层.md` —— 与 vault 的 `13-v20-企业AI运行时架构-中文综合.md` **编号撞车**，并入时重编为 **`17-DataWiki-ThemeWiki-IR中间关系层.md`**
2. `07-创新点总结.md` —— repo 版 16423 字节 vs vault 版 8610 字节，repo 版含 N9–N12 与 P14–P17，内容更全；以 repo 版为基础，按 P4-12 重写后落到权威目录

安全措施：vault 当前 git 状态干净，合并前后各提交一次，任何一步都可 `git revert`。

---

## 3. v25 论文大纲（产物写入 `academy/`）

结构取企业篇的架构广度 + 聚焦篇的方法学严谨度。详见 `academy/v25-outline.md`。

骨架：

1. Abstract / Introduction —— 单一研究问题（cost-aware capability-capacity separability）
2. Responsibility Model —— 四责任对象（Skill / Harness / Scaffold / 外置数据底座）
3. Contract Boundary —— 统一元组 `C=⟨I,O,G,A,B,V⟩`（P0-2）
4. Foundations & Novelty Boundary —— 经典谱系 + 2026 同期工作，含 P2-8 新增四篇
5. Six Measured Obligations —— 每条五项必报输出 + γ/ν/η 三阈值
6. Cluster-Period Crossover Study —— 唯一随机化单位（P0-3）
7. 四态判决规则（P1-5）+ margin 推导规则全局化（P1-6）+ `E(c,s)` 边际声明（P1-7）
8. 数据子系统与 IR —— `D₁–D₄`、5W1H+Which、Data Wiki / Theme Wiki
9. 次级协议与未来工作 —— P15/P16/P17 及 Skill 训练
10. Evidence Boundary / Threats / Conclusion —— 含连续两轮标记的"尚无实测"风险

---

## 4. 架构评审 PPT（产物写入 `academy/`）

- 受众：架构评审（非论文审稿），因此重心放在**责任边界、契约、判决规则**，而非统计细节
- 中文、16:9、约 16 页，构建脚本 `academy/review_deck_build.py`，产物 `academy/architecture-review-v25-zh.pptx`
- 配色沿用 `site/style.css` 已迁移的 Tailwind 系（logic `#3B82F6` / contract `#7C3AED` / phys `#EA580C` / data `#059669`）
- 必须包含一页"**本架构尚无实测结果**"，与论文的 evidence boundary 一致 —— 评审场合隐去这一点会误导

---

## 5. 执行顺序

1. 本计划落盘并提交
2. vault 笔记合并（§2），vault 侧提交
3. `academy/v25-outline.md` 落盘
4. `academy/review_deck_build.py` + PPTX 落盘
5. repo 提交并推送

**不在本轮**：改 `paper_source/main.tex` 生成真正的 v25 PDF。本轮只到大纲；正文重写是下一个独立任务，因为它要逐段合并 822 + 308 行 LaTeX 并重排 8 图。
