/* Generates 3 figures × 2 languages (EN/ZH) as standalone SVG + HTML.
   Audience: FIRST-TIME readers.
     Fig 1 (Layers)      — each box explains WHAT THE LAYER IS FOR (plain language).
     Fig 2 (Specs)       — each box holds a readable SPEC LIST.
     Fig 3 (Agent loop)  — a NUMBERED WALKTHROUGH of how the loop works.
   Geometry is defined once per figure and shared across languages (pixel-identical
   layout); only text differs, given as explicit line arrays so nothing overflows.
   Connectors use dedicated lanes; no arrow crosses a box, text, or another arrow. */
const fs = require("fs");
const path = require("path");
const OUT = __dirname;
const FIGDIR = path.join(OUT, "figures");
fs.mkdirSync(FIGDIR, { recursive: true });

const W = 1200, H = 860;

const C = {
  skillFill:"#e6f4ec", skillStroke:"#1a7d52", skillText:"#11603d",
  harnFill:"#ece4fb", harnStroke:"#6d3fd4", harnText:"#4f2da0", harnStrong:"#f4eeff",
  scafFill:"#fbe7d3", scafStroke:"#bc5a16", scafText:"#9a4d12",
  dataFill:"#ddeff8", dataStroke:"#1474a6", dataText:"#0f5e87",
  neutFill:"#fffdf8", neutStroke:"#cabfa8", ink:"#221f1a", mut:"#6b6357",
  page:"#fffdf8", grid:"#efe8db", badge:"#ffffff",
};

const esc = s => String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
function rect(x,y,w,h,{fill="#fff",stroke=C.neutStroke,sw=1.4,rx=12,dash=null,op=1,filter=true}={}){
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"`
    +(dash?` stroke-dasharray="${dash}"`:"")+` opacity="${op}"`+(filter?` filter="url(#sh)"`:"")+`/>`;
}
function tline(x,y,t,{size=13,fill=C.ink,weight=400,anchor="start",mono=false}={}){
  const ff=mono?` font-family="ui-monospace,Menlo,monospace"`:"";
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}" font-weight="${weight}" fill="${fill}"${ff}>${esc(t)}</text>`;
}
function center(cx,cy,lines,{size=13,fill=C.ink,weight=400,lh=null}={}){
  lh=lh||Math.round(size*1.4); const y0=cy-(lines.length-1)*lh/2;
  return lines.map((t,i)=>`<text x="${cx}" y="${y0+i*lh}" text-anchor="middle" dominant-baseline="middle" font-size="${size}" font-weight="${weight}" fill="${fill}">${esc(t)}</text>`).join("");
}
function leftLines(x,yTop,lines,{size=12.5,fill=C.ink,weight=400,lh=null}={}){
  lh=lh||Math.round(size*1.5);
  return lines.map((t,i)=>`<text x="${x}" y="${yTop+i*lh}" text-anchor="start" font-size="${size}" font-weight="${weight}" fill="${fill}">${esc(t)}</text>`).join("");
}
function bullets(x,yTop,items,{size=12,fill=C.ink,lh=21,marker="•",mcol=null}={}){
  mcol=mcol||fill;
  return items.map((t,i)=>{
    const y=yTop+i*lh;
    return `<text x="${x}" y="${y}" font-size="${size}" fill="${mcol}" font-weight="700">${marker}</text>`
      +`<text x="${x+15}" y="${y}" font-size="${size}" fill="${fill}">${esc(t)}</text>`;
  }).join("");
}
const vArrow=(x,y1,y2,{stroke=C.harnStroke,sw=2.1,head="a"}={})=>`<path d="M${x} ${y1} L${x} ${y2}" fill="none" stroke="${stroke}" stroke-width="${sw}" marker-end="url(#${head})"/>`;
const hArrow=(x1,x2,y,{stroke=C.harnStroke,sw=2.1,head="a"}={})=>`<path d="M${x1} ${y} L${x2} ${y}" fill="none" stroke="${stroke}" stroke-width="${sw}" marker-end="url(#${head})"/>`;
const elbow=(pts,{stroke=C.harnStroke,sw=2,head="a",dash=null}={})=>`<path d="M${pts.map(p=>p[0]+" "+p[1]).join(" L")}" fill="none" stroke="${stroke}" stroke-width="${sw}"`+(dash?` stroke-dasharray="${dash}"`:"")+` marker-end="url(#${head})"/>`;
function badge(cx,cy,n,col){
  return `<circle cx="${cx}" cy="${cy}" r="16" fill="${col}" stroke="#fff" stroke-width="2"/>`
    +`<text x="${cx}" y="${cy+1}" text-anchor="middle" dominant-baseline="middle" font-size="15" font-weight="800" fill="#fff">${n}</text>`;
}
function defs(){
  const m=(id,f)=>`<marker id="${id}" markerWidth="11" markerHeight="11" refX="7.5" refY="3.6" orient="auto"><path d="M0,0 L7.5,3.6 L0,7.2 Z" fill="${f}"/></marker>`;
  return `<defs>
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="${C.grid}" stroke-width="1"/></pattern>
    <filter id="sh" x="-12%" y="-12%" width="124%" height="124%"><feDropShadow dx="0" dy="3" stdDeviation="4.5" flood-color="#3c2d14" flood-opacity=".11"/></filter>
    ${m("a",C.harnStroke)}${m("g",C.skillStroke)}${m("o",C.scafStroke)}${m("t",C.dataStroke)}${m("k",C.mut)}
  </defs>`;
}
function frame(title,sub){
  return `<rect width="${W}" height="${H}" rx="20" fill="${C.page}"/>`
    +`<rect width="${W}" height="${H}" rx="20" fill="url(#grid)" opacity=".7"/>`
    +tline(54,52,title,{size:23,weight:800})
    +tline(54,80,sub,{size:13.5,fill:C.mut});
}
const svgWrap=inner=>`<svg viewBox="0 0 ${W} ${H}" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',Arial,sans-serif">${defs()}${inner}</svg>`;

/* ===================================================================
   FIGURE 1 — LAYERS (what each layer is FOR)
   =================================================================== */
