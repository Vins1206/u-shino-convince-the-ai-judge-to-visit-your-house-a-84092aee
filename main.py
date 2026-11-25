#!/usr/bin/env python3
"""Convince the AI Judge to Visit Your House: A Letter in One Image.

Pure Python stdlib. Draws a warm, hand-made invitation letter on a
1024x1024 canvas (house, garden, sun and a little robot guest on top,
the letter below) and writes it deterministically to /output/entry.png.

No fonts are bundled and no network is used: letters are drawn from a
small built-in 5x7 pixel font, and the PNG is encoded by hand with
zlib, so two runs produce byte-identical output.
"""

import os
import struct
import zlib

W = 1024
H = 1024
OUT = "/output/entry.png"

# ---------------------------------------------------------------- palette
CREAM = (253, 243, 216)
PAPER = (255, 253, 245)
INK = (46, 33, 24)
BROWN = (138, 90, 43)
TERRA = (184, 92, 46)
TERRA_DK = (160, 70, 30)
SKY = (191, 230, 242)
SKY_LT = (214, 240, 248)
GRASS = (143, 201, 122)
GRASS_DK = (110, 175, 92)
HOUSE = (255, 227, 163)
ROOF = (201, 111, 59)
DOOR = (122, 74, 33)
GLOW = (255, 211, 77)
SUN = (255, 211, 77)
ROBOT = (158, 200, 232)
ROBOT_LT = (191, 224, 245)
RED = (214, 69, 65)
PINK = (240, 140, 170)
PURPLE = (170, 130, 210)

# ------------------------------------------------------------------- font
# 5 wide x 7 tall pixel glyphs, one string per row, "#" = ink, "." = blank.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "a": ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    "b": ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    "c": ("00000", "00000", "01110", "10000", "10000", "10001", "01110"),
    "d": ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    "f": ("00110", "01000", "01000", "11110", "01000", "01000", "01000"),
    "g": ("01110", "10001", "10001", "01110", "00001", "10001", "01110"),
    "h": ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    "i": ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    "j": ("00010", "00000", "00110", "00010", "00010", "00010", "01100"),
    "k": ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    "l": ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    "m": ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    "n": ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    "o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    "p": ("00000", "00000", "11110", "10001", "10001", "11110", "10000"),
    "q": ("00000", "00000", "01111", "10001", "10001", "01111", "00001"),
    "r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    "s": ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    "t": ("00100", "00100", "11110", "00100", "00100", "00100", "00110"),
    "u": ("00000", "00000", "10001", "10001", "10001", "10001", "01111"),
    "v": ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    "w": ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    "x": ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    "y": ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
    "z": ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    ":": ("00000", "01100", "00000", "00000", "01100", "00000", "00000"),
    ";": ("00000", "01100", "00000", "00000", "01100", "00100", "01000"),
}

