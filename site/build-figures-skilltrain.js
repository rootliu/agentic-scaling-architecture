/* Generates 2 figures × 2 languages (EN/ZH) as standalone SVG + HTML, matching the
   visual language of build-figures.js (same palette, grid background, drop-shadow).
   Fig 7 (Dual-Subgoal Reward Loop) — goal/subgoal drawn as an ORG CHART (root -> leaves);
        formatted output drawn as one big container with SCATTERED, non-aligned subdomain
        chips (not a table) — each independently governed by its own benchmark; a Σ
        aggregation bridges the scattered chips into r_out; reflect -> dual-axis gate (P15).
   Fig 8 (Skill Lifecycle: NL Dialogue -> Code Tool) — natural-language dialogue -> step-
        explicit temporary code tool -> user confirms -> agent summarizes into an NL skill
        (goal is the org-chart root, the other five elements are leaves; the output-format
        leaf itself is a miniature scattered-subdomain container, echoing Fig. 7) -> stable
        parts compile into a code tool folded into the Harness (P14/P15/N9). */
const fs = require("fs");
const path = require("path");
const OUT = __dirname;
const FIGDIR = path.join(OUT, "figures");
fs.mkdirSync(FIGDIR, { recursive: true });

const C = {
  skillFill:"#e6f4ec", skillStroke:"#1a7d52", skillText:"#11603d",
  harnFill:"#ece4fb", harnStroke:"#6d3fd4", harnText:"#4f2da0", harnStrong:"#f4eeff",
  scafFill:"#fbe7d3", scafStroke:"#bc5a16", scafText:"#9a4d12",
  dataFill:"#ddeff8", dataStroke:"#1474a6", dataText:"#0f5e87",
  detFill:"#e3f4f0", detStroke:"#0f7a6b", detText:"#0b5e53",
  paraFill:"#f6efdf", paraStroke:"#9a6a12", paraText:"#7a530d",
  roseFill:"#fdecec", roseStroke:"#c14545", roseText:"#9a2f2f",
  neutFill:"#fffdf8", neutStroke:"#cabfa8", ink:"#221f1a", mut:"#6b6357",
  page:"#fffdf8", grid:"#efe8db", badge:"#ffffff",
};
const CHIP_PALETTE = [
  {fill:C.dataFill, stroke:C.dataStroke, text:C.dataText},
  {fill:C.paraFill,  stroke:C.paraStroke,  text:C.paraText},
  {fill:C.detFill,   stroke:C.detStroke,   text:C.detText},
  {fill:C.scafFill,  stroke:C.scafStroke,  text:C.scafText},
  {fill:C.skillFill, stroke:C.skillStroke, text:C.skillText},
  {fill:C.harnFill,  stroke:C.harnStroke,  text:C.harnText},
];