const D1 = {
  en:{
    title:"The Three Layers — What Each One Is For",
    sub:"A first look: an AI agent is built from three stacked layers, plus a data subsystem on the side.",
    bands:[
      {col:"skill",tag:"L3",name:"Skills  —  “What to do”",
       what:["Holds the job descriptions for tasks: the goal, the input/output format,","and the rules for when to act, when to stop, and when to loop."],
       analogy:"Like an employee’s playbook / SOP.", scale:"Add a Skill  →  the agent can do one more kind of task  (logical scaling)"},
      {col:"harn",tag:"L2",name:"Harness  —  “How the work gets done”",
       what:["Turns a Skill’s intent into concrete, runnable steps. Manages memory,","context, tools, code generation, safety checks and audit logs."],
       analogy:"Like a project manager + the runtime framework.", scale:"The single place where Skills and Scaffold meet  (the decoupling point)"},
      {col:"scaf",tag:"L1",name:"Scaffold  —  “Where it runs, safely”",
       what:["Provides the isolated place to execute: sandbox, shell, network,","storage and model-serving capacity, with security boundaries."],
       analogy:"Like a secure cloud computer.", scale:"Add an instance  →  more throughput  (physical scaling)"},
    ],
    dh:"Data Subsystem 𝒟",
    dsub:"What the agent knows about your data (kept off to the side, mostly offline)",
    ditems:["D₁  fetch — read the slice you need, on demand","D₂  semantic summary — pre-digest sources offline","D₃  governance — remember how to use the data","D₄  lifetime — freshness, scope & cost budget","Ω   workspace — run history, artifacts, LLM wiki"],
    foot:"Key idea: each kind of growth (more skills / more machines / more data) is added on a different axis, so they don’t slow each other down.",
  },
  zh:{
    title:"三个层 — 每一层是干什么的",
    sub:"第一眼认识：一个 AI agent 由三个层叠起来，旁边再加一个数据子系统。",
    bands:[
      {col:"skill",tag:"L3",name:"Skills  —  “要做什么”",
       what:["存放任务的“岗位说明书”：目标、输入/输出格式，","以及何时行动、何时停止、何时循环的规则。"],
       analogy:"就像员工的工作手册 / SOP。", scale:"加一个 Skill → 多一种能做的任务（逻辑扩展）"},
      {col:"harn",tag:"L2",name:"Harness  —  “怎么把活干成”",
       what:["把 Skill 的意图翻译成可执行的步骤。管理记忆、上下文、","工具、代码生成、安全检查与审计日志。"],
       analogy:"就像项目经理 + 运行时框架。", scale:"Skills 与 Scaffold 唯一相遇的地方（解耦点）"},
      {col:"scaf",tag:"L1",name:"Scaffold  —  “在哪里安全地跑”",
       what:["提供隔离的执行环境：sandbox、shell、网络、存储","与模型 serving 算力，并带安全边界。"],
       analogy:"就像一台安全的云电脑。", scale:"加一个实例 → 多一份吞吐（物理扩展）"},
    ],
    dh:"数据子系统 𝒟",
    dsub:"agent 对你数据的认知（放在一旁，主要离线）",
    ditems:["D₁  取数 — 按需只读你要的那一片","D₂  语义总结 — 离线把数据源预消化","D₃  治理记忆 — 记住“该怎么用这份数据”","D₄  lifetime — 时新性、口径与成本预算","Ω   工作区 — 运行历史、产物、LLM wiki"],
    foot:"关键点：每一种增长（更多 skill / 更多机器 / 更多数据）加在不同的轴上，因此互不拖累。",
  }
};
function fig1(t){
  const colmap={skill:[C.skillFill,C.skillStroke,C.skillText],harn:[C.harnFill,C.harnStroke,C.harnText],scaf:[C.scafFill,C.scafStroke,C.scafText]};
  const LX=56, LW=740;
  const ys=[112,300,488], BH=172;
  let s=frame(t.title,t.sub);
  t.bands.forEach((b,i)=>{
    const [f,st,tc]=colmap[b.col]; const y=ys[i];
    s+=rect(LX,y,LW,BH,{fill:f,stroke:st,sw:1.7,rx:16});
    s+=rect(LX+18,y+18,52,30,{fill:"#fff",stroke:st,sw:1.4,rx:8,filter:false});
    s+=tline(LX+44,y+39,b.tag,{size:16,weight:800,fill:tc,anchor:"middle"});
    s+=tline(LX+86,y+39,b.name,{size:17,weight:800,fill:tc});
    s+=leftLines(LX+24,y+74,b.what,{size:12.5,fill:tc,lh:19});
    s+=tline(LX+24,y+126,b.analogy,{size:12,weight:700,fill:st});
    s+=rect(LX+18,y+138,LW-36,24,{fill:"#fff",stroke:st,sw:1,rx:7,op:.85,filter:false});
    s+=tline(LX+28,y+155,b.scale,{size:11.5,weight:700,fill:tc});
  });
  // arrows between bands (right-of-text lane to avoid covering body text)
  const ax=LX+LW-40;
  s+=vArrow(ax,ys[0]+BH,ys[1],{stroke:colmap.harn[1]});
  s+=vArrow(ax,ys[1]+BH,ys[2],{stroke:colmap.scaf[1],head:"o"});
  // data column
  const DX=820, DW=324, DY=112, DH2=548;
  s+=rect(DX,DY,DW,DH2,{fill:C.dataFill,stroke:C.dataStroke,sw:1.7,rx:16});
  s+=tline(DX+22,DY+34,t.dh,{size:16,weight:800,fill:C.dataText});
  s+=leftLines(DX+22,DY+58,wrap(t.dsub,DW-44,11.5),{size:11.5,fill:"#3d7a99",lh:16});
  s+=bullets(DX+24,DY+118,t.ditems,{size:11.5,fill:C.dataText,lh:24,marker:"›",mcol:C.dataStroke});
  // footer
  s+=rect(LX,672,DX+DW-LX,80,{fill:"#f7f2e8",stroke:C.neutStroke,sw:1.3,rx:14,dash:"7 6",filter:false});
  s+=leftLines(LX+24,706,wrap(t.foot,DX+DW-LX-48,13.5),{size:13.5,weight:600,fill:C.ink,lh:21});
  return svgWrap(s);
}

/* ===================================================================
   FIGURE 2 — SPECS (a readable list inside each box)
   =================================================================== */
const D2 = {
  en:{
    title:"What Each Layer Actually Contains — the Spec Lists",
    sub:"The concrete, buildable pieces in every layer. Grounded in real formats: Anthropic SKILL.md, MCP tools, Claude Code, OpenAI connectors.",
    l3:{name:"L3 · Skills",note:"SkillSpec — Anthropic SKILL.md format",items:["name + description (when to use)","input / output schema","output format + constraints","call / stop / loop conditions","examples (shots) + anti-examples","personalization + verification"]},
    l2:{name:"L2 · Harness",note:"CapabilityCapsule — MCP-grounded",
      colA:["CapabilityCapsule: inputSchema · contract · invariants","tool routing (intent-scoped, top-k)","context assembly (shots · schema · memory)","code generation (Read/Edit/Bash + test/lint)"],
      colB:["tool synthesis (sandbox-validated capsule)","memory maintenance M (compaction · writeback","   · reflection · retrieval · GC)","reward / verifier + policy gate + audit log"]},
    l1:{name:"L1 · Scaffold",note:"ExecutionSpec — isolation & resources",
      colA:["isolation: microVM · container · wasm","bash / process / filesystem","network: allowlist · egress policy"],
      colB:["SSO / identity: OIDC · SAML · SCIM · RBAC","cloud: AWS/GCP/Azure · KMS · S3 · PrivateLink","serving (KV cache · batching) · lifecycle · obs."]},
    d:{name:"Data Subsystem 𝒟",items:["D₁ DataSourceCard — source · auth · quota · NFR","D₂ SemanticSummary — schema* · relations · themes","D₃ DataUsageSkill — sources · join plan · runs","D₄ Lifetime — freshness · retention · budget","Ω  Workspace — RunTrace · ArtifactManifest · LLM Wiki"]},
  },
  zh:{
    title:"每一层里到底装了什么 — Spec 清单",
    sub:"每层可落地、可构建的具体部件。对齐真实格式：Anthropic SKILL.md、MCP tools、Claude Code、OpenAI connectors。",
    l3:{name:"L3 · Skills",note:"SkillSpec — Anthropic SKILL.md 格式",items:["name + description（何时使用）","input / output schema","output format + 约束","call / stop / loop 条件","examples（shots）+ 反例","个性化 + verification"]},
    l2:{name:"L2 · Harness",note:"CapabilityCapsule — 以 MCP 为底座",
      colA:["CapabilityCapsule：inputSchema · contract · invariants","工具路由（intent-scoped, top-k）","context 组装（shots · schema · memory）","code generation（Read/Edit/Bash + test/lint）"],
      colB:["tool synthesis（沙箱验证的 capsule）","记忆维护 M（compaction · writeback","   · reflection · retrieval · GC）","reward / verifier + policy gate + 审计日志"]},
    l1:{name:"L1 · Scaffold",note:"ExecutionSpec — 隔离与资源",
      colA:["隔离：microVM · container · wasm","bash / process / filesystem","网络：allowlist · egress 策略"],
      colB:["SSO / 身份：OIDC · SAML · SCIM · RBAC","云：AWS/GCP/Azure · KMS · S3 · PrivateLink","serving（KV cache · batching）· lifecycle · 观测"]},
    d:{name:"数据子系统 𝒟",items:["D₁ DataSourceCard — source · auth · quota · NFR","D₂ SemanticSummary — schema* · relations · themes","D₃ DataUsageSkill — sources · join plan · runs","D₄ Lifetime — freshness · retention · budget","Ω  工作区 — RunTrace · ArtifactManifest · LLM Wiki"]},
  }
};
function fig2(t){
  const LX=56, LW=740;
  let s=frame(t.title,t.sub);
  // L3
  let y=112,h=132;
  s+=rect(LX,y,LW,h,{fill:C.skillFill,stroke:C.skillStroke,sw:1.7,rx:16});
  s+=tline(LX+24,y+30,t.l3.name,{size:16,weight:800,fill:C.skillText});
  s+=tline(LX+24,y+50,t.l3.note,{size:11.5,weight:700,fill:C.skillStroke});
  s+=bullets(LX+28,y+74,t.l3.items.slice(0,3),{size:11.5,fill:C.skillText,lh:20,mcol:C.skillStroke});
  s+=bullets(LX+390,y+74,t.l3.items.slice(3),{size:11.5,fill:C.skillText,lh:20,mcol:C.skillStroke});
  // L2
  y=270;h=188;
  s+=rect(LX,y,LW,h,{fill:C.harnFill,stroke:C.harnStroke,sw:1.7,rx:16});
  s+=tline(LX+24,y+30,t.l2.name,{size:16,weight:800,fill:C.harnText});
  s+=tline(LX+24,y+50,t.l2.note,{size:11.5,weight:700,fill:C.harnStroke});
  s+=bullets(LX+28,y+78,t.l2.colA,{size:11.5,fill:C.harnText,lh:24,mcol:C.harnStroke});
  s+=bullets(LX+390,y+78,t.l2.colB,{size:11.5,fill:C.harnText,lh:24,mcol:C.harnStroke});
  // L1
  y=484;h=164;
  s+=rect(LX,y,LW,h,{fill:C.scafFill,stroke:C.scafStroke,sw:1.7,rx:16});
  s+=tline(LX+24,y+30,t.l1.name,{size:16,weight:800,fill:C.scafText});
  s+=tline(LX+24,y+50,t.l1.note,{size:11.5,weight:700,fill:C.scafStroke});
  s+=bullets(LX+28,y+78,t.l1.colA,{size:11.5,fill:C.scafText,lh:24,mcol:C.scafStroke});
  s+=bullets(LX+390,y+78,t.l1.colB,{size:11.5,fill:C.scafText,lh:24,mcol:C.scafStroke});
  // arrows
  const ax=LX+LW-32;
  s+=vArrow(ax,112+132,270,{stroke:C.harnStroke});
  s+=vArrow(ax,270+188,484,{stroke:C.scafStroke,head:"o"});
  // data column
  const DX=820,DW=324,DY=112,DH2=536;
  s+=rect(DX,DY,DW,DH2,{fill:C.dataFill,stroke:C.dataStroke,sw:1.7,rx:16});
  s+=tline(DX+22,DY+34,t.d.name,{size:16,weight:800,fill:C.dataText});
  let yy=DY+70;
  t.d.items.forEach(it=>{
    const ln=wrap(it,DW-52,11.5);
    s+=`<text x="${DX+24}" y="${yy}" font-size="11.5" font-weight="700" fill="${C.dataStroke}">›</text>`;
    s+=leftLines(DX+40,yy,ln,{size:11.5,fill:C.dataText,lh:16});
    yy+=16*ln.length+14;
  });
  return svgWrap(s);
}

