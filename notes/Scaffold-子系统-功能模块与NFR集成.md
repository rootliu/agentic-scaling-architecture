# Scaffold 子系统 - 功能模块与非功能需求集成设计

> **来源**: 2026-08-17 用户原话整理 + Obsidian 精读内容综合
> **类型**: 架构功能清单（Scaffold 层完整子系统）
> **状态**: 草稿 v0.1
> **定位**: Scaffold 层（L1 执行/隔离面）的功能模块定义与 NFR 集成梳理。与 [[Harness-Memory-子系统-显隐双轨设计]]（Harness 层）对偶，共同构成三层架构中"基础设施侧"的两份核心功能清单。
> **关联**: [[论文草稿-三层可扩展Agentic-Runtime-综合v0.2]] | [[AI智能体网络工业化脚手架研究]] | [[05-控制面与数据面正交切分]] | [[09-并行度与局部性协同设计]] | [[精读-Helium-高效Agent服务-2603.16104]] | [[精读-Policy-Driven-Runtime-Layer-2605.27744]] | [[精读-Five-Plane-运行时治理-2606.12320]] | [[精读-Tool-Forge-2605.28000]]

---

## 0. 核心定位

Scaffold 是 **L1 执行/隔离面（Execution / Isolation Plane）**，回答 agent 的四个物理问题：**在哪里跑、跑多少、跑多快、跑多安全**。

> **关键边界**：Scaffold 管"通不通、快不快、够不够、安不安全"（管道层），Harness 管"调什么、给谁、为什么"（逻辑层）。例如 Token 的逻辑路由（什么 Token、给哪个模型）归 Harness；Token API 的可用性、效率、聚合归 Scaffold。

**职责三分**（对 [[05-控制面与数据面正交切分]] 的复用）：

| 面 | Scaffold 层职责 | 负载特征 |
|---|---|---|
| **数据面 DP** | sandbox 执行、进程、I/O、serving 前向、KV cache 命中 | ∝ token/执行流量，高频 |
| **控制面 CP** | 实例调度、网络策略、凭证分配、准入审批、版本登记 | ∝ 状态事件，低频 |

---

## 1. 三大功能模块总览

```
Scaffold = ⟨ Sandbox 环境, API 路由管理, 管理体系 ⟩
```

| 模块 | 一句话定位 | 核心问题 | 来源 |
|---|---|---|---|
| **1. Sandbox 环境** | agent 的"数字工位" | 隔离执行、内置工具、监控、网络管控 | 用户输入 + S-01/S-06/S-07 |
| **2. API 路由管理** | Token 与 Tool Call 的"交通系统" | 双轨路由、聚合、拥塞控制、弹性伸缩 | 用户输入 + Helium/Policy-Driven |
| **3. 管理体系** | 治理与版本的"登记处" | VM 生命周期、准入审批、版本溯源 | 用户输入 + Tool Forge/Five-Plane |

---

## 2. 模块一：Sandbox 环境（隔离执行单元）

### 2.1 隔离基底（Isolation Substrate）

提供多种隔离等级的执行单元，按需选择：

| runtime_kind | 隔离强度 | 冷启动 | 适用场景 |
|---|---|---|---|
| **microVM** | 强（硬件级虚拟化） | < 500ms（快照 < 100ms） | 长任务、不可信代码、需要完整 OS |
| container | 中（命名空间/cgroup） | 秒级 | 可信工具链、快速原型 |
| WASM sandbox | 中强（内存安全） | 毫秒级 | 轻量计算、跨平台分发 |
| OS process | 弱 | 毫秒级 | 内部可信进程 |

关键机制：**快速扩展与快速销毁**（create/pause/resume/snapshot/fork/terminate/GC 全生命周期），支持从快照秒级恢复大量并发实例。对应 [[论文草稿-三层可扩展Agentic-Runtime-综合v0.2]] §4.1 的 isolation substrate spec 与 S-01/S-06。

### 2.2 内置接口（Built-in Interfaces）

Sandbox 出厂即带、无需 agent 自行装配的接口：

| 接口类 | 内容 | 对应架构组件 |
|---|---|---|
| **Memory 访问接口** | 访问 [[Harness-Memory-子系统-显隐双轨设计]] 的显性 memory 查询 API（query/search/summarize） | Harness Memory（显性轨） |
| **Data Substrate 访问接口** | D₁ on-policy 取数 API、D₂ semantic-join 查询接口 | 数据子系统 𝒟 三阶记忆 |
| **Harness 工具集** | web search、file search、code interpreter 等常用工具的预装调用（详见 2.2.1 工具清单） | Harness tool registry |
| **凭证注入** | secret 按需注入（env/file/broker），least privilege，capability attenuation | credentials/IAM |

