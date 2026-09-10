"""Build a source archive from the canonical body, preserving v28's author block.

This performs source assembly, not a TeX compilation. The repository uses its
ReportLab renderer for local PDF validation. arXiv must compile the source.
"""
from pathlib import Path
import re
import shutil
import tarfile

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
    archive = ROOT / "arxiv" / "arxiv-submit-v29.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        for path in sorted(out.rglob("*")):
            if path.is_file():
                tar.add(path, arcname=str(path.relative_to(out)))
    print(archive)


if __name__ == "__main__":
    main()
