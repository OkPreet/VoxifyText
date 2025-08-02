import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def summarize_text(text):
    """
    Summarizes input text into clean educational points
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        f"Summarize this text into simple educational bullet points for students.\n"
        f"Remove any '*' '**',do not include bulletpoints, symbols or extra formatting.\n\n{text}"
    )
    response = model.generate_content(prompt)
    return response.text
