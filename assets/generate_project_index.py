import os
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1200
HEIGHT = 220
FPS = 15
DURATION_SEC = 4.0
TOTAL_FRAMES = int(FPS * DURATION_SEC)

BG_COLOR = (13, 17, 23)
GRID_COLOR = (33, 38, 45)
LINE_COLOR = (48, 54, 61)
TEXT_COLOR = (201, 209, 217)
MUTED_COLOR = (72, 79, 88)

def ease_out(t):
    return 1 - (1 - t) ** 3

frames = []

try:
    font_large = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 20)
    font_small = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
except IOError:
    font_large = ImageFont.load_default(size=20)
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
    
    # Grid / Construction lines
    draw.line([(100, 0), (100, HEIGHT)], fill=GRID_COLOR, width=1)
    
    # 4 rows
    projects = [
        ("01 / FIDUSCAN", 0.0, 0.8),
        ("02 / TRACE", 0.8, 1.6),
        ("03 / CYBERSCOPE", 1.6, 2.4),
        ("04 / SONIC RIDE", 2.4, 3.2)
    ]
    
    for idx, (text, start_sec, end_sec) in enumerate(projects):
        prog = get_progress(i, start_sec, end_sec)
        y_base = 40 + (idx * 40)
        
        # Slide effect
        y_offset = int(10 * (1 - prog))
        
        # Alpha blending
        draw_text_alpha(draw, (130, y_base + y_offset), text, font_large, TEXT_COLOR, prog)

    frames.append(img)

gif_path = "/Users/yashrajdnyaneshwarkuyate/Github/Yashraj2050/assets/project-index.gif"
frames[0].save(gif_path, save_all=True, append_images=frames[1:], optimize=False, duration=int(1000/FPS), loop=0)

size_mb = os.path.getsize(gif_path) / (1024 * 1024)
print(f"Generated {gif_path}")
print(f"Dimensions: {WIDTH}x{HEIGHT}")
print(f"Frames: {TOTAL_FRAMES}")
print(f"Duration: {DURATION_SEC} sec")
print(f"Size: {size_mb:.2f} MB")
