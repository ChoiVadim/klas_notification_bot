import os
import textwrap
import google.generativeai as genai

import telegramify_markdown
from telegramify_markdown.customize import get_runtime_config


async def generate_response(message: str):
    genai.configure(api_key=os.getenv("GEMINI_API_TOKEN"))

    gemini = genai.GenerativeModel("gemini-2.0-flash")

    information = "Kwangwoon University is a university in Seoul, South Korea. Here is a link to the Kwangwoon University website: https://www.kw.ac.kr/"
    abilities = "You can answer questions about Kwangwoon University."

    prompt = f"""System: You are a helpful assistant. Answer the user's question about university
    Information about the university: {information}
    Abilities of the assistant: {abilities}
    User question: {message}
    """

    res = await gemini.generate_content_async(prompt)

    return format_response(res.text)


def format_response(raw_text: str) -> str:
    if not raw_text:
        return ""

    converted = telegramify_markdown.markdownify(
        textwrap.dedent(raw_text),
    )
    
    return converted


def create_tuned_model():
    import time

    base_model = "models/gemini-1.5-flash-001-tuning"
    training_data = [
        {"Lib reservation system": "1", "output": "2"},
        {"Lib reservation system": "seven", "output": "eight"},
    ]
    operation = genai.create_tuned_model(
        display_name="increment",
        source_model=base_model,
        epoch_count=20,
        batch_size=2,  # Adjusted batch size to be no larger than training examples size
        learning_rate=0.001,
        training_data=training_data,
    )

    for status in operation.wait_bar():
        time.sleep(10)

    result = operation.result()
    print(result)
    # # You can plot the loss curve with:
    # snapshots = pd.DataFrame(result.tuning_task.snapshots)
    # sns.lineplot(data=snapshots, x='epoch', y='mean_loss')

    model = genai.GenerativeModel(model_name=result.name)
    try:
        result = model.generate_content("III")
        print(result.text)  # IV
    except ValueError as e:
        print(f"Error generating content: {e}")


if __name__ == "__main__":
    import asyncio
    import dotenv

    dotenv.load_dotenv()
    print(asyncio.run(generate_response("Hello, how are you?")))
    create_tuned_model()
