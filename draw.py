"""The World Today -- front page for Friday 20 November 2026.

Draws a newspaper front-page infographic (1024x1024 PNG) summing up the
day's verified world news. No network, no external images, no randomness:
running it twice produces byte-identical output.

Usage:  python3 draw.py
Output: $MAKEFUN_OUTPUT_DIR/entry.png (default: ./out/entry.png)
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
CONTENT = W - 2 * MARGIN

PAPER = (246, 241, 227)
INK = (22, 20, 17)
RED = (158, 27, 30)
GREY = (107, 102, 90)
BLUE = (31, 58, 95)
LIGHT_RULE = (190, 183, 166)
DARK_BAND = (28, 26, 22)
BAND_TEXT = (246, 241, 227)

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
]


def load_font(names, size):
    """Try each candidate font file, fall back to PIL's default font."""
    for directory in FONT_DIRS:
        for name in names:
            path = os.path.join(directory, name)
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except OSError:
                    continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


SERIF_BOLD = lambda s: load_font(["DejaVuSerif-Bold.ttf",
                                  "LiberationSerif-Bold.ttf"], s)
SERIF = lambda s: load_font(["DejaVuSerif.ttf",
                             "LiberationSerif-Regular.ttf"], s)
SANS_BOLD = lambda s: load_font(["DejaVuSans-Bold.ttf",
                                 "LiberationSans-Bold.ttf"], s)
SANS = lambda s: load_font(["DejaVuSans.ttf",
                            "LiberationSans-Regular.ttf"], s)


