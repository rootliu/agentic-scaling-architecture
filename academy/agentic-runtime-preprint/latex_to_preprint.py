from __future__ import annotations

import argparse
import datetime as dt
import math
import os
import re
from xml.sax.saxutils import escape as xml_escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
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
PREPRINT_VERSION = "v27"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Derived from PREPRINT_VERSION so a version bump cannot silently overwrite the
# previous version's PDF: v20 shipped three different documents (26, 27 and 33
# pages) under one filename before the two were tied together.
DEFAULT_OUTPUT = os.path.join(
    SCRIPT_DIR,
    "output",
    "pdf",
    f"Scalable_Manageable_Agentic_Runtime_Preprint_{PREPRINT_VERSION}.pdf",
)
RESPONSIBILITY_BAND_HEIGHT = 74


_SUB_OPEN = "__AGENTIC_RENDERER_SUB_OPEN_5D7A9C__"
_SUB_CLOSE = "__AGENTIC_RENDERER_SUB_CLOSE_5D7A9C__"
_SUPER_OPEN = "__AGENTIC_RENDERER_SUPER_OPEN_5D7A9C__"
_SUPER_CLOSE = "__AGENTIC_RENDERER_SUPER_CLOSE_5D7A9C__"
_RICH_TEXT_SENTINELS = {
    _SUB_OPEN: "<sub>",
    _SUB_CLOSE: "</sub>",
    _SUPER_OPEN: "<super>",
    _SUPER_CLOSE: "</super>",
}


def escape(text: str) -> str:
    """XML-escape text, restoring only markup emitted by this renderer."""
    escaped = xml_escape(text)
    for sentinel, tag in _RICH_TEXT_SENTINELS.items():
        escaped = escaped.replace(xml_escape(sentinel), tag)
    return escaped


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


def draw_orthogonal_arrow(canvas, points: list[tuple[float, float]],
                          color: str = "#2563eb", stroke_width: float = 1.15,
                          dashed: bool = False):
    if len(points) < 2:
        raise ValueError("An orthogonal arrow needs at least two points")
    canvas.saveState()
    canvas.setStrokeColor(hx(color))
    canvas.setFillColor(hx(color))
    canvas.setLineWidth(stroke_width)
    if dashed:
        canvas.setDash(4, 3)
    path = canvas.beginPath()
    path.moveTo(*points[0])
    for previous, point in zip(points, points[1:]):
        if previous[0] != point[0] and previous[1] != point[1]:
            raise ValueError("Orthogonal arrow segments must be horizontal or vertical")
        path.lineTo(*point)
    canvas.drawPath(path, stroke=1, fill=0)
    canvas.setDash()
    x1, y1 = points[-2]
    x2, y2 = points[-1]
    angle = math.atan2(y2 - y1, x2 - x1)
    size = 5
    for offset in (math.pi * 0.82, -math.pi * 0.82):
        canvas.line(
            x2,
            y2,
            x2 + size * math.cos(angle + offset),
            y2 + size * math.sin(angle + offset),
        )
    canvas.restoreState()


FIGURE_IMAGE_MAP = {
    "dual_scaling": "1.png",
    "harness_contract": "2.png",
    "control_data": "3.png",
    "derivation_closure": "4.png",
    "external_data": "5.png",
    "dry_run": "6.png",
    "skill_lifecycle": "7.png",
}