const esc = s => String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
function rect(x,y,w,h,{fill="#fff",stroke=C.neutStroke,sw=1.4,rx=12,dash=null,op=1,filter=true}={}){
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"`
    +(dash?` stroke-dasharray="${dash}"`:"")+` opacity="${op}"`+(filter?` filter="url(#sh)"`:"")+`/>`;
}
function tline(x,y,t,{size=13,fill=C.ink,weight=400,anchor="start",mono=false}={}){
  const ff=mono?` font-family="ui-monospace,Menlo,monospace"`:"";
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}" font-weight="${weight}" fill="${fill}"${ff}>${esc(t)}</text>`;
}
function centerText(cx,cy,t,{size=12,fill=C.ink,weight=700,mono=false}={}){
  const ff=mono?` font-family="ui-monospace,Menlo,monospace"`:"";
  return `<text x="${cx}" y="${cy}" text-anchor="middle" dominant-baseline="middle" font-size="${size}" font-weight="${weight}" fill="${fill}"${ff}>${esc(t)}</text>`;
}
function vText(cx,cy,t,{size=11,fill=C.ink,weight=700}={}){
  return `<text x="${cx}" y="${cy}" text-anchor="middle" dominant-baseline="middle" font-size="${size}" font-weight="${weight}" fill="${fill}" transform="rotate(-90 ${cx} ${cy})">${esc(t)}</text>`;
}
function leftLines(x,yTop,lines,{size=12.5,fill=C.ink,weight=400,lh=null}={}){
  lh=lh||Math.round(size*1.5);
  return lines.map((t,i)=>`<text x="${x}" y="${yTop+i*lh}" text-anchor="start" font-size="${size}" font-weight="${weight}" fill="${fill}">${esc(t)}</text>`).join("");
}
function bullets(x,yTop,items,{size=12,fill=C.ink,lh=20,marker="•",mcol=null}={}){
  mcol=mcol||fill;
  return items.map((t,i)=>{
    const y=yTop+i*lh;
    return `<text x="${x}" y="${y}" font-size="${size}" fill="${mcol}" font-weight="700">${marker}</text>`
      +`<text x="${x+15}" y="${y}" font-size="${size}" fill="${fill}">${esc(t)}</text>`;
  }).join("");
}
const vArrow=(x,y1,y2,{stroke=C.harnStroke,sw=2.1,head="a",dash=null}={})=>`<path d="M${x} ${y1} L${x} ${y2}" fill="none" stroke="${stroke}" stroke-width="${sw}"`+(dash?` stroke-dasharray="${dash}"`:"")+` marker-end="url(#${head})"/>`;
const hArrow=(x1,x2,y,{stroke=C.harnStroke,sw=2.1,head="a",dash=null}={})=>`<path d="M${x1} ${y} L${x2} ${y}" fill="none" stroke="${stroke}" stroke-width="${sw}"`+(dash?` stroke-dasharray="${dash}"`:"")+` marker-end="url(#${head})"/>`;
const elbow=(pts,{stroke=C.harnStroke,sw=2,head="a",dash=null}={})=>`<path d="M${pts.map(p=>p[0]+" "+p[1]).join(" L")}" fill="none" stroke="${stroke}" stroke-width="${sw}"`+(dash?` stroke-dasharray="${dash}"`:"")+` marker-end="url(#${head})"/>`;
function badge(cx,cy,n,col){
  return `<circle cx="${cx}" cy="${cy}" r="15" fill="${col}" stroke="#fff" stroke-width="2"/>`
    +`<text x="${cx}" y="${cy+1}" text-anchor="middle" dominant-baseline="middle" font-size="14" font-weight="800" fill="#fff">${n}</text>`;
}
function defs(){
  const m=(id,f)=>`<marker id="${id}" markerWidth="11" markerHeight="11" refX="7.5" refY="3.6" orient="auto"><path d="M0,0 L7.5,3.6 L0,7.2 Z" fill="${f}"/></marker>`;
  return `<defs>
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="${C.grid}" stroke-width="1"/></pattern>
    <filter id="sh" x="-12%" y="-12%" width="124%" height="124%"><feDropShadow dx="0" dy="3" stdDeviation="4.5" flood-color="#3c2d14" flood-opacity=".11"/></filter>
    ${m("a",C.harnStroke)}${m("g",C.skillStroke)}${m("o",C.scafStroke)}${m("t",C.dataStroke)}${m("k",C.mut)}${m("d",C.detStroke)}${m("p",C.paraStroke)}${m("r",C.roseStroke)}
  </defs>`;
}
/* title + wrapped subtitle (array of 1-2 short lines, caller pre-wraps to avoid overflow) */
function frame(W,H,title,subLines){
  let s = `<rect width="${W}" height="${H}" rx="20" fill="${C.page}"/>`
    +`<rect width="${W}" height="${H}" rx="20" fill="url(#grid)" opacity=".7"/>`
    +tline(54,50,title,{size:22,weight:800});
  (subLines||[]).forEach((line,i)=> s += tline(54,76+i*19,line,{size:13,fill:C.mut}));
  return s;
}
function svgWrap(W,H,inner){
  return `<svg viewBox="0 0 ${W} ${H}" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',Arial,sans-serif">${defs()}${inner}</svg>`;
}

/* ---- Org-chart helper: one root box fanning out into N leaf boxes via a bus line ---- */
function orgChart({root, leaves, busY, stroke=C.harnStroke}){
  let s = rect(root.x,root.y,root.w,root.h,{fill:root.fill||"#fff",stroke:root.stroke||stroke,sw:1.8});
  s += centerText(root.x+root.w/2, root.y+root.h*0.42, root.title, {size:14.5,weight:800,fill:root.textColor||C.ink});
  if(root.sub) s += centerText(root.x+root.w/2, root.y+root.h*0.72, root.sub, {size:10.5,weight:400,fill:C.mut});
  const rootCx = root.x+root.w/2, rootBottom = root.y+root.h;
  s += `<path d="M${rootCx} ${rootBottom} L${rootCx} ${busY}" fill="none" stroke="${stroke}" stroke-width="1.8"/>`;
  const leafCxs = leaves.map(lf=>lf.x+lf.w/2);
  const busX0 = Math.min(...leafCxs), busX1 = Math.max(...leafCxs);
  s += `<path d="M${busX0} ${busY} L${busX1} ${busY}" fill="none" stroke="${stroke}" stroke-width="1.8"/>`;
  leaves.forEach(lf=>{
    const cx = lf.x+lf.w/2;
    s += `<path d="M${cx} ${busY} L${cx} ${lf.y}" fill="none" stroke="${stroke}" stroke-width="1.8" marker-end="url(#a)"/>`;
    s += rect(lf.x,lf.y,lf.w,lf.h,{fill:lf.fill||"#fff",stroke:lf.stroke||stroke,sw:1.5});
    if(lf.mini){ s += lf.mini(lf); return; } // custom inner content (e.g. scatter container)
    const lines = lf.lines||[lf.title];
    const startY = lf.y + lf.h/2 - (lines.length-1)*8;
    lines.forEach((t,i)=> s += centerText(cx, startY+i*16, t, {size:lf.size||12, weight:i===0?700:400, fill:lf.textColor||C.ink}));
  });
  return s;
}