/* ===================================================================
   FIGURE 3 — AGENT LOOP WALKTHROUGH (numbered steps)
   =================================================================== */
const D3 = {
  en:{
    title:"How the Agent Works — a Step-by-Step Walkthrough",
    sub:"The Harness runs this loop. The LLM makes the choices; typed contracts, a policy gate and a verifier keep it safe and on track.",
    steps:[
      ["Understand the goal","Read the user’s request and constraints; figure out what “done” looks like."],
      ["Pick the skill","Choose the SkillSpec that fits and load its input/output schema."],
      ["Gather context","Pull in memory, relevant examples (shots) and the tools’ contracts."],
      ["Make a plan","The LLM drafts a plan with fallbacks and a clear stop condition."],
      ["Choose the next action","Pick the tool (O1), the model (O7) and the token budget (O8) for this step."],
      ["Check, then run","Policy gate checks scope & permissions, then it runs on Scaffold / queries Data."],
      ["Observe & score","Collect the result and evidence; a verifier / reward grades how good it is."],
      ["Good enough?","Yes → deliver the result.   No → reflect, revise the plan, and loop back to step 5."],
    ],
    scaf:["Scaffold","sandbox · shell · serving","filesystem · network · SSO/cloud"],
    data:["Data subsystem 𝒟","D₁/D₂ query · D₃/D₄ policy","Ω workspace evidence"],
    sysNote:"Running quietly in the background: System skills (M) compact, write back and retrieve memory between steps.",
    deliver:"Deliver artifact", retry:"reflect & loop back to 5",
  },
  zh:{
    title:"Agent 是怎么工作的 — 分步走查",
    sub:"Harness 运行这个循环。由 LLM 做选择；typed contract、policy gate 与 verifier 保证它安全、不跑偏。",
    steps:[
      ["读懂目标","读取用户的请求与约束；想清楚“做完”长什么样。"],
      ["挑选 skill","选出合适的 SkillSpec，加载它的输入/输出 schema。"],
      ["收集上下文","拉入记忆、相关示例（shots）和工具的契约。"],
      ["制定计划","LLM 起草带 fallback 和明确停止条件的计划。"],
      ["选择下一步动作","为这一步选 tool（O1）、模型（O7）和 token 预算（O8）。"],
      ["先检查，再执行","policy gate 校验范围与权限，然后在 Scaffold 执行 / 查询 Data。"],
      ["观察并打分","收集结果与证据；verifier / reward 给它打分。"],
      ["够好了吗？","够好 → 交付结果。   不够 → 反思、修订计划，回到第 5 步。"],
    ],
    scaf:["Scaffold","sandbox · shell · serving","filesystem · network · SSO/cloud"],
    data:["数据子系统 𝒟","D₁/D₂ 查询 · D₃/D₄ 策略","Ω workspace 证据"],
    sysNote:"在后台静默运行：System skills (M) 在步骤之间做记忆压缩、写回与检索。",
    deliver:"交付产物", retry:"反思并回到第 5 步",
  }
};
function fig3(t){
  let s=frame(t.title,t.sub);
  // central column of 8 numbered steps
  const BX=300, BW=520, x0=BX;
  const colTop=[C.skillStroke,C.skillStroke,C.dataStroke,C.harnStroke,C.harnStroke,C.harnStroke,C.harnStroke,C.scafStroke];
  const sy=108, sh=58, gap=14;
  const ys=[]; for(let i=0;i<8;i++) ys.push(sy+i*(sh+gap));
  // feedback lane (far left, x=150) drawn FIRST so boxes sit on top of nothing problematic
  const laneX=150;
  // boxes
  t.steps.forEach((st,i)=>{
    const y=ys[i], strong=(i===3||i===4||i===7);
    const col = (i===7)? C.scafStroke : C.harnStroke;
    s+=rect(BX,y,BW,sh,{fill:strong?C.harnStrong:"#fff",stroke:C.harnStroke,sw:strong?1.7:1.2,rx:13,filter:false});
    s+=badge(BX+30,y+sh/2,i+1,colTop[i]);
    s+=tline(BX+60,y+24,st[0],{size:13.5,weight:800,fill:C.harnText});
    s+=leftLines(BX+60,y+42,wrap(st[1],BW-78,10.8),{size:10.8,fill:C.mut,lh:13});
  });
  // down arrows between steps
  for(let i=0;i<7;i++) s+=vArrow(BX+BW/2,ys[i]+sh,ys[i+1],{stroke:C.harnStroke,sw:1.9});
  // input arrow from left into step 1
  s+=hArrow(laneX, BX, ys[0]+sh/2,{stroke:C.mut,sw:1.6,head:"k"});
  s+=tline(laneX-6, ys[0]+sh/2-10, t.title?"":"", {});
  // right-side Scaffold + Data, aligned to step 6
  const SX=874, SW=270;
  const y6=ys[5];
  s+=rect(SX,y6-40,SW,86,{fill:C.scafFill,stroke:C.scafStroke,sw:1.5,rx:13});
  s+=tline(SX+18,y6-16,t.scaf[0],{size:14,weight:800,fill:C.scafText});
  s+=tline(SX+18,y6+4,t.scaf[1],{size:10.8,fill:C.scafText});
  s+=tline(SX+18,y6+22,t.scaf[2],{size:10.8,fill:C.scafText});
  s+=rect(SX,y6+62,SW,86,{fill:C.dataFill,stroke:C.dataStroke,sw:1.5,rx:13});
  s+=tline(SX+18,y6+86,t.data[0],{size:14,weight:800,fill:C.dataText});
  s+=tline(SX+18,y6+106,t.data[1],{size:10.8,fill:"#3d7a99"});
  s+=tline(SX+18,y6+124,t.data[2],{size:10.8,fill:"#3d7a99"});
  // step6 -> scaffold (two-way style, single arrows to each)
  s+=elbow([[BX+BW,y6+sh/2-8],[SX,y6+3]],{stroke:C.scafStroke,sw:1.8,head:"o"});
  s+=elbow([[BX+BW,y6+sh/2+8],[845,y6+sh/2+8],[845,y6+105],[SX,y6+105]],{stroke:C.dataStroke,sw:1.8,head:"t"});
  // step8 decision -> deliver (right) and -> loop back (left lane to step5)
  const y8=ys[7];
  // deliver box bottom-right
  const DX=874,DY=ys[7]+0,DEW=270,DEH=58;
  s+=rect(DX,DY,DEW,DEH,{fill:"#eaf7f0",stroke:C.skillStroke,sw:1.5,rx:13,filter:false});
  s+=center(DX+DEW/2,DY+DEH/2,[t.deliver],{size:14,weight:800,fill:C.skillText});
  s+=hArrow(BX+BW,DX,y8+sh/2,{stroke:C.skillStroke,sw:1.9,head:"g"});
  // loop-back: step8 left edge -> far-left lane -> up -> into step5 left edge
  s+=elbow([[BX,y8+sh/2],[laneX,y8+sh/2],[laneX,ys[4]+sh/2],[BX,ys[4]+sh/2]],{stroke:C.scafStroke,sw:1.9,head:"o",dash:"6 5"});
  s+=tline(laneX+8, (y8+ys[4])/2, t.retry,{size:10.5,weight:700,fill:C.scafStroke});
  // system skills note (bottom band)
  const NY=ys[7]+96;
  s+=rect(BX,NY,SW+ (SX-BX),48,{fill:"#f1ebe0",stroke:C.harnStroke,sw:1.2,rx:12,dash:"6 6",filter:false});
  s+=leftLines(BX+18,NY+29,wrap(t.sysNote,SW+(SX-BX)-36,11.5),{size:11.5,fill:C.harnText,lh:15});
  return svgWrap(s);
}

/* simple width-aware wrap (CJK by char, latin by word) */
function wrap(text,maxw,size){
  const cjk=/[一-鿿]/.test(text);
  const cw=cjk?size*1.02:size*0.55;
  const per=Math.max(6,Math.floor(maxw/cw));
  if(cjk){const out=[];for(let i=0;i<text.length;i+=per)out.push(text.slice(i,i+per));return out;}
  const words=text.split(" ");const out=[];let cur="";
  for(const w of words){ if((cur+" "+w).trim().length<=per)cur=(cur+" "+w).trim();else{if(cur)out.push(cur);cur=w;} }
  if(cur)out.push(cur);return out;
}