class FigureGraphic(Flowable):
    def __init__(self, kind: str, width: float = FIGURE_WIDTH, height: float = 176,
                 paper_dir: str | None = None):
        super().__init__()
        self.kind = kind
        self.width = width
        self.content_height = height
        self.hAlign = "CENTER"
        self.image_path = None
        if paper_dir and kind in FIGURE_IMAGE_MAP:
            candidate = os.path.join(paper_dir, FIGURE_IMAGE_MAP[kind])
            if os.path.exists(candidate):
                self.image_path = candidate
        self.height = height if self.image_path else height + RESPONSIBILITY_BAND_HEIGHT

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
        if self.image_path:
            self._draw_image(canvas)
        else:
            canvas.translate(0, RESPONSIBILITY_BAND_HEIGHT)
            draw_method = getattr(self, f"_draw_{self.kind}", None)
            if draw_method is None:
                raise ValueError(f"Unknown figure kind: {self.kind}")
            draw_method(canvas)
            canvas.translate(0, -RESPONSIBILITY_BAND_HEIGHT)
            self._draw_responsibility_band(canvas)
        canvas.restoreState()

    def _draw_image(self, canvas):
        try:
            reader = ImageReader(self.image_path)
            img_w, img_h = reader.getSize()
        except Exception:
            return
        aspect = img_w / img_h
        margin = 4
        target_w = self.width - 2 * margin
        target_h = self.content_height - 2 * margin
        if target_w / target_h > aspect:
            draw_h = target_h
            draw_w = target_h * aspect
        else:
            draw_w = target_w
            draw_h = target_w / aspect
        x = margin + (target_w - draw_w) / 2
        y = margin + (target_h - draw_h) / 2
        canvas.drawImage(
            self.image_path, x, y, draw_w, draw_h,
            preserveAspectRatio=True, mask="auto",
        )

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
            "Chief Information Officer-governed semantic and telemetry foundation: data substrate",
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
        draw_wrapped(canvas, "Focused causal contract and measurement planes", 18, h - 12, w - 36,
                     "Helvetica-Bold", 9.2, "#0f172a")
        card_y, card_h, card_w = 101, 42, 118
        xs = [16, 172, 328]
        cards = [
            ("Capability change", "activated configuration c", "#f0fdfa", "#2dd4bf", "#115e59"),
            ("Harness contract", "admit + bind + trace", "#eff6ff", "#60a5fa", "#1d4ed8"),
            ("Scaffold capacity", "compatible configuration s", "#fffbeb", "#f59e0b", "#92400e"),
        ]
        for x, (title, subtitle, fill, stroke, color) in zip(xs, cards):
            self._pill(canvas, x, card_y, card_w, card_h, title, subtitle,
                       fill, stroke, color)
        draw_arrow(canvas, xs[0] + card_w, card_y + card_h / 2, xs[1], card_y + card_h / 2,
                   "#0f766e")
        draw_arrow(canvas, xs[1] + card_w, card_y + card_h / 2, xs[2], card_y + card_h / 2,
                   "#2563eb")

        data_x, data_y, data_w, data_h = 16, 30, 132, 46
        self._pill(
            canvas,
            data_x,
            data_y,
            data_w,
            data_h,
            "Governed data and evidence",
            "fixed snapshot | lineage",
            "#f5f3ff",
            "#a78bfa",
            "#5b21b6",
        )
        measure_x, measure_y, measure_w, measure_h = 172, 20, 274, 62
        self._pill(
            canvas,
            measure_x,
            measure_y,
            measure_w,
            measure_h,
            "Measurement plane",
            "semantic outcome Q(c,s) | runtime response R(c,s)\n"
            "condition coverage | enforcement overhead E(c,s)",
            "#ecfdf5",
            "#10b981",
            "#047857",
        )
        draw_arrow(
            canvas,
            data_x + data_w,
            data_y + data_h / 2,
            measure_x,
            data_y + data_h / 2,
            "#7c3aed",
            0.9,
        )
        draw_orthogonal_arrow(
            canvas,
            [
                (data_x + data_w / 2, data_y + data_h),
                (data_x + data_w / 2, 90),
                (xs[1] + card_w / 2, 90),
                (xs[1] + card_w / 2, card_y),
            ],
            "#7c3aed",
            0.9,
            dashed=True,
        )
        draw_arrow(
            canvas,
            xs[2] + card_w / 2,
            card_y,
            xs[2] + card_w / 2,
            measure_y + measure_h,
            "#b45309",
            0.9,
        )

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
            ("A", "authority, effects + evidence duties"),
            ("B", "time, cost, token, concurrency budgets"),
            ("V", "policy, model, data, capability, verifier + trace versions"),
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
        draw_wrapped(canvas, "Derivation closure with an explicit semantic join and stop gate",
                     18, h - 12, w - 36, "Helvetica-Bold", 9.2, "#0f172a")
        card_y, card_h = 112, 50
        card_w, gap = 98, 12
        xs = [16 + index * (card_w + gap) for index in range(4)]
        stages = [
            ("Main agent", "decompose request\nno task tools", "#eff6ff", "#60a5fa", "#1d4ed8"),
            ("Bounded sub-agents", "fixed tools + sources\nbounded outputs", "#f0fdfa", "#2dd4bf", "#115e59"),
            ("Verifier / semantic join", "field-level support\nbest evidence", "#f5f3ff", "#a78bfa", "#5b21b6"),
            ("Termination gate", "target | budget\ntyped failure", "#fff7ed", "#fb923c", "#9a3412"),
        ]
        for x, stage in zip(xs, stages):
            title, subtitle, fill, stroke, color = stage
            self._pill(canvas, x, card_y, card_w, card_h, title, subtitle,
                       fill, stroke, color)
        for index in range(3):
            draw_arrow(
                canvas,
                xs[index] + card_w,
                card_y + card_h / 2,
                xs[index + 1],
                card_y + card_h / 2,
                "#475569",
                0.9,
            )

        self._pill(canvas, xs[1], 57, card_w, 35, "Derivation condition",
                   "unmet declared domain", "#ffffff", "#2dd4bf", "#115e59")
        self._pill(canvas, xs[2], 57, card_w, 35, "Satisfaction ratio",
                   "supported / declared", "#ffffff", "#a78bfa", "#5b21b6")
        draw_arrow(canvas, xs[1] + card_w / 2, card_y, xs[1] + card_w / 2, 92,
                   "#0f766e", 0.8)
        draw_arrow(canvas, xs[2] + card_w / 2, 92, xs[2] + card_w / 2, card_y,
                   "#7c3aed", 0.8)
        draw_orthogonal_arrow(
            canvas,
            [
                (xs[3] + card_w / 2, card_y),
                (xs[3] + card_w / 2, 28),
                (xs[1] + card_w / 2, 28),
                (xs[1] + card_w / 2, 57),
            ],
            "#7c3aed",
            0.9,
            dashed=True,
        )
        draw_wrapped(
            canvas,
            "Continue only when the ratio is below target and a declared sub-domain still admits derivation.",
            xs[1] - 4,
            22,
            xs[3] + card_w - xs[1] + 4,
            "Helvetica-Bold",
            5.8,
            "#5b21b6",
            TA_LEFT,
        )

    def _draw_external_data(self, canvas):
        w, h = self.width, self.content_height
        draw_wrapped(canvas, "External data becomes evidence through a governed contract path", 18, h - 12, w - 36,
                     "Helvetica-Bold", 9.2, "#0f172a")
        specs = [
            (16, 100, "Data authority", "catalog + residency\nsource owner", "#f5f3ff", "#a78bfa", "#5b21b6"),
            (128, 116, "Resolved contract", "principal | schema\nsnapshot | budget", "#eff6ff", "#60a5fa", "#1d4ed8"),
            (256, 88, "Isolated fetch", "bound credential\nnetwork boundary", "#fffbeb", "#f59e0b", "#92400e"),
            (356, 90, "Evidence bundle", "typed result\nlineage + query hash", "#ecfdf5", "#10b981", "#047857"),
        ]
        card_y, card_h = 83, 56
        for x, width, title, subtitle, fill, stroke, color in specs:
            self._pill(canvas, x, card_y, width, card_h, title, subtitle,
                       fill, stroke, color)
        for left, right, color in zip(specs, specs[1:], ["#7c3aed", "#2563eb", "#b45309"]):
            draw_arrow(
                canvas,
                left[0] + left[1],
                card_y + card_h / 2,
                right[0],
                card_y + card_h / 2,
                color,
                0.9,
            )
        draw_wrapped(canvas, "Recorded contract and evidence duties", 18, 65, w - 36,
                     "Helvetica-Bold", 6.3, "#475569", TA_LEFT)
        obligations = [
            ("principal", 63, "#dbeafe"),
            ("source + snapshot", 85, "#ede9fe"),
            ("schema", 57, "#dcfce7"),
            ("residency", 61, "#fef3c7"),
            ("lineage", 58, "#ffe4e6"),
            ("query hash", 63, "#cffafe"),
        ]
        ox = 16
        for label, width, fill in obligations:
            canvas.setFillColor(hx(fill))
            canvas.roundRect(ox, 27, width, 22, 3, stroke=0, fill=1)
            draw_wrapped(canvas, label, ox + 3, 42, width - 6,
                         "Helvetica-Bold", 5.4, "#334155")
            ox += width + 5
        draw_wrapped(canvas, "No undeclared task semantics or credentials cross the path.",
                     18, 19, w - 36, "Helvetica", 5.8, "#475569", TA_LEFT)

    def _draw_dry_run(self, canvas):
        w, h = self.width, self.content_height
        draw_wrapped(canvas, "Dry-run separates logical control, physical execution, and evidence", 18, h - 12, w - 36,
                     "Helvetica-Bold", 9.2, "#0f172a")
        lane_x, lane_w, lane_h = 16, w - 32, 34
        lane_ys = [106, 64, 22]
        lane_specs = [
            ("Logical control", ["Plan", "Admit", "Commit gate"], "#eff6ff", "#60a5fa", "#1d4ed8"),
            ("Physical execution", ["Bind", "Run in isolation", "Effect boundary"], "#fffbeb", "#f59e0b", "#92400e"),
            ("Evidence", ["Graph hash", "Trace stream", "Attestation"], "#ecfdf5", "#10b981", "#047857"),
        ]
        label_w, node_w, node_gap = 104, 88, 12
        node_xs = [lane_x + 116 + index * (node_w + node_gap) for index in range(3)]
        for y, (label, nodes, fill, stroke, color) in zip(lane_ys, lane_specs):
            canvas.saveState()
            canvas.setFillColor(hx(fill))
            canvas.setStrokeColor(hx(stroke))
            canvas.setLineWidth(0.75)
            canvas.roundRect(lane_x, y, lane_w, lane_h, 5, stroke=1, fill=1)
            canvas.restoreState()
            draw_wrapped(canvas, label, lane_x + 8, y + 22, label_w - 12,
                         "Helvetica-Bold", 6.4, color, TA_LEFT)
            for node_x, node in zip(node_xs, nodes):
                self._pill(canvas, node_x, y + 6, node_w, 22, node, "",
                           "#ffffff", stroke, color)
            for index in range(2):
                draw_arrow(canvas, node_xs[index] + node_w, y + lane_h / 2,
                           node_xs[index + 1], y + lane_h / 2, color, 0.75)
        for node_x in node_xs:
            center_x = node_x + node_w / 2
            draw_arrow(canvas, center_x, lane_ys[0], center_x, lane_ys[1] + lane_h,
                       "#64748b", 0.7, dashed=True)
            draw_arrow(canvas, center_x, lane_ys[1], center_x, lane_ys[2] + lane_h,
                       "#64748b", 0.7, dashed=True)
        draw_wrapped(
            canvas,
            "Vertical links are illustrative, non-bijective mappings; each lane remains independently inspectable.",
            lane_x + 8,
            17,
            lane_w - 16,
            "Helvetica",
            5.5,
            "#475569",
            TA_LEFT,
        )

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
        draw_wrapped(canvas, "Falsification matrix: P1 is the primary release decision", 18, h - 10, w - 36,
                     "Helvetica-Bold", 9.2, "#0f172a")
        table_x = 16
        widths = [62, 126, 105, 137]
        xs = [table_x]
        for width in widths[:-1]:
            xs.append(xs[-1] + width)
        header_y, header_h = 250, 35
        headers = [
            "Hypothesis",
            "Intervention and control",
            "Evidence plane",
            "Falsification or inconclusive condition",
        ]
        for x, width, header in zip(xs, widths, headers):
            canvas.setFillColor(hx("#1e3a5f"))
            canvas.setStrokeColor(hx("#ffffff"))
            canvas.setLineWidth(0.5)
            canvas.rect(x, header_y, width, header_h, stroke=1, fill=1)
            draw_wrapped(canvas, header, x + 5, header_y + header_h - 7, width - 10,
                         "Helvetica-Bold", 5.8, "#ffffff", TA_LEFT, 6.7)

        primary_y, primary_h = 109, 141
        primary = [
            ("P1", "P1  PRIMARY\ncapability x Scaffold\nseparability"),
            (
                "",
                "Cluster-period randomized crossover. Independently vary activated capability "
                "configuration c and Scaffold capacity configuration s; hold workload and data "
                "snapshot fixed; preregister reset or washout.",
            ),
            (
                "",
                "Semantic outcome Q(c,s); runtime response R(c,s); enforcement overhead E(c,s); "
                "six condition-violation rates; cluster-aware uncertainty; capability-by-Scaffold "
                "interaction estimand.",
            ),
            (
                "",
                "Falsified within Omega if a semantic, runtime, or enforcement interaction exceeds "
                "its preregistered margin. Inconclusive if operating-region, condition, or detectable-"
                "interaction requirements fail. Otherwise supported within Omega.",
            ),
        ]
        for index, (x, width, (_, text)) in enumerate(zip(xs, widths, primary)):
            canvas.setFillColor(hx("#eff6ff" if index else "#dbeafe"))
            canvas.setStrokeColor(hx("#93c5fd"))
            canvas.setLineWidth(0.65)
            canvas.rect(x, primary_y, width, primary_h, stroke=1, fill=1)
            draw_wrapped(
                canvas,
                text,
                x + 6,
                primary_y + primary_h - 8,
                width - 12,
                "Helvetica-Bold" if index == 0 else "Helvetica",
                5.4 if index == 0 else 5.25,
                "#1e3a5f" if index == 0 else "#334155",
                TA_LEFT,
                6.35,
            )

        secondary = [
            ("P15", "Vector gate", "proposal-bank contrasts", "margin failure or phantom violation"),
            ("P16", "Evidence-path sufficiency", "held-out joint contrast", "direct-reading control wins"),
            ("P17", "Policy-contract decoupling", "dependency-change oracle", "unanticipated propagation"),
        ]
        row_h = 29
        for row_index, row in enumerate(secondary):
            y = primary_y - (row_index + 1) * row_h
            for column, (x, width, text) in enumerate(zip(xs, widths, row)):
                canvas.setFillColor(hx("#f8fafc" if row_index % 2 == 0 else "#f1f5f9"))
                canvas.setStrokeColor(hx("#cbd5e1"))
                canvas.setLineWidth(0.5)
                canvas.rect(x, y, width, row_h, stroke=1, fill=1)
                draw_wrapped(
                    canvas,
                    text,
                    x + 5,
                    y + row_h - 7,
                    width - 10,
                    "Helvetica-Bold" if column == 0 else "Helvetica",
                    5.0,
                    "#475569",
                    TA_LEFT,
                    5.8,
                )
        draw_wrapped(
            canvas,
            "Secondary protocols remain diagnostic; they do not substitute for the P1 release decision.",
            table_x + 4,
            16,
            sum(widths) - 8,
            "Helvetica-Bold",
            5.4,
            "#64748b",
            TA_LEFT,
        )


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


