import argparse
import datetime as dt
import math
import os
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    Flowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


TITLE = "A Contract-Centered Architecture for Scalable and Manageable Agentic Runtimes"
AUTHOR = "Yaxiao Liu"
AUTHOR_EMAIL = "rootliu@gmail.com"
FIGURE_WIDTH = 462
PREPRINT_VERSION = "v20"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUTPUT = os.path.join(
    SCRIPT_DIR,
    "output",
    "pdf",
    "Scalable_Manageable_Agentic_Runtime_Preprint_v20.pdf",
)
RESPONSIBILITY_BAND_HEIGHT = 74


def hx(value: str):
    return colors.HexColor(value)


def draw_wrapped(canvas, text: str, x: float, top: float, width: float, font_name: str,
                 font_size: float, color: str, align=TA_CENTER, leading: float | None = None):
    style = ParagraphStyle(
        "FigureText",
        fontName=font_name,
        fontSize=font_size,
        leading=leading or font_size + 1.8,
        textColor=hx(color),
        alignment=align,
    )
    para_obj = Paragraph(escape(text).replace("\n", "<br/>"), style)
    _, para_height = para_obj.wrap(width, 1000)
    para_obj.drawOn(canvas, x, top - para_height)
    return para_height


def draw_arrow(canvas, x1: float, y1: float, x2: float, y2: float,
               color: str = "#2563eb", stroke_width: float = 1.15, dashed: bool = False):
    canvas.saveState()
    canvas.setStrokeColor(hx(color))
    canvas.setFillColor(hx(color))
    canvas.setLineWidth(stroke_width)
    if dashed:
        canvas.setDash(4, 3)
    canvas.line(x1, y1, x2, y2)
    canvas.setDash()
    angle = math.atan2(y2 - y1, x2 - x1)
    size = 5
    left = angle + math.pi * 0.82
    right = angle - math.pi * 0.82
    canvas.line(x2, y2, x2 + size * math.cos(left), y2 + size * math.sin(left))
    canvas.line(x2, y2, x2 + size * math.cos(right), y2 + size * math.sin(right))
    canvas.restoreState()


