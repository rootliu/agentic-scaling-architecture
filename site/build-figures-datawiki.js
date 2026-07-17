/* Generates 2 figures × 2 languages (EN/ZH) as standalone SVG + HTML, matching the
   visual language of build-figures-skilltrain.js (same palette, grid background,
   drop-shadow, scatter-container / org-chart helpers).
   Fig 9 (Data Wiki Construction) — two lanes: (A) regular sources auto-summarized by
        the D2 off-policy loop into scattered Sigma chips (NL summary/format/keywords/
        foreign-key); (B) complex reports built human+agent collaboratively (source/
        frequency/maintenance/freshness), validated against a human reference report via
        reflective partial-table reconstruction — both lanes converge into Data Wiki.
   Fig 10 (Data Wiki / Theme Wiki / IR composition) — two scattered-chip wikis bridged by
        an Intermediate Relation layer carrying semantic join + explicit 5W+1H metadata;
        echoes Fig.7's "formatted-output scattered subdomain" visual language. */
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
function vText(cx,cy,t,{size=11,fill=C.ink,weight=700}={}){
  return `<text x="${cx}" y="${cy}" text-anchor="middle" dominant-baseline="middle" font-size="${size}" font-weight="${weight}" fill="${fill}" transform="rotate(-90 ${cx} ${cy})">${esc(t)}</text>`;
}
function diamond(cx,cy,w,h,{fill="#fffdf8",stroke=C.neutStroke,sw=1.4}={}){
  const pts=[[cx,cy-h/2],[cx+w/2,cy],[cx,cy+h/2],[cx-w/2,cy]];
  return `<path d="M${pts.map(p=>p[0]+" "+p[1]).join(" L")} Z" fill="${fill}" stroke="${stroke}" stroke-width="${sw}" filter="url(#sh)"/>`;
}
function defs(){
  const m=(id,f)=>`<marker id="${id}" markerWidth="11" markerHeight="11" refX="7.5" refY="3.6" orient="auto"><path d="M0,0 L7.5,3.6 L0,7.2 Z" fill="${f}"/></marker>`;
  return `<defs>
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="${C.grid}" stroke-width="1"/></pattern>
    <filter id="sh" x="-12%" y="-12%" width="124%" height="124%"><feDropShadow dx="0" dy="3" stdDeviation="4.5" flood-color="#3c2d14" flood-opacity=".11"/></filter>
    ${m("a",C.harnStroke)}${m("g",C.skillStroke)}${m("o",C.scafStroke)}${m("t",C.dataStroke)}${m("k",C.mut)}${m("d",C.detStroke)}${m("p",C.paraStroke)}${m("r",C.roseStroke)}
  </defs>`;
}
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
   FIGURE 9 — DATA WIKI CONSTRUCTION (two lanes converging)
   =================================================================== */
