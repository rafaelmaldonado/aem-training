"""Render Session 42 as nine illustrated teaching slides."""

import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
OUT = ROOT / "origin_image"
OUT.mkdir(exist_ok=True)
SLIDES = json.loads((ROOT / "deck_content.json").read_text())
assert len(SLIDES) == 11
W, H = 1672, 941
NAVY = "#06134f"
BLUE = "#1236f4"
PURPLE = "#7b0a99"
GREEN = "#075b25"
ORANGE = "#ef4b17"
MUTED = "#546381"
PALE = "#eef2ff"
PALE_GREEN = "#edf8f0"
PALE_ORANGE = "#fff1e9"
PALE_PURPLE = "#f7effa"
WHITE = "#fffefd"
DARK = "#101e38"
FONT_DIR = Path("/System/Library/Fonts/Supplemental")


def f(size, bold=False, mono=False):
    name = "Courier New.ttf" if mono else "Arial Bold.ttf" if bold else "Arial.ttf"
    return ImageFont.truetype(str(FONT_DIR / name), size)


def text(d, x, y, value, size=30, color=NAVY, bold=False, mono=False):
    face = f(size, bold, mono)
    assert x + d.textlength(value, font=face) <= W - 26, value
    d.text((x, y), value, font=face, fill=color)


def centered(d, cx, y, value, size=30, color=NAVY, bold=False, mono=False):
    face = f(size, bold, mono)
    x = cx - d.textlength(value, font=face) / 2
    text(d, x, y, value, size, color, bold, mono)


def box(d, xy, color=BLUE, fill=WHITE, radius=15, width=3):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=color, width=width)


def right_arrow(d, x1, y, x2, color=BLUE):
    d.line((x1, y, x2, y), fill=color, width=5)
    d.polygon(((x2, y), (x2 - 17, y - 11), (x2 - 17, y + 11)), fill=color)


def slide(number, section, title, subtitle=None):
    im = Image.new("RGB", (W, H), "#fcfaf7")
    d = ImageDraw.Draw(im)
    for x in range(0, W, 42):
        d.line((x, 0, x, H), fill="#f5f1ec", width=1)
    for y in range(0, H, 42):
        d.line((0, y, W, y), fill="#f5f1ec", width=1)
    if number == 0:
        return im, d
    text(d, 45, 27, f"{number:02d} · {section.upper()}", 34, NAVY, True)
    title_size = 72 if len(title) < 41 else 66
    text(d, 45, 77, title, title_size, NAVY, True)
    if subtitle:
        text(d, 48, 164, subtitle, 30, NAVY)
    d.line((44, 210, 1627, 210), fill=BLUE, width=3)
    return im, d


def footer(d, message, source=""):
    box(d, (47, 824, 1625, 903), BLUE, PALE, 10, 2)
    d.ellipse((69, 840, 108, 879), outline=BLUE, width=3)
    centered(d, 88, 841, "i", 27, BLUE, True)
    text(d, 129, 842, message, 32, BLUE, True)
    if source:
        text(d, 51, 913, source, 17, MUTED)


def save(im, number):
    im.save(OUT / f"slide_{number:02d}.png")


# 01 · The cover follows Session 37's title / three-part agenda composition.
im, d = slide(0, "", "")
text(d, 60, 70, "Class 42 · Week 9 · Day 42 · October 13, 2026", 39, NAVY, True)
d.line((60, 141, 1064, 141), fill=BLUE, width=4)
text(d, 60, 225, "Call an external", 105, NAVY, True)
text(d, 60, 350, "service safely", 105, NAVY, True)
text(d, 63, 550, "Bound the wait. Classify the result.", 42, BLUE, True)
text(d, 63, 604, "Make retries deliberate.", 42, BLUE, True)
d.line((62, 686, 1060, 686), fill=BLUE, width=3)
text(d, 63, 720, "30-minute technical session", 37, BLUE, True)
text(d, 63, 802, "Juan Maldonado", 35, NAVY, True)
d.line((1201, 255, 1201, 695), fill=BLUE, width=4)
for i, (head, sub, color) in enumerate((("1. Contract", "What is a valid response?", BLUE), ("2. Wait", "Who pays for latency?", GREEN), ("3. Recovery", "When is retry safe?", PURPLE))):
    y = 274 + i * 205
    d.ellipse((1141, y, 1261, y + 120), fill=WHITE, outline=color, width=5)
    centered(d, 1201, y + 29, str(i + 1), 48, color, True)
    text(d, 1284, y + 13, head, 38, NAVY, True)
    text(d, 1285, y + 69, sub, 26, NAVY)
