from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_summary(title: str, description: str, author: str) -> str:
    prompt = (
        "Summarize this book in 3 to 4  sentences for a reader.\n"
        f"Title: {title}\n"
        f"Description: {description}\n"
        f"Author: {author}\n"
    )
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        print("AI Summary Error:", e)
        return "No summary available."