const W9=1200, H9=980;
const D9 = {
  zh:{
    title:"Data Wiki 构建 — 常规数据源自动化 + 复杂报表人机协同校验",
    sub:["承 D2：常规数据源由 off-policy loop 自动读取总结；复杂报表（多 sheet / 口径漂移）",
         "则与人协同定规范，并用人常备报表作参照物，经还原式 reflection 校验总结质量。"],
    laneA:"① 常规数据源（数据库/API/日志）",
    srcTitle:"数据源 src", srcLines:["结构化/半结构化","可编程访问"],
    readTitle:"D2 off-policy loop：读取", readLines:["search 结构/内容/latent-fields","（异步 batch，不占主请求路径）"],
    sigmaLabel:"Σ(src) 四段 —— 写入 Data Wiki",
    chipsA:[
      {title:"自然语言总结", desc:"summary_NL"},
      {title:"格式", desc:"σ · schema*"},
      {title:"关键词", desc:"κ · 检索锚点"},
      {title:"关联关系/外键", desc:"FK · 跨源 rels"},
    ],
    laneB:"② 复杂报表（多 sheet / 口径随时间漂移）",
    reportTitle:"复杂报表", reportLines:["Excel / BI，隐藏公式","口径随部门/时间变"],
    collabTitle:"人机协同构建规范",
    chipsB:[
      {title:"来源", desc:"哪个系统/谁导出"},
      {title:"频率", desc:"日/周/月"},
      {title:"维护", desc:"谁负责/怎么改"},
      {title:"时效性", desc:"口径何时变过"},
    ],
    refTitle:"人常用报表", refLines:["记录实际使用的报表","作为 ground-truth 参照物"],
    reflectTitle:"还原式 reflection", reflectLines:["尝试从总结+规范还原参照报表","的部分表格结构/数值"],
    gateLabel:"还原成功？",
    gateYes:"通过 → 写入 Data Wiki",
    gateNo:"失败 → 回到协同构建规范补充",
    convergeLabel:"Data Wiki（长期累积、增量更新，供 semantic join 检索）",
    repSpecTitle:"报表规范+参照物", repIncrementTitle:"…增量累积",
    propTag:["P16 · 还原式 reflection", "是摘要充分性(P8)的可操作判据"],
  },
  en:{
    title:"Data Wiki Construction — Automated Regular Sources + Human-Agent Complex Reports",
    sub:["D2 lineage: regular sources are auto read+summarized by the off-policy loop; complex",
         "reports (multi-sheet/drifting definitions) are built with humans and validated via reflection."],
    laneA:"① Regular sources (databases/APIs/logs)",
    srcTitle:"Data source src", srcLines:["structured/semi-structured","programmatically accessible"],
    readTitle:"D2 off-policy loop: read", readLines:["search structure/content/latent-fields","(async batch, off the main request path)"],
    sigmaLabel:"Σ(src) four segments — written into Data Wiki",
    chipsA:[
      {title:"NL summary", desc:"summary_NL"},
      {title:"Format", desc:"σ · schema*"},
      {title:"Keywords", desc:"κ · retrieval anchor"},
      {title:"Foreign key / relations", desc:"FK · cross-src rels"},
    ],
    laneB:"② Complex reports (multi-sheet / drifting definitions)",
    reportTitle:"Complex report", reportLines:["Excel / BI, hidden formulas","definitions drift by dept/time"],
    collabTitle:"Human-agent collaborative spec",
    chipsB:[
      {title:"Source", desc:"which system"},
      {title:"Frequency", desc:"daily/weekly"},
      {title:"Maintenance", desc:"who owns it"},
      {title:"Freshness", desc:"last changed"},
    ],
    refTitle:"Human's common reports", refLines:["Record reports actually used","as ground-truth reference"],
    reflectTitle:"Reflective reconstruction", reflectLines:["Try to rebuild part of the reference","report's tables from summary+spec"],
    gateLabel:"Reconstruction OK?",
    gateYes:"Pass → write into Data Wiki",
    gateNo:"Fail → back to spec for more detail",
    convergeLabel:"Data Wiki (accumulates long-term, incremental, queried via semantic join)",
    repSpecTitle:"Report spec + reference", repIncrementTitle:"…accumulating",
    propTag:["P16 · Reflective reconstruction","is an operational test for summary sufficiency (P8)"],
  },
};