> 设计要点：内置接口保证"开箱即用"，同时经 Harness 契约暴露--Skill 不直接绑定 shell/API/路径/凭证（P2 契约充分性的物理保障）。

#### 2.2.1 内置 Harness 工具清单（基于 2608.00101 生产级 trace 统计）

以下清单基于 GitHub Copilot 生产环境 775M 次工具调用的实证统计（`~/academy/2608.00101v1 Agentic Coding in the Wild`）：**40+ 种工具中，top 11 覆盖 90%+ 调用，top 27 覆盖 99%**，长尾 4.6% 为自定义工具。按功能与性能特征分为四类：

**A. 读取/检索类（Read & Search）--高频、低延迟、近零失败**

| 工具 | 功能 | 调用占比 | 中位延迟 | 成功率 |
|---|---|---|---|---|
| `get_file` | 读取单个文件内容 | **35.0%**（绝对第一） | 数十 ms | ~100% |
| `file_search` | 按文件名/模式查找文件 | top 5 | 数十 ms | ~100% |
| `code_search` | 代码语义/文本搜索 | top 5 | 数十 ms | ~100% |
| `get_symbols_by_name` | 按名称查符号（函数/类/定义） | top 11 | 数十 ms | ~100% |
| `get_files_in_proj` | 列出项目文件树 | top 15 | 数十 ms | ~100% |
| `get_projs_in_soln` | 列出解决方案中的项目 | top 15 | 数十 ms | ~100% |
| `get_errs` | 获取当前错误/诊断列表 | top 11 | 数十 ms | ~100% |

**B. 修改类（Mutation）--中频、中延迟、受文件系统约束**

| 工具 | 功能 | 调用占比 | 中位延迟 | 成功率 |
|---|---|---|---|---|
| `replace_string_in_file` | 单处字符串替换 | **9.8%**（第三） | 0.25–0.6s | 较高 |
| `multi_replace_string_in_file` | 多处批量替换 | top 11 | 0.25–0.6s | 较高 |
| `apply_patch` | 应用代码补丁 | top 11 | 0.25–0.6s | 较高 |
| `create_file` | 创建新文件 | top 11 | 0.25–0.6s | 较高 |
| `edit_file` | 编辑文件（行级） | top 11 | 0.25–0.6s | ~73% 偏低 |

**C. 执行类（Execution）--低频、重尾、失败率高**

| 工具 | 功能 | 调用占比 | 中位延迟 | 均值延迟 | 成功率 |
|---|---|---|---|---|---|
| `run_command_in_terminal` | 执行任意终端命令 | **17.0%**（第二） | 数百 ms–数秒 | **68s** | ~73% |
| `run_build` | 构建项目 | top 5 | 数秒 | **78s** | ~73% |
| `run_tests` | 运行测试 | top 15 | 数秒 | 重尾 | ~73% |

**D. 元/编排类（Meta & Orchestration）**

| 工具 | 功能 | 特征 |
|---|---|---|
| `update_plan_progress` | 更新任务计划进度 | top 11，数十 ms，近乎零失败 |

**对 Sandbox 设计的四点实证启示**：

1. **读取类是性能底盘**：get_file 一家占 35%，读取/检索类合计过半调用且延迟仅数十 ms--Sandbox 的内置工具必须把这类工具做到亚百毫秒（本地 FS/索引直连），否则拖垮全局
2. **执行类是延迟重尾之源**：run_command/run_build 均值 68–78s、P99 达数百秒，中位数却只有数百 ms--近 100× 的均值/中位差说明**长任务必须异步化 + 超时熔断 + 资源可回收**，不能同步阻塞
3. **失败放大效应**：失败调用比成功调用 P95 长 48×（run_command）；失败 build 注入 7–8× token（编译器诊断日志）；9% 的 turn 因失败重试消耗 4× 算力--**liveness 监控（§2.3）与非 LLM API 轨的排队/重试策略（§3.2）必须把失败重试的雪崩效应纳入设计**
4. **长尾自定义工具**：4.6% 调用来自自定义工具，印证准入管理（§4.2）需要支持"agent 自带工具"的注册与验证通道，而非仅预置清单