save(im, 1)

# 02 · Three common provider contracts, with native AEM integrations named.
im, d = slide(2, "INTEGRATION EXAMPLES", SLIDES[1]["title"], SLIDES[1]["subtitle"])
examples = [
    (60, "Commerce data", "GET availability", "Page or refresh job", "Freshness + caching", GREEN, PALE_GREEN),
    (596, "CRM lead", "POST /leads", "Form submission", "Duplicate writes", PURPLE, PALE_PURPLE),
    (1132, "Translation job", "POST /jobs + poll", "Author workflow", "Long-running work", ORANGE, PALE_ORANGE),
]
for x, heading, method, trigger, risk, color, fill in examples:
    box(d, (x, 260, x + 480, 765), color, WHITE)
    d.rounded_rectangle((x + 2, 262, x + 478, 353), radius=13, fill=fill)
    d.rectangle((x + 2, 333, x + 478, 353), fill=fill)
    text(d, x + 27, 287, heading, 34, color, True)
    text(d, x + 28, 388, method, 26, NAVY, mono=True)
    d.line((x + 27, 453, x + 450, 453), fill="#dbe3ef", width=2)
    text(d, x + 28, 489, "TRIGGER", 25, color, True)
    text(d, x + 28, 530, trigger, 27, NAVY)
    d.line((x + 27, 597, x + 450, 597), fill="#dbe3ef", width=2)
    text(d, x + 28, 628, "DESIGN CONCERN", 25, color, True)
    text(d, x + 28, 673, risk, 27, NAVY)
footer(d, SLIDES[1]["takeaway"], SLIDES[1]["source_label"])
save(im, 2)