def reference_label_map(tex: str) -> dict[str, str]:
    """Map every cross-reference label to the number it renders as.

    Sections resolve to "N" or "N.M", figures and tables to their sequential
    number. Prose can then cite them through \\ref instead of a hard-coded
    numeral that silently desynchronizes when a section or figure moves.
    Proposition labels are excluded because clean_latex renders them as "P1".
    """
    labels: dict[str, str] = {}
    sec = [0, 0, 0]
    figure_no = 0
    table_no = 0
    pending_section = ""
    env = None
    for raw in split_document_body(tex).splitlines():
        line = raw.strip()
        if env is not None:
            match = re.search(r"\\label\{([^}]+)\}", line)
            if match:
                labels[match.group(1)] = str(
                    figure_no if env == "figure" else table_no
                )
            if line.startswith("\\end{" + env):
                env = None
            continue
        if re.match(r"\\begin\{figure\*?\}", line):
            env, figure_no, pending_section = "figure", figure_no + 1, ""
            continue
        if re.match(r"\\begin\{table\*?\}", line):
            env, table_no, pending_section = "table", table_no + 1, ""
            continue
        heading = re.match(r"\\(section|subsection|subsubsection)\{", line)
        if heading:
            level = ["section", "subsection", "subsubsection"].index(heading.group(1))
            sec[level] += 1
            for deeper in range(level + 1, len(sec)):
                sec[deeper] = 0
            pending_section = ".".join(str(n) for n in sec[: level + 1])
            continue
        match = re.match(r"\\label\{([^}]+)\}", line)
        if match and pending_section:
            if not match.group(1).startswith("prop:"):
                labels[match.group(1)] = pending_section
            pending_section = ""
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
        r"\min": "min",
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
    text = re.sub(r"\\widehat\{([^}]+)\}", r"\1-hat", text)
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
    text = re.sub(
        r"\b([A-Za-z][A-Za-z0-9-]*)_\{([^{}]+)\}",
        rf"\1{_SUB_OPEN}\2{_SUB_CLOSE}",
        text,
    )
    text = text.replace("{", "").replace("}", "")
    text = re.sub(
        r"\b([A-Za-z][A-Za-z0-9-]*)_([A-Za-z0-9-]+)\b",
        rf"\1{_SUB_OPEN}\2{_SUB_CLOSE}",
        text,
    )
    text = re.sub(
        r"\b([A-Za-z][A-Za-z0-9_]*(?:_hat)?)\s+subset of\s+([A-Za-z][A-Za-z0-9_]*)",
        r"\1 is a subset of \2",
        text,
    )
    return text


