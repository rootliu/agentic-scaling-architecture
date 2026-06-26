const fs = require("fs");

// ---- extract the architecture-plate SVG from architecture.html ----
const html = fs.readFileSync(__dirname + "/../architecture.html", "utf8");
const i = html.indexOf("architecture-plate");
const s = html.indexOf("<svg", i);
const e = html.indexOf("</svg>", s) + 6;
let svgZh = html.slice(s, e);

// native size from viewBox 0 0 1120 760
const W = 1120, H = 760;

// ---- English translation: ordered, unique exact-string replacements ----
const tx = [
  ['aria-label="Agentic 三层架构、控制数据面切分与栈外数据子系统总览图"',
   'aria-label="Overview of the Agentic three-layer architecture, control/data-plane split, and out-of-stack data subsystem"'],
  ['A = ⟨S, H, X⟩ 之外挂接数据子系统 𝒟；三条正交切分共享同一解耦不变量',
   'A = ⟨S, H, X⟩ with data subsystem 𝒟 attached; three orthogonal cuts share one decoupling invariant'],
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
  ['P1-P3: 扩展轴 · P4-P6: CP/DP 平面 · P7-P9: 数据子系统；核心证伪点是成本是否回流到高频在线路径。',
   'P1-P3: scaling axis · P4-P6: CP/DP planes · P7-P9: data subsystem; key falsifier: does cost flow back to the hot online path.'],
];

let svgEn = svgZh;
for (const [a, b] of tx) {
  if (!svgEn.includes(a)) { console.error("MISS:", a); process.exit(1); }
  svgEn = svgEn.split(a).join(b);
}
// shrink the big unified-invariant headline so the longer EN text fits
svgEn = svgEn.replace(
  '<text x="72" y="624" fill="#221f1a" font-size="22" font-weight="700">First-order cost',
  '<text x="72" y="624" fill="#221f1a" font-size="17" font-weight="700">First-order cost');
// D₂ / D₃ headers: shrink so they stay inside their narrow cards
svgEn = svgEn.replace(
  '<text x="950" y="204" fill="#0f5e87" font-size="15" font-weight="700">D₂ Semantic Σ</text>',
  '<text x="950" y="204" fill="#0f5e87" font-size="13" font-weight="700">D₂ Semantic Σ</text>');
svgEn = svgEn.replace(
  '<text x="812" y="306" fill="#0f5e87" font-size="15" font-weight="700">D₃ Governance</text>',
  '<text x="812" y="306" fill="#0f5e87" font-size="13" font-weight="700">D₃ Governance</text>');
// off-policy loop header: shrink to fit the dashed box width
svgEn = svgEn.replace(
  '<text x="812" y="420" fill="#0f5e87" font-size="15" font-weight="700">off-policy loop 𝓛₂ (out-of-stack)</text>',
  '<text x="812" y="420" fill="#0f5e87" font-size="13" font-weight="700">off-policy loop 𝓛₂ (out-of-stack)</text>');

const page = (svg, lang) => `<!DOCTYPE html>
<html lang="${lang}"><head><meta charset="UTF-8">
<style>
  @page { size: ${W}px ${H}px; margin: 0; }
  html,body { margin:0; padding:0; background:#fffdf8; }
  #plate { width:${W}px; height:${H}px; }
  #plate svg { display:block; width:${W}px; height:${H}px; }
</style></head>
<body><div id="plate">${svg}</div></body></html>`;

fs.writeFileSync(__dirname + "/arch_zh.html", page(svgZh, "zh-CN"));
fs.writeFileSync(__dirname + "/arch_en.html", page(svgEn, "en"));
console.log("wrote arch_zh.html and arch_en.html");