class FigureGraphic(Flowable):
    def __init__(self, kind: str, width: float = FIGURE_WIDTH, height: float = 176):
        super().__init__()
        self.kind = kind
        self.width = width
        self.content_height = height
        self.height = height + RESPONSIBILITY_BAND_HEIGHT
        self.hAlign = "CENTER"

    def wrap(self, availWidth, availHeight):
        self.width = min(FIGURE_WIDTH, availWidth)
        return self.width, self.height

    def draw(self):
        canvas = self.canv
        canvas.saveState()
        canvas.setFillColor(hx("#f8fafc"))
        canvas.roundRect(0, 0, self.width, self.height, 8, stroke=0, fill=1)
        canvas.setStrokeColor(hx("#cbd5e1"))
        canvas.setLineWidth(0.7)
        canvas.roundRect(0, 0, self.width, self.height, 8, stroke=1, fill=0)
        draw_method = getattr(self, f"_draw_{self.kind}", None)
        if draw_method is None:
            raise ValueError(f"Unknown figure kind: {self.kind}")
        canvas.translate(0, RESPONSIBILITY_BAND_HEIGHT)
        draw_method(canvas)
        canvas.translate(0, -RESPONSIBILITY_BAND_HEIGHT)
        self._draw_responsibility_band(canvas)
        canvas.restoreState()

    def _pill(self, canvas, x, y, w, h, title, subtitle="", fill="#ffffff",
              stroke="#94a3b8", title_color="#0f172a", align=TA_CENTER):
        canvas.saveState()
        canvas.setFillColor(hx(fill))
        canvas.setStrokeColor(hx(stroke))
        canvas.setLineWidth(0.8)
        canvas.roundRect(x, y, w, h, 6, stroke=1, fill=1)
        canvas.restoreState()
        top = y + h - 8
        used = draw_wrapped(canvas, title, x + 6, top, w - 12, "Helvetica-Bold", 7.6, title_color, align)
        if subtitle:
            draw_wrapped(canvas, subtitle, x + 6, top - used - 1.5, w - 12, "Helvetica", 6.15, "#475569", align)

    def _section_label(self, canvas, text, x, y, width, color="#2563eb"):
        canvas.saveState()
        canvas.setFillColor(hx(color))
        canvas.roundRect(x, y, width, 15, 3, stroke=0, fill=1)
        canvas.restoreState()
        draw_wrapped(canvas, text, x + 4, y + 12, width - 8, "Helvetica-Bold", 6.2, "#ffffff")

    def _draw_responsibility_band(self, canvas):
        w = self.width
        x = 14
        gap = 6
        card_y = 39
        card_h = 27
        card_w = (w - 28 - 2 * gap) / 3
        roles = [
            ("Business capability: Skill-as-Code", "#f0fdfa", "#2dd4bf", "#115e59"),
            ("Runtime governance: Harness", "#eff6ff", "#60a5fa", "#1d4ed8"),
            ("Execution and control boundary: Scaffold", "#fffbeb", "#f59e0b", "#92400e"),
        ]
        for index, (label, fill, stroke, color) in enumerate(roles):
            role_x = x + index * (card_w + gap)
            self._pill(canvas, role_x, card_y, card_w, card_h, label, "",
                       fill, stroke, color)
            if index:
                draw_arrow(canvas, role_x - gap, card_y + card_h / 2, role_x, card_y + card_h / 2,
                           "#64748b", 0.75)

        substrate_y = 8
        substrate_h = 21
        self._pill(
            canvas,
            x,
            substrate_y,
            w - 28,
            substrate_h,
            "CIO-governed semantic and telemetry foundation: data substrate",
            "",
            "#f5f3ff",
            "#a78bfa",
            "#5b21b6",
        )
        harness_x = x + card_w + gap + card_w / 2
        draw_arrow(
            canvas,
            harness_x,
            substrate_y + substrate_h,
            harness_x,
            card_y,
            "#7c3aed",
            0.8,
            dashed=True,
        )
        draw_wrapped(canvas, "governed-contract access", harness_x + 4, 35, 92,
                     "Helvetica", 4.9, "#5b21b6", TA_LEFT)

    def _draw_dual_scaling(self, canvas):
        w, h = self.width, self.content_height
        draw_wrapped(canvas, "One runtime, two scaling axes", 18, h - 12, w - 36,
                     "Helvetica-Bold", 9.2, "#0f172a")

        self._section_label(canvas, "LOGICAL CAPABILITY", 18, h - 43, 116, "#0f766e")
        skill_y = [94, 62, 30]
        skills = [
            ("S3", "Procurement", "candidate"),
            ("S2", "Code analysis", "released"),
            ("S1", "Data query", "released"),
        ]
        for y, (sid, name, state) in zip(skill_y, skills):
            self._pill(canvas, 18, y, 116, 25, f"{sid}  {name}", state,
                       "#f0fdfa", "#2dd4bf", "#115e59", TA_LEFT)
        draw_arrow(canvas, 8, 28, 8, 119, "#0f766e")
        draw_wrapped(canvas, "add versioned Skills", 14, 27, 96, "Helvetica", 5.8, "#0f766e", TA_LEFT)

        self._pill(canvas, w / 2 - 61, 46, 122, 88, "HARNESS",
                   "select + compile\nvalidate + gate\nbind + trace",
                   "#eff6ff", "#2563eb", "#1d4ed8")
        draw_wrapped(canvas, "typed contract boundary", w / 2 - 70, 39, 140,
                     "Helvetica-Bold", 6.1, "#1d4ed8")

        self._section_label(canvas, "PHYSICAL CAPACITY", w - 134, h - 43, 116, "#b45309")
        scaffold_y = [94, 62, 30]
        scaffolds = [
            ("X3", "Regional pool", "locality"),
            ("X2", "GPU sandbox", "isolated"),
            ("X1", "CPU worker", "isolated"),
        ]
        for y, (xid, name, state) in zip(scaffold_y, scaffolds):
            self._pill(canvas, w - 134, y, 116, 25, f"{xid}  {name}", state,
                       "#fffbeb", "#f59e0b", "#92400e", TA_LEFT)
        draw_arrow(canvas, w - 8, 28, w - 8, 119, "#b45309")
        draw_wrapped(canvas, "add execution envelopes", w - 126, 27, 104,
                     "Helvetica", 5.8, "#92400e", TA_RIGHT)

        for y in [106, 74, 42]:
            draw_arrow(canvas, 134, y, w / 2 - 61, 90, "#0f766e", 0.9)
            draw_arrow(canvas, w / 2 + 61, 90, w - 134, y, "#b45309", 0.9)

    def _draw_harness_contract(self, canvas):
        w, h = self.width, self.content_height
        draw_wrapped(canvas, "From generated intent to governed execution", 18, h - 12, w - 36,
                     "Helvetica-Bold", 9.2, "#0f172a")
        self._pill(canvas, 16, 89, 86, 44, "Request context", "intent + identity\npolicy snapshot",
                   "#f8fafc", "#94a3b8", "#334155")
        self._pill(canvas, 16, 35, 86, 38, "Skill candidates", "versioned contracts",
                   "#f0fdfa", "#2dd4bf", "#115e59")

        cx, cy, cw, ch = 125, 25, 218, 120
        canvas.saveState()
        canvas.setFillColor(hx("#eff6ff"))
        canvas.setStrokeColor(hx("#2563eb"))
        canvas.setLineWidth(1.0)
        canvas.roundRect(cx, cy, cw, ch, 6, stroke=1, fill=1)
        canvas.restoreState()
        draw_wrapped(canvas, "RESOLVED HARNESS CONTRACT", cx + 8, cy + ch - 8, cw - 16,
                     "Helvetica-Bold", 7.2, "#1d4ed8")
        rows = [
            ("I / O", "typed inputs and outputs"),
            ("G", "activated Skill graph"),
            ("B", "time, cost, token, concurrency budgets"),
            ("E", "authorized effects + evidence duties"),
            ("T", "policy, model, data, trace identities"),
        ]
        ry = cy + ch - 34
        for key, value in rows:
            canvas.setStrokeColor(hx("#bfdbfe"))
            canvas.setLineWidth(0.45)
            canvas.line(cx + 10, ry - 5, cx + cw - 10, ry - 5)
            draw_wrapped(canvas, key, cx + 12, ry + 8, 24, "Helvetica-Bold", 6.5, "#1d4ed8", TA_LEFT)
            draw_wrapped(canvas, value, cx + 40, ry + 8, cw - 54,
                         "Helvetica", 6.3, "#334155", TA_LEFT)
            ry -= 18

        self._pill(canvas, w - 96, 91, 80, 42, "Accepted unit", "graph hash\nbinding request",
                   "#ecfdf5", "#10b981", "#047857")
        self._pill(canvas, w - 96, 35, 80, 40, "Rejected unit", "reason + gate\nno side effect",
                   "#fff1f2", "#fb7185", "#9f1239")
        draw_arrow(canvas, 102, 111, 125, 111, "#64748b")
        draw_arrow(canvas, 102, 54, 125, 54, "#0f766e")
        draw_arrow(canvas, 343, 108, w - 96, 108, "#10b981")
        draw_arrow(canvas, 343, 55, w - 96, 55, "#e11d48")
        draw_wrapped(canvas, "deterministic gates", 348, 87, 94,
                     "Helvetica-Bold", 6.0, "#475569")

    def _draw_control_data(self, canvas):
        w, h = self.width, self.content_height
        draw_wrapped(canvas, "Control-plane activation versus request-path leakage", 18, h - 12, w - 36,
                     "Helvetica-Bold", 9.2, "#0f172a")
        gap = 12
        pw = (w - 44 - gap) / 2
        panels = [
            (16, "MANAGED ACTIVATION", "#0f766e", "#f0fdfa"),
            (16 + pw + gap, "EAGER LOADING", "#be123c", "#fff1f2"),
        ]
        for x, title, stroke, fill in panels:
            canvas.setFillColor(hx(fill))
            canvas.setStrokeColor(hx(stroke))
            canvas.setLineWidth(0.7)
            canvas.roundRect(x, 22, pw, 124, 5, stroke=1, fill=1)
            self._section_label(canvas, title, x + 8, 124, pw - 16, stroke)

        lx = 16
        self._pill(canvas, lx + 12, 89, pw - 24, 27, "Control plane",
                   "registry | policy | release state", "#ffffff", "#2dd4bf", "#115e59")
        self._pill(canvas, lx + 12, 49, pw - 24, 27, "Activated contract only",
                   "S2@v4 + opaque policy refs", "#ffffff", "#60a5fa", "#1d4ed8")
        draw_arrow(canvas, lx + pw / 2, 89, lx + pw / 2, 76, "#0f766e")
        draw_wrapped(canvas, "request + evidence", lx + 20, 40, pw - 40,
                     "Helvetica-Bold", 6.2, "#334155")
        draw_wrapped(canvas, "bounded context | explicit authority", lx + 20, 30, pw - 40,
                     "Helvetica", 5.8, "#0f766e")

        rx = 16 + pw + gap
        self._pill(canvas, rx + 12, 89, pw - 24, 27, "All Skills + all policies",
                   "released, draft, deprecated", "#ffffff", "#fb7185", "#9f1239")
        canvas.setFillColor(hx("#fecdd3"))
        for i, label in enumerate(["S1", "S2", "S3", "S4", "..."]):
            bx = rx + 20 + i * 34
            canvas.roundRect(bx, 56, 26, 19, 3, stroke=0, fill=1)
            draw_wrapped(canvas, label, bx, 69, 26, "Helvetica-Bold", 5.8, "#9f1239")
        draw_arrow(canvas, rx + pw / 2, 89, rx + pw / 2, 76, "#be123c")
        draw_wrapped(canvas, "request prompt", rx + 20, 46, pw - 40,
                     "Helvetica-Bold", 6.2, "#334155")
        draw_wrapped(canvas, "linear growth | ambiguous authority", rx + 20, 32, pw - 40,
                     "Helvetica", 5.8, "#be123c")

    def _draw_derivation_closure(self, canvas):
        w, h = self.width, self.content_height
        draw_wrapped(canvas, "Derivation closure: bounded sub-agents, satisfaction-driven loop",
                     18, h - 12, w - 36, "Helvetica-Bold", 9.2, "#0f172a")

        mx, mw = 16, 132
        # Left column and right panel are laid out bottom-up so the figure
        # stays correct if its declared height changes.
        band = 34          # bottom strip reserved for the loop-back path
        col_h = 38
        sat_y = band
        join_y = sat_y + col_h + 4
        main_y = join_y + col_h + 4

        self._pill(canvas, mx, main_y, mw, col_h, "MAIN AGENT",
                   "summarize returns\nno task tools", "#eff6ff", "#2563eb", "#1d4ed8")
        self._pill(canvas, mx, join_y, mw, col_h, "semantic join + top-k",
                   "best-supported evidence\nper output field", "#ffffff", "#60a5fa", "#1d4ed8")
        self._pill(canvas, mx, sat_y, mw, col_h, "satisfaction ratio",
                   "satisfied output domains over\ndeclared sub-domains", "#f5f3ff", "#8b5cf6", "#5b21b6")

        sx = mx + mw + 26
        sw = w - sx - 16
        panel_top = main_y + col_h
        panel_y = band + 14
        canvas.setFillColor(hx("#f0fdfa"))
        canvas.setStrokeColor(hx("#0f766e"))
        canvas.setLineWidth(0.7)
        canvas.roundRect(sx, panel_y, sw, panel_top - panel_y, 5, stroke=1, fill=1)
        self._section_label(canvas, "BOUNDED SUB-AGENTS", sx + 8, panel_top - 20, sw - 16, "#0f766e")

        cell_w = (sw - 32) / 3
        cell_y = panel_top - 78
        subs = [
            ("A1", "tool-set T1", "data-set D1"),
            ("A2", "tool-set T2", "data-set D2"),
            ("A3 (derived)", "tool-set T3", "data-set D3"),
        ]
        for i, (name, tset, dset) in enumerate(subs):
            cx = sx + 12 + i * (cell_w + 4)
            fill = "#ffffff" if i < 2 else "#fffbeb"
            stroke = "#2dd4bf" if i < 2 else "#f59e0b"
            color = "#115e59" if i < 2 else "#92400e"
            self._pill(canvas, cx, cell_y, cell_w, 44, name, f"{tset}\n{dset}",
                       fill, stroke, color)
            draw_wrapped(canvas, "output range bounded", cx, cell_y - 3, cell_w,
                         "Helvetica", 5.5, "#0f766e")

        note_top = cell_y - 15
        draw_wrapped(canvas, "unmet reference to a tool or source outside the fixed sets becomes a derivation condition, not an inline grant",
                     sx + 12, note_top, sw - 44, "Helvetica-Bold", 6.0, "#b45309")
        arrow_x = sx + sw - 16
        canvas.saveState()
        canvas.setStrokeColor(hx("#b45309"))
        canvas.setLineWidth(1.0)
        canvas.line(sx + sw - 32, note_top - 8, arrow_x, note_top - 8)
        canvas.restoreState()
        draw_arrow(canvas, arrow_x, note_top - 8, arrow_x, cell_y + 2, "#b45309", 1.0)

        draw_arrow(canvas, mx + mw, main_y + 14, sx, panel_top - 34, "#2563eb", 1.0)
        draw_wrapped(canvas, "invoke / derive", mx + mw - 4, main_y + col_h - 4, 74,
                     "Helvetica", 5.8, "#1d4ed8", TA_LEFT)
        draw_arrow(canvas, sx, cell_y + 12, mx + mw, join_y + 20, "#0f766e", 1.0)
        draw_wrapped(canvas, "summaries only", mx + mw - 4, join_y + col_h - 6, 74,
                     "Helvetica", 5.8, "#0f766e", TA_LEFT)

        by = 12
        loop_x = w - 150
        canvas.setStrokeColor(hx("#8b5cf6"))
        canvas.setLineWidth(0.8)
        canvas.setDash(4, 3)
        canvas.line(mx + mw / 2, sat_y, mx + mw / 2, by)
        canvas.line(mx + mw / 2, by, loop_x, by)
        canvas.setDash()
        draw_arrow(canvas, loop_x, by, loop_x, panel_y, "#8b5cf6", 1.0)
        draw_wrapped(canvas, "loop while ratio below target and an unsatisfied sub-domain still admits derivation",
                     mx + mw + 12, band - 2, loop_x - mx - mw - 22, "Helvetica-Bold", 6.0,
                     "#5b21b6", TA_LEFT)

        self._pill(canvas, w - 100, by - 6, 84, 32, "terminate",
                   "target met, budget out,\nor typed failure",
                   "#ffffff", "#94a3b8", "#334155")

    def _draw_external_data(self, canvas):
        w, h = self.width, self.content_height
        draw_wrapped(canvas, "External data is a governed contract path", 18, h - 12, w - 36,
                     "Helvetica-Bold", 9.2, "#0f172a")
        canvas.saveState()
        canvas.setFillColor(hx("#f5f3ff"))
        canvas.setStrokeColor(hx("#a78bfa"))
        canvas.setLineWidth(0.9)
        canvas.roundRect(16, 54, 132, 83, 6, stroke=1, fill=1)
        canvas.restoreState()
        self._section_label(canvas, "CIO DATA FOUNDATION", 24, 116, 116, "#7c3aed")
        self._pill(canvas, 26, 84, 50, 24, "Sources", "warehouse", "#ffffff", "#c4b5fd", "#5b21b6")
        self._pill(canvas, 86, 84, 50, 24, "Sources", "documents | APIs", "#ffffff", "#c4b5fd", "#5b21b6")
        draw_wrapped(canvas, "semantic catalog | residency policy | telemetry",
                     26, 78, 110, "Helvetica-Bold", 5.7, "#5b21b6")
        draw_wrapped(canvas, "independent data governance; no task semantics",
                     24, 62, 116, "Helvetica", 5.4, "#5b21b6")

        self._pill(canvas, 174, 64, 122, 70, "Harness contract",
                   "authorized source\nschema + snapshot\nprincipal + budget\nprovenance duty",
                   "#eff6ff", "#2563eb", "#1d4ed8")
        self._pill(canvas, 322, 76, 62, 46, "Scaffold", "bound credential\nisolated fetch",
                   "#fffbeb", "#f59e0b", "#92400e")
        self._pill(canvas, 400, 76, 46, 46, "Evidence", "typed bundle\nlineage ID",
                   "#ecfdf5", "#10b981", "#047857")
        draw_arrow(canvas, 148, 96, 174, 96, "#7c3aed", 1.0, dashed=True)
        draw_arrow(canvas, 296, 99, 322, 99, "#2563eb")
        draw_arrow(canvas, 384, 99, 400, 99, "#b45309")
        draw_wrapped(canvas, "governed contract", 149, 84, 54, "Helvetica-Bold", 5.4,
                     "#5b21b6", TA_LEFT)

        canvas.setStrokeColor(hx("#cbd5e1"))
        canvas.setDash(3, 2)
        canvas.line(16, 42, w - 16, 42)
        canvas.setDash()
        draw_wrapped(canvas, "Recorded obligations", 18, 35, 92,
                     "Helvetica-Bold", 6.2, "#475569", TA_LEFT)
        obligations = [
            ("principal", "#dbeafe", 56),
            ("source + snapshot", "#dcfce7", 70),
            ("query hash", "#fef3c7", 56),
            ("residency", "#ede9fe", 58),
            ("evidence lineage", "#ffe4e6", 70),
        ]
        ox = 114
        for label, fill, bw in obligations:
            canvas.setFillColor(hx(fill))
            canvas.roundRect(ox, 15, bw, 17, 3, stroke=0, fill=1)
            draw_wrapped(canvas, label, ox + 3, 27, bw - 6, "Helvetica-Bold", 5.2, "#334155")
            ox += bw + 5

    def _draw_dry_run(self, canvas):
        w, h = self.width, self.content_height
        draw_wrapped(canvas, "Dry-run exposes parallelism, locality, and effects before commit", 18, h - 12, w - 36,
                     "Helvetica-Bold", 9.2, "#0f172a")
        self._section_label(canvas, "1  PLAN + VALIDATE", 16, 128, 122, "#2563eb")
        self._section_label(canvas, "2  BIND BY LOCALITY", 170, 128, 126, "#0f766e")
        self._section_label(canvas, "3  EXECUTE + TRACE", 328, 128, 118, "#b45309")

        self._pill(canvas, 18, 82, 48, 30, "A", "discover", "#eff6ff", "#60a5fa")
        self._pill(canvas, 82, 96, 48, 30, "B", "query east", "#eff6ff", "#60a5fa")
        self._pill(canvas, 82, 60, 48, 30, "C", "query west", "#eff6ff", "#60a5fa")
        draw_arrow(canvas, 66, 97, 82, 111, "#2563eb")
        draw_arrow(canvas, 66, 97, 82, 75, "#2563eb")
        draw_wrapped(canvas, "B || C", 91, 53, 32, "Helvetica-Bold", 5.8, "#1d4ed8")

        self._pill(canvas, 172, 91, 55, 31, "Zone E", "data local", "#f0fdfa", "#2dd4bf")
        self._pill(canvas, 239, 91, 55, 31, "Zone W", "data local", "#f0fdfa", "#2dd4bf")
        self._pill(canvas, 204, 49, 58, 30, "Effect zone", "isolated", "#fff7ed", "#fb923c")
        draw_arrow(canvas, 130, 111, 172, 107, "#0f766e")
        draw_arrow(canvas, 130, 75, 239, 107, "#0f766e")

        self._pill(canvas, 330, 91, 52, 31, "Run B", "trace b", "#fffbeb", "#f59e0b")
        self._pill(canvas, 394, 91, 52, 31, "Run C", "trace c", "#fffbeb", "#f59e0b")
        self._pill(canvas, 361, 48, 52, 30, "Commit", "approval", "#ecfdf5", "#10b981")
        draw_arrow(canvas, 294, 107, 330, 107, "#b45309")
        draw_arrow(canvas, 294, 107, 394, 107, "#b45309")
        draw_arrow(canvas, 356, 91, 377, 78, "#b45309")
        draw_arrow(canvas, 420, 91, 397, 78, "#b45309")

        canvas.setStrokeColor(hx("#cbd5e1"))
        canvas.setDash(3, 2)
        canvas.line(16, 37, w - 16, 37)
        canvas.setDash()
        draw_wrapped(canvas, "dry-run report: graph hash | predicted budget | cross-zone bytes | missing capacity | irreversible effects",
                     20, 29, w - 40, "Helvetica-Bold", 6.0, "#475569")

    def _draw_skill_lifecycle(self, canvas):
        w, h = self.width, self.content_height
        draw_wrapped(canvas, "Skill-as-Code: capability growth as a release lifecycle", 18, h - 12, w - 36,
                     "Helvetica-Bold", 9.2, "#0f172a")
        stages = [
            ("Draft", "contract + criteria", "#f8fafc", "#94a3b8"),
            ("Train", "bounded edits", "#eff6ff", "#60a5fa"),
            ("Validate", "tests + closure", "#f0fdfa", "#2dd4bf"),
            ("Staged release", "signed + gradual", "#fffbeb", "#f59e0b"),
            ("Monitor", "drift + evidence", "#ecfdf5", "#10b981"),
        ]
        stage_gap = 9
        stage_w = (w - 28 - stage_gap * 4) / 5
        stage_y, stage_h = 96, 39
        stage_centers = []
        x = 14
        for idx, (title, subtitle, fill, stroke) in enumerate(stages):
            self._pill(canvas, x, stage_y, stage_w, stage_h, title, subtitle, fill, stroke, "#0f172a")
            stage_centers.append(x + stage_w / 2)
            if idx < len(stages) - 1:
                draw_arrow(canvas, x + stage_w, stage_y + stage_h / 2,
                           x + stage_w + stage_gap, stage_y + stage_h / 2, "#64748b", 0.8)
            x += stage_w + stage_gap

        controls = [
            ("Freeze / thaw", "code <-> training", "#f5f3ff", "#a78bfa"),
            ("Drift / revalidate", "signal -> gate", "#eff6ff", "#60a5fa"),
            ("Rollback", "restore release", "#fff1f2", "#fb7185"),
            ("Retire", "close activation", "#f8fafc", "#94a3b8"),
        ]
        control_gap = 11
        control_w = (w - 42 - control_gap * 3) / 4
        control_y, control_h = 24, 33
        control_centers = []
        x = 21
        for title, subtitle, fill, stroke in controls:
            self._pill(canvas, x, control_y, control_w, control_h,
                       title, subtitle, fill, stroke, "#0f172a")
            control_centers.append(x + control_w / 2)
            x += control_w + control_gap

        draw_arrow(canvas, control_centers[0], control_y + control_h,
                   stage_centers[1], stage_y, "#7c3aed", 0.85, dashed=True)
        draw_arrow(canvas, control_centers[1], control_y + control_h,
                   stage_centers[2], stage_y, "#2563eb", 0.85, dashed=True)
        draw_arrow(canvas, control_centers[2], control_y + control_h,
                   stage_centers[3], stage_y, "#be123c", 0.85, dashed=True)
        draw_arrow(canvas, stage_centers[4], stage_y,
                   control_centers[3], control_y + control_h, "#64748b", 0.85, dashed=True)
        draw_wrapped(canvas, "release controls and feedback", 16, 16, w - 32,
                     "Helvetica-Bold", 5.8, "#64748b")

    def _draw_evaluation_matrix(self, canvas):
        w, h = self.width, self.content_height
        draw_wrapped(canvas, "Falsification matrix", 18, h - 10, w - 36,
                     "Helvetica-Bold", 9.2, "#0f172a")
        relationships = [
            "Skill -> Harness: versioned capability contract",
            "Harness -> Scaffold: admission + compatible capacity binding",
            "Harness <-> data substrate: semantic join + governed evidence",
            "Scaffold -> Harness: enforceable execution facts",
        ]
        for index, relationship in enumerate(relationships):
            draw_wrapped(
                canvas,
                relationship,
                22,
                h - 28 - index * 12,
                w - 44,
                "Helvetica-Bold",
                6.3,
                "#334155",
                TA_LEFT,
                7.2,
            )
        panel_y = 129
        panel_h = 96
        panel_gap = 14
        panel_w = (w - 32 - panel_gap) / 2
        panels = [
            (
                16,
                "BUSINESS / USE-CASE PLANE",
                "Business/use-case evaluation",
                "Does the versioned Skill improve the declared workflow for its users?",
                "task outcome | quality | cycle time | correction | adoption",
                "#f0fdfa",
                "#0f766e",
                "#115e59",
            ),
            (
                16 + panel_w + panel_gap,
                "SYSTEM / RUNTIME PLANE",
                "System/runtime evaluation",
                "Does the admitted path meet its contract and enterprise NFR envelope?",
                "gate + trace integrity | isolation | capacity | latency | cost",
                "#eff6ff",
                "#2563eb",
                "#1d4ed8",
            ),
        ]
        for x, section, title, question, measures, fill, stroke, color in panels:
            canvas.saveState()
            canvas.setFillColor(hx(fill))
            canvas.setStrokeColor(hx(stroke))
            canvas.setLineWidth(0.85)
            canvas.roundRect(x, panel_y, panel_w, panel_h, 6, stroke=1, fill=1)
            canvas.restoreState()
            self._section_label(canvas, section, x + 8, panel_y + panel_h - 21, panel_w - 16, stroke)
            draw_wrapped(canvas, title, x + 10, panel_y + panel_h - 34, panel_w - 20,
                         "Helvetica-Bold", 7.1, color, TA_LEFT)
            draw_wrapped(canvas, question, x + 10, panel_y + 47, panel_w - 20,
                         "Helvetica", 6.0, "#334155", TA_LEFT, 7.1)
            draw_wrapped(canvas, measures, x + 10, panel_y + 22, panel_w - 20,
                         "Helvetica-Bold", 5.65, color, TA_LEFT, 6.7)

        draw_wrapped(canvas, "Each release names evidence from both planes; success in one does not substitute for the other.",
                     22, 117, w - 44, "Helvetica-Bold", 6.15, "#475569")
        draw_wrapped(canvas, "Protocol controls: preregistered intervention, fixed decision rule, and an explicit condition that counts against the claim.",
                     22, 105, w - 44, "Helvetica", 5.75, "#475569")

        protocol_y = 16
        protocol_h = 76
        protocol_gap = 8
        protocol_w = (w - 32 - 2 * protocol_gap) / 3
        protocols = [
            (
                "P15",
                "vector gate",
                "fixed proposal bank\nseparate (c)-(a) and (c)-(b) margins\nmulti-seed online\nfirst-attempt grading\nindependent grader\nphantom-violation oracle",
                "#f5f3ff",
                "#7c3aed",
                "#5b21b6",
            ),
            (
                "P16",
                "summary reconstruction",
                "strict held-out\ntoken-matched direct reading\nmetadata-only\nfield ablation\nshuffled summaries\njoint contrast",
                "#ecfeff",
                "#0891b2",
                "#155e75",
            ),
            (
                "P17",
                "registry change control",
                "preregistered dependency graph\nartifact-change oracle\nexpected versus unanticipated propagation",
                "#fff7ed",
                "#ea580c",
                "#9a3412",
            ),
        ]
        for index, (pid, title, detail, fill, stroke, color) in enumerate(protocols):
            x = 16 + index * (protocol_w + protocol_gap)
            canvas.saveState()
            canvas.setFillColor(hx(fill))
            canvas.setStrokeColor(hx(stroke))
            canvas.setLineWidth(0.8)
            canvas.roundRect(x, protocol_y, protocol_w, protocol_h, 6, stroke=1, fill=1)
            canvas.restoreState()
            used = draw_wrapped(
                canvas,
                f"{pid}  {title}",
                x + 6,
                protocol_y + protocol_h - 7,
                protocol_w - 12,
                "Helvetica-Bold",
                7.2,
                color,
                TA_LEFT,
            )
            draw_wrapped(
                canvas,
                detail,
                x + 6,
                protocol_y + protocol_h - 8.5 - used,
                protocol_w - 12,
                "Helvetica",
                5.4,
                "#475569",
                TA_LEFT,
                6.3,
            )
            if index < len(protocols) - 1:
                draw_arrow(canvas, x + protocol_w, protocol_y + protocol_h / 2,
                           x + protocol_w + protocol_gap, protocol_y + protocol_h / 2,
                           "#64748b", 0.75)