/* ---------- emit ---------- */
const FIGS={f1:fig1,f2:fig2,f3:fig3}, DICT={f1:D1,f2:D2,f3:D3};
const standalone=(svg,lang)=>`<!DOCTYPE html><html lang="${lang}"><head><meta charset="UTF-8">
<style>@page{size:${W}px ${H}px;margin:0}html,body{margin:0;padding:0;background:${C.page}}#p{width:${W}px;height:${H}px}#p svg{display:block;width:${W}px;height:${H}px}</style></head>
<body><div id="p">${svg}</div></body></html>`;
const built={};
for(const k of Object.keys(FIGS)){ built[k]={};
  for(const lang of ["en","zh"]){
    const svg=FIGS[k](DICT[k][lang]); built[k][lang]=svg;
    fs.writeFileSync(path.join(FIGDIR,`${k}-${lang}.svg`),svg);
    fs.writeFileSync(path.join(FIGDIR,`${k}-${lang}.html`),standalone(svg,lang==="en"?"en":"zh-CN"));
  }
}
console.log("figures written to",FIGDIR);

/* ===================================================================
   FULL ARCHITECTURE PAGES (self-contained, embed the 3 figures + prose)
   =================================================================== */
const PAGE = {
  en:{
    lang:"en", htmllang:"en",
    brand:"Agentic Runtime",
    title:"Three-Layer Scalable Agentic Runtime",
    lead:"A reference architecture for production AI agents — <b>A = ⟨S, H, X⟩</b> plus an out-of-stack data subsystem <b>𝒟</b>. The core claim: an agent’s <b>logical</b>, <b>physical</b> and <b>data</b> scaling can be decoupled, and the decoupling point is the explicit contract layer (the Harness).",
    intro:"This page is a first-time reader’s tour. It walks through the three layers, what each layer actually contains, and how the agent loop runs — then states the falsifiable claims that make this a research position, not just an engineering diagram.",
    secs:[
      {n:"1", h:"The Three Layers — what each one is for", fig:"f1",
       p:[ "An agent is built from three stacked layers. <b>Skills</b> say <i>what</i> to do (the task playbook). <b>Harness</b> decides <i>how</i> the work gets done (it turns intent into runnable steps, and owns memory, context, tools, code generation, safety and audit). <b>Scaffold</b> is <i>where</i> it runs safely (an isolated sandbox with shell, network, storage and model-serving).",
            "The trick is that each kind of growth is added on a different axis: add a <b>Skill</b> and the agent can do one more kind of task (logical scaling); add a <b>Scaffold</b> instance and you get more throughput (physical scaling). Because they only ever meet at the Harness contract, they don’t slow each other down. External <b>data</b> grows on yet another axis through the side subsystem 𝒟." ]},
      {n:"2", h:"What lives in each layer — the spec lists", fig:"f2",
       p:[ "Every layer is made of concrete, buildable pieces. We deliberately ground them in formats that already exist in the wild, so the architecture is an extension layer rather than a new protocol: <b>Skills</b> use the Anthropic <code>SKILL.md</code> format; the <b>Harness</b> capability object is grounded in <b>MCP</b> tool schemas and Claude-Code-style tools; the <b>Scaffold</b> spec covers isolation plus enterprise <b>SSO</b> and <b>cloud</b> integration.",
            "Two things are worth pointing out for builders. First, <b>code generation</b> (Read/Edit/Bash + test/lint) is distinct from <b>tool synthesis</b> (promote validated code into a reusable capsule). Second, <b>system skills</b> (memory compaction, write-back, reflection, retrieval, GC) live inside the Harness — they maintain the runtime, so they are not user-facing Skills." ]},
      {n:"3", h:"How the agent works — a step-by-step walkthrough", fig:"f3",
       p:[ "The Harness runs a loop. The <b>LLM makes the choices</b> — it plans, picks the next tool (<b>O1</b>), selects the model for the step (<b>O7</b>) and allocates the token budget (<b>O8</b>) — while typed contracts, a policy gate and a verifier keep it safe and on track. This is what we call a <b>probabilistic control plane</b> (claim N0): the decisions are LLM-driven, so they must be constrained by audit logs and invariants.",
            "Each step is checked before it runs, executed on the Scaffold or sent as a query to the data subsystem, then scored by a verifier/reward. If the score is good enough the artifact is delivered; otherwise the agent reflects, revises the plan and loops back. Quietly in the background, system skills keep memory compact and relevant between steps." ]},
    ],
    claimsH:"The falsifiable core",
    claims:[
      ["C5","Logical and physical scaling are <b>orthogonal</b>, with the Harness contract as the decoupling point."],
      ["P1","Adding Skills doesn’t drag down throughput (∂Θ/∂|S|≈0); adding Scaffold doesn’t change coverage (∂𝒯/∂|X|=0)."],
      ["N0","The control plane is <b>probabilistic</b> (LLM-driven) and is made trustworthy by audit logs + invariants."],
      ["P3","Adding a Skill must preserve safety invariants — benign-in-isolation skills can be harmful in composition."],
    ],
    propsH:"All nine falsifiable propositions",
    propsCols:["#","Axis","In one line","Falsified if"],
    props:[
      ["P1","Scaling","∂Θ/∂|S|≈0 and ∂𝒯/∂|X|=0 (orthogonal)","adding Skills clearly drags down throughput"],
      ["P2","Scaling","a well-defined contract H ⇒ S and X have no direct dependency","bypassing H still keeps them decoupled"],
      ["P3","Scaling","Inv(S) ⇒ Inv(S∪{s}) (composition stays safe)","composed skills escalate privilege / break an invariant"],
      ["P4","Plane","∂L_CP/∂τ̇ ≈ 0 (traffic doesn’t inflate control cost)","higher QPS inflates control-plane cost proportionally"],
      ["P5","Plane","logical→control plane, physical→data plane","both act on the same plane"],
      ["P6","Plane","maintenance M: trigger in CP, cost in DP","M trigger frequency scales with business traffic"],
      ["P7","Data","fixed use case ⇒ ∂ℓ/∂|src| ≈ 0","adding a data source raises per-request token cost"],
      ["P8","Data","off-policy summary Σ balances coverage and precision","Σ beats neither live discovery nor manual metadata"],
      ["P9","Data","data-usage skill makes fetch decisions converge","repeated use cases keep diverging / oscillating"],
    ],
    novH:"What is genuinely new (novelty ledger)",
    novCols:["#","Claim","The gap it fills"],
    nov:[
      ["C5","Logical/physical scaling decoupled, with the Harness contract as the seam","no 2026 work splits scalability into two orthogonal axes bound to different layers"],
      ["N0","A probabilistic control plane (LLM-driven decisions + audit/invariant guardrails)","classic SDN/K8s control planes push deterministic config"],
      ["N1","Off-policy, schema-on-read semantic summaries of data sources","fills the middle path left open by ‘Do Agents Need Semantic Metadata?’"],
      ["N2","Data governance as a reusable skill, not just boundary enforcement","governance work only does compliance enforcement"],
      ["N5","Skills split three ways: task / system / data-usage","existing skill surveys don’t treat data-usage as its own class"],
    ],
    figcaps:{f1:"Figure 1 — the three layers and what each is for.",f2:"Figure 2 — the spec list inside each layer.",f3:"Figure 3 — the agent loop, step by step."},
    foot:"Discussion draft · 2026-06-28 · companion to the synthesized paper draft v0.3.",
    other:"ZH",
    otherHref:"arch-zh.html",
  },
  zh:{
    lang:"zh", htmllang:"zh-CN",
    brand:"Agentic Runtime",
    title:"三层可扩展 Agentic Runtime",
    lead:"面向生产级 AI agent 的参考架构 —— <b>A = ⟨S, H, X⟩</b>，外挂一个栈外数据子系统 <b>𝒟</b>。核心主张：agent 的<b>逻辑扩展</b>、<b>物理扩展</b>与<b>数据扩展</b>可以解耦，解耦点是显式契约层（Harness）。",
    intro:"本页是面向第一次接触者的导览：先走过三个层，再看每一层里到底装了什么，最后讲清楚 agent loop 如何运行 —— 并给出让它成为“研究主张”而非“工程图”的可证伪命题。",
    secs:[
      {n:"1", h:"三个层 — 每一层是干什么的", fig:"f1",
       p:[ "一个 agent 由三层叠成。<b>Skills</b> 说明<i>要做什么</i>（任务手册）；<b>Harness</b> 决定<i>怎么把活干成</i>（把意图翻译成可执行步骤，并掌管记忆、上下文、工具、代码生成、安全与审计）；<b>Scaffold</b> 是<i>在哪里安全地跑</i>（带 shell、网络、存储与模型 serving 的隔离 sandbox）。",
            "关键在于：每一种增长加在不同的轴上 —— 加一个 <b>Skill</b>，多一种能做的任务（逻辑扩展）；加一个 <b>Scaffold</b> 实例，多一份吞吐（物理扩展）。因为它们只在 Harness 契约处相遇，所以互不拖累。外部<b>数据</b>则在旁边的子系统 𝒟 上沿第三条轴增长。" ]},
      {n:"2", h:"每一层里装了什么 — Spec 清单", fig:"f2",
       p:[ "每一层都由可落地、可构建的部件组成。我们刻意把它们对齐到业界已有的格式，使本架构成为“扩展层”而非新协议：<b>Skills</b> 采用 Anthropic 的 <code>SKILL.md</code> 格式；<b>Harness</b> 的能力对象以 <b>MCP</b> tool schema 与 Claude Code 风格工具为底座；<b>Scaffold</b> 的 spec 覆盖隔离以及企业 <b>SSO</b> 与<b>云</b>集成。",
            "对工程实现有两点值得强调。其一，<b>code generation</b>（Read/Edit/Bash + test/lint）与 <b>tool synthesis</b>（把验证过的代码升级为可复用 capsule）是两件事。其二，<b>system skills</b>（记忆压缩、写回、反思、检索、GC）位于 Harness 内部 —— 它们维护 runtime 自身，因此不是面向用户的 Skill。" ]},
      {n:"3", h:"Agent 是怎么工作的 — 分步走查", fig:"f3",
       p:[ "Harness 运行一个循环。由 <b>LLM 做选择</b> —— 它制定计划、选下一个工具（<b>O1</b>）、为该步选模型（<b>O7</b>）、分配 token 预算（<b>O8</b>）—— 同时 typed contract、policy gate 与 verifier 保证它安全、不跑偏。这就是我们说的<b>概率性控制面</b>（命题 N0）：决策由 LLM 驱动，因此必须用审计日志 + 不变量来约束。",
            "每一步先被检查再执行：在 Scaffold 上运行，或作为查询发往数据子系统，然后由 verifier/reward 打分。够好就交付产物；否则 agent 反思、修订计划并回到循环。后台里，system skills 在步骤之间持续保持记忆的精简与相关。" ]},
    ],
    claimsH:"可证伪的内核",
    claims:[
      ["C5","逻辑扩展与物理扩展<b>正交</b>，Harness 契约是解耦点。"],
      ["P1","加 Skills 不拖垮吞吐（∂Θ/∂|S|≈0）；加 Scaffold 不改变覆盖（∂𝒯/∂|X|=0）。"],
      ["N0","控制面是<b>概率性</b>的（LLM 驱动），靠审计日志 + 不变量使其可信。"],
      ["P3","加 Skill 必须保持安全不变量 —— 单独 benign 的 skill 组合后可能有害。"],
    ],
    propsH:"九条可证伪命题",
    propsCols:["#","维度","一句话","证伪条件"],
    props:[
      ["P1","扩展轴","∂Θ/∂|S|≈0 且 ∂𝒯/∂|X|=0（正交）","加 Skills 明显拖垮吞吐"],
      ["P2","扩展轴","良定义契约 H ⇒ S 与 X 无直接依赖","旁路 H 后仍保持解耦"],
      ["P3","扩展轴","Inv(S) ⇒ Inv(S∪{s})（组合仍安全）","组合后越权 / 破坏不变量"],
      ["P4","平面","∂L_CP/∂τ̇ ≈ 0（流量不放大控制开销）","QPS 升高同比放大控制面开销"],
      ["P5","平面","逻辑→控制面，物理→数据面","二者作用于同一平面"],
      ["P6","平面","维护 M：触发在 CP，开销在 DP","M 触发频率随业务流量增长"],
      ["P7","数据","固定 use case ⇒ ∂ℓ/∂|src| ≈ 0","加数据源抬高单请求 token 成本"],
      ["P8","数据","off-policy 摘要 Σ 兼顾覆盖与精度","Σ 既不优于在线发现也不优于人工元数据"],
      ["P9","数据","data-usage skill 使取数决策收敛","重复 use case 仍发散 / 震荡"],
    ],
    novH:"真正的新意（创新点登记）",
    novCols:["#","主张","填补的空白"],
    nov:[
      ["C5","逻辑/物理扩展解耦，Harness 契约即接缝","2026 无工作把可扩展性拆成绑定不同层的两条正交轴"],
      ["N0","概率性控制面（LLM 驱动决策 + 审计/不变量护栏）","经典 SDN/K8s 控制面下发确定性配置"],
      ["N1","对数据源做 off-policy、schema-on-read 的语义摘要","填补《Do Agents Need Semantic Metadata?》留空的折中路"],
      ["N2","数据治理即可复用 skill，而非只做边界 enforcement","治理类工作只做合规 enforcement"],
      ["N5","skill 三分：task / system / data-usage","现有 skill 综述未把 data-usage 当独立一类"],
    ],
    figcaps:{f1:"图 1 — 三个层及各自的用途。",f2:"图 2 — 每一层里的 spec 清单。",f3:"图 3 — agent loop 的分步走查。"},
    foot:"讨论稿 · 2026-06-28 · 配套综合论文草稿 v0.3。",
    other:"English",
    otherHref:"arch-en.html",
  }
};
function pageHTML(P){
  const card=(fig,cap)=>`<figure class="fig">${built[fig][P.lang]}<figcaption>${cap}</figcaption></figure>`;
  const secs=P.secs.map(s=>`
  <section class="sec">
    <h2><span class="num">${s.n}</span>${s.h}</h2>
    ${s.p.map(x=>`<p>${x}</p>`).join("\n    ")}
    ${card(s.fig,P.figcaps[s.fig])}
  </section>`).join("\n");
  const claims=P.claims.map(c=>`<div class="claim"><span class="tag">${c[0]}</span><p>${c[1]}</p></div>`).join("");
  const tbl=(cols,rows,kind)=>`<table class="tbl ${kind}"><thead><tr>${cols.map(c=>`<th>${c}</th>`).join("")}</tr></thead><tbody>${
    rows.map(r=>`<tr>${r.map((cell,i)=>i===0?`<td class="id">${cell}</td>`:`<td>${cell}</td>`).join("")}</tr>`).join("")}</tbody></table>`;
  return `<!DOCTYPE html><html lang="${P.htmllang}"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${P.title}</title>
<style>
  :root{--ink:#221f1a;--mut:#6b6357;--page:#fffdf8;--card:#ffffff;--line:#e7dfce;
        --skill:#1a7d52;--harn:#6d3fd4;--scaf:#bc5a16;--data:#1474a6;}
  *{box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{margin:0;background:var(--page);color:var(--ink);
       font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',Arial,sans-serif;
       line-height:1.7;-webkit-font-smoothing:antialiased}
  .wrap{max-width:1080px;margin:0 auto;padding:0 28px}
  nav{position:sticky;top:0;z-index:10;background:rgba(255,253,248,.86);backdrop-filter:saturate(1.4) blur(8px);
      border-bottom:1px solid var(--line)}
  nav .wrap{display:flex;align-items:center;gap:18px;height:56px}
  nav .brand{font-weight:800;letter-spacing:.2px}
  nav a{margin-left:auto;color:var(--harn);text-decoration:none;font-weight:700;font-size:14px;
        border:1px solid var(--harn);padding:6px 14px;border-radius:999px}
  header{padding:60px 0 30px}
  .kicker{color:var(--harn);font-weight:800;letter-spacing:2px;font-size:12px;text-transform:uppercase}
  h1{font-size:42px;line-height:1.12;margin:.3em 0 .35em}
  .lead{font-size:19px;color:#3a352c;max-width:880px}
  .intro{font-size:15px;color:var(--mut);max-width:880px;margin-top:14px}
  .sec{padding:30px 0;border-top:1px solid var(--line)}
  h2{font-size:25px;margin:.2em 0 .6em;display:flex;align-items:center;gap:14px}
  .num{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;border-radius:11px;
       background:var(--harn);color:#fff;font-size:19px;font-weight:800}
  .sec p{font-size:15.5px;max-width:900px;margin:.5em 0}
  code{background:#f1ebdd;padding:1px 6px;border-radius:5px;font-size:.92em}
  .fig{margin:24px 0 6px;padding:14px;background:var(--card);border:1px solid var(--line);
       border-radius:18px;box-shadow:0 6px 22px rgba(60,45,20,.07)}
  .fig svg{display:block;width:100%;height:auto;border-radius:10px}
  figcaption{margin-top:10px;text-align:center;color:var(--mut);font-size:13px}
  .claims{padding:34px 0 10px;border-top:1px solid var(--line)}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:14px}
  .claim{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;display:flex;gap:14px}
  .claim .tag{flex:0 0 auto;font-weight:800;color:#fff;background:var(--data);border-radius:9px;
              padding:5px 11px;height:fit-content;font-size:14px}
  .claim p{margin:0;font-size:14.5px}
  .th{font-size:19px;font-weight:800;margin:.2em 0 .7em}
  .tbl{width:100%;border-collapse:collapse;font-size:14px;background:var(--card);
       border:1px solid var(--line);border-radius:12px;overflow:hidden}
  .tbl th{background:#f3ecff;color:var(--harn);text-align:left;font-weight:800;padding:10px 14px;font-size:13px}
  .tbl td{padding:9px 14px;border-top:1px solid var(--line);vertical-align:top}
  .tbl td.id{font-weight:800;color:var(--data);white-space:nowrap}
  .tbl tbody tr:nth-child(even){background:#fbf8f1}
  footer{padding:40px 0 70px;color:var(--mut);font-size:13.5px;border-top:1px solid var(--line);margin-top:20px}
  @media (max-width:720px){h1{font-size:32px}.grid{grid-template-columns:1fr}.tbl{font-size:12.5px}}
</style></head>
<body>
<nav><div class="wrap"><span class="brand">${P.brand}</span>
  <a href="index.html" style="border:none;color:var(--mut);margin-left:auto;padding-right:4px">${P.lang==="en"?"Full site":"完整站点"}</a>
  <a href="dry-run-${P.lang}.html" style="border:none;color:var(--harn);padding-right:4px">${P.lang==="en"?"Dry Run":"Dry Run 走查"}</a>
  <a href="${P.otherHref}">${P.other}</a></div></nav>
<header class="wrap">
  <div class="kicker">Reference Architecture</div>
  <h1>${P.title}</h1>
  <p class="lead">${P.lead}</p>
  <p class="intro">${P.intro}</p>
</header>
<main class="wrap">
${secs}
  <section class="claims">
    <h2><span class="num">★</span>${P.claimsH}</h2>
    <div class="grid">${claims}</div>
  </section>
  <section class="sec">
    <h3 class="th">${P.propsH}</h3>
    ${tbl(P.propsCols,P.props,"props")}
  </section>
  <section class="sec">
    <h3 class="th">${P.novH}</h3>
    ${tbl(P.novCols,P.nov,"nov")}
  </section>
</main>
<footer class="wrap">${P.foot}</footer>
</body></html>`;
}
for(const lang of ["en","zh"]){
  fs.writeFileSync(path.join(OUT,`arch-${lang}.html`), pageHTML(PAGE[lang]));
}
console.log("pages written: arch-en.html, arch-zh.html");