def clean_latex(
    text: str,
    cite_map: dict | None = None,
    ref_map: dict[str, str] | None = None,
) -> str:
    cite_map = cite_map or {}
    ref_map = ref_map or {}
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
    def named_ref_repl(kind: str, fallback: str):
        def repl(match):
            number = ref_map.get(match.group(1))
            return f"{kind} {number}" if number is not None else fallback

        return repl

    for kind, plural, fallback in [
        ("Table", "Tables", "the table"),
        ("Figure", "Figures", "the figure"),
        ("Section", "Sections", "the section"),
        ("Protocol", "Protocols", "the protocol"),
    ]:
        # "Sections~\ref{a}--\ref{b}" must keep the plural noun and the range.
        text = re.sub(
            rf"\b{plural}\s+\\ref\{{([^}}]+)\}}\s*(--|-|\u2013)\s*\\ref\{{([^}}]+)\}}",
            lambda m, p=plural, f=fallback: (
                f"{p} {ref_map[m.group(1)]}--{ref_map[m.group(3)]}"
                if m.group(1) in ref_map and m.group(3) in ref_map
                else f
            ),
            text,
        )
        text = re.sub(
            rf"\b{plural}\s+\\ref\{{([^}}]+)\}}\s+and\s+\\ref\{{([^}}]+)\}}",
            lambda m, p=plural, f=fallback: (
                f"{p} {ref_map[m.group(1)]} and {ref_map[m.group(2)]}"
                if m.group(1) in ref_map and m.group(2) in ref_map
                else f
            ),
            text,
        )
        text = re.sub(
            rf"\b{kind}\s+\\ref\{{([^}}]+)\}}", named_ref_repl(kind, fallback), text
        )
    text = re.sub(r"\bProposition\s+\\ref\{prop:p([0-9]+)\}", lambda m: f"Proposition P{m.group(1)}", text)
    text = re.sub(r"\\ref\{prop:p([0-9]+)\}", lambda m: f"P{m.group(1)}", text)
    text = re.sub(r"\\ref\{([^}]+)\}", lambda m: ref_map.get(m.group(1), ""), text)
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
    ref_map: dict[str, str] | None = None,
) -> Paragraph:
    return Paragraph(escape(clean_latex(text, cite_map, ref_map)), style)


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