### 2.3 Liveness 监控（活性检测）

内置监控代理，回答"sandbox 还活着吗、健康吗"：

- **心跳机制**：sandbox 内置 watchdog，周期上报心跳；miss N 次 -> 判定失联
- **资源水位**：CPU/内存/磁盘/网络的使用率实时采集，超阈告警
- **进程级探活**：关键进程（工具服务、监控代理）的健康检查
- **僵尸检测**：识别"活着但挂死"（进程在但无响应）的状态，触发重启/回收
- **级联处理**：sandbox 失联 -> 上报管理体系 -> 决策重建/迁移 -> 通知受影响 agent

对应 spec 表的 observability 项（trace id、tool log、resource usage、replay evidence）。

### 2.4 网络访问控制（Network Policy）

内外网分级管控，**未授权网段不可达**：

```
network_policy:
  egress: deny_all | allowlist | unrestricted
  allowlist: [域名/IP/CIDR 列表]
  网段策略:
    - 公网（互联网）: 按角色 allowlist 放行（如 web search 代理）
    - 内网（企业系统）: 按租户/项目放行
    - 敏感网段（如财务网段）: 默认全拒，仅经内置代理接口白名单访问
  DNS/Proxy: 强制经代理，记录 egress 日志
  rate limit: 每 sandbox 出站带宽/请求数上限
```

**关键规则**：财务等敏感网段**不可被未内置接口的 agent 通过 sandbox 网络直接访问**--必须经 Scaffold 预置的受控代理（带审计、限流、权限校验），这正是 Five-Plane 治理中 Network Plane 的落地点。

### 2.5 依赖版本显式声明（Dependency Manifest）

Sandbox 自身的升级与适配**必须显式声明、可追溯**：

```yaml
ScaffoldManifest:
  os: { distribution: "ubuntu-24.04", kernel: "6.8" }       # OS 与内核
  runtime: { python: "3.12.4", node: "22.x", golang: "1.23" } # 编程工具版本
  dependencies:                                              # 系统依赖
    - { name: ffmpeg, version: "7.0", source: apt }
  harness_tools:                                             # 内置工具版本
    - { name: web_search, version: "2.1" }
  upgrade_policy: { channel: stable|canary, window: "低峰期" }
  compat_matrix:                                             # 与上游兼容性
    - { harness_api: ">=1.4", memory_schema: "v3" }
```

升级原则：**不可变镜像 + 版本化快照**（升级 = 换镜像而非原地改），保证同版本 agent 复现一致性；灰度发布（canary 先行）；兼容性矩阵声明与 Harness API/Skill 的匹配关系。呼应 P14 跨模型稳定性在物理层的对偶。

---

## 3. 模块二：API 路由管理（双轨路由）

### 3.1 LLM API 轨（Token 管道路由）

**职责边界**：不判断 Token 的逻辑行为（路由给什么模型是 Harness 的决策），只管 Token 管道层--可用性、效率、速度、聚合。

| 子功能 | 说明 | 机制 |
|---|---|---|
| **多 Provider 可用性探测** | 周期健康检查各 provider 的 token API：是否可用、限流状态、配额余量 | 主动拨测 + 被动失败统计；可用性分数实时更新 |
| **效率与速度计量** | 每 provider 的 TTFT、tokens/s、p95 延迟、错误率、成本 | 请求级打点，滚动窗口统计 |
| **多 Agent 聚合（cache 共享）** | 多个同类 agent 的请求**聚合到同一 provider 会话/prefix**，共享 KV cache | prefix routing：相同 system prompt/工具 schema 的请求路由到同 serving 实例，cache 命中率 H↑（对应 [[09-并行度与局部性协同设计]] P11） |
| **可用性广播** | 让 agent 知道"哪些 token API 现在可用、可用性如何" | 可用性面板 API，Harness 组装 context 时查询注入 |
| **Provider 故障切换** | 主 provider 异常 -> 备用 provider 接管 | 熔断 + 自动 failover，切换 < 5s（S-05） |
| **纯日志记录** | 路由决策、延迟、失败、切换事件全记录--**是日志不是 memory** | append-only log，供事后查询/审计/计费，不参与语义推理 |

> 关键区分：LLM API 轨的记录是**纯日志**（log），不是 memory--不做语义总结、不进三阶记忆、仅供查询。语义层面的沉淀（如"这个 provider 最近质量差"的经验）归 Harness D₃ governance memory。