/* ---- Scattered (non-aligned, non-tabular) subdomain container ---- */
function scatterContainer({box, label, chips}){
  let s = rect(box.x,box.y,box.w,box.h,{fill:"#fbfaf6",stroke:"#e6dfd1",sw:1.6});
  s += tline(box.x+16, box.y+24, label, {size:12, weight:700, fill:C.mut, mono:true});
  chips.forEach((c,i)=>{
    const pal = CHIP_PALETTE[i % CHIP_PALETTE.length];
    s += rect(c.x,c.y,c.w,c.h,{fill:c.fill||pal.fill, stroke:c.stroke||pal.stroke, sw:1.5, rx:10});
    const tcol = c.textColor||pal.text;
    s += tline(c.x+10, c.y+c.h*0.42, c.title, {size:c.tsize||11.5, weight:800, fill:tcol});
    if(c.desc) s += tline(c.x+10, c.y+c.h*0.42+15, c.desc, {size:9.6, weight:400, fill:tcol});
  });
  return s;
}

/* ===================================================================
   FIGURE 7 — DUAL-SUBGOAL REWARD LOOP (org-chart decomposition + scattered subdomains)
   =================================================================== */
const W7=1200, H7=760;
const D7 = {
  zh:{
    title:"双子目标 Reward 训练环 — 从 goal 到验证 benchmark",
    sub:["Harness 把 goal 分解成子目标（组织图）；正/反例顺序执行，把结果并行填进"
        ,"「格式化输出」容器里彼此独立、不对齐的子域小格 —— 每个子域各自的 benchmark 独立打分（P15）。"],
    rootTitle:"用户 goal", rootSub:"筛选带隙≈1.3eV材料·写可复现报告",
    leaves:["检索","候选","取物性","筛选","分析","报告"],
    seqTitle:"顺序执行：正例 / 反例",
    posTitle:"正例 rollout E⁺", posLines:["成功轨迹：命中候选·数值合理","→ 保留有效行为模式"],
    negTitle:"反例 rollout E⁻", negLines:["失败轨迹：检索源错·格式偏差","→ 提出缺失/纠正规则"],
    parallelNote:"两类轨迹并行填充下方各子域（非顺序依赖）",
    containerLabel:"σ_out 格式化输出 —— 子域各自独立、不对齐、不是表格",
    chips:[
      {title:"数字子域", desc:"带隙数值·容差匹配"},
      {title:"总结子域", desc:"内容摘要·rubric/LLM-judge"},
      {title:"引用子域", desc:"检索命中率·evidence_ref"},
      {title:"结构子域", desc:"表格/字段完整性"},
      {title:"图表子域", desc:"可视化·坐标轴校验"},
      {title:"格式子域", desc:"引用规范·输出 schema"},
    ],
    sumLabel:"Σ w_d·r_d",
    reflectTitle:"反思 reflection", reflectLines:["优化器模型分析成功/失败 minibatch","提出 bounded add/delete/replace 编辑"],
    verifyTitle:"验证：分域 benchmark",
    outTitle:"r_out 结果子目标", outLines:["每个子域独立标注 benchmark","汇总：Σ w_d·r_d(output_d,benchmark_d)"],
    procTitle:"r_proc 过程子目标", procLines:["工具/数据源调用是否正确","逻辑分析·是否达进阶标准"],
    gateTitle:"双维 validation gate", gateLines:["r=α·r_out+β·r_proc 提升 → accept","否则 reject → rejected-edit buffer"],
    loopBack:"未达阈值 → 回到目标分解，重新切分/重跑",
    propTag:["P15 · 双子目标分解","提升归因清晰度、加速收敛"],
  },
  en:{
    title:"Dual-Subgoal Reward Training Loop — from Goal to Benchmark Verification",
    sub:["The Harness decomposes the goal into subgoals (org chart); positive/negative examples"
        ,"run in parallel to fill independent, non-aligned subdomain chips, each scored by its own benchmark (P15)."],
    rootTitle:"User goal", rootSub:"screen band-gap≈1.3eV candidates · reproducible report",
    leaves:["search","candidates","properties","screen","analyze","report"],
    seqTitle:"Sequential rollout: positive / negative",
    posTitle:"Positive rollout E⁺", posLines:["Successful trajectory: hit candidate · sane value","→ preserve behaviors that already work"],
    negTitle:"Negative rollout E⁻", negLines:["Failed trajectory: wrong source · format drift","→ propose missing/corrective rules"],
    parallelNote:"Both trajectory types fill subdomains below in parallel",
    containerLabel:"σ_out formatted output — each subdomain independent, unaligned, not a table",
    chips:[
      {title:"Numeric subdomain", desc:"band-gap value · tolerance match"},
      {title:"Summary subdomain", desc:"content summary · rubric/LLM-judge"},
      {title:"Citation subdomain", desc:"retrieval hit rate · evidence_ref"},
      {title:"Structure subdomain", desc:"table/field completeness"},
      {title:"Chart subdomain", desc:"visualization · axis checks"},
      {title:"Format subdomain", desc:"citation style · output schema"},
    ],
    sumLabel:"Σ w_d·r_d",
    reflectTitle:"Reflection", reflectLines:["Optimizer model reads success/failure minibatches","proposes bounded add/delete/replace edits"],
    verifyTitle:"Verify: per-subdomain benchmark",
    outTitle:"r_out outcome subgoal", outLines:["Independent benchmark per subdomain","Aggregate: Σ w_d·r_d(output_d,benchmark_d)"],
    procTitle:"r_proc process subgoal", procLines:["Were the right tools/data sources called?","logical analysis · met next-step criteria?"],
    gateTitle:"Dual-axis validation gate", gateLines:["r=α·r_out+β·r_proc improves → accept","else reject → rejected-edit buffer"],
    loopBack:"Below threshold → back to decomposition",
    propTag:["P15 · dual-subgoal decomposition","sharpens attribution, speeds convergence"],
  },
};

