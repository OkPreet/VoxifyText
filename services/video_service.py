import os, re, requests
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from config import UPLOAD_FOLDER

SLIDES_FOLDER = os.path.join(UPLOAD_FOLDER, "slides")
ASSETS_FOLDER = os.path.join("assets", "images")

os.makedirs(SLIDES_FOLDER, exist_ok=True)
os.makedirs(ASSETS_FOLDER, exist_ok=True)

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def extract_keywords(summary_text):
    keywords = []
    for line in summary_text.split("\n"):
        if not line.strip():
            continue
        words = re.findall(r"[A-Za-z]+", line)
        if words:
            keyword = " ".join(words[:2]).capitalize()
            keywords.append(keyword)
    return keywords

def fetch_image_from_pexels(keyword):
    safe_keyword = re.sub(r'[\\/*?:"<>|]', "_", keyword)

    if PEXELS_API_KEY:
        try:
            headers = {"Authorization": PEXELS_API_KEY}
            url = f"https://api.pexels.com/v1/search?query={keyword}&per_page=1"
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("photos"):
                    img_url = data["photos"][0]["src"]["medium"]
                    img_data = requests.get(img_url, timeout=5).content
                    path = os.path.join(SLIDES_FOLDER, f"{safe_keyword}.jpg")
                    with open(path, "wb") as f:
                        f.write(img_data)
                    return path
        except Exception as e:
            print(f"Pexels fetch failed: {e}")

    # fallback placeholder
    img = Image.new("RGB", (800, 600), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((100, 250), keyword, fill=(0, 0, 0), font=font)

    placeholder_path = os.path.join(SLIDES_FOLDER, f"default_{safe_keyword}.png")
    img.save(placeholder_path)
    return placeholder_path

def generate_video(summary_text, audio_path):
    keywords = extract_keywords(summary_text)
    image_paths = [fetch_image_from_pexels(word) for word in keywords]

    clips = []
    for path in image_paths:
        img_clip = ImageClip(path).set_duration(3).resize(width=640)
        img_clip = img_clip.resize(lambda t: 1 + 0.05 * t)
        clips.append(img_clip)

    video = concatenate_videoclips(clips, method="compose")
    audio = AudioFileClip(audio_path)
    video = video.set_audio(audio)

    video_path = os.path.join(UPLOAD_FOLDER, "animated_study_video.mp4")
    video.write_videofile(video_path, fps=24)

    return video_path