**与 Helium 的对应**：proactive caching（预填缓存）+ cache-aware scheduling（缓存感知调度）正是本轨的核心技术；Helium 的 1.56x 加速证明 workflow 级缓存复用是吞吐杠杆。

### 3.2 非 LLM API 轨（Tool Call 路由与资源调度）

**职责**：当**同时起几千几万个 agent** 时，tool call API 如何冗余部署、如何路由、如何不拥塞、如何弹性扩缩。

| 子功能 | 说明 | 机制 |
|---|---|---|
| **API 冗余部署** | 同一 tool API 多副本部署，消除单点 | 多实例池 + 健康检查摘除 |
| **路由与负载均衡** | 海量 tool call 请求分发到健康副本 | 一致性哈希 / 最少连接 / 基于亲和性（seed affinity，M4） |
| **拥塞控制与排队** | 高峰期请求排队，防雪崩 | 令牌桶限流、优先级队列、backpressure（反压）、幂等去重（相同请求合并） |
| **动态扩容（调云接口）** | 排队超阈 -> 调用云接口扩充 API 实例/算力 | 弹性伸缩策略：队列深度 + 预测流量触发 scale-out；对接 cloud integration（S-05） |
| **及时释放** | 低谷期/任务结束后释放多余资源 | 闲置超时回收、scale-in 冷却期防抖动、终态 agent 资源 GC |
| **请求合并** | 多 agent 的相同 tool call 聚合 | result memoization（Policy-Driven 九策略之一）：相同参数的调用共享结果 |

**排队机制设计**（借鉴 S-08 Serving Capacity Scheduling）：

```
queue_policy:
  priority: [interactive > batch > background]   # 交互式优先
  backpressure: 队列深度 > 阈值时向上游反压（降低 agent 并行度或暂缓派生）
  dedup: { key: hash(tool_id, params), ttl: 60s }  # 短时幂等合并
  autoscale:
    trigger: { queue_depth_pps: 100, wait_p95_ms: 2000 }
    action: cloud_api.scale_out(replicas += ceil(deficit))
  release:
    idle_timeout: 300s          # 副本闲置 5 分钟回收
    scale_in_cooldown: 120s     # 回收冷却，防抖动
```

> 关键设计律：**扩展速度与治理能力同步进化**（不能只扩不管）。扩容动作本身要受管理体系（§4）的配额与审批约束。

---

## 4. 模块三：管理体系（治理与版本）

### 4.1 VM/Sandbox 生命周期管理

常规基础设施管理：

- **实例池管理**：预热池（warm pool）、快照池，平衡冷启动延迟与资源占用
- **调度与放置**：seed 亲和（同种子 co-locate 复用镜像/热缓存）+ 异种反亲和（spread 降争用）--对应 [[09-并行度与局部性协同设计]] M4/P12
- **配额管理**：CPU/GPU/Token/Storage/Network 租户级配额、burst 控制、优先级抢占（G-04：配额遵守率 100%、burst 响应 < 500ms、无饥饿）
- **回收与 GC**：终态实例资源回收、孤儿资源检测、快照清理

### 4.2 Tool/Skill 准入管理（Admission Control）

**外部引入的 tool/skill 必须过准入关卡**，避免引入不恰当能力：

```
准入流程:
  1. 发布者核验（publisher verification）
     - 来源核验：官方发布/签名校验/checksum 比对
     - 发布者信誉：历史记录、组织认证
  2. 内部审批流程（internal approval）
     - 提交：能力描述、依赖清单、权限申请（credential scopes）
     - 审批：按风险等级分级（低风险自动、高风险人工）
     - 记录：审批人、时间、依据，全留痕
  3. 沙箱验证（sandbox validation）
     - 在隔离 sandbox 中实跑测试集，产出 validation evidence
     - 对应 Tool Forge capsule: intent/capability contract/implementation/
       dependency policy/tests/docs/validation evidence/lifecycle state
  4. 编目登记（catalog registration）
     - 生命周期状态: draft -> verified -> approved -> deprecated
     - 凭证绑定: credential bindings 显式声明
```

**组合风险防线**（来自 [[精读-Benign-in-Isolation-技能组合风险-2606.15242]]）：单独无害 ≠ 组合无害。准入不仅评估孤立工件，还需评估 **activated path（激活路径）** 级风险：