function fig7(lang){
  const D = D7[lang];
  let s = frame(W7,H7,D.title,D.sub);

  /* ---- Zone A: goal org-chart (root -> 6 leaves), left content area x:54-760 ---- */
  const rootW=320, rootX=54+(706-rootW)/2;
  const root = {x:rootX,y:114,w:rootW,h:58,title:D.rootTitle,sub:D.rootSub,fill:C.harnStrong,stroke:C.harnStroke,textColor:C.harnText};
  const leafW=109, leafGap=10, leafY=214, leafH=52;
  const leaves = D.leaves.map((t,i)=>({x:54+i*(leafW+leafGap), y:leafY, w:leafW, h:leafH, title:t, size:12.5, fill:"#fff", stroke:C.harnStroke, textColor:C.harnText}));
  s += orgChart({root, leaves, busY:186, stroke:C.harnStroke});
  s += vArrow(rootX+rootW/2, leafY+leafH, leafY+leafH+22, {stroke:C.mut,sw:1.6,dash:"3 4"});

  /* ---- Zone B: sequential rollout E+/E- ---- */
  const rbY = leafY+leafH+34;
  s += tline(54, rbY-8, D.seqTitle, {size:12.5, weight:700, fill:C.mut, mono:true});
  const boxH=88, boxW=330, gapMid=44;
  const b1x=54, b2x=b1x+boxW+gapMid;
  s += rect(b1x,rbY,boxW,boxH,{fill:C.skillFill,stroke:C.skillStroke,sw:1.7});
  s += badge(b1x+26,rbY+26,"1",C.skillStroke);
  s += tline(b1x+46,rbY+31,D.posTitle,{size:13,weight:800,fill:C.skillText});
  s += leftLines(b1x+46,rbY+51,D.posLines,{size:10.5,fill:C.skillText});
  s += rect(b2x,rbY,boxW,boxH,{fill:C.roseFill,stroke:C.roseStroke,sw:1.7});
  s += badge(b2x+26,rbY+26,"2",C.roseStroke);
  s += tline(b2x+46,rbY+31,D.negTitle,{size:13,weight:800,fill:C.roseText});
  s += leftLines(b2x+46,rbY+51,D.negLines,{size:10.5,fill:C.roseText});
  s += hArrow(b1x+boxW,b2x,rbY+26,{stroke:C.mut,sw:1.8});
  s += tline((b1x+boxW+b2x)/2, rbY-8, D.parallelNote, {size:10.3, weight:400, fill:C.mut});

  /* ---- Zone C: scattered subdomain container (parallel fan-in from both rollouts) ---- */
  const cy = rbY+boxH+40, cx=54, cw=706, ch=220;
  const chips = [
    {x:cx+26, y:cy+38, w:206, h:64, ...D.chips[0]},
    {x:cx+250,y:cy+30, w:224, h:52, ...D.chips[1]},
    {x:cx+498,y:cy+42, w:186, h:58, ...D.chips[2]},
    {x:cx+40, y:cy+114,w:180, h:56, ...D.chips[3]},
    {x:cx+240,y:cy+134,w:190, h:48, ...D.chips[4]},
    {x:cx+458,y:cy+116,w:226, h:64, ...D.chips[5]},
  ];
  s += scatterContainer({box:{x:cx,y:cy,w:cw,h:ch}, label:D.containerLabel, chips});
  // fan-in from both rollout boxes into the container top edge at staggered x
  [cx+90, cx+300, cx+560].forEach((tx,i)=>{
    const from = i%2===0 ? b1x+boxW/2 : b2x+boxW/2;
    s += elbow([[from, rbY+boxH],[from, cy-16],[tx, cy-16],[tx, cy-2]], {stroke: i%2===0?C.skillStroke:C.roseStroke, sw:1.5, dash:"4 4", head: i%2===0?"g":"r"});
  });

  /* ---- Sum bridge: container bottom -> Σ node (below, centered) -> right column ---- */
  const sumCx = cx+cw/2, sumCy = cy+ch+42;
  s += vArrow(sumCx, cy+ch, sumCy-20, {stroke:C.dataStroke, sw:1.8, dash:"3 4"});
  s += `<circle cx="${sumCx}" cy="${sumCy}" r="20" fill="#fff" stroke="${C.dataStroke}" stroke-width="1.8"/>`;
  s += centerText(sumCx, sumCy+1, "Σ", {size:17, weight:800, fill:C.dataStroke});
  s += tline(sumCx+28, sumCy+5, D.sumLabel, {size:10.5, weight:700, fill:C.dataStroke, mono:true});

  /* ---- Zone D: right column (optimizer) ---- */
  const rx=800, rw=346;
  s += rect(rx,114,rw,542,{fill:"#fbfaf6",stroke:"#e6dfd1"});
  s += tline(rx+18,140,"OPTIMIZER MODEL",{size:11,fill:C.mut,mono:true});
  s += rect(rx+16,158,rw-32,92,{fill:C.harnStrong,stroke:C.harnStroke});
  s += tline(rx+34,182,D.reflectTitle,{size:13.5,weight:800,fill:C.harnText});
  s += leftLines(rx+34,201,D.reflectLines,{size:10.3,fill:C.harnText});

  s += tline(rx+18,272,D.verifyTitle,{size:12,weight:700,fill:C.ink});
  const outY=286, outH=94;
  s += rect(rx+16,outY,rw-32,outH,{fill:C.dataFill,stroke:C.dataStroke,sw:1.7});
  s += tline(rx+34,outY+24,D.outTitle,{size:12.5,weight:800,fill:C.dataText});
  s += leftLines(rx+34,outY+43,D.outLines,{size:10,fill:C.dataText});

  const procY=outY+outH+8, procH=94;
  s += rect(rx+16,procY,rw-32,procH,{fill:"#fff2e6",stroke:C.scafStroke,sw:1.7});
  s += tline(rx+34,procY+24,D.procTitle,{size:12.5,weight:800,fill:C.scafText});
  s += leftLines(rx+34,procY+43,D.procLines,{size:10,fill:C.scafText});

  s += vArrow(rx+rw/2,250,outY,{stroke:C.harnStroke});
  s += vArrow(rx+rw/2,outY+outH,procY,{stroke:C.harnStroke,sw:1.6,dash:"3 4"});
  // Σ (below container) -> r_out box left edge, via a clean right-angle turn
  s += elbow([[sumCx+20,sumCy],[rx-20,sumCy],[rx-20,outY+outH/2],[rx+16,outY+outH/2]], {stroke:C.dataStroke, sw:1.8});

  const gateY=procY+procH+16, gateH=88;
  s += rect(rx,gateY,rw,gateH,{fill:C.detFill,stroke:C.detStroke,sw:1.8});
  s += tline(rx+18,gateY+24,D.gateTitle,{size:12.5,weight:800,fill:C.detText});
  s += leftLines(rx+18,gateY+44,D.gateLines,{size:10,fill:C.detText});
  s += vArrow(rx+rw/2,procY+procH,gateY,{stroke:C.detStroke});

  const tagY=gateY+gateH+16;
  s += rect(rx,tagY,rw,54,{fill:"#fff",stroke:C.detStroke,dash:"5 5",filter:false});
  s += leftLines(rx+18,tagY+22,D.propTag,{size:10.6,weight:700,fill:C.detText});

  /* loop-back: gate -> goal decomposition, routed along the narrow corridor between
     container (ends at cx+cw=760) and right column (starts at rx=800); label is
     vertical text placed IN that corridor so it never overlaps the chips or the panel */
  const laneX = 780;
  s += elbow([[rx,gateY+gateH-20],[laneX,gateY+gateH-20],[laneX,186],[rootX+rootW,186]], {stroke:C.scafStroke, sw:2, dash:"6 5", head:"o"});
  s += vText(laneX-14, (cy+240), D.loopBack, {size:10, weight:700, fill:C.scafText});

  return svgWrap(W7,H7,s);
}