def strip_comments(text: str) -> str:
    out = []
    for line in text.splitlines():
        cut = None
        for i, ch in enumerate(line):
            if ch == "%" and (i == 0 or line[i - 1] != "\\"):
                cut = i
                break
        out.append(line if cut is None else line[:cut])
    return "\n".join(out)


def read_source(paper_dir: str) -> tuple[str, str]:
    with open(os.path.join(paper_dir, "main.tex"), "r", encoding="utf-8") as f:
        tex = f.read()
    bib_path = os.path.join(paper_dir, "references.bib")
    bib = ""
    if os.path.exists(bib_path):
        with open(bib_path, "r", encoding="utf-8") as f:
            bib = f.read()
    return strip_comments(tex), strip_comments(bib)


def balanced_entries(bib: str) -> dict:
    entries = {}
    i = 0
    while True:
        m = re.search(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", bib[i:], re.S)
        if not m:
            break
        start = i + m.start()
        key = m.group(2).strip()
        body_start = i + m.end()
        depth = 1
        j = body_start
        while j < len(bib) and depth > 0:
            if bib[j] == "{":
                depth += 1
            elif bib[j] == "}":
                depth -= 1
            j += 1
        body = bib[body_start : j - 1]
        entries[key] = parse_bib_fields(body)
        i = j
    return entries


def parse_bib_fields(body: str) -> dict:
    fields = {}
    cur = []
    depth = 0
    in_quote = False
    chunks = []
    for ch in body:
        if ch == '"' and (not cur or cur[-1] != "\\"):
            in_quote = not in_quote
        if ch == "{" and not in_quote:
            depth += 1
        elif ch == "}" and not in_quote and depth > 0:
            depth -= 1
        if ch == "," and depth == 0 and not in_quote:
            chunks.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if cur:
        chunks.append("".join(cur))

    for chunk in chunks:
        if "=" not in chunk:
            continue
        k, v = chunk.split("=", 1)
        k = k.strip().lower()
        v = v.strip().strip(",").strip()
        if len(v) >= 2 and ((v[0] == "{" and v[-1] == "}") or (v[0] == '"' and v[-1] == '"')):
            v = v[1:-1]
        fields[k] = clean_latex(v)
    return fields


def citation_order(tex: str) -> list[str]:
    keys = []
    seen = set()
    for m in re.finditer(r"\\cite[a-zA-Z*]*\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}", tex):
        for key in m.group(1).split(","):
            key = key.strip()
            if key and key not in seen:
                seen.add(key)
                keys.append(key)
    return keys


def table_label_map(tex: str) -> dict[str, int]:
    labels = {}
    table_pattern = re.compile(
        r"\\begin\{table\*?\}(?:\[[^\]]+\])?.*?\\end\{table\*?\}",
        re.S,
    )
    for number, match in enumerate(table_pattern.finditer(tex), start=1):
        label_match = re.search(r"\\label\{([^}]+)\}", match.group(0))
        if label_match:
            labels[label_match.group(1)] = number
    return labels


def clean_math(text: str) -> str:
    text = re.sub(r"\\xrightarrow\{\\mathcal\{([^}]+)\}\}", r"-[\1]->", text)
    text = re.sub(r"\\bigwedge_([A-Za-z0-9]+)", r"conjunction over \1", text)
    text = re.sub(r"\\sigma(?:\^\{out\}|_\{?out\}?)", "output schema", text)
    # Two adjacent LaTeX commands (e.g. \lambda\rho) must not fuse into one
    # word once each resolves to a bare identifier; separate them first.
    text = re.sub(r"(\\[A-Za-z]+)(?=\\[A-Za-z])", r"\1 ", text)
    repl = {
        r"\Delta": "Delta",
        r"\delta": "delta",
        r"\epsilon": "epsilon",
        r"\theta": "theta",
        r"\Theta": "Theta",
        r"\phi": "phi",
        r"\pi": "pi",
        r"\sigma": "output schema",
        r"\rho": "rho",
        r"\tau": "tau",
        r"\lambda": "overlap coefficient",
        r"\mu": "mu",
        r"\geq": " at least ",
        r"\leq": " at most ",
        r"\approx": "~",
        r"\equiv": "==",
        r"\times": "x",
        r"\checkmark": "yes",
        r"\sim": "~",
        r"\rightarrow": "->",
        r"\to": "->",
        r"\subseteq": "subset of",
        r"\langle": "<",
        r"\rangle": ">",
        r"\cdot": "*",
        r"\mid": "|",
        r"\emptyset": "empty",
        r"\cup": "union",
        r"\cap": "intersection",
        r"\sum": "sum",
        r"\forall": "for all",
        r"\exists": "exists",
        r"\gg": ">>",
        r"\ll": "<<",
        r"\uparrow": "increases",
        r"\downarrow": "decreases",
        r"\infty": "infinity",
        r"\in": " in ",
        r"\left": "",
        r"\right": "",
        r"\textwidth": "text width",
        r"\;": " ",
        r"\,": " ",
        r"\quad": " ",
    }
    for k, v in repl.items():
        text = text.replace(k, v)
    text = re.sub(r"\\mathbb\{1\}", "indicator", text)
    text = re.sub(r"\\mathcal\{([^}]+)\}", r"\1", text)
    text = re.sub(r"\\hat\{([^}]+)\}", r"\1_hat", text)
    text = re.sub(r"\\bar\{([^}]+)\}", r"\1_bar", text)
    text = re.sub(r"\\text\{([^}]+)\}", r"\1", text)
    text = re.sub(r"\\mathrm\{([^}]+)\}", r"\1", text)
    text = re.sub(r"\\mathbf\{([^}]+)\}", r"\1", text)
    text = re.sub(r"\\operatorname\{([^}]+)\}", r"\1", text)
    text = re.sub(r"\\(?:bigl|bigr|Bigl|Bigr|big|Big|bigg|Bigg)(?=[({\[\]}|)]|\Z)", "", text)
    # \frac must resolve after \mathrm/\text so its arguments are brace-free.
    for _ in range(3):
        new = re.sub(r"\\frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"(\1)/(\2)", text)
        if new == text:
            break
        text = new
    text = re.sub(r"\bsum_\{([^{}]+)\}", r"sum over \1 of", text)
    text = re.sub(r"\bsum_([A-Za-z0-9]+)", r"sum over \1 of", text)
    text = text.replace("{", "").replace("}", "")
    text = re.sub(
        r"\b([A-Za-z][A-Za-z0-9_]*(?:_hat)?)\s+subset of\s+([A-Za-z][A-Za-z0-9_]*)",
        r"\1 is a subset of \2",
        text,
    )
    return text


def clean_latex(
    text: str,
    cite_map: dict | None = None,
    table_map: dict[str, int] | None = None,
) -> str:
    cite_map = cite_map or {}
    table_map = table_map or {}
    text = text.replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\\xrightarrow\{\\mathcal\{([^}]+)\}\}", r"-[\1]->", text)
    text = re.sub(r"\\bigwedge_([A-Za-z0-9]+)", r"conjunction over \1", text)
    text = re.sub(r"\\sigma(?:\^\{out\}|_\{?out\}?)", "output schema", text)
    text = text.replace(r"\lambda", "overlap coefficient")
    text = text.replace(r"\geq", " at least ").replace(r"\leq", " at most ")
    text = text.replace("Guti茅rrez", "Gutierrez").replace("guti茅rrez", "gutierrez")
    text = re.sub(r'\{\\"([A-Za-z])\}', r"\1", text)
    text = re.sub(r'\\"([A-Za-z])', r"\1", text)
    text = re.sub(r"\{\\['`^~=.]([A-Za-z])\}", r"\1", text)
    text = re.sub(r"\\['`^~=.]([A-Za-z])", r"\1", text)
    text = re.sub(r"``|''", '"', text)
    text = text.replace("---", " - ").replace("--", "-")
    text = text.replace("~", " ")
    text = text.replace(r"\[", " ").replace(r"\]", " ")
    text = re.sub(r"Figure\s+\\ref\{fig:architecture\}\s*\(not shown\)", "The architecture flow diagram", text)
    text = re.sub(r"\\textsc\{5w1h\}", "5W1H", text, flags=re.I)
    text = text.replace(r"\ldots", "...").replace(r"\dots", "...")
    text = text.replace(r"\checkmark", "yes")
    text = re.sub(r"\\(?:toprule|midrule|bottomrule|hline|cmidrule)(?:\([^)]*\))?(?:\{[^}]*\})?", " ", text)
    text = re.sub(r"\\begin\{(?:itemize|enumerate)\*?\}(?:\[[^\]]+\])?", " ", text)
    text = re.sub(r"\\end\{(?:itemize|enumerate)\*?\}", " ", text)
    text = re.sub(r"\\begin\{(?:table|figure|tabular|center|small|proposition)\*?\}(?:\[[^\]]+\])?", " ", text)
    text = re.sub(r"\\end\{(?:table|figure|tabular|center|small|proposition)\*?\}", " ", text)
    text = re.sub(r"\\fbox\s*\{", "", text)
    text = re.sub(r"\\parbox(?:\[[^\]]*\])?\{[^{}]*\}\s*\{", "", text)
    text = re.sub(r"\b(?:leftmargin|noitemsep)\s*=\s*[^,\]\s]+,?", "", text)
    text = re.sub(r"\blabel\s*=\s*\\textbf\{\\arabic\*\.\},?", "", text)
    text = text.replace(r"\arabic*", "")
    text = text.replace(r"\%", "%").replace(r"\&", "&").replace(r"\_", "_")
    text = text.replace(r"\#", "#").replace(r"\$", "$")
    text = re.sub(r"\\S(?![a-zA-Z])", "Section ", text)

    def cite_repl(match):
        keys = [k.strip() for k in match.group(1).split(",") if k.strip()]
        nums = [str(cite_map.get(k, k)) for k in keys]
        return "[" + ", ".join(nums) + "]"

    text = re.sub(r"\\cite[a-zA-Z*]*\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}", cite_repl, text)
    def table_ref_repl(match):
        label = match.group(1)
        number = table_map.get(label)
        return f"Table {number}" if number is not None else "the table"

    text = re.sub(r"\bTable\s+\\ref\{([^}]+)\}", table_ref_repl, text)
    text = re.sub(r"\bFigure\s+\\ref\{[^}]+\}", "the figure", text)
    text = re.sub(r"\bSection\s+\\ref\{[^}]+\}", "the section", text)
    text = re.sub(r"\bProposition\s+\\ref\{prop:p([0-9]+)\}", lambda m: f"Proposition P{m.group(1)}", text)
    text = re.sub(r"\\ref\{prop:p([0-9]+)\}", lambda m: f"P{m.group(1)}", text)
    text = re.sub(r"\\ref\{[^}]+\}", "", text)
    text = re.sub(r"(^|[.!?]\s+)the table\b", lambda m: m.group(1) + "The table", text)
    text = re.sub(r"\\label\{[^}]+\}", "", text)
    text = re.sub(r"\\url\{([^}]+)\}", r"\1", text)
    text = re.sub(r"\\href\{([^}]+)\}\{([^}]+)\}", r"\2 (\1)", text)

    for _ in range(3):
        before = text
        for cmd in ["textbf", "textit", "emph", "texttt", "textsc", "textsuperscript"]:
            text = re.sub(rf"\\{cmd}\{{([^{{}}]*)\}}", r"\1", text)
        if text == before:
            break
    text = re.sub(r"\$([^$]+)\$", lambda m: clean_math(m.group(1)), text)
    text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\(?:quad|qquad|bigl|bigr|Bigl|Bigr|left|right|centering|small)\b", " ", text)
    text = re.sub(r"\\(?:big|Big|bigg|Bigg)(?=[({\[\]}|)])", "", text)
    text = text.replace(r"\;", " ").replace(r"\,", " ")
    text = re.sub(r"\\([A-Za-z][A-Za-z0-9_-]*)", r"\1", text)
    text = re.sub(r"\\.", " ", text)
    text = text.replace("{", "").replace("}", "")
    text = re.sub(r"\b(?:textbf|textit|emph|texttt|textsc|textsuperscript)([A-Za-z0-9_./:+-]+)", r"\1", text)
    text = text.replace("langle", "<").replace("rangle", ">")
    text = re.sub(
        r"\b([A-Za-z][A-Za-z0-9_]*(?:_hat)?)\s+subset of\s+([A-Za-z][A-Za-z0-9_]*)",
        r"\1 is a subset of \2",
        text,
    )
    text = re.sub(r"\s+", " ", text).strip()
    return text


def para(
    text: str,
    style: ParagraphStyle,
    cite_map: dict | None = None,
    table_map: dict[str, int] | None = None,
) -> Paragraph:
    return Paragraph(escape(clean_latex(text, cite_map, table_map)), style)


def split_document_body(tex: str) -> str:
    tex = re.sub(r"\\documentclass(?:\[[^\]]*\])?\{[^}]+\}", "", tex)
    tex = re.sub(r"\\usepackage(?:\[[^\]]*\])?\{[^}]+\}", "", tex)
    tex = tex.replace(r"\begin{document}", "")
    tex = tex.replace(r"\end{document}", "")
    tex = re.sub(r"\\bibliographystyle\{[^}]+\}", "", tex)
    tex = re.sub(r"\\bibliography\{[^}]+\}", "", tex)
    return tex.strip()


def read_braced(line: str, command: str) -> tuple[str, str] | None:
    prefix = "\\" + command
    if not line.startswith(prefix):
        return None
    start = line.find("{")
    if start < 0:
        return None
    depth = 0
    for i in range(start, len(line)):
        if line[i] == "{":
            depth += 1
        elif line[i] == "}":
            depth -= 1
            if depth == 0:
                return line[start + 1 : i], line[i + 1 :].strip()
    return None


def collect_environment(lines: list[str], i: int, env_name: str) -> tuple[str, int]:
    chunks = [lines[i]]
    env_base = re.escape(env_name.rstrip("*"))
    end_re = re.compile(rf"\\end\{{{env_base}\*?\}}")
    i += 1
    while i < len(lines):
        chunks.append(lines[i])
        if end_re.search(lines[i]):
            return "\n".join(chunks), i + 1
        i += 1
    return "\n".join(chunks), i


def extract_tabular_body(block: str) -> str | None:
    match = re.search(r"\\begin\{tabular\}(?:\[[^\]]+\])?", block)
    if not match:
        return None
    i = match.end()
    while i < len(block) and block[i].isspace():
        i += 1
    if i >= len(block) or block[i] != "{":
        return None

    depth = 0
    spec_end = None
    for j in range(i, len(block)):
        if block[j] == "{":
            depth += 1
        elif block[j] == "}":
            depth -= 1
            if depth == 0:
                spec_end = j + 1
                break
    if spec_end is None:
        return None

    end_match = re.search(r"\\end\{tabular\}", block[spec_end:], re.S)
    if not end_match:
        return None
    return block[spec_end : spec_end + end_match.start()]


def extract_command_arg(block: str, command: str) -> str | None:
    match = re.search(rf"\\{re.escape(command)}\s*\{{", block)
    if not match:
        return None
    start = block.find("{", match.start())
    depth = 0
    for i in range(start, len(block)):
        ch = block[i]
        escaped = i > 0 and block[i - 1] == "\\"
        if ch == "{" and not escaped:
            depth += 1
        elif ch == "}" and not escaped:
            depth -= 1
            if depth == 0:
                return block[start + 1 : i]
    return None


def clean_table_cell(cell: str, cite_map: dict, table_map: dict[str, int]) -> str:
    raw = cell.strip()
    if re.fullmatch(r"\$?\s*\\checkmark\s*\$?", raw):
        return "yes"
    if re.fullmatch(r"\$?\s*\\times\s*\$?", raw):
        return "no"
    return clean_latex(cell, cite_map, table_map)


def table_from_latex(
    block: str,
    styles,
    cite_map: dict,
    table_map: dict[str, int] | None = None,
    table_number: int = 1,
) -> list:
    table_map = table_map or {}
    caption = ""
    caption_arg = extract_command_arg(block, "caption")
    if caption_arg:
        caption = clean_latex(caption_arg, cite_map, table_map)

    elements = []
    if caption:
        elements.append(
            Paragraph(f"<b>Table {table_number}.</b> " + escape(caption), styles["Caption"])
        )
        elements.append(Spacer(1, 4))
    raw = extract_tabular_body(block)
    if raw is None:
        return elements

    raw = re.sub(r"\\(?:hline|toprule|midrule|bottomrule|cmidrule)(?:\([^)]*\))?(?:\{[^}]*\})?", "", raw)
    raw = raw.replace("\n", " ")
    rows = []
    for part in re.split(r"\\\\", raw):
        part = part.strip()
        if not part or "&" not in part:
            continue
        cells = [clean_table_cell(c, cite_map, table_map) for c in part.split("&")]
        rows.append(cells)
    if not rows:
        return elements

    max_cols = max(len(r) for r in rows)
    for r in rows:
        while len(r) < max_cols:
            r.append("")

    font_size = 6.8 if max_cols >= 5 else 7.5
    cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Body"],
        fontName="Times-Roman",
        fontSize=font_size,
        leading=font_size + 1.5,
        alignment=TA_LEFT,
    )
    header_style = ParagraphStyle(
        "TableHeader",
        parent=cell_style,
        fontName="Times-Bold",
        textColor=colors.HexColor("#111827"),
    )
    data = []
    for ridx, row in enumerate(rows):
        data.append([Paragraph(escape(c), header_style if ridx == 0 else cell_style) for c in row])

    if max_cols == 4:
        col_widths = [90, 124, 136, 90]
    else:
        weights = []
        for c in range(max_cols):
            lens = [len(rows[r][c]) for r in range(len(rows))]
            weights.append(min(max(max(lens), 24), 42))
        total = sum(weights) or max_cols
        col_widths = [440 * w / total for w in weights]

    tbl = Table(data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eef2f7")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#111827")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    elements.append(tbl)
    elements.append(Spacer(1, 8))
    return [KeepTogether(elements)]


