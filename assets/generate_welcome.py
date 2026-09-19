import os
from PIL import Image, ImageDraw, ImageFont

# Settings
WIDTH = 1200
HEIGHT = 400
FPS = 15
DURATION_SEC = 4.0
TOTAL_FRAMES = int(FPS * DURATION_SEC)

BG_COLOR = (13, 17, 23)  # GitHub dark #0d1117
GRID_COLOR = (33, 38, 45) # Subtle grid
LINE_COLOR = (48, 54, 61)
ACCENT_COLOR = (88, 166, 255) # GitHub accent blue #58a6ff
TEXT_COLOR = (201, 209, 217)  # #c9d1d9
SUBTEXT_COLOR = (139, 148, 158) # #8b949e

def ease_out(t):
    return 1 - (1 - t) ** 3

frames = []

# Try to load a nice font, fallback to default
try:
    font_large = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 54)
    font_medium = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 28)
    font_small = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 16)
except IOError:
    font_large = ImageFont.load_default(size=54)
    font_medium = ImageFont.load_default(size=28)
    font_small = ImageFont.load_default(size=16)

def draw_text_alpha(draw, pos, text, font, base_color, alpha):
    if alpha <= 0: return
    # Basic alpha blending over BG_COLOR manually
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
    
    # 0.0–0.6 sec: Grid appears
    grid_prog = get_progress(i, 0.0, 0.6)
    if grid_prog > 0:
        # Subtle horizontal/vertical construction lines
        # Let's draw 3 vertical, 2 horizontal lines
        vl_x = [150, 600, 1050]
        hl_y = [100, 300]
        
        # Color interpolation for grid
        gr = int((GRID_COLOR[0] * grid_prog) + (BG_COLOR[0] * (1-grid_prog)))
        gg = int((GRID_COLOR[1] * grid_prog) + (BG_COLOR[1] * (1-grid_prog)))
        gb = int((GRID_COLOR[2] * grid_prog) + (BG_COLOR[2] * (1-grid_prog)))
        
        for x in vl_x:
            draw.line([(x, 0), (x, HEIGHT)], fill=(gr, gg, gb), width=1)
        for y in hl_y:
            draw.line([(0, y), (WIDTH, y)], fill=(gr, gg, gb), width=1)
            
    # 0.6–1.5 sec: Horizontal rule
    rule_prog = get_progress(i, 0.6, 1.5)
    if rule_prog > 0:
        # Draw from left 150 to right 1050
        start_x = 150
        max_len = 900
        current_len = max_len * rule_prog
        draw.line([(start_x, 150), (start_x + current_len, 150)], fill=LINE_COLOR, width=2)
        
        # Add a tiny accent box at the start of the line
        draw.rectangle([start_x, 149, start_x+4, 152], fill=ACCENT_COLOR)

    # 1.2–2.2 sec: YASHRAJ KUYATE
    t1_prog = get_progress(i, 1.2, 2.2)
    # Slide up slightly and fade in
    y_offset1 = int(20 * (1 - t1_prog))
    draw_text_alpha(draw, (150, 170 + y_offset1), "YASHRAJ KUYATE", font_large, TEXT_COLOR, t1_prog)

    # 2.0–2.8 sec: AI & DATA SCIENCE ENGINEER
    t2_prog = get_progress(i, 2.0, 2.8)
    y_offset2 = int(15 * (1 - t2_prog))
    draw_text_alpha(draw, (150, 240 + y_offset2), "AI & DATA SCIENCE ENGINEER", font_medium, TEXT_COLOR, t2_prog)
    
    # 2.6–3.4 sec: APPLIED AI · SECURITY · SYSTEMS
    t3_prog = get_progress(i, 2.6, 3.4)
    y_offset3 = int(10 * (1 - t3_prog))
    draw_text_alpha(draw, (150, 280 + y_offset3), "APPLIED AI  ·  SECURITY  ·  SYSTEMS", font_small, SUBTEXT_COLOR, t3_prog)

    frames.append(img)

gif_path = "/Users/yashrajdnyaneshwarkuyate/Github/Yashraj2050/assets/welcome.gif"
frames[0].save(gif_path, save_all=True, append_images=frames[1:], optimize=False, duration=int(1000/FPS), loop=0)

import os
size_mb = os.path.getsize(gif_path) / (1024 * 1024)
print(f"Generated {gif_path}")
print(f"Dimensions: {WIDTH}x{HEIGHT}")
print(f"Frames: {TOTAL_FRAMES}")
print(f"Duration: {DURATION_SEC} sec")
print(f"Size: {size_mb:.2f} MB")