function fig9(lang){
  const D = D9[lang];
  let s = frame(W9,H9,D.title,D.sub);

  /* ---- Lane A: regular sources ---- */
  const laneAY = 128;
  s += tline(54, laneAY, D.laneA, {size:13, weight:800, fill:C.dataText});
  const srcY = laneAY+16;
  s += rect(54,srcY,200,66,{fill:"#fff",stroke:C.neutStroke});
  s += tline(70,srcY+26,D.srcTitle,{size:13,weight:800,fill:C.ink});
  s += leftLines(70,srcY+46,D.srcLines,{size:10,fill:C.mut});

  s += hArrow(254,326,srcY+33,{stroke:C.dataStroke});
  s += rect(326,srcY,300,66,{fill:C.dataFill,stroke:C.dataStroke,sw:1.7});
  s += tline(342,srcY+26,D.readTitle,{size:13,weight:800,fill:C.dataText});
  s += leftLines(342,srcY+46,D.readLines,{size:10,fill:C.dataText});

  const sigmaY = srcY+66+34;
  s += vArrow(476, srcY+66, sigmaY-2, {stroke:C.dataStroke});
  const sigmaBox = {x:54, y:sigmaY, w:706, h:110};
  const chA = D.chipsA;
  const chipsA = [
    {x:sigmaBox.x+24, y:sigmaBox.y+38, w:158, h:56, ...chA[0]},
    {x:sigmaBox.x+200,y:sigmaBox.y+30, w:150, h:48, ...chA[1]},
    {x:sigmaBox.x+368,y:sigmaBox.y+42, w:150, h:56, ...chA[2]},
    {x:sigmaBox.x+536,y:sigmaBox.y+32, w:150, h:60, ...chA[3]},
  ];
  s += scatterContainer({box:sigmaBox, label:D.sigmaLabel, chips:chipsA});

  /* ---- Lane B: complex reports ---- */
  const laneBY = sigmaY+110+56;
  s += tline(54, laneBY, D.laneB, {size:13, weight:800, fill:C.scafText});
  const repY = laneBY+16;
  s += rect(54,repY,200,66,{fill:"#fff2e6",stroke:C.scafStroke,sw:1.6});
  s += tline(70,repY+26,D.reportTitle,{size:13,weight:800,fill:C.scafText});
  s += leftLines(70,repY+46,D.reportLines,{size:10,fill:C.scafText});

  s += hArrow(254,326,repY+33,{stroke:C.scafStroke});
  const collabBox = {x:326, y:repY, w:454, h:110};
  const chB = D.chipsB;
  const chipsB = [
    {x:collabBox.x+18, y:collabBox.y+38, w:104, h:52, ...chB[0]},
    {x:collabBox.x+134,y:collabBox.y+30, w:104, h:46, ...chB[1]},
    {x:collabBox.x+250,y:collabBox.y+44, w:104, h:52, ...chB[2]},
    {x:collabBox.x+366,y:collabBox.y+32, w:78, h:60, ...chB[3]},
  ];
  s += scatterContainer({box:collabBox, label:D.collabTitle, chips:chipsB});

  const refY = repY+66+30;
  s += vArrow(154, repY+66, refY-2, {stroke:C.mut,sw:1.6,dash:"3 4"});
  s += rect(54,refY,200,64,{fill:"#fff",stroke:C.neutStroke,dash:"5 5",filter:false});
  s += tline(70,refY+26,D.refTitle,{size:12.5,weight:800,fill:C.ink});
  s += leftLines(70,refY+44,D.refLines,{size:9.6,fill:C.mut});

  const reflectY = refY;
  const reflectBox = {x:326, y:reflectY, w:454, h:80};
  s += rect(reflectBox.x,reflectBox.y,reflectBox.w,reflectBox.h,{fill:C.detFill,stroke:C.detStroke,sw:1.7});
  s += tline(reflectBox.x+18,reflectBox.y+26,D.reflectTitle,{size:13,weight:800,fill:C.detText});
  s += leftLines(reflectBox.x+18,reflectBox.y+46,D.reflectLines,{size:10,fill:C.detText});
  s += vArrow(538, collabBox.y+collabBox.h, reflectBox.y-2, {stroke:C.scafStroke,sw:1.6,dash:"3 4"});
  s += hArrow(254, reflectBox.x, refY+32, {stroke:C.mut, sw:1.6, dash:"3 4"});

  /* decision diamond */
  const gateY = reflectY+80+56;
  const gateCx = 538;
  s += vArrow(gateCx, reflectBox.y+reflectBox.h, gateY-38, {stroke:C.detStroke});
  s += diamond(gateCx, gateY, 220, 62, {stroke:C.detStroke});
  s += centerText(gateCx, gateY, D.gateLabel, {size:12, weight:800, fill:C.detText});

  const convergeY = gateY+120;
  s += elbow([[gateCx+110,gateY],[900,gateY],[900,convergeY-14]], {stroke:C.detStroke, sw:1.8});
  s += tline(700, gateY-10, D.gateYes, {size:10.6, weight:700, fill:C.detText});

  s += elbow([[gateCx,gateY-31],[gateCx,gateY-90],[collabBox.x+collabBox.w+40,gateY-90],[collabBox.x+collabBox.w+40,collabBox.y+collabBox.h/2],[collabBox.x+collabBox.w,collabBox.y+collabBox.h/2]], {stroke:C.roseStroke, sw:1.7, dash:"5 4"});
  s += vText(collabBox.x+collabBox.w+56, gateY-140, D.gateNo, {size:9.6, weight:700, fill:C.roseText});

  /* both lanes converge into Data Wiki — route lane-A's feed down the LEFT margin
     (x=20), clear of every box in lane B (which starts at x=54), then in to the
     converge box's top-left area */
  const laneAFeedX = 20;
  s += elbow([[476, sigmaY+110],[476, sigmaY+110+18],[laneAFeedX, sigmaY+110+18],[laneAFeedX, convergeY-14],[130, convergeY-14]], {stroke:C.dataStroke, sw:1.8, dash:"3 4"});

  const convergeBox = {x:54, y:convergeY, w:1092, h:120};
  s += rect(convergeBox.x,convergeBox.y,convergeBox.w,convergeBox.h,{fill:C.harnStrong,stroke:C.harnStroke,sw:1.8});
  s += tline(convergeBox.x+18,convergeBox.y+30,D.convergeLabel,{size:13.5,weight:800,fill:C.harnText});
  // representative scattered chips inside, echoing fig7 language
  const repChips = [
    {x:convergeBox.x+20, y:convergeBox.y+50, w:150, h:46, title:"Σ(src₁)", desc:"", fill:"#fff", stroke:C.dataStroke, textColor:C.dataText},
    {x:convergeBox.x+186,y:convergeBox.y+58, w:150, h:46, title:"Σ(src₂)", desc:"", fill:"#fff", stroke:C.dataStroke, textColor:C.dataText},
    {x:convergeBox.x+352,y:convergeBox.y+48, w:180, h:46, title:D.repSpecTitle, desc:"", fill:"#fff", stroke:C.scafStroke, textColor:C.scafText},
    {x:convergeBox.x+548,y:convergeBox.y+60, w:150, h:46, title:"Σ(src₃)", desc:"", fill:"#fff", stroke:C.dataStroke, textColor:C.dataText},
    {x:convergeBox.x+714,y:convergeBox.y+50, w:170, h:46, title:D.repIncrementTitle, desc:"", fill:"#fff", stroke:C.neutStroke, textColor:C.mut},
  ];
  repChips.forEach(c=>{
    s += rect(c.x,c.y,c.w,c.h,{fill:c.fill,stroke:c.stroke,sw:1.4,rx:9,filter:false});
    s += centerText(c.x+c.w/2,c.y+c.h/2+1,c.title,{size:11,weight:700,fill:c.textColor});
  });

  const tagY = convergeY+120+20;
  s += rect(880,tagY,266,66,{fill:"#fff",stroke:C.detStroke,dash:"5 5",filter:false});
  s += leftLines(898,tagY+24,D.propTag,{size:10.4,weight:700,fill:C.detText});

  return svgWrap(W9,H9,s);
}

