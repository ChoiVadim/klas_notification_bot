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


def create_tuned_model():
    import time

    base_model = "models/gemini-1.5-flash-001-tuning"
    training_data = [
        {"text_input": "1", "output": "2"},
        {"text_input": "seven", "output": "eight"},
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