def figure_caption_from_latex(
    block: str,
    cite_map: dict,
    table_map: dict[str, int],
) -> str:
    caption_arg = extract_command_arg(block, "caption")
    return (
        clean_latex(caption_arg, cite_map, table_map)
        if caption_arg
        else "Source figure from the LaTeX manuscript."
    )


def proposition_from_latex(
    block: str,
    styles,
    cite_map: dict,
    table_map: dict[str, int],
) -> list:
    title_match = re.search(r"\\begin\{proposition\}(?:\[([^\]]+)\])?", block)
    title = (
        clean_latex(title_match.group(1), cite_map, table_map)
        if title_match and title_match.group(1)
        else "Proposition"
    )
    body = re.sub(r"\\begin\{proposition\}(?:\[[^\]]+\])?", "", block)
    body = re.sub(r"\\end\{proposition\}", "", body)
    body = clean_latex(body, cite_map, table_map)
    text = f"<b>{escape(title)}.</b> {escape(body)}"
    return [Paragraph(text, styles["Proposition"]), Spacer(1, 7)]


def code_block(
    block: str,
    styles,
    cite_map: dict,
    table_map: dict[str, int],
) -> list:
    if r"\mathcal{P}_{\text{raw}}" in block and r"\mathcal{P}_{\text{full}}" in block:
        lines = [
            "Retrieval policies:",
            "P_raw(q, C): scan Raw directly with keyword or embedding matching.",
            "P_idx(q, C): navigate the Index first, then fetch supporting Raw evidence.",
            "P_full(q, C): consult Theme, traverse Index, then fetch Raw evidence.",
        ]
        text = "<br/>".join(escape(line) for line in lines)
        return [Paragraph(text, styles["Formula"]), Spacer(1, 6)]
    block = re.sub(r"\\begin\{[^}]+\}", "", block)
    block = re.sub(r"\\end\{[^}]+\}", "", block)
    block = block.replace("&", " ").replace(r"\\", "\n")
    block = re.sub(r"\\label\{[^}]+\}", "", block)
    # Display equations carry no $ delimiters, so clean_latex never routes them
    # through clean_math; normalize the math-only constructs here first.
    block = re.sub(r"\\mathrm\{([^{}]+)\}", r"\1", block)
    block = re.sub(r"\\text\{([^{}]+)\}", r"\1", block)
    block = re.sub(r"\\mathbb\{1\}", "indicator", block)
    brace = r"((?:[^{}]|\{[^{}]*\})*)"
    for _ in range(3):
        new = re.sub(rf"\\frac\s*\{{{brace}\}}\s*\{{{brace}\}}", r"(\1)/(\2)", block)
        if new == block:
            break
        block = new
    block = re.sub(r"\\sum_\{((?:[^{}]|\{[^{}]*\})+)\}", r"\\sum over \1 of", block)
    block = re.sub(r"\\sum_([A-Za-z0-9]+)", r"\\sum over \1 of", block)
    block = block.replace(r"\mapsto", "->")
    block = block.replace(r"\in", " in ")
    block = block.replace(r"\cdot", "*")
    text = clean_latex(block, cite_map, table_map)
    text = re.sub(r"[ \t]+", " ", text).strip()
    return [Paragraph(escape(text).replace("\n", "<br/>"), styles["Formula"]), Spacer(1, 6)]


