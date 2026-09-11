"""Build a source archive from the canonical body, preserving v28's author block.

This performs source assembly, not a TeX compilation. The repository uses its
ReportLab renderer for local PDF validation. arXiv must compile the source.
"""
from pathlib import Path
import re
import shutil
import tarfile
import zipfile
import gzip

ROOT = Path(__file__).resolve().parent


def main():
    body = (ROOT / "paper_source/main.tex").read_text()
    old = (ROOT / "arxiv/main.tex").read_text()
    preamble = old.split(r"\begin{document}", 1)[0]
    body = body.replace(r"\begin{document}", r"\begin{document}" + "\n" + r"\maketitle", 1)
    body = body.replace(r"\section{Abstract}", r"\begin{abstract}", 1)
    body = body.replace(r"\section{Introduction}", r"\end{abstract}" + "\n\n" + r"\section{Introduction}", 1)
    # Figure file numbers are not manuscript order (dry-run=6, external-data=5).
    # The eighth figure is a native TeX matrix, not another image.
    graphics = {}
    pattern = r"\\begin\{figure\}\[t\].*?\\end\{figure\}"
    for block in re.findall(pattern, old, re.S):
        label = re.search(r"\\label\{([^}]+)\}", block).group(1)
        graphics[label] = block.split(r"\centering", 1)[1].split(r"\caption", 1)[0]
    graphics["fig:evaluation-matrix"] = graphics["fig:evaluation-matrix"].replace(
        r"Falsified within $\Omega$ if a semantic, runtime, or enforcement interaction exceeds its preregistered margin. Inconclusive if operating-region, condition, or detectable-interaction requirements fail. Otherwise supported within $\Omega$.",
        "Insufficient evidence: inconclusive. Clearly violated obligations: conditional-engineering. "
        "Only after all obligation gates pass, resolve runtime interaction, semantic non-inferiority, "
        "and cost bounds as supported, falsified, or inconclusive.",
    )

    def insert_figure(match):
        block = match.group(0)
        label = re.search(r"\\label\{([^}]+)\}", block).group(1)
        return block.replace(r"\centering", r"\centering" + graphics[label], 1)

    body = re.sub(pattern, insert_figure, body, flags=re.S)
    assert len(graphics) == 8 and body.count(r"\includegraphics") == 7
    out = ROOT / "arxiv-v29"
    out.mkdir(exist_ok=True)
    (out / "main.tex").write_text(preamble + body)
    shutil.copy2(ROOT / "paper_source/references.bib", out / "references.bib")
    for i in range(1, 8):
        shutil.copy2(ROOT / "arxiv" / f"{i}.png", out / f"{i}.png")
    artifact = out / "anc" / "artifact_v29"
    artifact.mkdir(parents=True, exist_ok=True)
    for name in ["ir_contract.py", "evaluate.py", "test_contract.py", "README.md"]:
        shutil.copy2(ROOT / "artifact_v29" / name, artifact / name)
    shutil.copytree(ROOT / "artifact_v29/results", artifact / "results", dirs_exist_ok=True)
    # Explicit allowlist keeps stale build files and unrelated local data out.
    names = ["main.tex", "references.bib"] + [f"{i}.png" for i in range(1, 8)]
    names += [f"anc/artifact_v29/{n}" for n in
              ["ir_contract.py", "evaluate.py", "test_contract.py", "README.md",
               "results/summary.json", "results/fault-cases.csv"]]
    archive = ROOT / "arxiv" / "arxiv-submit-v29.tar.gz"
    with archive.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
            with tarfile.open(fileobj=gz, mode="w") as tar:
                for name in sorted(names):
                    info = tar.gettarinfo(str(out / name), arcname=name)
                    info.uid = info.gid = 0
                    info.uname = info.gname = ""
                    info.mtime = 0
                    info.mode = 0o644
                    with (out / name).open("rb") as source:
                        tar.addfile(info, source)
    upload_zip = archive.with_name("arxiv-submit-v29.zip")
    with zipfile.ZipFile(upload_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(names):
            entry = zipfile.ZipInfo(name, date_time=(2026, 9, 11, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o644 << 16
            z.writestr(entry, (out / name).read_bytes())
    print(archive)
    print(upload_zip)


if __name__ == "__main__":
    main()
