from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "resources" / "icons"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def make_icon(size: int) -> Image.Image:
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    # Background rounded square
    pad = size // 10
    bg = (255, 0, 0, 255)
    draw.rounded_rectangle((pad, pad, size - pad, size - pad), radius=size // 6, fill=bg)
    # Play triangle
    triangle = [(size * 0.33, size * 0.26), (size * 0.33, size * 0.74), (size * 0.72, size * 0.5)]
    draw.polygon(triangle, fill=(255, 255, 255, 255))
    # Download arrow
    arrow_x = size * 0.58
    arrow_y = size * 0.58
    draw.line((arrow_x, size * 0.22, arrow_x, size * 0.56), fill=(255, 255, 255, 255), width=max(3, size // 18))
    draw.line((arrow_x - size * 0.14, size * 0.56, arrow_x + size * 0.14, size * 0.56), fill=(255, 255, 255, 255), width=max(3, size // 18))
    draw.line((arrow_x + size * 0.14, size * 0.56, arrow_x, size * 0.74), fill=(255, 255, 255, 255), width=max(3, size // 18))
    draw.line((arrow_x - size * 0.14, size * 0.56, arrow_x, size * 0.74), fill=(255, 255, 255, 255), width=max(3, size // 18))
    return image


def main() -> None:
    for size in (16, 24, 32, 48, 64, 128, 256):
        make_icon(size).save(OUT_DIR / f"app_icon_{size}.png")
    # ICO export with multiple sizes
    icon_images = [Image.open(OUT_DIR / f"app_icon_{size}.png").convert("RGBA") for size in (16, 24, 32, 48, 64, 128, 256)]
    icon_images[0].save(OUT_DIR / "app_icon.ico", format="ICO", sizes=[(img.size[0], img.size[1]) for img in icon_images])


if __name__ == "__main__":
    main()