def wrap(text, font, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if font.getlength(trial) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, text, font, x, y, width, fill=INK, leading=1.25):
    """Draw wrapped text; return the y just below the last line."""
    for line in wrap(text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += int(font.size * leading)
    return y


def hline(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, text, x, y, color=RED):
    draw.text((x, y), text, font=SANS_BOLD(15), fill=color)
    return y + 22


def headline(draw, text, font, x, y, width, leading=1.08):
    return draw_wrapped(draw, text, font, x, y, width, leading=leading)


def story(draw, x, y, width, kick, head, body, head_size=25,
          body_size=17, kick_color=RED):
    """One column story: kicker, headline, body. Returns bottom y."""
    y = kicker(draw, kick, x, y, color=kick_color)
    y = headline(draw, head, SERIF_BOLD(head_size), x, y, width)
    y += 6
    y = draw_wrapped(draw, body, SANS(body_size), x, y, width, leading=1.3)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    left = MARGIN
    right = W - MARGIN

    # ---------- masthead ----------
    title = "THE WORLD TODAY"
    tf = SERIF_BOLD(56)
    tw = tf.getlength(title)
    d.text(((W - tw) / 2, 24), title, font=tf, fill=INK)
    hline(d, left, right, 98, width=3)
    hline(d, left, right, 103, width=1)

    date_font = SANS_BOLD(17)
    d.text((left, 114), "FRIDAY, 20 NOVEMBER 2026", font=date_font, fill=INK)
    tag = "ONE IMAGE  ·  THE WHOLE DAY"
    d.text((right - date_font.getlength(tag), 114), tag, font=date_font,
           fill=GREY)
    hline(d, left, right, 144, width=2)

    # ---------- lead story: ICJ ----------
    y = 160
    y = kicker(d, "THE HAGUE  ·  JUSTICE", left, y)
    y = headline(d, "World court: Myanmar committed genocide",
                 SERIF_BOLD(40), left, y, CONTENT)
    y += 8
    y = draw_wrapped(
        d,
        "The International Court of Justice ruled that Myanmar's security "
        "forces committed genocide against the Rohingya minority \u2014 the "
        "first such finding against a state by the world court. The 9\u20136 "
        "decision cited mass killings and widespread sexual violence in "
        "northern Rakhine State.",
        SANS(18), left, y, CONTENT, leading=1.32)
    hline(d, left, right, y + 12, width=2)

    # ---------- row 1: two stories ----------
    y = y + 22
    col_w = (CONTENT - 28) // 2
    y1 = story(
        d, left, y, col_w,
        "SHENZHEN  ·  SUMMIT",
        "Trump, Xi and Putin meet; joint declaration, no breakthrough",
        "The leaders of the US, China and Russia held their first three-way "
        "summit in Shenzhen and signed a four-point joint declaration after "
        "about 70 minutes of talks \u2014 with no breakthrough on Ukraine, "
        "Iran or nuclear-arms limits.",
        body_size=16)
    y2 = story(
        d, left + col_w + 28, y, col_w,
        "KYIV  ·  WAR",
        "Russia hits Kyiv bridges overnight; eight killed",
        "Russian missiles and drones struck bridges in Kyiv overnight, "
        "killing eight people and injuring 28 across nine regions. Two "
        "missiles and a drone strayed into Polish airspace during the "
        "attack.",
        kick_color=BLUE, body_size=16)
    row_bottom = max(y1, y2)
    d.line([(left + col_w + 14, y), (left + col_w + 14, row_bottom)],
           fill=LIGHT_RULE, width=1)
    hline(d, left, right, row_bottom + 12, width=2)

    # ---------- row 2: three stories ----------
    y = row_bottom + 24
    col3 = (CONTENT - 2 * 24) // 3
    x2 = left + col3 + 24
    x3 = x2 + col3 + 24
    b1 = story(
        d, left, y, col3,
        "NEW YORK  ·  MARKETS",
        "Anthropic soars on debut as stocks slide",
        "Anthropic closed about 17% above its $83 IPO price on its Nasdaq "
        "debut. The S&P 500 fell about 2%, its fifth straight loss.",
        head_size=21, body_size=16)
    b2 = story(
        d, x2, y, col3,
        "RIYADH  ·  CONFLICT",
        "Houthi missile damages Riyadh's tallest tower",
        "A Houthi missile struck Riyadh's financial district, damaging the "
        "Saudi sovereign wealth fund tower and nearby buildings.",
        head_size=21, body_size=16, kick_color=BLUE)
    b3 = story(
        d, x3, y, col3,
        "WASHINGTON  ·  POLITICS",
        "Senate passes energy bill, 62\u201333",
        "The Senate passed a bipartisan bill overhauling federal permitting "
        "rules to speed up power plants, pipelines and data centres.",
        head_size=21, body_size=16)
    row2_bottom = max(b1, b2, b3)
    for xv in (left + col3 + 12, x2 + col3 + 12):
        d.line([(xv, y), (xv, row2_bottom)], fill=LIGHT_RULE, width=1)
    hline(d, left, right, row2_bottom + 12, width=2)

    # ---------- also today ----------
    y = row2_bottom + 22
    y = kicker(d, "ALSO TODAY", left, y)
    items = [
        ("KENYA", "Last Ebola patient discharged; 42-day countdown to an "
         "Ebola-free declaration begins."),
        ("INDIA", "Cyclone Akvan makes landfall in Odisha."),
        ("BRUSSELS", "EU pays Ukraine nearly \u20ac8bn \u2014 its largest "
         "Ukraine Facility payment yet."),
        ("GLOBAL", "IMF warns public debt nears 100% of world GDP; "
         "GTA 6 launch tops $2.3bn in sales."),
    ]
    half = (CONTENT - 28) // 2
    tag_font = SANS_BOLD(15)
    body_font = SANS(15)
    line_h = int(15 * 1.28)
    for pair in range(0, len(items), 2):
        pair_lines = 0
        for i in range(pair, min(pair + 2, len(items))):
            tag_text, text = items[i]
            xx = left if i % 2 == 0 else left + half + 28
            label = "\u25aa  " + tag_text + " \u2014 "
            lw = tag_font.getlength(label)
            d.text((xx, y), label, font=tag_font, fill=RED)
            lines = wrap(text, body_font, half - lw)
            for j, line in enumerate(lines):
                d.text((xx + lw, y + j * line_h), line, font=body_font,
                       fill=INK)
            pair_lines = max(pair_lines, len(lines))
        y += pair_lines * line_h + 8
    hline(d, left, right, y + 4, width=2)

    # ---------- markets band ----------
    y += 16
    band_h = 40
    d.rectangle([left, y, right, y + band_h], fill=DARK_BAND)
    band = ("MARKETS   S&P 500 \u22122.0%  ·  Nikkei \u22124.8%  ·  "
            "Anthropic +17%  ·  SoftBank \u221216%")
    bf = SANS_BOLD(17)
    d.text((left + 14, y + 10), band, font=bf, fill=BAND_TEXT)
    y += band_h + 12

    # ---------- footer ----------
    foot = ("Sources: Just Security (Early Edition, 20 Nov) · One Turn · "
            "Augerton Digest · Bangladesh Chronicle · h.ua")
    ff = SANS(13)
    d.text((left, y), foot, font=ff, fill=GREY)
    y += 19
    d.text((left, y), "All stories happened or were first reported on "
           "20 November 2026.", font=ff, fill=GREY)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "out")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, "PNG")
    print("wrote", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
