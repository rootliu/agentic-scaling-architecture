# v29 arXiv 替换投稿：完整交付包

准备日期：2026-09-11。目标文章：2608.27086；使用已有文章的 Replace / 更新版本入口。
内部版本 v29 不等于 arXiv 版本号；本次尚未代你提交。

## 你今天要上传哪个文件

上传 **arxiv-submit-v29.zip** 或同内容的 **arxiv-submit-v29.tar.gz**，二选一。
仓库位置在 ../arxiv/。ZIP 根目录就是 main.tex，可直接上传整个 ZIP。
**不要把 v29-arxiv-complete.zip 整体上传**：它是供下载携带的总交付包，含说明、阅读 PDF 和上传包。

上传包内有独立 main.tex、references.bib、7张PNG，以及 anc/artifact_v29/ 下的代码和逐例结果。
正文共8个 figure 环境：7张图片加1个原生 TeX 评估矩阵。不存在第8张图片缺失问题。
不含历史稿、PPT、缓存、编译中间文件或本地凭据。

## 网页填写与处理顺序

1. 登录 arXiv，找到 2608.27086，选择 Replace。如果你已经创建但尚未完成替换提交，继续那个草稿。
2. 在文件步骤确认使用新上传包的完整文件集；不要留下旧 main.tex 或其他旧版本入口。
3. 选择 main.tex 为主文件，LaTeX 的 PDF 模式（PDFLaTeX）；参考文献为 plain + BibTeX。
4. 四个 TXT 文件可直接复制到同名字段：title、authors、abstract、comments。摘要为 1463 个 ASCII 字符，与论文一致。
5. 保留原文章类别 cs.AI（主类）、cs.MA、cs.SE，以及原有 CC BY 4.0 许可。作者顺序和正文单位沿用前版。
6. 查看 arXiv 实际生成的 PDF，确认全部作者、摘要、8幅图、表格、附录和53条引用，无未解析引用或缺页。
7. Comments 未填写页数：本地阅读稿为 44 页，但 arXiv 排版可能不同；如添加页数，以网页生成 PDF 为准。
8. 最后提交并保存 receipt。是否成功更新，以 arXiv 的提交状态与后续公告为准。

## 已完成的检查与仍需网页确认的部分

已检查独立源码入口、环境和花括号平衡、交叉引用与引用键闭合、作者顺序、图片完整性、
ZIP/TAR内容一致、附件与参考实现逐字节一致、摘要与本地PDF及网页文本一致，并保留 v28 PDF。
VALIDATION.json 和 SHA256SUMS.txt 记录清单与校验和。

本地 PDF 由仓库 ReportLab 生成器产生，是完整阅读稿；**不是上传源码经 TeX 编译后的预览**。
仓库工作规范禁止运行 pdflatex/latexmk，所以本地未验证 TeX 编译和浮动体最终分页；
必须完成第6步。当前 arXiv 支持直接处理 .bib，不需要伪造或手写 .bbl。

## 修订内容

统一论文和投稿摘要；补齐新引用在 plain 样式下可见的 arXiv 标识；
保留 v29 的可执行数据契约、有限一致性验证、5项生命周期检查和尚未验证 P1 的边界。
未添加未经运行的真实任务或扩展实验结果。

## 重建

在 academy/agentic-runtime-preprint/ 目录运行：
python prepare_arxiv_v29_release.py

依赖与已有PDF生成器相同，另外使用 Pillow 和 pypdf。源码入口仍是 paper_source/main.tex 和 references.bib。

## 官方依据

- [源码与参考文献处理](https://info.arxiv.org/help/submit_tex.html)
- [标题、作者、摘要与 Comments 字段](https://info.arxiv.org/help/prep.html)
- [替换已有文章](https://info.arxiv.org/help/replace.html)