| 组合风险 | 攻击面 | 准入防线 |
|---|---|---|
| **SCR-CapFlow**（能力流） | 组合后能力越权扩散（攻击成功率 33.6%） | capability containment 不变量校验 |
| **SCR-TrustLift**（信任提升） | 信任沿 skill 链非法提升（>96.5% 成功率） | no trust escalation 校验 |
| **SCR-AuthBlur**（授权混淆） | 授权上下文被污染（风险审批 +71.8%） | auth isolation 校验 |

### 4.3 Agent 版本管理（Version Registry）

回答"agent 在扩展时调用的是哪个版本的什么东西"：

- **版本登记**：agent 定义（prompt/skill 组合/配置）、tool/skill 包、sandbox 镜像、依赖清单，全部版本化登记
- **绑定快照**：一次 agent 部署 = 一份**不可变版本组合快照**（agent def v2.3 + skill A v1.1 + sandbox image ubuntu-24.04-py312 + ...）
- **调用溯源**：运行时每次调用记录实际使用的版本；扩展（fork 出的第 N 个 agent）继承并可追溯到母版本
- **回滚支持**：版本快照保留，支持快速回滚到历史组合
- **漂移检测**：运行版本 vs 声明版本不一致时告警（防静默漂移）

与 [[10-Skill-as-Code与确定性固化]] 的关系：P14 让 skill 输出与模型版本解耦（时间维稳定）；版本管理让 agent 调用与工件版本解耦可追溯（物理维稳定）。

### 4.4 企业身份与云集成（Enterprise Integration）

来自 S-04/S-05 的治理基座：

| 组件 | 内容 | 指标 |
|---|---|---|
| **SSO/Identity** | OIDC/SAML 2.0 联合登录、SCIM 同步、RBAC/ABAC、租户隔离、JIT 授权 | SSO 成功率 > 99.9%、越权 = 0 |
| **Cloud Integration** | Workload Identity（免静态密钥）、KMS、对象存储、VPC/PrivateLink、模型端点 | 密钥泄漏面 = 0、故障切换 < 5s |
| **Security Policy** | syscall filter、path/network policy、malware scan、prompt/tool boundary 统一下发 | 阻断模式 violation = 0、审计完整 100% |

---

## 5. 非功能需求（NFR）集成梳理

### 5.1 NFR 总矩阵

Scaffold 层 NFR 按"模块 × 需求类别"集成，每格绑定可量化指标：

| NFR 类别 | Sandbox 环境 | API 路由管理 | 管理体系 | 可证伪验证 |
|---|---|---|---|---|
| **性能/延迟** | 冷启动 < 500ms；快照恢复 < 100ms | TTFT p95 < 2s；tool call p95 < 3s | 准入审批 SLA | S-01/S-02 基准 |
| **吞吐** | 并发实例数；serving tokens/s | cache 聚合后吞吐 +6~14%（CacheSage 实测） | - | 并发扩展线性度 R² > 0.95 |
| **可用性** | liveness 检测 miss < N 跳 | provider 故障切换 < 5s；冗余副本无单点 | 版本回滚 RTO | 切换演练、混沌测试 |
| **可扩展性** | fork 冷启动 < 1s；scale-out 秒级 | 排队触发自动扩容；backpressure 防雪崩 | 配额 burst 响应 < 500ms | 1 -> 10000 agent 压测 |
| **安全性** | escape rate < 0.01%；敏感网段全拒 | API 凭证 least privilege | 准入越权 = 0；组合风险三不变量 | SCR-Bench 攻击测试 |
| **效率/成本** | 资源配额；闲置回收 | cache 命中率 H↑；请求 dedup/memoization；及时释放 | 版本复用减少重复验证 | token 效率比 > 2x（S-03） |
| **可观测性** | trace id、心跳、资源水位全覆盖 | 纯日志全记录（路由/延迟/失败） | 审计完整性 100% | replay 成功率 > 95%（G-02） |
| **合规/审计** | egress 日志、依赖声明 | 调用日志不可篡改 | 审批全留痕、版本可溯源 | 审计抽查通过率 |
| **版本/复现** | 不可变镜像、manifest 显式 | provider 版本记录 | 版本绑定快照、漂移检测 | 同版本重跑一致率 |

### 5.2 NFR 的分层归属

不是所有 NFR 都落在 Scaffold。按 [[05-控制面与数据面正交切分]] 的精神分层：

