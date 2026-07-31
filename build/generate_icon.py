"""Generate app icon using Pillow"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(output_path="gui/assets/icon.png"):
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background circle with gradient effect
    for i in range(size//2, 0, -1):
        ratio = i / (size//2)
        r = int(15 + (100-15) * ratio)
        g = int(15 + (200-15) * ratio)
        b = int(35 + (255-35) * ratio)
        draw.ellipse([size//2-i, size//2-i, size//2+i, size//2+i], fill=(r, g, b, 255))

    # Inner glow
    draw.ellipse([60, 60, size-60, size-60], fill=(100, 220, 255, 180), outline=(150, 240, 255, 100), width=3)

    # Text "P" in center
    try:
        font = ImageFont.truetype("segoeui.ttf", 120)
    except:
        font = ImageFont.load_default()

    text = "P"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 10

    # Shadow
    draw.text((x+3, y+3), text, font=font, fill=(0, 0, 0, 100))
    # Main text
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

    # Save multiple sizes
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)

    # Create .ico file
    icon_path = output_path.replace('.png', '.ico')
    img.save(icon_path, format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])

    print(f"Icon created: {output_path} and {icon_path}")
    return icon_path

if __name__ == "__main__":
    create_icon()