def parse_items(
    block: str,
    styles,
    cite_map: dict,
    table_map: dict[str, int],
    ordered: bool = False,
) -> list:
    block = re.sub(r"\\begin\{(?:itemize|enumerate)\*?\}(?:\[[^\]]+\])?", "", block)
    block = re.sub(r"\\end\{(?:itemize|enumerate)\*?\}", "", block)
    parts = re.split(r"\\item\b", block)
    elements = []
    n = 1
    for part in parts[1:]:
        txt = clean_latex(part, cite_map, table_map)
        if not txt:
            continue
        bullet = f"{n}." if ordered else "-"
        elements.append(Paragraph(escape(txt), styles["Bullet"], bulletText=bullet))
        n += 1
    elements.append(Spacer(1, 4))
    return elements


def build_story(tex: str, bib: str, styles) -> list:
    cite_keys = citation_order(tex)
    cite_map = {k: i + 1 for i, k in enumerate(cite_keys)}
    table_map = table_label_map(tex)
    entries = balanced_entries(bib)
    body = split_document_body(tex)
    lines = body.splitlines()

    story = [
        Paragraph(escape(TITLE), styles["Title"]),
        Spacer(1, 10),
        Paragraph(escape(f"{AUTHOR}"), styles["Author"]),
        Paragraph(escape(AUTHOR_EMAIL), styles["Affiliation"]),
        Spacer(1, 8),
        Paragraph(
            "Working preprint | " + dt.date.today().isoformat(),
            styles["Subtitle"],
        ),
        Spacer(1, 18),
    ]

    figure_no = 0
    def add_figure(kind: str, caption: str, height: float = 176):
        nonlocal figure_no
        figure_no += 1
        story.append(
            KeepTogether(
                [
                    FigureGraphic(kind, height=height),
                    Spacer(1, 4),
                    Paragraph(f"<b>Figure {figure_no}.</b> {escape(caption)}", styles["Caption"]),
                    Spacer(1, 10),
                ]
            )
        )

    figure_map = {
        "fig:dual-scaling": ("dual_scaling", 176),
        "fig:harness-contract": ("harness_contract", 176),
        "fig:control-data": ("control_data", 176),
        "fig:derivation-closure": ("derivation_closure", 200),
        "fig:external-data": ("external_data", 176),
        "fig:dry-run": ("dry_run", 176),
        "fig:skill-as-code": ("skill_lifecycle", 176),
        "fig:evaluation-matrix": ("evaluation_matrix", 310),
    }

    sec_counter = [0, 0, 0]
    table_no = 0
    buf = []

    def flush():
        nonlocal buf
        text = " ".join(x.strip() for x in buf if x.strip()).strip()
        if text:
            m = re.match(r"\\paragraph\{([^}]+)\}\.?\s*(.*)", text, re.S)
            if m:
                story.append(
                    Paragraph(
                        escape(clean_latex(m.group(1), cite_map, table_map)),
                        styles["ParaHead"],
                    )
                )
                if m.group(2).strip():
                    story.append(para(m.group(2), styles["Body"], cite_map, table_map))
            else:
                story.append(para(text, styles["Body"], cite_map, table_map))
            story.append(Spacer(1, 5))
        buf = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            flush()
            i += 1
            continue
        if line.startswith(r"\newpage"):
            flush()
            story.append(PageBreak())
            i += 1
            continue
        if re.match(r"\\begin\{itemize\*?\}", line):
            flush()
            block, i = collect_environment(lines, i, "itemize")
            story.extend(parse_items(block, styles, cite_map, table_map, ordered=False))
            continue
        if re.match(r"\\begin\{enumerate\*?\}", line):
            flush()
            block, i = collect_environment(lines, i, "enumerate")
            story.extend(parse_items(block, styles, cite_map, table_map, ordered=True))
            continue
        if re.match(r"\\begin\{table\*?\}", line):
            flush()
            block, i = collect_environment(lines, i, "table")
            table_no += 1
            story.extend(table_from_latex(block, styles, cite_map, table_map, table_no))
            continue
        if re.match(r"\\begin\{figure\*?\}", line):
            flush()
            block, i = collect_environment(lines, i, "figure")
            caption = figure_caption_from_latex(block, cite_map, table_map)
            label_match = re.search(r"\\label\{([^}]+)\}", block)
            label = label_match.group(1) if label_match else ""
            if label not in figure_map:
                raise ValueError(f"No renderer registered for figure label: {label or '<missing>'}")
            kind, height = figure_map[label]
            add_figure(kind, caption, height)
            continue
        if re.match(r"\\begin\{proposition\}", line):
            flush()
            block, i = collect_environment(lines, i, "proposition")
            story.extend(proposition_from_latex(block, styles, cite_map, table_map))
            continue
        if re.match(r"\\begin\{(?:align|equation)\*?\}", line):
            flush()
            env = "align" if "align" in line else "equation"
            block, i = collect_environment(lines, i, env)
            story.extend(code_block(block, styles, cite_map, table_map))
            continue
        handled = False
        for command, style_name in [
            ("section", "H1"),
            ("subsection", "H2"),
            ("subsubsection", "H3"),
        ]:
            rb = read_braced(line, command)
            if rb:
                flush()
                title, rest = rb
                clean_title = clean_latex(title, cite_map, table_map)
                if command == "section":
                    sec_counter[0] += 1
                    sec_counter[1] = 0
                    sec_counter[2] = 0
                    numbered_title = f"{sec_counter[0]}. {clean_title}"
                elif command == "subsection":
                    sec_counter[1] += 1
                    sec_counter[2] = 0
                    numbered_title = f"{sec_counter[0]}.{sec_counter[1]} {clean_title}"
                elif command == "subsubsection":
                    sec_counter[2] += 1
                    numbered_title = f"{sec_counter[0]}.{sec_counter[1]}.{sec_counter[2]} {clean_title}"
                else:
                    numbered_title = clean_title
                heading_style = styles[style_name]
                heading_spacer = 4
                if command == "section" and clean_title == "Conclusion":
                    heading_style = styles["Conclusion"]
                    heading_spacer = 0
                story.append(Paragraph(escape(numbered_title), heading_style))
                story.append(Spacer(1, heading_spacer))
                if rest:
                    buf.append(rest)
                i += 1
                handled = True
                break
        if handled:
            continue
        if line.startswith(r"\label") or line.startswith(r"\centering") or line.startswith(r"\small"):
            i += 1
            continue
        buf.append(line)
        i += 1
    flush()

    if cite_keys:
        story.append(PageBreak())
        story.append(Paragraph("References", styles["H1"]))
        story.append(Spacer(1, 6))
        for key in cite_keys:
            number = cite_map[key]
            fields = entries.get(key, {})
            if fields:
                author = fields.get("author", "").replace(" and ", ", ")
                publication_date = fields.get("date") or fields.get("year", "")
                title = fields.get("title", key)
                venue = fields.get("journal") or fields.get("booktitle") or fields.get("howpublished") or ""
                ref = f"[{number}] {author}. {publication_date}. {title}."
                if venue:
                    ref += f" {venue}."
                volume = fields.get("volume")
                issue = fields.get("number") or fields.get("issue")
                pages = fields.get("pages")
                if volume or issue or pages:
                    publication_parts = []
                    if volume:
                        publication_parts.append(f"Volume {volume}")
                    if issue:
                        publication_parts.append(f"issue {issue}")
                    if pages:
                        publication_parts.append(f"pages {pages}")
                    ref += " " + ", ".join(publication_parts) + "."
                if fields.get("doi"):
                    ref += f" DOI: {fields['doi']}."
                if fields.get("url"):
                    ref += f" URL: {fields['url']}."
            else:
                ref = f"[{number}] {key}."
            story.append(Paragraph(escape(ref), styles["Reference"]))
            story.append(Spacer(1, 3))
    return story