def clean_table_cell(cell: str, cite_map: dict, ref_map: dict[str, str]) -> str:
    raw = cell.strip()
    if re.fullmatch(r"\$?\s*\\checkmark\s*\$?", raw):
        return "yes"
    if re.fullmatch(r"\$?\s*\\times\s*\$?", raw):
        return "no"
    return clean_latex(cell, cite_map, ref_map)


def table_from_latex(
    block: str,
    styles,
    cite_map: dict,
    ref_map: dict[str, str] | None = None,
    table_number: int = 1,
) -> list:
    ref_map = ref_map or {}
    caption = ""
    caption_arg = extract_command_arg(block, "caption")
    if caption_arg:
        caption = clean_latex(caption_arg, cite_map, ref_map)

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
        cells = [clean_table_cell(c, cite_map, ref_map) for c in part.split("&")]
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
    ref_map: dict[str, str],
) -> str:
    caption_arg = extract_command_arg(block, "caption")
    return (
        clean_latex(caption_arg, cite_map, ref_map)
        if caption_arg
        else "Source figure from the LaTeX manuscript."
    )


def proposition_from_latex(
    block: str,
    styles,
    cite_map: dict,
    ref_map: dict[str, str],
) -> list:
    title_match = re.search(r"\\begin\{proposition\}(?:\[([^\]]+)\])?", block)
    title = (
        clean_latex(title_match.group(1), cite_map, ref_map)
        if title_match and title_match.group(1)
        else "Proposition"
    )
    body = re.sub(r"\\begin\{proposition\}(?:\[[^\]]+\])?", "", block)
    body = re.sub(r"\\end\{proposition\}", "", body)
    body = clean_latex(body, cite_map, ref_map)
    text = f"<b>{escape(title)}.</b> {escape(body)}"
    return [Paragraph(text, styles["Proposition"]), Spacer(1, 7)]


