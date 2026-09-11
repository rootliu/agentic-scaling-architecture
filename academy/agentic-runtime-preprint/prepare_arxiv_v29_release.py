"""Build and statically validate an arXiv replacement handoff; no TeX compilation."""
from pathlib import Path, PurePosixPath
import collections
import hashlib
import json
import re
import subprocess
import sys
import tarfile
import zipfile
from PIL import Image
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "arxiv-release-v29"
AUTHORS = ["Yaxiao Liu", "Pengbo Liu", "Yiwen Liu", "Yihua Guan", "Zhenghe Hou", "Jiaxing Song"]
BASE = ROOT / "arxiv-v29"
PDF = ROOT / "output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v29.pdf"
def digest(b):
    return hashlib.sha256(b).hexdigest()

def main():
    subprocess.run([sys.executable, str(ROOT / "build_arxiv_v29.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / "latex_to_preprint.py")], check=True)
    tex = (BASE / "main.tex").read_text()
    bib = (BASE / "references.bib").read_text()
    canonical = (ROOT / "paper_source/main.tex").read_text()
    abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S)[1].strip()
    canonical_abstract = re.search(r"\\section\{Abstract\}(.*?)\\section\{Introduction\}", canonical, re.S)[1].strip()
    assert abstract == canonical_abstract
    assert len(abstract) <= 1920 and abstract.isascii()
    assert tex.startswith(r"\documentclass") and tex.count(r"\maketitle") == 1
    assert tex.count(r"\begin{document}") == tex.count(r"\end{document}") == 1
    assert tex.isascii()
    stack = []
    for match in re.finditer(r"\\(begin|end)\{([^}]+)\}", tex):
        kind, env = match.groups()
        if kind == "begin": stack.append(env)
        else: assert stack.pop() == env, (env, stack)
    assert not stack
    depth = 0
    i = 0
    while i < len(tex):
        if tex[i] == "\\":
            i += 2
            continue
        if tex[i] == "%":
            i = tex.find("\n", i)
            if i == -1: break
            continue
        if tex[i] == "{": depth += 1
        if tex[i] == "}": depth -= 1
        assert depth >= 0
        i += 1
    assert depth == 0
    labels = re.findall(r"\\label\{([^}]+)\}", tex)
    assert len(labels) == len(set(labels))
    refs = re.findall(r"\\ref\{([^}]+)\}", tex)
    assert not set(refs) - set(labels)
    cites = {x.strip() for group in re.findall(r"\\cite\{([^}]+)\}", tex) for x in group.split(",")}
    keys = re.findall(r"@\w+\s*\{\s*([^,\s]+)", bib)
    assert len(keys) == len(set(keys)) == 53
    assert cites == set(keys)
    assert bib == (ROOT / "paper_source/references.bib").read_text()
    authorblock = tex.split(r"\author{", 1)[1].split(r"\date", 1)[0]
    positions = [authorblock.index(a) for a in AUTHORS]
    assert positions == sorted(positions) and authorblock.count(r"\and") == 5
    graphics = re.findall(r"\\includegraphics\[[^]]*\]\{([^}]+)\}", tex)
    assert graphics == ["1.png", "2.png", "3.png", "4.png", "6.png", "5.png", "7.png"]
    assert tex.count(r"\begin{figure}") == 8
    for name in graphics:
        with Image.open(BASE / name) as im: im.verify()
    archive = ROOT / "arxiv/arxiv-submit-v29.tar.gz"
    upload = ROOT / "arxiv/arxiv-submit-v29.zip"
    with tarfile.open(archive) as tar:
        members = tar.getmembers()
        assert all(x.isfile() and not PurePosixPath(x.name).is_absolute() and ".." not in PurePosixPath(x.name).parts for x in members)
        payload = {x.name: tar.extractfile(x).read() for x in members}
    with zipfile.ZipFile(upload) as z:
        assert z.testzip() is None
        assert payload == {n: z.read(n) for n in z.namelist()}
    expected = {"main.tex", "references.bib", *graphics}
    expected |= {"anc/artifact_v29/" + n for n in [
        "ir_contract.py", "evaluate.py", "test_contract.py", "README.md",
        "results/summary.json", "results/fault-cases.csv"]}
    assert set(payload) == expected
    for name, data in payload.items():
        assert data == (BASE / name).read_bytes()
        if name.startswith("anc/artifact_v29/"):
            assert data == (ROOT / name.removeprefix("anc/")).read_bytes()
    summary = json.loads(payload["anc/artifact_v29/results/summary.json"])
    assert (summary["cases"], summary["accepted"], summary["rejected"], summary["oracle_disagreements"]) == (1024, 1, 1023, 0)
    for name, sha in summary["sha256"].items():
        assert digest(payload["anc/artifact_v29/" + name]) == sha
    reader = PdfReader(PDF)
    pdftext = "\n".join(page.extract_text() or "" for page in reader.pages)
    for a in AUTHORS: assert a in pdftext
    assert "1,024" in pdftext
    # Whitespace may differ in PDF layout; all abstract sentences must survive.
    norm = lambda s: re.sub(r"\s+", " ", s).strip()
    assert norm(abstract) in norm(pdftext)
    assert digest((ROOT / "output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v28.pdf").read_bytes()) == "6e5d3e12e226311219f12189577f88c3bcd757c2b7b6b0ef8140b61c2340f19b"
    OUT.mkdir(exist_ok=True)
    title = re.search(r"\\title\{([^}]+)\}", tex)[1]
    comments = ("8 figures; revised data-use contracts with an executable reference model and finite "
                "synthetic conformance artifact; updated related work and experimental decision rules. "
                "Runtime scaling remains empirically untested.")
    fields = {
        "title.txt": title,
        "authors.txt": ", ".join(AUTHORS),
        "abstract.txt": abstract,
        "comments.txt": comments,
    }
    for name, value in fields.items():
        assert value.isascii()
        (OUT / name).write_text(value + "\n")
    report = {
        "prepared_date": "2026-09-11",
        "existing_article": "2608.27086",
        "internal_revision": "v29",
        "arxiv_submission_performed": False,
        "validation": "static source checks and repository ReportLab PDF; NOT TeX compilation",
        "tex_compilation": "pending arXiv processing and preview",
        "abstract_characters": len(abstract),
        "abstract_identical_across_source_pdf_metadata": True,
        "authors": AUTHORS,
        "citation_entries": len(keys),
        "unresolved_citation_or_reference_keys": [],
        "figure_environments": 8,
        "image_files_in_manuscript_order": graphics,
        "upload_file_count": len(payload),
        "pdf_pages_reportlab_only": len(reader.pages),
        "archived_files": [{"path": n, "bytes": len(b), "sha256": digest(b)} for n, b in sorted(payload.items())],
        "deliverables": [{"path": str(f.relative_to(ROOT)), "bytes": f.stat().st_size,
                          "sha256": digest(f.read_bytes())} for f in [archive, upload, PDF]]
    }
    (OUT / "VALIDATION.json").write_text(json.dumps(report, indent=2) + "\n")
    checksums = "\n".join(x["sha256"] + "  " + x["path"] for x in report["deliverables"])
    (OUT / "SHA256SUMS.txt").write_text(checksums + "\n")
    guide = f"""# v29 arXiv 替换投稿：完整交付包

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
4. 四个 TXT 文件可直接复制到同名字段：title、authors、abstract、comments。摘要为 {len(abstract)} 个 ASCII 字符，与论文一致。
5. 保留原文章类别 cs.AI（主类）、cs.MA、cs.SE，以及原有 CC BY 4.0 许可。作者顺序和正文单位沿用前版。
6. 查看 arXiv 实际生成的 PDF，确认全部作者、摘要、8幅图、表格、附录和53条引用，无未解析引用或缺页。
7. Comments 未填写页数：本地阅读稿为 {len(reader.pages)} 页，但 arXiv 排版可能不同；如添加页数，以网页生成 PDF 为准。
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
"""
    (OUT / "README-提交说明.md").write_text(guide)
    combined = OUT / "v29-arxiv-complete.zip"
    with zipfile.ZipFile(combined, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(OUT.iterdir()):
            if f.is_file() and f != combined: z.write(f, f.name)
        z.write(upload, upload.name)
        z.write(PDF, PDF.name)
    print(json.dumps({k: report[k] for k in ["abstract_characters", "citation_entries", "figure_environments", "upload_file_count", "pdf_pages_reportlab_only"]}))
    print(combined)

if __name__ == "__main__":
    main()