def make_styles():
    base = getSampleStyleSheet()
    styles = {}
    styles["Title"] = ParagraphStyle(
        "Title",
        parent=base["Title"],
        fontName="Times-Bold",
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#111827"),
        spaceAfter=4,
    )
    styles["Author"] = ParagraphStyle(
        "Author",
        parent=base["Normal"],
        fontName="Times-Roman",
        fontSize=12,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#111827"),
    )
    styles["Affiliation"] = ParagraphStyle(
        "Affiliation",
        parent=base["Normal"],
        fontName="Times-Roman",
        fontSize=10,
        leading=13,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#334155"),
    )
    styles["Subtitle"] = ParagraphStyle(
        "Subtitle",
        parent=base["Normal"],
        fontName="Times-Italic",
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#475569"),
    )
    styles["H1"] = ParagraphStyle(
        "H1",
        parent=base["Heading1"],
        fontName="Times-Bold",
        fontSize=14,
        leading=17,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=9,
        spaceAfter=4,
    )
    styles["Conclusion"] = ParagraphStyle(
        "Conclusion",
        parent=styles["H1"],
        spaceBefore=4,
        spaceAfter=2,
    )
    styles["H2"] = ParagraphStyle(
        "H2",
        parent=base["Heading2"],
        fontName="Times-Bold",
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=8,
        spaceAfter=3,
    )
    styles["H3"] = ParagraphStyle(
        "H3",
        parent=base["Heading3"],
        fontName="Times-BoldItalic",
        fontSize=10.6,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceBefore=6,
        spaceAfter=2,
    )
    styles["ParaHead"] = ParagraphStyle(
        "ParaHead",
        parent=base["Normal"],
        fontName="Times-Bold",
        fontSize=10,
        leading=12.5,
        textColor=colors.HexColor("#111827"),
        spaceBefore=4,
        spaceAfter=1,
    )
    styles["Body"] = ParagraphStyle(
        "Body",
        parent=base["BodyText"],
        fontName="Times-Roman",
        fontSize=10,
        leading=12.7,
        alignment=TA_JUSTIFY,
        firstLineIndent=12,
        textColor=colors.HexColor("#111827"),
    )
    styles["Bullet"] = ParagraphStyle(
        "Bullet",
        parent=styles["Body"],
        leftIndent=18,
        firstLineIndent=0,
        bulletIndent=6,
        alignment=TA_LEFT,
    )
    styles["Caption"] = ParagraphStyle(
        "Caption",
        parent=base["Normal"],
        fontName="Times-Italic",
        fontSize=8.2,
        leading=10,
        textColor=colors.HexColor("#334155"),
        alignment=TA_LEFT,
    )
    styles["Formula"] = ParagraphStyle(
        "Formula",
        parent=base["Normal"],
        fontName="Times-Italic",
        fontSize=10.5,
        leading=13,
        leftIndent=10,
        rightIndent=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#111827"),
    )
    styles["Proposition"] = ParagraphStyle(
        "Proposition",
        parent=styles["Body"],
        fontName="Times-Roman",
        fontSize=9.4,
        leading=12.2,
        firstLineIndent=0,
        leftIndent=8,
        rightIndent=8,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#111827"),
        backColor=colors.HexColor("#f8fafc"),
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=0.45,
        borderPadding=6,
        spaceBefore=2,
        spaceAfter=4,
    )
    styles["Reference"] = ParagraphStyle(
        "Reference",
        parent=base["Normal"],
        fontName="Times-Roman",
        fontSize=8.6,
        leading=10.5,
        leftIndent=16,
        firstLineIndent=-16,
        textColor=colors.HexColor("#111827"),
    )
    return styles