/* ===================================================================
   FIGURE 10 — DATA WIKI / THEME WIKI / IR COMPOSITION
   =================================================================== */
const W10=1200, H10=880;
const D10 = {
  zh:{
    title:"Data Wiki × Theme Wiki × IR 中间关系层 —— 组成图",
    sub:["两个 wiki 各自是散落、不对齐、非表格的子域容器（同图 7 σ_out 视觉语言）；",
         "IR 是唯一显式耦合点：给定 theme，查 semantic join 命中集 + 5W+1H，其余部分保持正交独立（P17）。"],
    dwLabel:"Data Wiki（承 D2）—— 数据是什么",
    dwChips:[
      {title:"Σ(销售流水)", desc:"summary·σ·κ·FK"},
      {title:"Σ(库存表)", desc:"summary·σ·κ·FK"},
      {title:"Σ(CRM客户)", desc:"summary·σ·κ·FK"},
      {title:"Σ(供应链)", desc:"summary·σ·κ·FK"},
      {title:"月度报表规范", desc:"来源·频率·维护·时效"},
    ],
    irLabel:"IR · Intermediate Relation",
    irSub:"theme ↦ ⟨semantic-join 命中集, 5W+1H⟩",
    fiveWH:[
      {title:"When", desc:"时效性/更新频率"},
      {title:"Where", desc:"内网/外网/互联网"},
      {title:"Who", desc:"数据拥有者/授权"},
      {title:"What", desc:"数据语义(=Σ)"},
      {title:"Why", desc:"集成逻辑(join 理由)"},
      {title:"How", desc:"物理访问方式"},
    ],
    joinLabel:"semantic join ⋈",
    twLabel:"Theme Wiki（承 D3 产出侧）—— 产出该长什么样",
    twChips:[
      {title:"季度报表模板", desc:"σ_out·报表子域"},
      {title:"KPI 图表模板", desc:"σ_out·图表子域"},
      {title:"董事会 PPT", desc:"σ_out·PPT子域"},
      {title:"分析报告框架", desc:"σ_out·报告子域"},
      {title:"预测模型程序", desc:"σ_out·模型子域"},
    ],
    hFlowLabel:"H 契约映射：𝓘 → IR(theme) → ⟨{Σ}, 5W1H⟩ → D₁ 取数 → 𝓔",
    propTag:["P17 · IR 松耦合","数据源变更 / 产出格式变更互不传播，只需更新 IR"],
  },
  en:{
    title:"Data Wiki × Theme Wiki × IR — Composition Diagram",
    sub:["Both wikis are scattered, unaligned, non-tabular subdomain containers (same visual",
         "language as Fig.7's σ_out); IR is the only explicit coupling point (P17)."],
    dwLabel:"Data Wiki (D2 lineage) — what the data is",
    dwChips:[
      {title:"Σ(sales ledger)", desc:"summary·σ·κ·FK"},
      {title:"Σ(inventory)", desc:"summary·σ·κ·FK"},
      {title:"Σ(CRM customers)", desc:"summary·σ·κ·FK"},
      {title:"Σ(supply chain)", desc:"summary·σ·κ·FK"},
      {title:"Monthly report spec", desc:"source·freq·maint·freshness"},
    ],
    irLabel:"IR · Intermediate Relation",
    irSub:"theme ↦ ⟨semantic-join hit set, 5W+1H⟩",
    fiveWH:[
      {title:"When", desc:"freshness/cadence"},
      {title:"Where", desc:"intra/extranet"},
      {title:"Who", desc:"owner/auth"},
      {title:"What", desc:"data semantics"},
      {title:"Why", desc:"join rationale"},
      {title:"How", desc:"access method"},
    ],
    joinLabel:"semantic join ⋈",
    twLabel:"Theme Wiki (D3 output side) — what output looks like",
    twChips:[
      {title:"Quarterly report tpl", desc:"σ_out·report"},
      {title:"KPI chart tpl", desc:"σ_out·chart"},
      {title:"Board PPT", desc:"σ_out·PPT"},
      {title:"Analysis report frame", desc:"σ_out·report"},
      {title:"Forecast model program", desc:"σ_out·model"},
    ],
    hFlowLabel:"H contract map: 𝓘 → IR(theme) → ⟨{Σ}, 5W1H⟩ → D₁ access → 𝓔",
    propTag:["P17 · IR decoupling","src changes / output-format changes don't propagate, only IR updates"],
  },
};

