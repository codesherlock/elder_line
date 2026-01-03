import requests, base64, random, io, os
from PIL import Image, ImageDraw, ImageFont

# 從 GitHub Secrets 讀取金鑰
LINE_ACCESS_TOKEN = os.getenv('LINE_ACCESS_TOKEN')
IMGBB_API_KEY = os.getenv('IMGBB_API_KEY')
FONT_PATH = './fonts/kaiu.ttf' 

def generate_ai_morning_image():
    # 30 天攝影風格與語錄配對資料庫
   data_pool = [
        {"style": "Breathtaking sunrise over a misty lavender field, cinematic lighting, photorealistic, 8k", "text": "歲月~靜好~安暖~"},
        {"style": "Traditional Chinese ink wash painting of lotus flowers with golden sun, artistic", "text": "好運~連連~吉祥~"},
        {"style": "A beautiful bouquet of red roses on a sunlit Parisian cafe table, blurred city background, 8k", "text": "平安~健康~快樂~"},
        {"style": "A steaming cup of coffee with heart-shaped latte art on a wooden balcony, sunrise mountains, highly detailed", "text": "幸福~喜樂~平安~"},
        {"style": "Close up of dew on blooming jasmine flowers in a quiet garden, morning sun flare, photorealistic", "text": "心情~燦爛~如花~"},
        {"style": "Warm autumn sunlight filtering through golden maple leaves onto a park bench, sharp focus, cinematic", "text": "知足~常樂~福寬~"},
        {"style": "An elegant tea set on a marble table at a luxury balcony, seaside sunrise, soft bokeh", "text": "心平~氣和~自在~"},
        {"style": "Zen stone garden with cherry blossoms falling at dawn, peaceful atmosphere, realistic photography", "text": "福氣~滿滿~如意~"},
        {"style": "Golden wheat field under a vast blue sky at dawn, vibrant colors, wide shot, 8k", "text": "萬事~亨通~順利~"},
        {"style": "Sunlight through a stained glass window, vibrant reflections on a wooden floor", "text": "光彩~奪目~希望~"},
        {"style": "A wooden bridge over a crystal clear stream in a green forest, morning mist, ray of light", "text": "順風~順水~安康~"},
        {"style": "Fresh sunflowers in a glass vase on a white windowsill, bright morning sun, 8k photography", "text": "陽光~萬丈~有你~"},
        {"style": "Mountain range with orange clouds at dawn, national geographic style, ultra-wide angle", "text": "步步~高升~輝煌~"},
        {"style": "A quiet cobblestone street in Europe at dawn, vintage street lamps glowing, soft fog", "text": "生活~有味~悠然~"},
        {"style": "Macro shot of a butterfly landing on a daisy, morning dew, vibrant nature photography", "text": "自在~悠閒~美好~"},
        {"style": "Row of colorful hot air balloons rising over a valley, cinematic golden hour, epic scale", "text": "夢想~成真~啟航~"},
        {"style": "Interior of a cozy library, morning sun hitting an open book and glasses, dusty air", "text": "智慧~如海~充實~"},
        {"style": "Peaceful white swans on a turquoise lake at dawn, reflection of sunrise on water", "text": "純淨~美好~如詩~"},
        {"style": "A bamboo forest path with light filtering through the leaves, zen atmosphere, realistic", "text": "清新~自然~寧靜~"},
        {"style": "Classic still life of fruits and a glass of juice on a linen tablecloth, morning light", "text": "碩果~累累~豐收~"},
        {"style": "Tropical beach with palm trees and a hammock, soft pastel sunrise colors, dreamy", "text": "放鬆~心情~愉快~"},
        {"style": "Stained glass lamp on a nightstand, warm glow, cozy morning bedroom atmosphere", "text": "溫馨~相伴~幸福~"},
        {"style": "Raindrops on a window with a blurred garden view outside, soft mood, high quality photography", "text": "雨過~天晴~希望~"},
        {"style": "An ancient stone castle on a hill shrouded in morning mist, epic fantasy style photography", "text": "宏圖~大展~威武~"},
        {"style": "A field of tulips in various colors under a bright blue morning sky, crisp focus", "text": "繽紛~世界~喜悅~"},
        {"style": "Traditional Japanese tea room overlooking a koi pond, soft morning light, hyper-realistic", "text": "禪意~生活~定心~"},
        {"style": "Snowy pine forest with golden sun rays piercing through branches, winter wonderland photography", "text": "純潔~無瑕~康泰~"},
        {"style": "Organic breakfast with honey and bread on a rustic table, outdoor garden setting, sunlit", "text": "品味~人生~活力~"},
        {"style": "Modern city skyline with glass buildings reflecting the sunrise, cinematic 8k photography", "text": "展望~未來~無限~"},
        {"style": "Cute kittens playing in a sunlit sunroom with yarn, soft and warm atmosphere", "text": "童心~未泯~快樂~"}
    ]
    
    pick = random.choice(data_pool)
    selected_style = pick["style"]
    sub_text = pick["text"]
    
    # 1. 調用 AI 繪圖 (調整為直式比例)
    prompt = requests.utils.quote(selected_style)
    ai_url = f"https://image.pollinations.ai/prompt/{prompt}?width=800&height=1000&nologo=true&seed={random.randint(1,999)}"
    resp = requests.get(ai_url)
    img = Image.open(io.BytesIO(resp.content))
    draw = ImageDraw.Draw(img)
    w, h = img.size
    
    # 2. 載入字體
    try:
        font_big = ImageFont.truetype(FONT_PATH, 120)  # 大字「早安」
        font_small = ImageFont.truetype(FONT_PATH, 55)  # 下方小字
    except:
        font_big = font_small = ImageFont.load_default()

    # 3. 仿造文青風錯落排版
    x_big, y_big = 100, h * 0.65
    x_small, y_small = w/2, h * 0.9
    
    # 繪製「早安」 (帶發光底彩)
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            draw.text((x_big+dx, y_big+dy), "早安", fill=(100, 149, 237, 150), font=font_big)
    draw.text((x_big, y_big), "早安", fill="white", font=font_big)
    
    # 繪製下方小字 (居中)
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            draw.text((x_small+dx, y_small+dy), sub_text, fill="black", font=font_small, anchor="mm")
    draw.text((x_small, y_small), sub_text, fill="white", font=font_small, anchor="mm")
    
    img.save("result.jpg")
    return "result.jpg"

def upload_and_broadcast():
    local_file = generate_ai_morning_image()
    with open(local_file, "rb") as f:
        img_resp = requests.post("https://api.imgbb.com/1/upload", data={
            "key": IMGBB_API_KEY, "image": base64.b64encode(f.read())
        })
    public_url = img_resp.json()['data']['url']

    line_url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"}
    payload = {"messages": [{"type": "image", "originalContentUrl": public_url, "previewImageUrl": public_url}]}
    requests.post(line_url, headers=headers, json=payload)

if __name__ == "__main__":
    upload_and_broadcast()
