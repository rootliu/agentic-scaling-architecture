## 01. 契约驱动的 Agentic Runtime

建议用25分钟讲解，另留10分钟讨论。先说明这是内部版本v29，已有arXiv论文是前版。本次真正新增的是可执行数据边界与有限验证，不是完整系统或顶会录用结果。作者顺序沿用论文。

- [Existing arXiv / 已发表前版](https://arxiv.org/abs/2608.27086)

## 02. 一个任务成功，不代表一个系统可管理

用一份季度经营报告引入。最后数字看起来正确，仍可能使用错期间、越权数据或旧文件。我们要同时问业务任务是否完成，以及运行路径是否满足约束。

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 03. v29 将设计主张推进到可执行边界

强调三项贡献的证据等级不同。责任架构是设计，契约参考模型可执行，P1是仍待验证的经验假设。不要把它们统称为已验证架构。

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 04. 四个责任对象，三个运行时层

Skill声明业务能力，Harness进行准入和绑定，Scaffold提供执行边界与资源。外部数据基座不调度计算，也不被某个运行层私有化。这是责任模型，不要求企业必须设四个团队。

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 05. P1：能力与容量是否能有条件分离？

以两种能力配置、两种容量配置解释2×2实验。扩容改善时延是预期主效应，不是P1的证明。需要检验改变能力的效果是否因容量改变而变化，同时语义不退化、开销不超预算。阈值必须由决策确定。

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 06. 最小反例：列名相同，业务意义不同

不要讲成一次SQL join就能发现的普通类型错误。两张表在语法和字段名上都可能一致，但单位、范围和期间不同。我们要求这些语义进入契约，而不是依赖模型临场猜测。

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 07. Data Wiki、Theme Wiki 与 IR 各回答什么

Data Wiki面向数据本身，Theme面向结果要求，IR记录本任务怎样使用这些数据。摘要可以帮助发现，不能替代原始来源。IR在这里是Intermediate Relation，执行票据是从关系中解析出来的另一个对象。

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 08. 让 5W1H+Which 成为可检查条件

这些问句不是七项独立创新。技术工作在于把字段连接到可信输入、执行检查和明确故障。Why只是批准的整合理由，不是模型生成的因果证明。当前参考模型只实现简化检查，不实现多源join。

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 09. 从候选检索，到执行票据，再到证据

分清发现和授权：搜索结果只是候选，不能直接授予工具或源权限。执行前重查版本与策略，返回字节后绑定证据。失败进入typed rejection，回退只能选择已允许路径。

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 10. 撤权发生在排队期间：准入检查还够吗？

时间顺序是关键。t0准入有效，t1撤权，t2真正读数据。旧票据不能继续放行。检查与读必须相对于更新共享线性化点。已在撤权前读出的字节不能被自动收回；发布必须是另一个检查。

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 11. 变更影响可沿显式依赖传播

遍历依赖图本身是成熟算法。值得研究的是是否能完整记录语义、策略、算子、主题与产物的依赖，并减少真实变更重验证工作。当前实现是保守的全局epoch，没有实现细粒度优化。

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 12. 文件存在，仍不等于任务已完成

内部团队容易把生成文件当成完成。举例：上次运行留下同名PPT、脚本写好但没运行、引用能打开但不支持结论。这些都应留下未解决义务，而不是勾选完成。

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 13. 已经执行：有限契约一致性验证

这些数值从提交的JSON结果读取。1,024种组合中，只有没有故障的组合应通过；其余1,023种应拒绝。零分歧说明这个有限域的规则执行一致。不能把1,024解释为统计样本量，也不能把零分歧换成生产失效率上界。

- [Raw cases / 逐例结果](../agentic-runtime-preprint/artifact_v29/results/fault-cases.csv)
- [Summary / 汇总](../agentic-runtime-preprint/artifact_v29/results/summary.json)

## 14. 证据边界：我们现在可以说什么

明确区分实现边界和未来承诺。没有自然检索、并发压力、跨租户攻击或完整P1数据。参考模型依赖可信描述与完整中介，不是安全沙箱。保持这个区分能让工程讨论更有效。

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 15. 近期工作：执行、研究与交付

三篇都不是我们的实验结果。Prime Agent说明长期状态与核算已有实现；AutoResearch区分产物和证据；Apodex区分生成和受控交付。v29不能再以这些泛化能力作为独有创新。

- [Prime Agent](https://arxiv.org/html/2608.23552v1)
- [AutoResearch](https://arxiv.org/html/2608.17906v1)
- [Apodex 1.1](https://arxiv.org/html/2608.23283v1)

## 16. 近期工作：索引、路由与来源读取

VoiceMem消融提醒索引与路由要分别控制；NeoHorse记录需求与实际路由，提醒容量变化可能偷偷改变模型；Beyond Top-K要求强BM25对照且不能忽视转换错误。最后一篇是已有引用的复核。

- [VoiceMem](https://arxiv.org/html/2608.26005v1)
- [NeoHorse-1](https://arxiv.org/html/2609.08183v1)
- [Beyond Top-K](https://arxiv.org/html/2608.06305v1)

## 17. v29 修正了哪些方法学风险

关键是四态判定不再重叠。先确认是否有足够测量证据，再确认义务是否成立，最后才谈P1。另删除错误的p95功效推算；用pilot模拟决定样本量，不能用噪声扩大允许退化。

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 18. 下一步实验：隔离契约本身的作用

相同候选、相同工具、相同模型和预算，只改变描述是否被执行边界强制执行。加入自然错误和合成注入，按来源和时间划分留出集。误拒绝必须与违规一起报告，否则拒绝所有请求就会看起来很好。

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 19. 内部试点：先选一个边界清楚的工作流

建议选季度报告或内部研究简报，从人工可核验字段和一个受控源开始。业务负责人定义可容忍错误，数据负责人定义源与策略，平台负责人实现执行边界。每阶段设进入下一阶段的证据条件，而非承诺任意日期。

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 20. 投稿方向由主贡献与实证决定

数据契约路线优先考虑SIGMOD，完整P1运行时路线考虑OSDI，契约演进与维护考虑ICSE/FSE。SIGMOD十月窗口很紧；不能为了赶时间把合成检查当实证。ICSE2027已经截止。FSE2027截止日期未确认。

- [SIGMOD 2027 CFP](https://2027.sigmod.org/calls_papers_sigmod_research.shtml)
- [OSDI 2027 CFP](https://www.usenix.org/conference/osdi27/call-for-papers)
- [ICSE 2027 CFP](https://conf.researchr.org/track/icse-2027/icse-2027-research-track)

## 21. 内部讨论需要做的三个决定

结尾不要以论文已经完成所有验证作为行动理由。团队需要决定优先研究问题、可用真实数据与合格阈值。产出应是责任明确的试点协议，而不是新的架构命名。

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 22. 阅读与复现入口

页内论文链接可以点击。讲稿备注保留章节级阅读提示。代码和逐例CSV位于同一仓库artifact_v29。现有arXiv链接是前版，本地v29尚未完成arXiv替换。

- [Existing arXiv](https://arxiv.org/abs/2608.27086)
- [v29 evidence record](../agentic-runtime-preprint/V29_REVIEW.md)