def code_block(
    block: str,
    styles,
    cite_map: dict,
    ref_map: dict[str, str],
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
    text = clean_latex(clean_math(block), cite_map, ref_map)
    text = re.sub(r"[ \t]+", " ", text).strip()
    return [Paragraph(escape(text).replace("\n", "<br/>"), styles["Formula"]), Spacer(1, 6)]


def parse_items(
    block: str,
    styles,
    cite_map: dict,
    ref_map: dict[str, str],
    ordered: bool = False,
) -> list:
    block = re.sub(r"\\begin\{(?:itemize|enumerate)\*?\}(?:\[[^\]]+\])?", "", block)
    block = re.sub(r"\\end\{(?:itemize|enumerate)\*?\}", "", block)
    parts = re.split(r"\\item\b", block)
    elements = []
    n = 1
    for part in parts[1:]:
        txt = clean_latex(part, cite_map, ref_map)
        if not txt:
            continue
        bullet = f"{n}." if ordered else "-"
        elements.append(Paragraph(escape(txt), styles["Bullet"], bulletText=bullet))
        n += 1
    elements.append(Spacer(1, 4))
    return elements


def build_story(tex: str, bib: str, styles, paper_dir: str | None = None) -> list:
    cite_keys = citation_order(tex)
    cite_map = {k: i + 1 for i, k in enumerate(cite_keys)}
    ref_map = reference_label_map(tex)
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
                    FigureGraphic(kind, height=height, paper_dir=paper_dir),
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
                        escape(clean_latex(m.group(1), cite_map, ref_map)),
                        styles["ParaHead"],
                    )
                )
                if m.group(2).strip():
                    story.append(para(m.group(2), styles["Body"], cite_map, ref_map))
            else:
                story.append(para(text, styles["Body"], cite_map, ref_map))
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
            story.extend(parse_items(block, styles, cite_map, ref_map, ordered=False))
            continue
        if re.match(r"\\begin\{enumerate\*?\}", line):
            flush()
            block, i = collect_environment(lines, i, "enumerate")
            story.extend(parse_items(block, styles, cite_map, ref_map, ordered=True))
            continue
        if re.match(r"\\begin\{table\*?\}", line):
            flush()
            block, i = collect_environment(lines, i, "table")
            table_no += 1
            story.extend(table_from_latex(block, styles, cite_map, ref_map, table_no))
            continue
        if re.match(r"\\begin\{figure\*?\}", line):
            flush()
            block, i = collect_environment(lines, i, "figure")
            caption = figure_caption_from_latex(block, cite_map, ref_map)
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
            story.extend(proposition_from_latex(block, styles, cite_map, ref_map))
            continue
        if re.match(r"\\begin\{(?:align|equation)\*?\}", line):
            flush()
            env = "align" if "align" in line else "equation"
            block, i = collect_environment(lines, i, env)
            story.extend(code_block(block, styles, cite_map, ref_map))
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
                clean_title = clean_latex(title, cite_map, ref_map)
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
    story = build_story(tex, bib, styles, paper_dir=paper_dir)
    doc.build(story, onFirstPage=draw_page, onLaterPages=draw_page)


def main():
    global TITLE
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-dir", default=os.path.join(SCRIPT_DIR, "paper_source"))
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    # v25 retired the two-paper split. --title exists so that if the series is
    # ever split again, the sub-papers cannot silently ship under one identical
    # title as v21/v22 did (both cover and PDF metadata read this global).
    parser.add_argument("--title", default=None,
                        help="override the cover and PDF-metadata title")
    args = parser.parse_args()
    if args.title:
        TITLE = args.title
    build_pdf(args.paper_dir, args.output)
    print(args.output)


if __name__ == "__main__":
    main()
