# v29 内部分享 / Internal sharing

两份演示各 22 页，建议讲解 25 分钟、讨论 10 分钟。内容覆盖三层责任架构、能力与容量解耦问题、Data Wiki / Theme Wiki / IR、5W1H+Which 数据契约、执行期重验证、有限验证、近期论文与后续实验。

| 语言 / Language | PowerPoint | 讲稿 / Speaker notes | PDF 预览 / Preview |
|---|---|---|---|
| 中文 | [中文 PPT](paper-v29-internal-zh.pptx) | [逐页讲稿](speaker-notes-zh.md) | [预览 PDF](paper-v29-internal-zh-preview.pdf) |
| English | [English PPT](paper-v29-internal-en.pptx) | [Speaker notes](speaker-notes-en.md) | [Preview PDF](paper-v29-internal-en-preview.pdf) |

图形和文本为可编辑的 PowerPoint 元素；备注中含讲稿和可点击来源。字体使用 Noto Sans CJK SC，缺少字体时 PowerPoint 可能替换字体并改变版面。

The deck distinguishes implemented finite checks from proposed empirical studies. The 1,024 cases are an exhaustive constructed domain, not a statistical sample. P1 and real-world improvements remain unevaluated. Internal manuscript v29 has not yet replaced the existing arXiv version.

PDF 和缩略图由同一布局描述生成，属于场景预览，并非 PowerPoint/LibreOffice 实际渲染。已检查两份 PPT 均为 22 页、备注非空、文本测量可容纳且所有元素位于画布内，并人工检查中英文缩略图。

Rebuild from this directory with `python build_decks.py`. Requires Python, python-pptx 1.0.2, Pillow, ReportLab, and the Noto Sans CJK regular/bold font files at the paths in the script. Evidence numbers are read from the committed artifact results.

- [v29 manuscript review and limitations](../agentic-runtime-preprint/V29_REVIEW.md)
- [Today's literature notes](../../notes/2026-09-10-v29/README.md)
