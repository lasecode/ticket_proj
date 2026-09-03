"""
Management command to generate images for all events using Pillow and attach them.

Run with: python manage.py generate_images
"""
import os
import math
import random
from PIL import Image, ImageDraw, ImageFont
from django.core.management.base import BaseCommand
from django.conf import settings
from events.models import Event

MEDIA_EVENTS_DIR = settings.MEDIA_ROOT / 'events'


def create_gradient_bg(width, height, color1, color2):
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    for y in range(height):
        for x in range(width):
            p = (x + y) / (width + height)
            mask.putpixel((x, y), int(p * 255))
    base.paste(top, (0, 0), mask)
    return base


def draw_tech_pattern(draw, width, height):
    grid_size = 40
    color = (255, 255, 255, 25)
    for x in range(0, width, grid_size):
        draw.line([(x, 0), (x, height)], fill=color, width=1)
    for y in range(0, height, grid_size):
        draw.line([(0, y), (width, y)], fill=color, width=1)
    random.seed(42)
    for _ in range(35):
        cx = random.randint(1, width // grid_size - 1) * grid_size
        cy = random.randint(1, height // grid_size - 1) * grid_size
        r = random.choice([3, 5, 8])
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(6, 182, 212, 180))


def draw_music_pattern(draw, width, height):
    random.seed(99)
    bars = 30
    bar_w = width // bars
    for i in range(bars):
        h = random.randint(40, height // 2)
        x = i * bar_w + 5
        y = height - h - 50
        draw.rectangle([x, y, x + bar_w - 10, height - 50], fill=(236, 72, 153, 100))
        draw.rectangle([x, y, x + bar_w - 10, y + 10], fill=(250, 204, 21, 200))


def draw_business_pattern(draw, width, height):
    color = (255, 255, 255, 20)
    for i in range(-height, width + height, 60):
        draw.line([(i, 0), (i + height, height)], fill=color, width=2)
    draw.polygon([(width - 300, 0), (width, 0), (width, 300)], fill=(234, 179, 8, 40))


def draw_sports_pattern(draw, width, height):
    for i in range(0, height, 25):
        draw.line([(0, i), (width, i + 100)], fill=(255, 255, 255, 15), width=4)


def draw_entertainment_pattern(draw, width, height):
    cx, cy = width // 2, -100
    for angle in range(0, 180, 15):
        rad = math.radians(angle)
        x2 = cx + math.cos(rad) * width * 1.5
        y2 = cy + math.sin(rad) * height * 2
        draw.polygon([(cx, cy), (x2 - 40, y2), (x2 + 40, y2)], fill=(255, 255, 255, 15))


DEFAULT_DESIGNS = {
    'technology': {
        'c1': (15, 23, 42), 'c2': (30, 27, 75), 'accent': (6, 182, 212),
        'badge': 'TECHNOLOGY EVENT', 'pattern': draw_tech_pattern,
    },
    'concert': {
        'c1': (46, 16, 101), 'c2': (126, 34, 206), 'accent': (236, 72, 153),
        'badge': 'LIVE MUSIC & CONCERT', 'pattern': draw_music_pattern,
    },
    'business': {
        'c1': (15, 23, 42), 'c2': (30, 58, 138), 'accent': (234, 179, 8),
        'badge': 'BUSINESS & SUMMIT', 'pattern': draw_business_pattern,
    },
    'sports': {
        'c1': (6, 78, 59), 'c2': (4, 120, 87), 'accent': (245, 158, 11),
        'badge': 'SPORTS & ATHLETICS', 'pattern': draw_sports_pattern,
    },
    'education': {
        'c1': (49, 46, 129), 'c2': (67, 56, 202), 'accent': (20, 184, 166),
        'badge': 'EDUCATION & MASTERCLASS', 'pattern': draw_tech_pattern,
    },
    'entertainment': {
        'c1': (88, 28, 135), 'c2': (168, 85, 247), 'accent': (250, 204, 21),
        'badge': 'ENTERTAINMENT & SHOW', 'pattern': draw_entertainment_pattern,
    },
}


def generate_event_image(event):
    os.makedirs(MEDIA_EVENTS_DIR, exist_ok=True)
    slug_title = "".join(c if c.isalnum() else "_" for c in event.title.lower())[:30].strip('_')
    filename = f"{slug_title}_{event.id}.png"
    filepath = MEDIA_EVENTS_DIR / filename

    info = DEFAULT_DESIGNS.get(event.category, DEFAULT_DESIGNS['entertainment'])
    w, h = 1200, 675

    img = create_gradient_bg(w, h, info['c1'], info['c2'])

    pattern_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(pattern_img)
    info['pattern'](pdraw, w, h)
    img = Image.alpha_composite(img.convert('RGBA'), pattern_img)

    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    for y in range(h // 3, h):
        alpha = int(((y - h // 3) / (h - h // 3)) ** 1.5 * 220)
        odraw.line([(0, y), (w, y)], fill=(0, 0, 0, alpha))

    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        badge_font = ImageFont.truetype("arialbd.ttf", 20)
        sub_font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        title_font = ImageFont.load_default()
        badge_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    badge_text = info['badge']
    b_padding = (16, 8)
    try:
        bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
    except AttributeError:
        tw, th = 180, 20

    bx, by = 60, 60
    draw.rounded_rectangle(
        [bx, by, bx + tw + b_padding[0] * 2, by + th + b_padding[1] * 2],
        radius=8,
        fill=(info['accent'][0], info['accent'][1], info['accent'][2], 230),
    )
    draw.text((bx + b_padding[0], by + b_padding[1]), badge_text, fill=(0, 0, 0), font=badge_font)

    tx, ty = 60, h - 180
    title_text = event.title if len(event.title) <= 35 else event.title[:32] + "..."
    draw.text((tx, ty), title_text, fill=(255, 255, 255), font=title_font)

    sub_text = f"📍 {event.location}  |  📅 {event.date}"
    draw.text((tx, ty + 70), sub_text, fill=(203, 213, 225), font=sub_font)

    img.convert('RGB').save(filepath, quality=95)
    return f"events/{filename}"


class Command(BaseCommand):
    help = 'Generates custom banner images for all events using Pillow.'

    def handle(self, *args, **options):
        events = Event.objects.all()
        count = 0
        for event in events:
            rel_path = generate_event_image(event)
            event.image = rel_path
            event.save(update_fields=['image'])
            count += 1
            self.stdout.write(self.style.SUCCESS(f'Updated image for: {event.title} -> {rel_path}'))

        self.stdout.write(self.style.SUCCESS(f'\n[OK] Successfully generated and attached images to {count} event(s)!'))