function fig10(lang){
  const D = D10[lang];
  let s = frame(W10,H10,D.title,D.sub);

  const topY = 128;
  const dwBox = {x:40, y:topY, w:360, h:340};
  const twBox = {x:800, y:topY, w:360, h:340};
  const irBox = {x:432, y:topY+30, w:336, h:280};

  /* Data Wiki (left, scattered) */
  const dwChips = [
    {x:dwBox.x+20, y:dwBox.y+42, w:150, h:56, ...D.dwChips[0]},
    {x:dwBox.x+190,y:dwBox.y+34, w:150, h:50, ...D.dwChips[1]},
    {x:dwBox.x+16, y:dwBox.y+116,w:160, h:56, ...D.dwChips[2]},
    {x:dwBox.x+196,y:dwBox.y+132,w:144, h:60, ...D.dwChips[3]},
    {x:dwBox.x+40, y:dwBox.y+206,w:270, h:56, ...D.dwChips[4], fill:"#fff2e6", stroke:C.scafStroke, textColor:C.scafText},
  ];
  s += scatterContainer({box:dwBox, label:D.dwLabel, chips:dwChips});

  /* Theme Wiki (right, scattered) */
  const twChips = [
    {x:twBox.x+20, y:twBox.y+42, w:160, h:54, ...D.twChips[0]},
    {x:twBox.x+198,y:twBox.y+36, w:144, h:48, ...D.twChips[1]},
    {x:twBox.x+18, y:twBox.y+114,w:150, h:54, ...D.twChips[2]},
    {x:twBox.x+188,y:twBox.y+130,w:154, h:58, ...D.twChips[3]},
    {x:twBox.x+40, y:twBox.y+206,w:270, h:56, ...D.twChips[4]},
  ];
  s += scatterContainer({box:twBox, label:D.twLabel, chips:twChips});

  /* IR bridge in the middle */
  s += rect(irBox.x,irBox.y,irBox.w,irBox.h,{fill:C.harnStrong,stroke:C.harnStroke,sw:2});
  s += centerText(irBox.x+irBox.w/2, irBox.y+28, D.irLabel, {size:14.5, weight:800, fill:C.harnText});
  s += centerText(irBox.x+irBox.w/2, irBox.y+50, D.irSub, {size:10, weight:400, fill:C.mut, mono:true});

  // 5W1H as a clean 3x2 grid (deliberately grid-like here — it IS a defined 6-tuple, unlike the free-form subdomains)
  const cellW=104, cellH=64, gx=8, gy=8;
  const gridX0 = irBox.x + (irBox.w - (3*cellW+2*gx))/2;
  const gridY0 = irBox.y + 66;
  D.fiveWH.forEach((f,i)=>{
    const col=i%3, row=Math.floor(i/3);
    const x=gridX0+col*(cellW+gx), y=gridY0+row*(cellH+gy);
    const pal = CHIP_PALETTE[i%CHIP_PALETTE.length];
    s += rect(x,y,cellW,cellH,{fill:pal.fill, stroke:pal.stroke, sw:1.4, rx:9, filter:false});
    s += centerText(x+cellW/2, y+22, f.title, {size:12, weight:800, fill:pal.text});
    s += centerText(x+cellW/2, y+42, f.desc, {size:8.6, weight:400, fill:pal.text});
  });

  // arrows: Data Wiki -> IR (semantic join), IR -> Theme Wiki (theme lookup)
  s += hArrow(dwBox.x+dwBox.w, irBox.x, dwBox.y+dwBox.h/2, {stroke:C.dataStroke, sw:1.9});
  s += tline((dwBox.x+dwBox.w+irBox.x)/2 - 30, dwBox.y+dwBox.h/2 - 10, D.joinLabel, {size:10, weight:700, fill:C.dataStroke, mono:true});
  s += hArrow(irBox.x+irBox.w, twBox.x, twBox.y+twBox.h/2, {stroke:C.harnStroke, sw:1.9});

  /* H contract flow strip at the bottom */
  const flowY = topY+340+56;
  s += rect(40,flowY,1120,56,{fill:"#f1ebe0",stroke:C.harnStroke,dash:"6 6",filter:false});
  s += centerText(600, flowY+30, D.hFlowLabel, {size:12.5, weight:700, fill:C.harnText, mono:true});
  s += vArrow(600, topY+340+30, flowY-2, {stroke:C.harnStroke, sw:1.6, dash:"3 4"});

  const tagY = flowY+56+24;
  s += rect(40,tagY,1120,58,{fill:"#fff",stroke:C.detStroke,dash:"5 5",filter:false});
  s += leftLines(60,tagY+24,D.propTag,{size:11,weight:700,fill:C.detText});

  return svgWrap(W10,H10,s);
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
  const svg9 = fig9(lang);
  fs.writeFileSync(path.join(FIGDIR,`f9-${lang}.svg`), svg9);
  fs.writeFileSync(path.join(FIGDIR,`f9-${lang}.html`), htmlWrap(W9,H9,svg9));
  built.push({num:9,lang});

  const svg10 = fig10(lang);
  fs.writeFileSync(path.join(FIGDIR,`f10-${lang}.svg`), svg10);
  fs.writeFileSync(path.join(FIGDIR,`f10-${lang}.html`), htmlWrap(W10,H10,svg10));
  built.push({num:10,lang});
}
console.log(`built ${built.length} figure variants:`);
built.forEach(b => console.log(`  f${b.num}-${b.lang}`));
module.exports = { W9,H9,W10,H10, built };
