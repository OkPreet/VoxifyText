import requests, os
from config import UNSPLASH_API_KEY, UPLOAD_FOLDER

IMAGES_FOLDER = os.path.join(UPLOAD_FOLDER, "images")
os.makedirs(IMAGES_FOLDER, exist_ok=True)

def fetch_image(keyword):
    """
    Fetch an image from Unsplash API using keyword.
    """
    url = "https://api.unsplash.com/photos/random"
    params = {"query": keyword, "orientation": "landscape"}
    headers = {"Authorization": f"Client-ID {UNSPLASH_API_KEY}"}

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        image_url = data['urls']['regular']

        img_data = requests.get(image_url).content
        path = os.path.join(IMAGES_FOLDER, f"{keyword}.jpg")
        with open(path, "wb") as f:
            f.write(img_data)
        return path
    else:
        return None