/* ===================================================================
   FIGURE 8 — SKILL LIFECYCLE: NL DIALOGUE -> TEMP CODE -> NL SKILL (org
   chart, goal=root; output-format leaf = mini scattered container,
   echoing Fig.7) -> COMPILED CODE TOOL FOLDED INTO HARNESS
   =================================================================== */
const W8=1200, H8=1000;
const D8 = {
  zh:{
    title:"Skill 生命周期 — 从自然语言对话到融入 Harness 的 code 工具",
    sub:["对话把步骤显式化为临时 code 工具；用户确认后，agent 把过程总结为以 goal 为根节点、"
        ,"输出格式/工具数据源/检查标准/正反例为分支的自然语言 skill；收敛后固化为 code tool 融入 Harness。"],
    d1Title:"① 自然语言对话", d1Lines:["用户与 agent 逐步讨论任务","how-to 逐步显式化"],
    d2Title:"② 生成临时 code 工具", d2Lines:["把讨论中显式化的步骤","写成一次性脚本/函数（未定形）"],
    d3Title:"③ 用户确认", d3Lines:["跑通、检查输出","用户同意：\"这个过程可复用\""],
    d4Label:"④ Agent 总结为 NL skill", rootTitle:"goal", rootSub:"（skill 的根）",
    leafOutTitle:"σ_out", leafOutSub:"格式化输出",
    leafOutChips:[{title:"数字",desc:""},{title:"摘要",desc:""},{title:"引用",desc:""}],
    leaf2:["工具/数据源","列表"], leaf3:["调用与反思","检查标准"], leaf4:["正例","E⁺"], leaf5:["反例","E⁻"],
    d5Title:"⑤ 双子目标 Reward 迭代", d5Lines:["r_out（结果子域）× r_proc（过程一致性）","（见图 7 · P15）驱动 skill 收敛"],
    d6Title:"⑥ 收敛部分固化为 code tool", d6Lines:["κ(s) 达阈 → 过程编译为确定函数","（P14 · Skill-as-Code）"],
    d7Title:"⑦ 融入 Harness 工具集", d7Lines:["注册为 capability，供其它 agent 复用","（capability capsule 形态）"],
    remainTitle:"未固化部分保留 NL", remainLines:["reflection / 多样性校验仍用 LLM","防止 code 化锁死泛化（§4 梯度）"],
    axisNote:"确定性沿生命周期单向递增：对话 → 临时代码 → NL skill（可训练）→ 固化 code（不可变）",
    sumNote:"Σ",
  },
  en:{
    title:"Skill Lifecycle — from NL Dialogue to a Code Tool Folded into the Harness",
    sub:["Dialogue makes steps explicit as a temporary code tool; once the user confirms, the"
        ,"agent summarizes the process into an NL skill rooted at goal, branching into output"
        ,"format / tools+data sources / check criteria / examples; converged parts compile into a Harness code tool."],
    d1Title:"① Natural-language dialogue", d1Lines:["User and agent discuss the task step by step","how-to becomes explicit"],
    d2Title:"② Generate a temporary code tool", d2Lines:["Steps made explicit in dialogue","become a one-off script/function (not yet a skill)"],
    d3Title:"③ User confirms", d3Lines:["Runs it, checks the output","User agrees: \"this process is reusable\""],
    d4Label:"④ Agent summarizes into an NL skill", rootTitle:"goal", rootSub:"(skill root)",
    leafOutTitle:"σ_out", leafOutSub:"output format",
    leafOutChips:[{title:"num",desc:""},{title:"sum",desc:""},{title:"cite",desc:""}],
    leaf2:["tools/data","source list"], leaf3:["invocation &","reflection criteria"], leaf4:["positive","E⁺"], leaf5:["negative","E⁻"],
    d5Title:"⑤ Dual-subgoal reward iteration", d5Lines:["r_out (outcome subdomains) × r_proc (process)","(see Fig. 7 · P15) drives skill convergence"],
    d6Title:"⑥ Converged parts compile into a code tool", d6Lines:["κ(s) above threshold → compiles to a deterministic fn","(P14 · Skill-as-Code)"],
    d7Title:"⑦ Folded into the Harness tool set", d7Lines:["Registered as a capability, reusable by other agents","(capability-capsule form)"],
    remainTitle:"Unconverged part stays NL", remainLines:["Reflection / diversity checks still use the LLM","prevents premature code-lock (§4 gradient)"],
    axisNote:"Determinism increases monotonically: dialogue → temp code → NL skill (trainable) → frozen code (immutable)",
    sumNote:"Σ",
  },
};