/* ===================================================================
   DRY RUN PAGE — data-driven examples (AI4Science is the first).
   Add more examples to EXAMPLES[lang] later; the selector renders them all.
   =================================================================== */
const EXAMPLES = {
  en: [
    {
      id:"ai4science", tag:"AI4Science",
      name:"Perovskite band-gap screening",
      goal:"From the latest literature, compute-screen perovskite candidates with a target band gap (~1.3 eV) and produce a report with citations and a reproducible script.",
      why:"Exercises all three layers + the data subsystem at once: literature (D2 temporal summaries), known-property DB (D1 fetch), simulation (code-gen + Scaffold + cloud/HPC), multi-signal verification (numeric sanity + citation grounding), report (doc skill), write-back (D2/Ω/D3).",
      layers:[
        ["L3 Skills","lit-review.skill · materials-screening.skill · data-report.skill (each with I/O schema, call/stop/loop, verification)"],
        ["L2 Harness","capsules: arxiv_search · materials_db_query(D1) · code_execution · dft_screen(may be live-coded) · doc_generation; + context assembly / policy gate / verifier / audit / maintenance M"],
        ["L1 Scaffold","ExecutionSpec: microVM(scripts) + GPU serving(models) + cloud(HPC for screening) + SSO/identity(institutional HPC) + network allowlist(Materials Project / arXiv)"],
        ["D1","DataSourceCard: Materials Project API · OQMD · arXiv"],
        ["D2","temporally-constrained SummaryEntry (“band-gap SOTA as of T”, with evidence_ref) in a structured DB"],
        ["D3","DataUsageSkill: source selection + join plan + top-k weights for the perovskite-screening use case"],
        ["D4","lifetime: literature freshness (as-of date) · property-DB conventions · HPC budget"],
        ["Ω","RunTrace · screening script/result artifacts · IntermediateRelation(candidate↔property↔paper) · LLM Wiki"],
      ],
      phases:[
        {h:"Phase 0 · Intake (CP)", steps:[
          ["01","parse_intent(U)","parse goal / constraints / done-criteria"],
          ["02","O4 plan","decompose sub-goals {lit → candidates → properties → screen → analyze → report}"],
        ]},
        {h:"Phase 1 · Skill activation (CP)", steps:[
          ["03","activate lit-review","required_data_themes = [perovskite, bandgap]"],
          ["04","activate materials-screening","required_capabilities = [materials_db_query, code_execution, dft_screen]"],
          ["05","activate data-report","output_format = report{citations required}"],
        ]},
        {h:"Phase 2 · Context assembly (CP→DP)", steps:[
          ["06","consult D3.DataUsageSkill","get preferred_sources + semantic_join_plan(top_k, weights)"],
          ["07","consult D4.lifetime","get freshness(as_of=today) + HPC nfr_budget"],
          ["08","query D2.semantic_join(valid_at=today)","DP online: fetch temporally-constrained SummaryEntry, each with evidence_ref"],
          ["09","O2 shots + O3 output schema","shots ← D2 pos/neg examples; schema ← SkillSpec"],
        ]},
        {h:"Phase 3 · Capability routing + resources (CP)", steps:[
          ["10","O1 tool selection","capsules {arxiv_search, materials_db_query, code_execution, doc_generation}"],
          ["11","O5 live-coding (if dft_screen missing)","synthesize capsule → sandbox-validate → register"],
          ["12","O7 model + O8 token","plan/analysis = Opus-tier; bulk lit triage = Haiku-tier; allocate token budget"],
          ["13","policy gate + ExecutionSpec","SSO → institutional HPC; cloud = GPU pool; network allowlist = [MP, arXiv]"],
        ]},
        {h:"Phase 4 · Execution loop (DP — per sub-goal)", steps:[
          ["14","execute arxiv_search","skip if already covered by a shared D2 summary (less re-digestion)"],
          ["15","execute D1.materials_db_query","DP online fetch: candidate properties from MP"],
          ["16","O5 code generation","Read/Edit/Bash write screening script + run tests/lint"],
          ["17","execute dft_screen","on Scaffold (cloud HPC microVM)"],
          ["18","observe + verifier/reward","① numeric sanity (band-gap physical range/units) ② citation grounding (every claim has evidence_ref)"],
          ["19","if verify fails → O6 reflect","non-physical band gap / unverifiable claim → revise plan → back to 14/16"],
        ]},
        {h:"Phase 5 · Output + write-back (CP/DP)", steps:[
          ["20","execute doc_generation","report artifact (citations + reproducible script)"],
          ["21","writeback (M) → D2","new SummaryEntry {claim, valid_from=T, evidence_ref=run_id} — logical append, no overwrite"],
          ["22","write RunTrace + IntermediateRelation → Ω",""],
          ["23","distill DataUsageSkill → D3","this run's winning sources/weights/fallbacks (P9 convergence)"],
        ]},
      ],
      invariants:[
        ["[06–08] precede [14]","query D3/D4/D2 first; a shared-summary hit avoids re-pulling the source → less inter-agent contention, lower per-request cost (P7)"],
        ["[10–13] go through the Harness contract","a Skill only declares required_capabilities; H translates intent 𝓘 → executable 𝓔 (P2)"],
        ["[21] is logical append + evidence_ref","overflow demotes (cold-tier), never hard-deletes; old claims stay back-traceable to source → anti-hallucination (§4.4.1 S3/S4)"],
      ],
      diagram:[
        "                      ┌──── offline off-policy loop 𝓛₂ (out-of-stack, not scheduled by H) ─────┐",
        " external sources     │  arXiv / journals / MP snapshot ─▶ D2.summarize ─▶ SummaryEntry{claim,  │",
        " (papers, MP, OQMD) ──┼─▶                                  (schema-on-read)  valid_from/to,     │",
        "                      │                                                  evidence_ref, supersedes}│",
        "                      │                                          └─▶ Structured Summary DB        │",
        "                      │                                             (index: source / theme / valid)│",
        "                      └──────────────────────────────────────────────────────────────────────────┘",
        "                                                                        │ ▲",
        "               semantic_join(valid_at=T, top_k)                         │ │ writeback [21] (append)",
        "                              ▼                                         │ │",
        " ┌ L3 Skills ─┐  intent/specs  ┌──── L2 Harness (contract / control plane) ┴─┴────┐",
        " │ lit-review  │ ──[03-05]────▶ │ context assembly ← D2 summary / D3 usage / D4    │",
        " │ materials   │               │ O1 route · O5 code-gen · O7 model · O8 token · ver│",
        " │ data-report │ ◀─report schema│ policy gate ──▶ translate 𝓘 → 𝓔                  │",
        " └─────────────┘               └───┬───────────────────────────────┬──────────────┘",
        "      ▲ deliver artifact            │ executable 𝓔                   │ D1 fetch (online)",
        "      │                             ▼                                ▼",
        "      │                 ┌ L1 Scaffold (data plane) ┐        ┌ D1 Fetch API ┐",
        "      │                 │ microVM·bash·GPU serving  │        │ MP / OQMD    │",
        "      │                 │ cloud HPC · SSO · network │        └──────┬───────┘",
        "      │                 └────────────┬──────────────┘               │ property slice",
        "      │  RunTrace/artifact [22]      │ results + evidence            │",
        "      └─────────────── Ω workspace ◀─┴───────────────────────────────┘",
        "                       (RunTrace · IntermediateRelation: cand↔property↔paper · LLM Wiki)",
        "                                  │",
        "                                  └─▶ D3 DataUsageSkill update [23]  (fetch-decision entropy ↓, P9)",
      ],
      reading:[
        "Two separate data paths — offline 𝓛₂ pre-digests raw papers/DBs into temporally-constrained SummaryEntries (off the request path → adding sources doesn't raise per-request token cost, P7); online does only D2.semantic_join (shared summaries) + D1.query (live properties), both through the Harness contract.",
        "The summary DB is a shared read-only hot spot — many agents / runs read the same SummaryEntry (snapshot reads) instead of each re-pulling the same PDF → contention removed, repeated inference saved (AOHP-style token ↓); retrieval uses the valid-interval index for point-in-time filtering.",
        "Write-back is one-way & logical-append — results → Ω → distilled into new SummaryEntries fed back to D2 (with evidence_ref; old entries logically invalidated, not deleted) + D3 updates. A closed loop: offline summarize → online consume → execute → feed back, with every recallable claim back-traceable to source.",
      ],
    },
  ],
  zh: [
    {
      id:"ai4science", tag:"AI4Science",
      name:"钙钛矿带隙筛选",
      goal:"基于最新文献，计算筛选目标带隙(~1.3 eV)的钙钛矿候选材料，并产出带引用与可复现脚本的报告。",
      why:"同时压满三层 + 数据子系统：文献(→D2 时序摘要)、已知物性库(→D1 取数)、仿真计算(→code gen + Scaffold + cloud/HPC)、多信号验证(数值合理性 + 引用接地)、报告(→doc skill)、回写(→D2/Ω/D3)。",
      layers:[
        ["L3 Skills","lit-review.skill · materials-screening.skill · data-report.skill（各含 I/O schema、call/stop/loop、verification）"],
        ["L2 Harness","capsule：arxiv_search · materials_db_query(D1) · code_execution · dft_screen(可能 live-code) · doc_generation；+ context assembly / policy gate / verifier / audit / 维护子系统 M"],
        ["L1 Scaffold","ExecutionSpec：microVM(脚本) + GPU serving(模型) + cloud(HPC 跑筛选) + SSO/identity(机构 HPC) + network allowlist(Materials Project / arXiv)"],
        ["D1","DataSourceCard：Materials Project API · OQMD · arXiv"],
        ["D2","带时序约束的 SummaryEntry（“截至 T 的带隙 SOTA”，带 evidence_ref）存结构化 DB"],
        ["D3","DataUsageSkill：perovskite-screening 用例的源选择 + join plan + top-k 权重"],
        ["D4","lifetime：文献时新性(as-of 日期) · 物性库口径 · HPC 预算"],
        ["Ω","RunTrace · 筛选脚本/结果 artifact · IntermediateRelation(候选↔物性↔文献) · LLM Wiki"],
      ],
      phases:[
        {h:"阶段 0 · Intake（CP）", steps:[
          ["01","parse_intent(U)","解析目标 / 约束 / 做完判据"],
          ["02","O4 plan","分解 sub-goals {文献 → 候选 → 取物性 → 筛选 → 分析 → 报告}"],
        ]},
        {h:"阶段 1 · Skill 激活（CP）", steps:[
          ["03","activate lit-review","required_data_themes = [perovskite, bandgap]"],
          ["04","activate materials-screening","required_capabilities = [materials_db_query, code_execution, dft_screen]"],
          ["05","activate data-report","output_format = report{引用必填}"],
        ]},
        {h:"阶段 2 · Context 组装（CP→DP）", steps:[
          ["06","consult D3.DataUsageSkill","取 preferred_sources + semantic_join_plan(top_k, weights)"],
          ["07","consult D4.lifetime","取 freshness(as_of=今日) + HPC nfr_budget"],
          ["08","query D2.semantic_join(valid_at=今日)","DP 在线：取带时序约束 SummaryEntry，每条带 evidence_ref"],
          ["09","O2 shots + O3 output schema","shots ← D2 正反例；schema ← SkillSpec"],
        ]},
        {h:"阶段 3 · 能力路由 + 资源就绪（CP）", steps:[
          ["10","O1 tool 选择","capsule {arxiv_search, materials_db_query, code_execution, doc_generation}"],
          ["11","O5 live-coding（若缺 dft_screen）","合成 capsule → sandbox 验证 → 注册"],
          ["12","O7 model + O8 token","plan/分析 = Opus 级；海量文献初筛 = Haiku 级；分发 token 预算"],
          ["13","policy gate + ExecutionSpec","SSO 授权机构 HPC；cloud = GPU pool；network allowlist = [MP, arXiv]"],
        ]},
        {h:"阶段 4 · 执行循环（DP — 逐 sub-goal）", steps:[
          ["14","execute arxiv_search","D2 已覆盖则跳过(命中共享摘要) → 减少重复消化"],
          ["15","execute D1.materials_db_query","DP 在线取数：MP 候选集物性"],
          ["16","O5 code generation","Read/Edit/Bash 写筛选脚本 + 跑测试/lint"],
          ["17","execute dft_screen","在 Scaffold(cloud HPC microVM)"],
          ["18","observe + verifier/reward","① 数值合理性(带隙物理区间/单位) ② 引用接地(每条结论有 evidence_ref)"],
          ["19","验证失败 → O6 reflect","带隙非物理 / 结论 unverifiable → revise plan → 回 14/16"],
        ]},
        {h:"阶段 5 · 产出 + 回写（CP/DP）", steps:[
          ["20","execute doc_generation","report artifact(含引用、可复现脚本)"],
          ["21","writeback(M) → D2","新 SummaryEntry {claim, valid_from=T, evidence_ref=run_id} — 逻辑追加，不覆盖"],
          ["22","write RunTrace + IntermediateRelation → Ω",""],
          ["23","distill DataUsageSkill → D3","本次成功源/权重/失败回退（P9 收敛）"],
        ]},
      ],
      invariants:[
        ["[06–08] 先于 [14]","先查 D3/D4/D2；命中共享摘要就不重拉原文 → 减少多 agent 争用、降单请求成本（P7）"],
        ["[10–13] 经 Harness 契约","Skill 只声明 required_capabilities；H 翻译意图 𝓘 → 可执行 𝓔（P2）"],
        ["[21] 逻辑追加 + evidence_ref","溢出降冷不硬删；旧结论可回指原文 → 防幻觉（§4.4.1 S3/S4）"],
      ],
      diagram:[
        "                      ┌──── 离线 off-policy loop 𝓛₂（栈外，不被 H 调度）─────┐",
        " 外部源               │  arXiv / 期刊 / MP 快照 ─▶ D2.summarize ─▶ SummaryEntry{claim, │",
        " (papers, MP, OQMD) ──┼─▶                         (schema-on-read)  valid_from/to,      │",
        "                      │                                          evidence_ref, supersedes}│",
        "                      │                                       └─▶ 【结构化摘要 DB】       │",
        "                      │                                          (索引: source/theme/valid)│",
        "                      └──────────────────────────────────────────────────────────────────┘",
        "                                                                     │ ▲",
        "            semantic_join(valid_at=T, top_k)                         │ │ writeback [21] (逻辑追加)",
        "                           ▼                                         │ │",
        " ┌ L3 Skills ─┐ intent/specs ┌──── L2 Harness（契约 / 控制面）────────┴─┴────┐",
        " │ lit-review  │ ─[03-05]───▶ │ context assembly ← D2摘要 / D3用法 / D4时效    │",
        " │ materials   │             │ O1路由 · O5 code-gen · O7 model · O8 token · ver│",
        " │ data-report │ ◀─报告schema─│ policy gate ──▶ 翻译 𝓘 → 𝓔                     │",
        " └─────────────┘             └───┬───────────────────────────────┬────────────┘",
        "      ▲ 交付 artifact             │ 可执行单元 𝓔                    │ D1 取数(在线)",
        "      │                          ▼                                ▼",
        "      │              ┌ L1 Scaffold（数据面）┐         ┌ D1 取数 API ┐",
        "      │              │ microVM·bash·GPU serving│       │ MP / OQMD 物性│",
        "      │              │ cloud HPC · SSO · network│      └──────┬───────┘",
        "      │              └────────────┬─────────────┘             │ 物性切片",
        "      │  RunTrace/artifact [22]   │ 计算结果 + evidence         │",
        "      └────────────── Ω 工作区 ◀──┴────────────────────────────┘",
        "                      (RunTrace · IntermediateRelation: 候选↔物性↔文献 · LLM Wiki)",
        "                                 │",
        "                                 └─▶ D3 DataUsageSkill 更新 [23]  (取数决策熵 ↓，P9)",
      ],
      reading:[
        "两条数据路径分离 — 离线 𝓛₂ 把原始文献/库预消化成带时序约束的 SummaryEntry（不在请求路径上 → 加数据源不抬单请求 token 成本，P7）；在线只做 D2.semantic_join(读共享摘要) + D1.query(读实时物性)，都经 Harness 契约。",
        "摘要 DB 是共享只读热点 — 多 agent / 多次运行读同一份 SummaryEntry(快照读)，不各自重拉同一篇 PDF → 消除争用、省重复推理(AOHP 同类机理 token↓)；检索靠 valid 区间索引做时点过滤。",
        "写回单向 + 逻辑追加 — 执行结果 → Ω → 蒸馏出新 SummaryEntry 回灌 D2(带 evidence_ref，旧条逻辑失效不删) + 更新 D3。闭环：离线总结 → 在线消费 → 执行产出 → 回灌总结，每个可召回结论都能回指原文。",
      ],
    },
  ],
};