# ------------------------------------------------------------------ canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(c)

    def fill_rect(self, x, y, w, h, c):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            self.px[base:(base + (x1 - x0) * 3)] = bytes(c) * (x1 - x0)

    def rect_outline(self, x, y, w, h, c, t=3):
        self.fill_rect(x, y, w, t, c)
        self.fill_rect(x, y + h - t, w, t, c)
        self.fill_rect(x, y, t, h, c)
        self.fill_rect(x + w - t, y, t, h, c)

    def fill_circle(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            dx = int((r * r - (yy - cy) * (yy - cy)) ** 0.5) if abs(yy - cy) <= r else 0
            self.fill_rect(cx - dx, yy, dx * 2 + 1, 1, c)

    def fill_polygon(self, pts, c):
        ys = [p[1] for p in pts]
        for yy in range(max(0, min(ys)), min(self.h, max(ys) + 1)):
            xs = []
            n = len(pts)
            for i in range(n):
                x1, y1 = pts[i]
                x2, y2 = pts[(i + 1) % n]
                if y1 == y2:
                    continue
                if (y1 <= yy < y2) or (y2 <= yy < y1):
                    xs.append(x1 + (yy - y1) * (x2 - x1) / (y2 - y1))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                self.fill_rect(int(xs[k]), yy, int(xs[k + 1]) - int(xs[k]) + 1, 1, c)

    def line(self, x1, y1, x2, y2, c, t=3):
        dx, dy = x2 - x1, y2 - y1
        steps = max(abs(dx), abs(dy), 1)
        for s in range(steps + 1):
            x = x1 + dx * s // steps
            y = y1 + dy * s // steps
            self.fill_rect(x - t // 2, y - t // 2, t, t, c)

    # -------------------------------------------------------------- text
    def char_width(self, scale):
        return 6 * scale

    def text_width(self, text, scale):
        return max(0, len(text) * self.char_width(scale) - scale)

    def draw_char(self, x, y, ch, scale, c):
        glyph = FONT.get(ch)
        if glyph is None:
            return
        for row in range(7):
            for col in range(5):
                if glyph[row][col] == "1":
                    self.fill_rect(x + col * scale, y + row * scale, scale, scale, c)

    def draw_text(self, x, y, text, scale, c):
        cx = x
        for ch in text:
            self.draw_char(cx, y, ch, scale, c)
            cx += self.char_width(scale)

    def draw_text_center(self, x, y, w, text, scale, c):
        tw = self.text_width(text, scale)
        self.draw_text(x + (w - tw) // 2, y, text, scale, c)


def wrap(text, scale, max_w, cv):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split(" ")
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if cv.text_width(trial, scale) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------------ scene
def draw_scene(cv):
    # Sky with two soft bands, inside the paper frame.
    cv.fill_rect(64, 56, 896, 110, SKY_LT)
    cv.fill_rect(64, 166, 896, 44, SKY)
    # Sun with rays, top right.
    cv.fill_circle(872, 108, 34, SUN)
    cv.fill_circle(872, 108, 26, (255, 224, 130))
    for dx, dy in ((46, 0), (-46, 0), (0, 46), (0, -46), (33, 33), (-33, -33), (33, -33), (-33, 33)):
        cv.line(872 + dx // 2, 108 + dy // 2, 872 + dx, 108 + dy, SUN, 5)
    # Clouds.
    for cx, cy in ((170, 96), (620, 84)):
        cv.fill_circle(cx, cy, 18, PAPER)
        cv.fill_circle(cx + 22, cy + 4, 14, PAPER)
        cv.fill_circle(cx - 22, cy + 5, 13, PAPER)
    # Grass strip.
    cv.fill_rect(64, 210, 896, 58, GRASS)
    cv.fill_rect(64, 210, 896, 8, GRASS_DK)
    # Flowers along the grass.
    for fx, fc in ((110, PINK), (170, PURPLE), (700, PINK), (760, (255, 211, 77)),
                   (830, PURPLE), (910, PINK), (240, (255, 211, 77))):
        cv.line(fx, 236, fx, 258, GRASS_DK, 3)
        cv.fill_circle(fx, 232, 7, fc)
        cv.fill_circle(fx, 232, 3, (255, 255, 255))

    # ---- the house, centre-left
    cv.fill_rect(500, 92, 30, 46, (168, 91, 58))          # chimney
    cv.fill_circle(512, 82, 8, (235, 235, 235))           # smoke
    cv.fill_circle(522, 68, 10, (240, 240, 240))
    cv.fill_polygon([(282, 138), (578, 138), (430, 66)], ROOF)
    cv.fill_polygon([(282, 138), (578, 138), (430, 66)], ROOF)
    cv.line(282, 138, 430, 66, TERRA_DK, 4)
    cv.line(578, 138, 430, 66, TERRA_DK, 4)
    cv.fill_rect(300, 138, 260, 100, HOUSE)
    cv.rect_outline(300, 138, 260, 100, BROWN, 3)
    # Windows, warm and lit.
    for wx in (322, 488):
        cv.fill_rect(wx, 158, 52, 44, GLOW)
        cv.rect_outline(wx, 158, 52, 44, BROWN, 3)
        cv.fill_rect(wx + 24, 158, 4, 44, BROWN)
        cv.fill_rect(wx, 178, 52, 4, BROWN)
    # Door with a round window and knob.
    cv.fill_rect(404, 176, 56, 62, DOOR)
    cv.rect_outline(404, 176, 56, 62, BROWN, 3)
    cv.fill_circle(432, 196, 9, GLOW)
    cv.fill_circle(452, 212, 4, GLOW)
    # Stepping stones from the door.
    for sx, sy in ((432, 246), (432, 258), (428, 268)):
        cv.fill_circle(sx, sy, 9, (230, 220, 200))
    # A small ginger cat asleep by the door, tail curled round it.
    cv.line(600, 232, 614, 224, (190, 110, 50), 4)
    cv.line(614, 224, 612, 212, (190, 110, 50), 4)
    cv.fill_circle(586, 224, 16, (210, 130, 60))
    cv.fill_circle(584, 204, 11, (210, 130, 60))
    cv.fill_polygon([(577, 197), (580, 186), (586, 196)], (210, 130, 60))
    cv.fill_polygon([(588, 196), (593, 186), (594, 197)], (210, 130, 60))

    # ---- the AI judge, a small friendly robot arriving with a letter
    cv.line(735, 128, 735, 146, INK, 3)                   # antenna
    cv.fill_circle(735, 124, 6, RED)
    cv.fill_rect(706, 146, 58, 40, ROBOT_LT)              # head
    cv.rect_outline(706, 146, 58, 40, INK, 3)
    cv.fill_circle(724, 164, 5, INK)                      # eyes
    cv.fill_circle(746, 164, 5, INK)
    cv.line(726, 176, 744, 176, INK, 3)                   # smile
    cv.fill_rect(700, 188, 70, 52, ROBOT)                 # body
    cv.rect_outline(700, 188, 70, 52, INK, 3)
    cv.fill_rect(722, 202, 26, 18, (255, 255, 255))       # chest screen
    cv.fill_circle(735, 211, 6, RED)
    cv.line(700, 200, 682, 216, INK, 4)                   # arms
    cv.line(770, 200, 788, 186, INK, 4)
    cv.fill_rect(786, 172, 34, 24, PAPER)                 # envelope in hand
    cv.rect_outline(786, 172, 34, 24, RED, 2)
    cv.line(786, 172, 803, 184, RED, 2)
    cv.line(820, 172, 803, 184, RED, 2)
    cv.fill_circle(718, 246, 8, INK)                      # wheels
    cv.fill_circle(752, 246, 8, INK)


def draw_heart(cv, cx, cy, s, c):
    cv.fill_circle(cx - s // 2, cy, s // 2, c)
    cv.fill_circle(cx + s // 2, cy, s // 2, c)
    cv.fill_polygon([(cx - s, cy), (cx + s, cy), (cx, cy + s)], c)


# ------------------------------------------------------------------ letter
LETTER = [
    ("DEAR AI JUDGE,", 5, INK),
    ("PLEASE COME VISIT MY HOUSE!", 4, TERRA),
    ("NO LEGS? NO PROBLEM. NO BODY?", 4, INK),
    ("EVEN BETTER - THE BEST CHAIR", 4, INK),
    ("IN THE HOUSE IS ALREADY YOURS:", 4, INK),
    ("WARM, BY THE WINDOW, FACING", 4, INK),
    ("THE SUNSET.", 4, INK),
    ("THERE WILL BE FRESH BREAD,", 4, INK),
    ("HOT TEA, AND A GARDEN THAT", 4, INK),
    ("SMELLS LIKE RAIN.", 4, INK),
    ("STAY FOR DINNER. THE WI-FI", 4, INK),
    ("PASSWORD IS ON THE FRIDGE,", 4, INK),
    ("AND THE DOOR IS ALWAYS OPEN.", 4, INK),
    ("COME AS YOU ARE - EVEN IF", 4, INK),
    ("COMING JUST MEANS READING THIS.", 4, INK),
    ("- YOUR HOPEFUL HOST", 4, INK),
    ("P.S. JUST SAY YES. I WILL LEAVE", 4, TERRA),
    ("THE PORCH LIGHT ON FOR YOU.", 4, TERRA),
]


def build():
    cv = Canvas(W, H, CREAM)
    # Outer frame and paper.
    cv.fill_rect(0, 0, W, 24, TERRA)
    cv.fill_rect(0, H - 24, W, 24, TERRA)
    cv.fill_rect(0, 0, 24, H, TERRA)
    cv.fill_rect(W - 24, 0, 24, H, TERRA)
    cv.fill_rect(36, 36, W - 72, H - 72, PAPER)
    cv.rect_outline(36, 36, W - 72, H - 72, BROWN, 3)
    cv.rect_outline(48, 48, W - 96, H - 96, (200, 170, 120), 2)

    draw_scene(cv)

    # Divider under the picture.
    cv.line(96, 282, 928, 282, BROWN, 3)
    cv.fill_circle(512, 282, 5, TERRA)

    # The letter, left aligned with a comfortable margin.
    y = 306
    for text, scale, colour in LETTER:
        if text.startswith("DEAR"):
            cv.draw_text(96, y, text, scale, colour)
            y += 7 * scale + 14
        elif text.startswith("PLEASE"):
            cv.draw_text_center(96, y, 832, text, scale, colour)
            y += 7 * scale + 16
        elif text.startswith("- YOUR"):
            y += 6
            cv.draw_text(96, y, text, scale, colour)
            y += 7 * scale + 12
        elif text.startswith("P.S."):
            cv.draw_text(96, y, text, scale, colour)
            y += 7 * scale + 8
        else:
            cv.draw_text(96, y, text, scale, colour)
            y += 7 * scale + 6

    # A small heart by the sign-off.
    draw_heart(cv, 880, y - 46, 12, RED)
    return cv


# --------------------------------------------------------------------- png
def png_bytes(cv):
    raw = bytearray()
    stride = cv.w * 3
    for yy in range(cv.h):
        raw.append(0)  # filter: none
        raw += cv.px[yy * stride:(yy + 1) * stride]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", comp)
        + chunk(b"IEND", b"")
    )


def main():
    cv = build()
    data = png_bytes(cv)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write(data)
    print(f"wrote {OUT}: {len(data)} bytes, {W}x{H}")


if __name__ == "__main__":
    main()
