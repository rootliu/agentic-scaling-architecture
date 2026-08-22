const fs = require("fs");

// ---- extract the three-layer architecture SVG from architecture.html ----
// Find the SVG with the aria-label containing "三层架构" (the main architecture plate)
const html = fs.readFileSync(__dirname + "/../architecture.html", "utf8");
const marker = 'aria-label="Agentic 三层架构';
const i = html.indexOf(marker);
if (i === -1) { console.error("Cannot find architecture SVG marker"); process.exit(1); }
const s = html.lastIndexOf("<svg", i);
const e = html.indexOf("</svg>", s) + 6;
let svgZh = html.slice(s, e);

// native size from viewBox 0 0 1120 760
const W = 1120, H = 760;

// ---- English translation: ordered, unique exact-string replacements ----
const tx = [
  ['aria-label="Agentic 三层架构、控制数据面切分与栈外数据子系统总览图"',
   'aria-label="Overview of the Agentic three-layer architecture, control/data-plane split, and out-of-stack data subsystem"'],
  ['A = ⟨S, H, X⟩ + 𝒟；扩展轴 · CP/DP · 数据子系统 · 并行局部性共享同一解耦不变量',
   'A = ⟨S, H, X⟩ + 𝒟; scaling axes · CP/DP · data subsystem · parallel locality share one decoupling invariant'],
  ['task specs · I/O schema · 调用 / 终止 / 循环条件',
   'task specs · I/O schema · call / stop / loop conditions'],
  ['逻辑扩展：+Skill → 能力覆盖 𝒯↑',
   'Logical scaling: +Skill → capability coverage 𝒯↑'],
  ['唯一解耦点：H 把意图 𝓘 翻译为可执行单元 𝓔',
   'Sole decoupling point: H translates intent 𝓘 into executable units 𝓔'],
  ['>契约翻译<', '>contract xlate<'],
  ['>路由/工具<', '>routing / tools<'],
  ['>维护 M<', '>maintenance M<'],
  ['microVM · sandbox · serving · 吞吐 Θ↑',
   'microVM · sandbox · serving · throughput Θ↑'],
  ['>CP 控制面<', '>CP · Control Plane<'],
  ['skill 选择 · H 翻译', 'skill selection · H translate'],
  ['M 触发 · 审计日志', 'M trigger · audit log'],
  ['>不变量执行<', '>invariant enforcement<'],
  ['N0：概率性控制面', 'N0: probabilistic CP'],
  ['>DP 数据面<', '>DP · Data Plane<'],
  ['成本 ∝ token 流量', 'cost ∝ token traffic'],
  ['D₁ 取数 API', 'D₁ Fetch API'],
  ['D₂ 语义 Σ', 'D₂ Semantic Σ'],
  ['D₃ 治理记忆', 'D₃ Governance'],
  ['栈外 off-policy loop 𝓛₂', 'off-policy loop 𝓛₂ (out-of-stack)'],
  ['schema-on-read · async · 不截断 lake',
   'schema-on-read · async · non-trunc lake'],
  ['新增能力的一阶成本，落在与主请求路径解耦的平面 / 子系统上',
   'First-order cost of new capability lands on a plane / subsystem decoupled from the main request path'],
  ['>逻辑扩展 → CP<', '>Logical scaling → CP<'],
  ['覆盖 𝒯↑ · 吞吐不被拖垮', 'coverage 𝒯↑ · throughput unharmed'],
  ['>物理扩展 → DP<', '>Physical scaling → DP<'],
  ['吞吐 Θ↑ · 语义覆盖不变', 'throughput Θ↑ · coverage unchanged'],
  ['>数据扩展 → 𝓛₂<', '>Data scaling → 𝓛₂<'],
  ['源增加 · 单请求成本不升', 'more sources · per-request cost flat'],
  ['>并行扩展 → 工具集边界<', '>Parallel scaling → toolset boundary<'],
  ['ρ↓ · H↑ · 只传摘要', 'ρ↓ · H↑ · summary-only'],
  ['P1-P3: 扩展轴 · P4-P6: CP/DP · P7-P9: 𝒟 · P10-P13: 并行局部性 · P14: Skill-as-Code 确定性锚 · P15: 双子目标 Reward 训练。',
   'P1-P3: scaling axes · P4-P6: CP/DP · P7-P9: 𝒟 · P10-P13: parallel locality · P14: Skill-as-Code determinism anchor · P15: dual-subgoal reward training.'],
];

let svgEn = svgZh;
for (const [a, b] of tx) {
  if (!svgEn.includes(a)) { console.error("MISS:", a); process.exit(1); }
  svgEn = svgEn.split(a).join(b);
}
// shrink the big unified-invariant headline so the longer EN text fits
svgEn = svgEn.replace(
  '<text x="72" y="624" fill="#111827" font-size="22" font-weight="700">First-order cost',
  '<text x="72" y="624" fill="#111827" font-size="17" font-weight="700">First-order cost');
// D₂ / D₃ headers: shrink so they stay inside their narrow cards
svgEn = svgEn.replace(
  '<text x="950" y="204" fill="#047857" font-size="15" font-weight="700">D₂ Semantic Σ</text>',
  '<text x="950" y="204" fill="#047857" font-size="13" font-weight="700">D₂ Semantic Σ</text>');
svgEn = svgEn.replace(
  '<text x="812" y="306" fill="#047857" font-size="15" font-weight="700">D₃ Governance</text>',
  '<text x="812" y="306" fill="#047857" font-size="13" font-weight="700">D₃ Governance</text>');
// off-policy loop header: shrink to fit the dashed box width
svgEn = svgEn.replace(
  '<text x="812" y="420" fill="#047857" font-size="15" font-weight="700">off-policy loop 𝓛₂ (out-of-stack)</text>',
  '<text x="812" y="420" fill="#047857" font-size="13" font-weight="700">off-policy loop 𝓛₂ (out-of-stack)</text>');

const page = (svg, lang) => `<!DOCTYPE html>
<html lang="${lang}"><head><meta charset="UTF-8">
<style>
  @page { size: ${W}px ${H}px; margin: 0; }
  html,body { margin:0; padding:0; background:#FFFFFF; }
  #plate { width:${W}px; height:${H}px; }
  #plate svg { display:block; width:${W}px; height:${H}px; }
</style></head>
<body><div id="plate">${svg}</div></body></html>`;

fs.writeFileSync(__dirname + "/arch_zh.html", page(svgZh, "zh-CN"));
fs.writeFileSync(__dirname + "/arch_en.html", page(svgEn, "en"));
console.log("wrote arch_zh.html and arch_en.html");