const DRY = {
  en:{ htmllang:"en", brand:"Agentic Runtime", title:"Dry Run — Architecture Walkthrough",
    lead:"Pick a use case and trace one full run through <b>A = ⟨S, H, X⟩</b> + the data subsystem 𝒟 — the spec call sequence, the layer instantiation, and the data-flow diagram.",
    note:"This is the first example. More will be added; the selector lists them all.",
    other:"ZH", otherHref:"dry-run-zh.html",
    L:{usecase:"Use case",why:"Why this one",layers:"Layer instantiation",seq:"Spec call sequence",inv:"Structural invariants (↔ propositions)",diagram:"Data diagram (online / offline)",reading:"How to read it",full:"Full site",arch:"Architecture"} },
  zh:{ htmllang:"zh-CN", brand:"Agentic Runtime", title:"Dry Run — 架构走查",
    lead:"选一个用例，沿 <b>A = ⟨S, H, X⟩</b> + 数据子系统 𝒟 走查一次完整运行——spec 调用顺序、各层实例化、数据流图。",
    note:"这是第一个实例。后续会加更多；选择器会列出全部。",
    other:"EN", otherHref:"dry-run-en.html",
    L:{usecase:"用例",why:"为什么选它",layers:"各层实例化",seq:"Spec 调用顺序集",inv:"结构性约束（↔ 命题）",diagram:"Data diagram（在线 / 离线）",reading:"读图要点",full:"完整站点",arch:"架构"} },
};