def draw_page(canvas, doc):
    canvas.saveState()
    w, h = letter
    canvas.setStrokeColor(colors.HexColor("#cbd5e1"))
    canvas.setLineWidth(0.4)
    canvas.line(doc.leftMargin, h - 0.48 * inch, w - doc.rightMargin, h - 0.48 * inch)
    canvas.setFont("Times-Roman", 8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(doc.leftMargin, h - 0.38 * inch, "Contract-Centered Agentic Runtime")
    canvas.drawRightString(w - doc.rightMargin, 0.42 * inch, str(canvas.getPageNumber()))
    canvas.restoreState()


def build_pdf(paper_dir: str, output_pdf: str):
    tex, bib = read_source(paper_dir)
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        leftMargin=0.82 * inch,
        rightMargin=0.82 * inch,
        topMargin=0.72 * inch,
        bottomMargin=0.72 * inch,
        title=TITLE,
        author=f"{AUTHOR} <{AUTHOR_EMAIL}>",
        subject=f"{PREPRINT_VERSION} enterprise agentic runtime responsibility architecture",
    )
    styles = make_styles()
    story = build_story(tex, bib, styles)
    doc.build(story, onFirstPage=draw_page, onLaterPages=draw_page)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-dir", default=os.path.join(SCRIPT_DIR, "paper_source"))
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    build_pdf(args.paper_dir, args.output)
    print(args.output)


if __name__ == "__main__":
    main()
