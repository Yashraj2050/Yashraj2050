import os
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1200
HEIGHT = 400
FPS = 15
DURATION_SEC = 4.0
TOTAL_FRAMES = int(FPS * DURATION_SEC)

BG_COLOR = (13, 17, 23)
GRID_COLOR = (33, 38, 45)
LINE_COLOR = (48, 54, 61)
ACCENT_COLOR = (88, 166, 255)
TEXT_COLOR = (201, 209, 217)
SUBTEXT_COLOR = (139, 148, 158)
MUTED_COLOR = (72, 79, 88)

def ease_out(t):
    return 1 - (1 - t) ** 3

frames = []

try:
    font_xl = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 60)
    font_large = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 26)
    font_medium = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 16)
    font_small = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
except IOError:
    font_xl = ImageFont.load_default(size=60)
    font_large = ImageFont.load_default(size=26)
    font_medium = ImageFont.load_default(size=16)
    font_small = ImageFont.load_default(size=13)

def draw_text_alpha(draw, pos, text, font, base_color, alpha):
    if alpha <= 0: return
    a = alpha
    r = int((base_color[0] * a) + (BG_COLOR[0] * (1-a)))
    g = int((base_color[1] * a) + (BG_COLOR[1] * (1-a)))
    b = int((base_color[2] * a) + (BG_COLOR[2] * (1-a)))
    draw.text(pos, text, font=font, fill=(r,g,b))

def get_progress(f_idx, start_sec, end_sec):
    start_f = start_sec * FPS
    end_f = end_sec * FPS
    if f_idx < start_f: return 0.0
    if f_idx > end_f: return 1.0
    return ease_out((f_idx - start_f) / (end_f - start_f))

for i in range(TOTAL_FRAMES):
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 0.0-0.5 Grid
    grid_prog = get_progress(i, 0.0, 0.5)
    if grid_prog > 0:
        gr = int((GRID_COLOR[0] * grid_prog) + (BG_COLOR[0] * (1-grid_prog)))
        gg = int((GRID_COLOR[1] * grid_prog) + (BG_COLOR[1] * (1-grid_prog)))
        gb = int((GRID_COLOR[2] * grid_prog) + (BG_COLOR[2] * (1-grid_prog)))
        # Draw some editorial construction lines
        draw.line([(100, 0), (100, HEIGHT)], fill=(gr,gg,gb), width=1)
        draw.line([(1100, 0), (1100, HEIGHT)], fill=(gr,gg,gb), width=1)
        draw.line([(0, 360), (WIDTH, 360)], fill=(gr,gg,gb), width=1)

    # 0.4-1.0 Top-left / Top-right labels
    top_prog = get_progress(i, 0.4, 1.0)
    draw_text_alpha(draw, (100, 40), "YK / 001", font_small, SUBTEXT_COLOR, top_prog)
    draw_text_alpha(draw, (1060, 40), "2026", font_small, SUBTEXT_COLOR, top_prog)

    # 0.8-1.6 Horizontal rule
    rule_prog = get_progress(i, 0.8, 1.6)
    if rule_prog > 0:
        start_x = 100
        max_len = 1000
        current_len = max_len * rule_prog
        y_pos = 230
        draw.line([(start_x, y_pos), (start_x + current_len, y_pos)], fill=LINE_COLOR, width=1)
        draw.rectangle([start_x, y_pos-1, start_x+4, y_pos+1], fill=ACCENT_COLOR)

    # 1.2-2.0 YASHRAJ KUYATE
    name_prog = get_progress(i, 1.2, 2.0)
    y_name = int(15 * (1 - name_prog))
    draw_text_alpha(draw, (100, 110 + y_name), "YASHRAJ KUYATE", font_xl, TEXT_COLOR, name_prog)

    # 1.7-2.5 AI & DATA SCIENCE ENGINEER
    title_prog = get_progress(i, 1.7, 2.5)
    y_title = int(10 * (1 - title_prog))
    draw_text_alpha(draw, (100, 185 + y_title), "AI & DATA SCIENCE ENGINEER", font_large, SUBTEXT_COLOR, title_prog)

    # 2.3-3.1 Focus labels
    focus_prog = get_progress(i, 2.3, 3.1)
    y_focus = int(5 * (1 - focus_prog))
    draw_text_alpha(draw, (100, 250 + y_focus), "APPLIED AI     SECURITY     SYSTEMS     DATA", font_medium, TEXT_COLOR, focus_prog)

    # 3.0-3.6 Bottom metadata (Projects)
    proj_prog = get_progress(i, 3.0, 3.6)
    y_proj = int(5 * (1 - proj_prog))
    draw_text_alpha(draw, (100, 370 + y_proj), "FIDUSCAN     TRACE     CYBERSCOPE     SONIC RIDE", font_small, MUTED_COLOR, proj_prog)

    frames.append(img)

gif_path = "/Users/yashrajdnyaneshwarkuyate/Github/Yashraj2050/assets/welcome.gif"
frames[0].save(gif_path, save_all=True, append_images=frames[1:], optimize=False, duration=int(1000/FPS), loop=0)

size_mb = os.path.getsize(gif_path) / (1024 * 1024)
print(f"Generated {gif_path}")
print(f"Dimensions: {WIDTH}x{HEIGHT}")
print(f"Frames: {TOTAL_FRAMES}")
print(f"Duration: {DURATION_SEC} sec")
print(f"Size: {size_mb:.2f} MB")
