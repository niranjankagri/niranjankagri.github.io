"""Regenerate checked-in 1200×630 sharing cards (requires Pillow and DejaVu Sans)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from project_data import PROJECTS

ROOT = Path(__file__).resolve().parent.parent
FONT = Path('/usr/share/fonts/truetype/dejavu')
OUTPUT = ROOT / 'img' / 'social'
OUTPUT.mkdir(parents=True, exist_ok=True)


def card(slug, title, subtitle):
    image = Image.new('RGB', (1200, 630), '#f5f7fb')
    draw = ImageDraw.Draw(image)
    def regular(size):
        return ImageFont.truetype(str(FONT / 'DejaVuSans.ttf'), size)
    def bold(size):
        return ImageFont.truetype(str(FONT / 'DejaVuSans-Bold.ttf'), size)
    for x in range(0, 1200, 48):
        for y in range(0, 630, 48):
            draw.ellipse((x, y, x+2, y+2), fill='#dce2ed')
    draw.rounded_rectangle((56, 48, 1144, 582), radius=28, fill='white', outline='#dce2ed', width=2)
    draw.rounded_rectangle((92, 84, 156, 148), radius=15, fill='#08665e')
    draw.text((102, 100), 'NA', font=bold(26), fill='white')
    draw.text((180, 90), 'NIRANJAN KUMAR AGRI', font=bold(23), fill='#171717')
    draw.text((180, 124), 'QUALITY ENGINEERING', font=regular(16), fill='#526176')
    title_font = bold(48)
    lines = ['']
    for word in title.split():
        candidate = (lines[-1] + ' ' + word).strip()
        if draw.textlength(candidate, font=title_font) > 1000:
            lines.append(word)
        else:
            lines[-1] = candidate
    if len(lines) > 3:
        raise ValueError(f'Sharing title is too long: {title}')
    y = 206
    for line in lines:
        if draw.textlength(line, font=title_font) > 1010:
            raise ValueError(f'Sharing title line overflows: {line}')
        draw.text((92, y), line, font=title_font, fill='#171717')
        y += 65
    draw.text((92, 444), subtitle, font=regular(22), fill='#526176')
    draw.line((92, 500, 1108, 500), fill='#dce2ed', width=2)
    draw.text((92, 526), 'niranjankagri.github.io', font=bold(20), fill='#315cd5')
    draw.text((810, 528), 'Explore the evidence →', font=regular(19), fill='#526176')
    image.save(OUTPUT / (slug + '.jpg'), quality=90, optimize=True)


card('portfolio', 'Reliable releases start with clear evidence.', 'Technical Lead QA  /  Senior SDET  /  Automation Architect')
for project in PROJECTS:
    card(project['page'], project['title'], 'Engineering case study · decisions, results and dated evidence')
print(f'Generated {len(PROJECTS) + 1} sharing cards.')