| NFR | 归属层 | 说明 |
|---|---|---|
| 隔离/逃逸/网络边界 | **Scaffold**（CP+DP） | 物理边界，Scaffold 独有 |
| 管道可用性/速度/聚合 | **Scaffold** | API 路由双轨的核心 |
| 准入/版本/审计 | **Scaffold**（CP） | 治理登记处 |
| 语义正确性/工具选择 | **Harness** | 逻辑判断不进 Scaffold |
| 语义沉淀/经验复用 | **Harness**（D₃） | Scaffold 只留纯日志 |
| 任务完成质量 | **Skill** | 业务层 |

> **核心设计律**：Scaffold 的 NFR 全部是**可测的物理指标**（毫秒、百分比、次数），不含语义判断。这保证 P1 解耦成立的前提--物理扩展（+X）提升 Θ(A) 而不触碰 𝒯(A)。

### 5.3 NFR 冲突与调和

典型冲突及调和策略：

| 冲突 | 调和 |
|---|---|
| 快速扩容 vs 准入审批慢 | 预批准工具池 + 高风险才人工审批；warm pool 预热 |
| cache 聚合（省成本） vs 路由自由（低延迟） | prefix routing 优先同 provider 聚合，延迟超阈才跨 provider |
| 及时释放 vs 冷启动代价 | 快照恢复（< 100ms）让"销毁重建"成本接近零，敢放敢收 |
| 强隔离 vs 性能开销 | 分级隔离（microVM/WASM/process），按信任级选 runtime_kind |
| 资源独占（性能） vs 多租户公平 | 配额 + 优先级抢占 + fairness 策略（Policy-Driven 九策略之一） |

---

## 6. 与四条正交切分的映射

| 切分 | Scaffold 层体现 |
|---|---|
| **1. 扩展轴（逻辑/物理）** | Scaffold 是物理扩展（+X）的唯一载体；三大模块中 Sandbox/API 轨主扩吞吐，管理体系保扩展有序 |
| **2. 平面切分（CP/DP）** | §0 职责三分表；API 路由的探测/广播在 CP，请求搬运在 DP |
| **3. 数据子系统** | Sandbox 内置 D₁/D₂ 查询接口；API 轨纯日志与三阶记忆的边界（日志 ≠ memory） |
| **4. 并行/局部性** | seed 亲和调度（M4/P12）；LLM API 轨的 cache 聚合即 P11 前缀冻结命中的系统侧实现 |

---

## 7. 与相关论文的机制对应

| 论文 | 借用机制 | 落在 Scaffold 哪里 |
|---|---|---|
| **Helium**（2603.16104） | proactive caching、cache-aware scheduling、workflow 级复用 | LLM API 轨的聚合与缓存 |
| **Policy-Driven Runtime Layer**（2605.27744） | observe/score/predict/act 四原语；fairness、memoization、safety enforcement 九策略 | API 路由双轨的策略接入点 |
| **Five-Plane 治理**（2606.12320） | Network/Identity/Endpoint/Data 四执行面；stop-anywhere mediation；capability attenuation | 网络管控、准入管理、凭证注入 |
| **Tool Forge**（2605.28000） | tool capsule（validation evidence/lifecycle/credential binding）；intent-scoped 路由 | 准入管理的工件形态；API 轨的按需暴露 |
| **Benign in Isolation**（2606.15242） | activated path 级评估；三类组合不变量 | 准入管理的组合风险防线 |
| **Dynamic Runtime Graphs**（2603.22386） | template/realized-graph/trace 三分 | 版本管理（template）/实例调度（graph）/纯日志（trace） |

---

## 8. 开放问题

1. **日志与 memory 的精确分界**：API 轨纯日志何时升级为 Harness D₃ 治理经验？（候选：人工/策略显式触发迁移，不自动）
2. **跨 Scaffold 的 cache 聚合边界**：聚合到什么粒度（prompt 前缀/工具 schema/会话）收益最优？需实验
3. **敏感网段代理的性能损耗**：受控代理引入的额外延迟是否可接受（目标 < 50ms，S-05 标准）
4. **版本爆炸治理**：agent × skill × sandbox 镜像的组合版本数如何管理（语义化版本 + 兼容矩阵自动推导）
5. **非 LLM API 轨的全局视图**：几千 agent 分散在多集群时，排队与扩容决策需要多少全局信息（完全局最优 vs 本地近似）
