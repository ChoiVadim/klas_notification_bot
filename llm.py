import os
import google.generativeai as genai


async def generate_advice(message: str):
    genai.configure(api_key=os.getenv("GEMINI_API_TOKEN"))

    gemini = genai.GenerativeModel("gemini-1.5-flash")
    gemini_pro = genai.GenerativeModel("gemini-1.5-pro")

    information = "Kwangwoon University is a university in Seoul, South Korea. It was founded in 1953. It has 13 colleges and 93 departments."
    prompt = f"System: You are a helpful assistant. Answer the user's question about university. There is some information about the university below."
    abilities = " Welcome! Please register to use the service.\n Use /register to start registration. Use /show to see your all assignments to do."
    prompt += f"\n\nInformation about the university: {information}"
    prompt += f"\n\nAbilities of the assistant: {abilities}"
    prompt += f"\n\nUser: {message}"

    res = await gemini_pro.generate_content_async(prompt)

    return res.text


if __name__ == "__main__":
    import asyncio
    import dotenv

    dotenv.load_dotenv()
    print(asyncio.run(generate_advice("Hello, how are you?")))
