import requests, base64, random, io, os
from PIL import Image, ImageDraw, ImageFont

# 這些金鑰會從 GitHub Secrets 讀取，不要直接寫在程式裡
LINE_ACCESS_TOKEN = os.getenv('LINE_ACCESS_TOKEN')
IMGBB_API_KEY = os.getenv('IMGBB_API_KEY')
FONT_PATH = './fonts/kaiu.ttf' # 指向你剛建立的 fonts 資料夾

def generate_ai_morning_image():
     # 1. 30 天風格與語錄對應資料庫
    data_pool = [
        {"style": "Breathtaking sunrise over a misty lavender field, cinematic lighting", "text": "早安\n歲月靜好"},
        {"style": "Traditional Chinese ink wash painting of lotus flowers, artistic", "text": "早安\n好運連連"},
        {"style": "Golden wheat field at dawn, oil painting style, warm tones", "text": "早安\n知足常樂"},
        {"style": "Ethereal forest with sunlight beams, dreamy fantasy style", "text": "早安\n平安喜樂"},
        {"style": "Macro photography of dew on a red rose, vibrant colors", "text": "早安\n心情燦爛"},
        {"style": "Zen style rock garden with cherry blossoms, peaceful atmosphere", "text": "早安\n福氣滿滿"},
        {"style": "Majestic snow-capped mountains at sunrise, 8k resolution", "text": "早安\n萬事亨通"},
        {"style": "Cozy cottage garden in spring, watercolor painting style", "text": "早安\n幸福安康"},
        {"style": "Abstract gold leaf and blue ink textures, modern art style", "text": "早安\n大吉大利"},
        {"style": "Calm ocean sunrise with soft pastel clouds, photorealistic", "text": "早安\n心平氣和"},
        {"style": "Sunlight through a stained glass window, vibrant reflections", "text": "早安\n光彩奪目"},
        {"style": "A peaceful tea set on a wooden table with morning mist", "text": "早安\n品味生活"},
        {"style": "Japanese Ukiyo-e style wave and golden sun", "text": "早安\n勇往直前"},
        {"style": "Soft bokeh of spring flowers in a sunlit meadow", "text": "早安\n春意盎然"},
        {"style": "Ancient temple in autumn with falling maple leaves", "text": "早安\n禪意生活"},
        {"style": "Lush tropical rainforest with exotic birds, vibrant greens", "text": "早安\n生機蓬勃"},
        {"style": "A quiet library with morning light hitting an open book", "text": "早安\n智慧如海"},
        {"style": "Starry sky fading into dawn over a quiet village", "text": "早安\n星光依舊"},
        {"style": "Minimalist Scandinavian interior with morning sun", "text": "早安\n簡約美好"},
        {"style": "Vivid sunflower field under a bright blue sky", "text": "早安\n陽光萬丈"},
        {"style": "Impressionist painting of a lily pond, Monet style", "text": "早安\n如詩如畫"},
        {"style": "Steaming cup of coffee on a balcony overlooking mountains", "text": "早安\n活力充沛"},
        {"style": "Graceful white swans on a lake at dawn", "text": "早安\n純淨美好"},
        {"style": "A path through a bamboo forest, soft sunlight filtering through", "text": "早安\n步步高升"},
        {"style": "Glowing paper lanterns in a misty morning garden", "text": "早安\n希望無限"},
        {"style": "Classic still life of fruits and flowers, Dutch masters style", "text": "早安\n碩果累累"},
        {"style": "A quaint stone bridge over a small stream in summer", "text": "早安\n順風順水"},
        {"style": "Vibrant hot air balloons rising over a valley at dawn", "text": "早安\n夢想成真"},
        {"style": "A field of daisies with a butterfly, macro style", "text": "早安\n自在悠閒"},
        {"style": "Golden statues in a grand hall with morning rays", "text": "早安\n富貴吉祥"}
    ]
    
    # 隨機抽取一組資料
    pick = random.choice(data_pool)
    selected_style = pick["style"]
    text = pick["text"]
    
    print(f"🎨 今日 AI 風格：{selected_style}")
    
    # 2. 調用 AI 繪圖接口
    prompt = requests.utils.quote(selected_style)
    ai_url = f"https://image.pollinations.ai/prompt/{prompt}?width=800&height=600&nologo=true&seed={random.randint(1,999)}"
    resp = requests.get(ai_url)
    img = Image.open(io.BytesIO(resp.content))
    draw = ImageDraw.Draw(img)
    w, h = img.size
    
    # 3. 載入字體
    try:
        font = ImageFont.truetype(FONT_PATH, 80)
    except:
        font = ImageFont.load_default()

    # 4. 繪製文字外框與內容 (強化清晰度)
    x, y = w/2, h/2
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            draw.text((x+dx, y+dy), text, fill="white", font=font, anchor="mm", align="center")
    draw.text((x, y), text, fill="#1A237E", font=font, anchor="mm", align="center")
    
    img.save("result.jpg")
    return "result.jpg"

def upload_and_broadcast():
    # 1. 生成圖片
    local_file = generate_ai_morning_image()

    # 2. 上傳到 ImgBB
    with open(local_file, "rb") as f:
        img_resp = requests.post("https://api.imgbb.com/1/upload", data={
            "key": IMGBB_API_KEY,
            "image": base64.b64encode(f.read())
        })
    public_url = img_resp.json()['data']['url']

    # 3. 使用「廣播」發送給所有加好友的人
    line_url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {
        "messages": [
            {
                "type": "image",
                "originalContentUrl": public_url,
                "previewImageUrl": public_url
            }
        ]
    }
    requests.post(line_url, headers=headers, json=payload)

if __name__ == "__main__":

    upload_and_broadcast()