function dryRunHTML(D){
  const exs = EXAMPLES[D.htmllang==="en"?"en":"zh"];
  const lang = D.htmllang==="en"?"en":"zh";
  const tabs = exs.map((e,i)=>`<button class="tab${i===0?" on":""}" data-ex="${e.id}">${esc(e.tag)} · ${esc(e.name)}</button>`).join("");
  const panel = e=>{
    const layers = e.layers.map(([k,v])=>`<tr><td class="id">${esc(k)}</td><td>${esc(v)}</td></tr>`).join("");
    const phases = e.phases.map(ph=>`
      <div class="phase"><h4>${esc(ph.h)}</h4>
      <table class="seq">${ph.steps.map(([n,a,d])=>`<tr><td class="sn">${esc(n)}</td><td class="sa">${esc(a)}</td><td class="sd">${esc(d)}</td></tr>`).join("")}</table></div>`).join("");
    const inv = e.invariants.map(([k,v])=>`<li><b>${esc(k)}</b> — ${esc(v)}</li>`).join("");
    const reading = e.reading.map((r,i)=>`<li><b>${i+1}.</b> ${esc(r)}</li>`).join("");
    return `<section class="ex" id="ex-${e.id}">
      <div class="goal"><span class="badge">${esc(e.tag)}</span><p>${esc(e.goal)}</p></div>
      <h3 class="th">${D.L.why}</h3><p class="muted">${esc(e.why)}</p>
      <h3 class="th">${D.L.layers}</h3><table class="tbl">${layers}</table>
      <h3 class="th">${D.L.seq}</h3>${phases}
      <h3 class="th">${D.L.inv}</h3><ul class="inv">${inv}</ul>
      <h3 class="th">${D.L.diagram}</h3><pre class="diagram">${esc(e.diagram.join("\n"))}</pre>
      <h3 class="th">${D.L.reading}</h3><ul class="reading">${reading}</ul>
    </section>`;
  };
  const panels = exs.map((e,i)=>`<div class="exwrap${i===0?" on":""}" data-ex="${e.id}">${panel(e)}</div>`).join("");
  return `<!DOCTYPE html><html lang="${D.htmllang}"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0"><title>${D.title}</title>
<style>
  :root{--ink:#221f1a;--mut:#6b6357;--page:#fffdf8;--card:#fff;--line:#e7dfce;--harn:#6d3fd4;--data:#1474a6;--skill:#1a7d52;--scaf:#bc5a16}
  *{box-sizing:border-box} body{margin:0;background:var(--page);color:var(--ink);line-height:1.65;
    font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',Arial,sans-serif}
  .wrap{max-width:1080px;margin:0 auto;padding:0 28px}
  nav{position:sticky;top:0;z-index:10;background:rgba(255,253,248,.86);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
  nav .wrap{display:flex;align-items:center;gap:14px;height:56px}
  nav .brand{font-weight:800} nav a{color:var(--harn);text-decoration:none;font-weight:700;font-size:14px}
  nav a.r{margin-left:auto}
  header{padding:50px 0 24px} .kicker{color:var(--harn);font-weight:800;letter-spacing:2px;font-size:12px;text-transform:uppercase}
  h1{font-size:38px;margin:.3em 0 .3em} .lead{font-size:18px;color:#3a352c;max-width:880px}
  .note{font-size:13.5px;color:var(--mut);margin-top:10px}
  .tabs{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0 6px;border-bottom:1px solid var(--line);padding-bottom:16px}
  .tab{cursor:pointer;border:1px solid var(--harn);background:#fff;color:var(--harn);font-weight:700;font-size:14px;
       padding:9px 16px;border-radius:999px;font-family:inherit}
  .tab.on{background:var(--harn);color:#fff}
  .exwrap{display:none} .exwrap.on{display:block}
  .goal{display:flex;gap:14px;align-items:flex-start;background:#f6f1fe;border:1px solid #e3d7fb;border-radius:14px;padding:16px 18px;margin:20px 0}
  .goal .badge{flex:0 0 auto;background:var(--harn);color:#fff;font-weight:800;border-radius:9px;padding:5px 11px;font-size:13px}
  .goal p{margin:0;font-size:16px;font-weight:600}
  .th{font-size:17px;font-weight:800;margin:26px 0 8px;color:var(--ink)}
  .muted{color:var(--mut);font-size:14.5px;max-width:900px}
  .tbl{width:100%;border-collapse:collapse;font-size:13.5px;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden}
  .tbl td{padding:8px 13px;border-top:1px solid var(--line);vertical-align:top} .tbl tr:first-child td{border-top:none}
  .tbl td.id{font-weight:800;color:var(--data);white-space:nowrap}
  .phase{margin:12px 0} .phase h4{margin:6px 0;font-size:14px;color:var(--harn);font-weight:800}
  table.seq{width:100%;border-collapse:collapse;font-size:13px;background:var(--card);border:1px solid var(--line);border-radius:8px;overflow:hidden}
  table.seq td{padding:6px 12px;border-top:1px solid #f0eadd;vertical-align:top}
  table.seq td.sn{font-family:ui-monospace,Menlo,monospace;font-weight:800;color:var(--scaf);width:36px}
  table.seq td.sa{font-weight:700;width:300px}
  table.seq td.sd{color:var(--mut)}
  .inv,.reading{font-size:14px;max-width:940px} .inv li,.reading li{margin:7px 0}
  .diagram{background:#1f1b16;color:#e9e2d2;border-radius:12px;padding:18px 16px;overflow-x:auto;
           font-family:ui-monospace,Menlo,'SFMono-Regular',monospace;font-size:11.5px;line-height:1.35;white-space:pre}
  footer{padding:36px 0 70px;color:var(--mut);font-size:13px;border-top:1px solid var(--line);margin-top:30px}
  @media(max-width:720px){h1{font-size:28px}table.seq td.sa{width:auto}}
</style></head>
<body>
<nav><div class="wrap"><span class="brand">${D.brand}</span>
  <a href="arch-${lang}.html">${D.L.arch}</a>
  <a href="index.html" style="color:var(--mut)">${D.L.full}</a>
  <a class="r" href="${D.otherHref}">${D.other}</a></div></nav>
<header class="wrap">
  <div class="kicker">Dry Run</div>
  <h1>${D.title}</h1>
  <p class="lead">${D.lead}</p>
  <p class="note">${D.note}</p>
</header>
<main class="wrap">
  <div class="tabs">${tabs}</div>
  ${panels}
</main>
<footer class="wrap">Dry Run · 2026-06-29 · companion to the synthesized paper draft v0.4 (§4.4.1 / §5).</footer>
<script>
const tabs=document.querySelectorAll('.tab'),wraps=document.querySelectorAll('.exwrap');
tabs.forEach(t=>t.addEventListener('click',()=>{
  const id=t.dataset.ex;
  tabs.forEach(x=>x.classList.toggle('on',x===t));
  wraps.forEach(w=>w.classList.toggle('on',w.dataset.ex===id));
}));
</script>
</body></html>`;
}
for(const lang of ["en","zh"]){
  fs.writeFileSync(path.join(OUT,`dry-run-${lang}.html`), dryRunHTML(DRY[lang]));
}
console.log("pages written: dry-run-en.html, dry-run-zh.html");
module.exports={built,W,H};