# 03 · Ownership map plus a concrete request and response.
im, d = slide(3, "HTTP CONTRACT", SLIDES[2]["title"], SLIDES[2]["subtitle"])
steps = [(55, 275, 320, "Workflow", PURPLE), (397, 275, 702, "Process Step", BLUE), (780, 275, 1135, "OSGi service", BLUE), (1213, 275, 1616, "Provider", GREEN)]
for x, y, x2, label, color in steps:
    box(d, (x, y, x2, y + 120), color, PALE_PURPLE if color == PURPLE else PALE_GREEN if color == GREEN else WHITE)
    centered(d, (x + x2) // 2, y + 35, label, 34, color, True)
for x1, x2 in ((330, 387), (712, 770), (1145, 1203)):
    right_arrow(d, x1, 335, x2)
box(d, (57, 445, 998, 781), BLUE, WHITE)
text(d, 82, 467, "ILLUSTRATIVE HTTP EXCHANGE", 29, BLUE, True)
d.line((80, 520, 972, 520), fill="#b9c6e0", width=2)
text(d, 88, 545, "REQUEST", 25, BLUE, True)
text(d, 265, 540, "GET /ok", 33, NAVY, mono=True)
text(d, 265, 593, "X-API-Key: [server value]", 28, NAVY, mono=True)
text(d, 88, 665, "RESPONSE", 25, GREEN, True)
text(d, 265, 661, "200 + headers + body", 30, NAVY, mono=True)
box(d, (1030, 445, 1615, 781), PURPLE, PALE_PURPLE)
text(d, 1055, 467, "RESPONSE CONTRACT", 29, PURPLE, True)
d.line((1050, 520, 1592, 520), fill="#cfb8dc", width=2)
text(d, 1059, 549, "Accepted status", 29, NAVY)
text(d, 1059, 602, "Content-Type + body size", 27, NAVY)
text(d, 1059, 657, "Required fields", 28, NAVY)
text(d, 1059, 714, "Error meanings", 27, NAVY)
footer(d, SLIDES[2]["takeaway"], SLIDES[2]["source_label"])
save(im, 3)

# 04 · Credential value, reference, and request stay at distinct boundaries.
im, d = slide(4, "CREDENTIALS", SLIDES[3]["title"], SLIDES[3]["subtitle"])
box(d, (60, 255, 1001, 777), PURPLE, WHITE)
text(d, 87, 280, "WHERE THE KEY GOES", 31, PURPLE, True)
d.line((85, 333, 975, 333), fill="#d9cae3", width=2)
for i, (label, value, color) in enumerate((
    ("CLOUD MANAGER · SECRET VALUE", "STATUS_API_KEY = [secret value]", GREEN),
    ("UI.CONFIG · REFERENCE IN GIT", '"apiKey": "$[secret:STATUS_API_KEY]"', PURPLE),
    ("OSGI SERVICE · OUTBOUND HEADER", "X-API-Key: [resolved value]", BLUE),
)):
    y = 365 + i * 125
    text(d, 88, y, label, 25, color, True)
    text(d, 88, y + 43, value, 28, NAVY, mono=True)
    if i < 2:
        d.line((87, y + 103, 973, y + 103), fill="#d9e0eb", width=2)
box(d, (1032, 255, 1613, 777), BLUE, WHITE)
text(d, 1060, 280, "PROTECT THE VALUE", 31, BLUE, True)
for i, (head, detail, color) in enumerate((
    ("Fixed HTTPS host", "No redirect to another host.", GREEN),
    ("Server only", "No /content, HTML or JavaScript.", PURPLE),
    ("Safe diagnostics", "No key or payload in logs.", ORANGE),
)):
    y = 368 + i * 119
    d.ellipse((1060, y + 6, 1083, y + 29), fill=color)
    text(d, 1102, y, head, 29, color, True)
    text(d, 1102, y + 44, detail, 25, NAVY)
text(d, 1060, 721, "Password field masks UI; it is not storage.", 23, MUTED)
footer(d, SLIDES[3]["takeaway"], SLIDES[3]["source_label"])
save(im, 4)

# 05 · One latency comparison, then the two timeout meanings.
im, d = slide(5, "LATENCY", SLIDES[4]["title"], SLIDES[4]["subtitle"])
text(d, 66, 252, "ILLUSTRATIVE SYNCHRONOUS PAGE", 30, BLUE, True)
box(d, (64, 306, 410, 428), BLUE, PALE)
centered(d, 237, 327, "AEM render", 36, NAVY, True)
centered(d, 237, 377, "150 ms local", 26, NAVY)
right_arrow(d, 420, 366, 490)
box(d, (502, 306, 1340, 428), ORANGE, PALE_ORANGE)
centered(d, 921, 327, "Remote provider", 36, ORANGE, True)
centered(d, 921, 377, "2 s waiting", 27, NAVY)
right_arrow(d, 1351, 366, 1412)
text(d, 1436, 329, "HTML", 36, GREEN, True)
text(d, 1436, 379, "~2.15 s", 26, ORANGE, True)
box(d, (64, 495, 790, 762), PURPLE, WHITE)
text(d, 92, 520, "CONNECT TIMEOUT", 33, PURPLE, True)
text(d, 92, 581, "1,000 ms", 42, NAVY, True)
text(d, 92, 643, "Limits connection establishment.", 27, NAVY)
text(d, 92, 690, "DNS may add time before it.", 27, MUTED)
box(d, (827, 495, 1612, 762), BLUE, WHITE)
text(d, 858, 520, "READ TIMEOUT", 33, BLUE, True)
text(d, 858, 581, "2,000 ms", 42, NAVY, True)
text(d, 858, 643, "Limits each blocked read.", 27, NAVY)
text(d, 858, 690, "/slow waits 3 s; this read times out first.", 26, MUTED)
footer(d, SLIDES[4]["takeaway"], SLIDES[4]["source_label"])
save(im, 5)

# 06 · Evidence first, following Session 37's concrete log treatment.
im, d = slide(6, "OBSERVED RESULT", SLIDES[5]["title"], SLIDES[5]["subtitle"])
box(d, (58, 251, 1035, 779), BLUE, DARK)
text(d, 83, 273, "ILLUSTRATIVE ERROR.LOG · FOUR SEPARATE RUNS", 29, WHITE, True)
d.line((81, 324, 1012, 324), fill="#62708e", width=2)
log_rows = [
    ("/ok", "upstreamStatus=200 outcome=OK", GREEN),
    ("/ok · wrong key", "upstreamStatus=401 outcome=STOP", PURPLE),
    ("/unavailable", "upstreamStatus=503 outcome=RETRY", ORANGE),
    ("/slow", "transportFailure=SocketTimeoutException outcome=RETRY", ORANGE),
]
for i, (path, evidence, color) in enumerate(log_rows):
    y = 346 + i * 100
    text(d, 88, y, f"[RUN {i + 1}] {path}", 27, "#c8d7f4", mono=True)
    text(d, 88, y + 40, evidence, 27, "#ffffff", mono=True)
    d.rectangle((962, y + 42, 1007, y + 59), fill=color)
box(d, (1060, 251, 1614, 779), BLUE, WHITE)
text(d, 1090, 276, "READ THE EVIDENCE", 32, BLUE, True)
for i, (head, desc, color) in enumerate((("200", "Continue; validate data if needed.", GREEN), ("401", "Fix key or access before a new run.", PURPLE), ("503", "Inspect provider before retry.", ORANGE), ("Timeout", "Locate the failed read wait.", ORANGE))):
    y = 349 + i * 101
    d.line((1090, y - 13, 1585, y - 13), fill="#dce3ef", width=2)
    text(d, 1090, y, head, 32, color, True)
    text(d, 1090, y + 44, desc, 24, NAVY)
footer(d, SLIDES[5]["takeaway"], SLIDES[5]["source_label"])
save(im, 6)

# 07 · A finite retry budget beside the distinct remote-write risk.
im, d = slide(7, "RETRY POLICY", SLIDES[6]["title"], SLIDES[6]["subtitle"])
box(d, (60, 252, 935, 770), BLUE, WHITE)
text(d, 86, 275, "POLICY EXAMPLE · 3 ATTEMPTS TOTAL", 28, BLUE, True)
segments = [(92, 349, 249, "2 s", BLUE), (253, 349, 364, "1 s", MUTED), (368, 349, 525, "2 s", BLUE), (529, 349, 640, "2 s", MUTED), (644, 349, 801, "2 s", BLUE)]
for x1, y, x2, value, color in segments:
    box(d, (x1, y, x2, y + 103), color, PALE if color == BLUE else "#f0f1f3", 8, 2)
    centered(d, (x1 + x2) // 2, y + 23, value, 34, color, True)
text(d, 122, 473, "try 1", 25, BLUE)
text(d, 405, 473, "try 2", 25, BLUE)
text(d, 685, 473, "try 3", 25, BLUE)
d.line((99, 558, 887, 558), fill=PURPLE, width=5)
for x in (99, 803, 887):
    d.ellipse((x - 9, 549, x + 9, 567), fill=PURPLE)
text(d, 91, 582, "0", 26, PURPLE)
text(d, 778, 582, "9 s", 26, PURPLE)
text(d, 812, 630, "10 s cap", 25, PURPLE)
text(d, 92, 692, "3 job deliveries × 3 HTTP tries = 9 calls", 26, ORANGE, True)
box(d, (960, 252, 1612, 770), ORANGE, WHITE)
text(d, 987, 275, "LOST RESPONSE · CONCEPTUAL POST", 28, ORANGE, True)
stages = [("1", "Send write"), ("2", "Provider commits"), ("3", "Reply is lost"), ("4", "Retry can duplicate")]
for i, (num, label) in enumerate(stages):
    y = 343 + i * 90
    d.ellipse((990, y, 1044, y + 54), outline=ORANGE if i > 1 else GREEN, width=3)
    centered(d, 1017, y + 7, num, 29, ORANGE if i > 1 else GREEN, True)
    text(d, 1064, y + 8, label, 28, NAVY, i == 3)
text(d, 987, 710, "Same business key + provider dedup", 27, GREEN, True)
footer(d, SLIDES[6]["takeaway"], SLIDES[6]["source_label"])
save(im, 7)

# 08 · Actual code excerpt with an interpretation panel, not another flowchart.
im, d = slide(8, "THE CLIENT", SLIDES[7]["title"], SLIDES[7]["subtitle"])
box(d, (58, 253, 1038, 779), BLUE, DARK)
text(d, 82, 275, "ExternalStatusService.check()", 32, "#ffffff", mono=True)
d.line((80, 330, 1016, 330), fill="#62708e", width=2)
code = [
    "connection.setConnectTimeout(...);",
    "connection.setReadTimeout(...);",
    "connection.setInstanceFollowRedirects(false);",
    "connection.setRequestMethod(\"GET\");",
    "connection.setRequestProperty(\"X-API-Key\", apiKey);",
    "int status = connection.getResponseCode();",
]
for i, value in enumerate(code):
    text(d, 82, 355 + i * 60, value, 26, "#ffffff", mono=True)
text(d, 83, 730, "finally { ... connection.disconnect(); }", 24, "#c3d0e9", mono=True)
box(d, (1062, 253, 1613, 779), BLUE, WHITE)
text(d, 1089, 279, "WHAT THIS PROVES", 31, BLUE, True)
for i, (head, desc, color) in enumerate((("Bounded waits", "Connect and blocked read.", PURPLE), ("Fixed destination", "Redirects disabled.", GREEN), ("Observed status", "No body validation yet.", ORANGE))):
    y = 374 + i * 130
    d.line((1089, y - 17, 1585, y - 17), fill="#dce3ef", width=2)
    text(d, 1090, y, head, 29, color, True)
    text(d, 1090, y + 43, desc, 25, NAVY)
footer(d, SLIDES[7]["takeaway"], SLIDES[7]["source_label"])
save(im, 8)

# 09 · Environment comparison and ordered investigation.
im, d = slide(9, "CLOUD DIAGNOSIS", SLIDES[8]["title"], SLIDES[8]["subtitle"])
box(d, (58, 259, 788, 494), GREEN, PALE_GREEN)
text(d, 86, 284, "LOCAL AUTHOR SDK", 34, GREEN, True)
text(d, 86, 345, "127.0.0.1:8765 → loopback stub", 29, NAVY, mono=True)
text(d, 86, 408, "A local 200 proves this local path.", 28, NAVY)
box(d, (824, 259, 1612, 494), PURPLE, PALE_PURPLE)
text(d, 851, 284, "AEM CLOUD", 34, PURPLE, True)
text(d, 851, 345, "approved host → external route", 28, NAVY)
text(d, 851, 408, "Loopback points to the Cloud instance.", 27, NAVY)
text(d, 63, 542, "CHECK THE FAILED STAGE IN ORDER", 30, BLUE, True)
checks = [("1", "Config", "URL + secret", PURPLE), ("2", "Network", "DNS + egress", BLUE), ("3", "TLS", "cert + host", ORANGE), ("4", "HTTP / data", "status + fields", GREEN)]
for i, (num, heading, detail, color) in enumerate(checks):
    x = 61 + i * 401
    box(d, (x, 598, x + 370, 770), color, WHITE, 12, 2)
    d.ellipse((x + 22, 620, x + 76, 674), outline=color, width=3)
    centered(d, x + 49, 628, num, 29, color, True)
    text(d, x + 92, 617, heading, 30, color, True)
    text(d, x + 25, 704, detail, 28, NAVY)
footer(d, SLIDES[8]["takeaway"], SLIDES[8]["source_label"])
save(im, 9)

# 10 · Bullet summary of the integration decisions.
im, d = slide(10, "SUMMARY", SLIDES[9]["title"], SLIDES[9]["subtitle"])
bullets = [
    "Choose a supported connector or one narrow OSGi HTTP client.",
    "Keep endpoint and credential on the server; use Cloud secrets.",
    "Bound connect and read waits; measure total time and page impact.",
    "Classify failures; budget retries and deduplicate remote writes.",
    "Verify local and Cloud paths separately, with safe log evidence.",
]
for i, value in enumerate(bullets):
    y = 265 + i * 108
    d.ellipse((77, y + 14, 100, y + 37), fill=BLUE)
    text(d, 127, y, value, 34, NAVY, True)
    if i < 4:
        d.line((127, y + 77, 1602, y + 77), fill="#dbe3ef", width=2)
save(im, 10)

# 11 · Deliberately only the closing words.
im, d = slide(0, "", "")
text(d, 45, 91, "Questions", 113, NAVY, True)
text(d, 50, 247, "Thank you.", 47, BLUE)
d.line((45, 324, 1625, 324), fill=BLUE, width=3)
save(im, 11)

for stale in OUT.glob("slide_*.png"):
    if int(stale.stem.split("_")[-1]) > len(SLIDES):
        stale.unlink()
assert len(list(OUT.glob("slide_*.png"))) == len(SLIDES)
print(f"Rendered {len(SLIDES)} slides in {OUT}")
