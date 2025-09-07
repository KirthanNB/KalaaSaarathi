import qrcode, datetime
from PIL import Image, ImageDraw, ImageFont

def make_poster(shop_url: str, hero_img: str, price: int) -> str:
    qr = qrcode.make(shop_url)
    canvas = Image.new("RGB", (600, 900), "white")
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    draw.text((50, 50), "Scan & Buy", fill="black", font=font)
    canvas.paste(qr.resize((200, 200)), (200, 700))
    poster_path = f"posters/{uuid.uuid4().hex}.pdf"
    os.makedirs("posters", exist_ok=True)
    canvas.save(poster_path, "PDF", resolution=100)
    return poster_path