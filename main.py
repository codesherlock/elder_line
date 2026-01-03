import requests, base64, random, io, os
from PIL import Image, ImageDraw, ImageFont

# 這些金鑰會從 GitHub Secrets 讀取，不要直接寫在程式裡
LINE_ACCESS_TOKEN = os.getenv('LINE_ACCESS_TOKEN')
IMGBB_API_KEY = os.getenv('IMGBB_API_KEY')
FONT_PATH = './fonts/kaiu.ttf' # 指向你剛建立的 fonts 資料夾

def generate_ai_morning_image():
    # 1. AI 風格提示詞
    styles = [
        "oil painting of a peaceful sunrise forest",
        "traditional chinese ink wash painting of mountains",
        "soft watercolor flowers with morning dew",
        "zen style stone garden with sunlight"
    ]
    prompt = requests.utils.quote(random.choice(styles))
    
    # 2. 調用 AI 繪圖接口
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

    # 4. 隨機語錄
    quotes = ["平安喜樂", "早安吉祥", "萬事如意", "健康長壽"]
    text = f"早安\n{random.choice(quotes)}"
    
    # 5. 繪製文字外框與內容
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