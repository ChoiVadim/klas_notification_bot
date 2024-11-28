import os
import google.generativeai as genai


async def generate_response(message: str):
    genai.configure(api_key=os.getenv("GEMINI_API_TOKEN"))

    gemini = genai.GenerativeModel("gemini-1.5-flash")
    gemini_pro = genai.GenerativeModel("gemini-1.5-pro")

    information = "Kwangwoon University is a university in Seoul, South Korea."
    abilities = "You can answer questions about Kwangwoon University."

    prompt = f"""System: You are a helpful assistant. Answer the user's question about university
Information about the university: {information}
Abilities of the assistant: {abilities}
User question: {message}"""

    res = await gemini_pro.generate_content_async(prompt)

    return res.text


if __name__ == "__main__":
    import asyncio
    import dotenv

    dotenv.load_dotenv()
    print(asyncio.run(generate_response("Hello, how are you?")))