function fig8(lang){
  const D = D8[lang];
  let s = frame(W8,H8,D.title,D.sub);
  const subLines = D.sub.length;
  const topY = 78 + subLines*19 + 30;

  const boxW=300, boxH=92, gapX=40;
  const xs=[54, 54+boxW+gapX, 54+2*(boxW+gapX)];
  s += rect(xs[0],topY,boxW,boxH,{fill:"#fff",stroke:C.neutStroke});
  s += tline(xs[0]+18,topY+28,D.d1Title,{size:14,weight:800,fill:C.ink});
  s += leftLines(xs[0]+18,topY+50,D.d1Lines,{size:11,fill:C.mut});
  s += hArrow(xs[0]+boxW,xs[1],topY+boxH-24,{stroke:C.mut});

  s += rect(xs[1],topY,boxW,boxH,{fill:"#fff2e6",stroke:C.scafStroke,sw:1.6});
  s += tline(xs[1]+18,topY+28,D.d2Title,{size:14,weight:800,fill:C.scafText});
  s += leftLines(xs[1]+18,topY+50,D.d2Lines,{size:11,fill:C.scafText});
  s += hArrow(xs[1]+boxW,xs[2],topY+boxH-24,{stroke:C.mut});

  s += rect(xs[2],topY,boxW,boxH,{fill:"#fff",stroke:C.neutStroke,dash:"5 5"});
  s += tline(xs[2]+18,topY+28,D.d3Title,{size:14,weight:800,fill:C.ink});
  s += leftLines(xs[2]+18,topY+50,D.d3Lines,{size:11,fill:C.mut});

  /* ---- Stage 4: org chart, goal=root, 5 leaves (σ_out leaf = mini scatter container) ---- */
  const y4label = topY+boxH+40;
  s += tline(54, y4label, D.d4Label, {size:13.5, weight:800, fill:C.skillText});
  const rootY = y4label+14, rootW4=180, rootX4=54+(706-rootW4)/2;
  const root = {x:rootX4,y:rootY,w:rootW4,h:52,title:D.rootTitle,sub:D.rootSub,fill:C.skillFill,stroke:C.skillStroke,textColor:C.skillText};
  const leafY4 = rootY+52+42, leafH4=94;
  const widths=[190,117,117,117,117], gap=12;
  let lx=54; const lxs=[]; widths.forEach(w=>{lxs.push(lx); lx+=w+gap;});
  const leaves = [
    {x:lxs[0],y:leafY4,w:widths[0],h:leafH4, mini:(lf)=>{
      let inner = tline(lf.x+10, lf.y+18, `${D.leafOutTitle} · ${D.leafOutSub}`, {size:10.5, weight:800, fill:C.dataText});
      const chipDefs = [ [10,30,64,26], [86,24,90,24], [22,60,150,22] ];
      D.leafOutChips.forEach((c,i)=>{
        const [ox,oy,cw,ch2] = chipDefs[i];
        const pal = CHIP_PALETTE[i%CHIP_PALETTE.length];
        inner += rect(lf.x+ox, lf.y+oy, cw, ch2, {fill:pal.fill, stroke:pal.stroke, sw:1.2, rx:7, filter:false});
        inner += centerText(lf.x+ox+cw/2, lf.y+oy+ch2/2+1, c.title, {size:9.6, weight:700, fill:pal.text});
      });
      return inner;
    }, stroke:C.dataStroke, fill:"#fff"},
    {x:lxs[1],y:leafY4,w:widths[1],h:leafH4, lines:D.leaf2, size:10.6, stroke:C.harnStroke, textColor:C.harnText},
    {x:lxs[2],y:leafY4,w:widths[2],h:leafH4, lines:D.leaf3, size:10.6, stroke:C.harnStroke, textColor:C.harnText},
    {x:lxs[3],y:leafY4,w:widths[3],h:leafH4, lines:D.leaf4, size:11, stroke:C.skillStroke, textColor:C.skillText, fill:C.skillFill},
    {x:lxs[4],y:leafY4,w:widths[4],h:leafH4, lines:D.leaf5, size:11, stroke:C.roseStroke, textColor:C.roseText, fill:C.roseFill},
  ];
  s += orgChart({root, leaves, busY:rootY+52+18, stroke:C.skillStroke});

  /* ---- Stage 5 beside the org chart, fed by Σ from the σ_out leaf (routed below,
     clear of all leaf boxes, then up into stage 5's left edge) ---- */
  const rx5=800, rw5=346, ry5=leafY4-4, rh5=leafH4+40;
  s += rect(rx5,ry5,rw5,rh5,{fill:C.detFill,stroke:C.detStroke,sw:1.7});
  s += tline(rx5+18,ry5+26,D.d5Title,{size:12.5,weight:800,fill:C.detText});
  s += leftLines(rx5+18,ry5+46,D.d5Lines,{size:10.2,fill:C.detText});
  /* ---- Stage 6/7 below stage 4 (placed first so Σ's crossbar can be routed clearly below it) ---- */
  const y6 = leafY4+leafH4+92;
  s += vArrow(rootX4+rootW4/2, leafY4+leafH4, y6-14, {stroke:C.skillStroke});
  s += tline(rootX4+rootW4/2+14, y6-24, "κ(s) ↑", {size:11.5, fill:C.skillStroke, weight:800, mono:true});

  const sumCx = lxs[0]+widths[0]/2, sumCy = y6-24;
  const corridorX = (lxs[4]+widths[4]+rx5)/2; // clear gap between last leaf (ends at lxs[4]+widths[4]) and stage-5 box (starts at rx5)
  const box5EntryY = ry5+rh5-16; // near stage-5 box's bottom-left corner, inside its border
  s += vArrow(sumCx, leafY4+leafH4, sumCy-16, {stroke:C.dataStroke, sw:1.6, dash:"3 4"});
  s += `<circle cx="${sumCx}" cy="${sumCy}" r="16" fill="#fff" stroke="${C.dataStroke}" stroke-width="1.6"/>`;
  s += centerText(sumCx, sumCy+1, D.sumNote, {size:14, weight:800, fill:C.dataStroke});
  s += elbow([[sumCx+16,sumCy],[corridorX,sumCy],[corridorX,box5EntryY],[rx5,box5EntryY]], {stroke:C.dataStroke, sw:1.6});

  s += rect(300,y6,320,104,{fill:C.detFill,stroke:C.detStroke,sw:1.8});
  s += tline(322,y6+26,D.d6Title,{size:13,weight:800,fill:C.detText});
  s += leftLines(322,y6+46,D.d6Lines,{size:10.3,fill:C.detText});
  s += hArrow(620,678,y6+84,{stroke:C.detStroke});

  s += rect(678,y6,222,104,{fill:C.harnFill,stroke:C.harnStroke,sw:1.8});
  s += tline(698,y6+26,D.d7Title,{size:13,weight:800,fill:C.harnText});
  s += leftLines(698,y6+46,D.d7Lines,{size:10,fill:C.harnText});

  /* remain-NL side note near stage 4 bottom-left */
  const yR = y6;
  s += rect(54,yR,224,104,{fill:"#fff",stroke:C.neutStroke,dash:"5 5",filter:false});
  s += tline(72,yR+26,D.remainTitle,{size:12,weight:800,fill:C.ink});
  s += leftLines(72,yR+46,D.remainLines,{size:10,fill:C.mut});
  s += elbow([[300,y6+52],[278,y6+52],[278,yR+10]], {stroke:C.mut, sw:1.6, dash:"4 4", head:"k"});

  /* axis note at bottom */
  const yA = y6+140;
  s += rect(54,yA,1092,44,{fill:"#f1ebe0",stroke:C.harnStroke,dash:"6 6",filter:false});
  s += tline(72,yA+26,D.axisNote,{size:11.2,weight:700,fill:C.harnText});

  return svgWrap(W8,H8,s);
}

/* ===================================================================
   Build + write standalone SVG/HTML (PNG rendered separately via sharp)
   =================================================================== */
function htmlWrap(W,H,svgInner){
  return `<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<style>@page{size:${W}px ${H}px;margin:0}html,body{margin:0;padding:0;background:${C.page}}#p{width:${W}px;height:${H}px}#p svg{display:block;width:${W}px;height:${H}px}</style></head>
<body><div id="p">${svgInner}</div></body></html>`;
}

const built = [];
for (const lang of ["zh","en"]) {
  const svg7 = fig7(lang);
  fs.writeFileSync(path.join(FIGDIR,`f7-${lang}.svg`), svg7);
  fs.writeFileSync(path.join(FIGDIR,`f7-${lang}.html`), htmlWrap(W7,H7,svg7));
  built.push({num:7,lang});

  const svg8 = fig8(lang);
  fs.writeFileSync(path.join(FIGDIR,`f8-${lang}.svg`), svg8);
  fs.writeFileSync(path.join(FIGDIR,`f8-${lang}.html`), htmlWrap(W8,H8,svg8));
  built.push({num:8,lang});
}
console.log(`built ${built.length} figure variants:`);
built.forEach(b => console.log(`  f${b.num}-${b.lang}`));
module.exports = { W7,H7,W8,H8, built };
