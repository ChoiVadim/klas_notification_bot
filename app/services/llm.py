import os
import json
import logging

import textwrap
import telegramify_markdown
import google.generativeai as genai


async def generate_response(message: str, chat_history: list[dict]):
    genai.configure(api_key=os.getenv("GEMINI_API_TOKEN"))

    # Create model with specific parameters for better responses
    generation_config = {
        "temperature": 0.2,  # Lower temperature for more factual responses
        "top_p": 0.8,  # Control diversity
        "top_k": 40,  # Consider more options for responses
        "max_output_tokens": 2048,  # Allow longer responses if needed
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    gemini = genai.GenerativeModel(
        "gemini-2.0-flash",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )

    # Structure university information as a knowledge base
    information = {
        "general": {
            "name": "Kwangwoon University",
            "location": "Seoul, South Korea",
            "website": "https://www.kw.ac.kr/",
            "library-website": "https://kupis.kw.ac.kr/",
            "website-for-foreigners": "https://oia.kw.ac.kr/",
            "university-map": "https://www.kw.ac.kr/ko/tour/tour01.jsp",
            "phone": "+82-2-940-5114",
            "address": "서울 노원구 광운로 20",
            "buses": "261, 1017, 1137, 1140"
        },
        "faq": [
            {
                "question": "How do I apply for lectures?",
                "answer": "There are 2 different periods of application for classes. 1st one consists of 3 days for different departments. Only 2-4 year students can apply during this period. 2nd one is for 1st year students and lasts for 1 day. You can apply for lectures via Kwangwoon Class Registration program. <a href='https://klas.kw.ac.kr/std/cps/atnlc/LctreReqstNewProgPage.do' target='_blank'>Download here!</a>",
            },
            {
                "question": "Can you apply for part payment, what are the conditions?",
                "answer": "Part payment is available only if you have to pay more than 1,000,000 KRW. The sum is divided by 1,000,000 KRW; e.g. If your tuition is 1,500,000 this term, the payment is divided into two parts: 1,000,000 KRW and 500,000 KRW. The first part is paid before the semester starts, the second part is paid next month.",
            },
            {"question": "How to pay tuition?", "answer": "online bank transfer"},
            {
                "question": "Why are there already subjects saying '1 year only'?",
                "answer": "Some subjects are meant for 1 years only, so you can apply for them only during that period.",
            },
            {
                "question": "What papers do one require to get part-work permit?",
                "answer": "Check immigration office website or Kwangwoon news feed.",
            },
            {
                "question": "Many questions about lecture registration",
                "answer": "There is a PDF document for that in the university portal.",
            },
            {
                "question": "There is a compulsory Korean lectures for foreigners, can I cancel them?",
                "answer": "If you have 5th level of Korean or more, attend the office to request an exemption.",
            },
            {
                "question": "Visa related questions",
                "answer": "Check Kwangwoon newsfeed for the most current information.",
            },
            {
                "question": "Credits related questions",
                "answer": "If you have high average grade, you're able to apply for 21 credit, otherwise – 18 credits. 1 hour a week lecture – 1 credit, practical lectures – 2 credits, 3 hours a week lectures – 3 credits.",
            },
            {
                "question": "How do I register subjects on MacOS?",
                "answer": "There is no available program for MacOS, find a Windows PC (ask friend or PC).",
            },
            {
                "question": "Can I listen to the lectures from other departments?",
                "answer": "Yes, they will appear on your record. If you take 2nd major or minor later, they will be applied to those requirements.",
            },
            {
                "question": "Are there any special lectures to help foreigners with TOPIK exam?",
                "answer": "Yes, sometimes 2 weeks before TOPIK the university holds small term courses to prepare for TOPIK. One should check the newsfeed.",
            },
            {
                "question": "What do I do if I've missed some lectures due to illness?",
                "answer": "You need to have a paper from the doctor which confirms you were ill. Bring it to the office of your department.",
            },
            {
                "question": "Do foreigners need to listen to lectures?",
                "answer": "They are obligatory for Koreans, foreigners are allowed to skip them.",
            },
            {
                "question": "How to sign up for library application?",
                "answer": "Use your student ID and password is your birthdate.",
            },
            {
                "question": "TOPIK fee refund and TOPIK level scholarship",
                "answer": "You can get a refund of TOPIK fee once a semester, check the newsfeed; There is also a scholarship for TOPIK level: 600k won for the first time you increase your level 3->4 and so on, and 300k the second time you increase it 4->5 and so on). Check for news at the international tab.",
            },
            {
                "question": "Graduation conditions for foreigners",
                "answer": "You need to have a valid TOPIK of 4 or higher, so make sure to pass the TOPIK 6 months before graduation. Most departments require just to have an appropriate total number of credits, either 133 or 130; 60 or 45 for major credits and 30 for elective courses. Some departments also need a graduation project.",
            },
            {
                "question": "Double major or minor",
                "answer": "You can go for double major (45-60 credits, depends on the major requirements) or minor (21 credits). To be able to register for that, you must have 3.0 or higher GPA, be 2-4 year student. Check for news at the relevant tab on the website.",
            },
        ],
    }

    # System instructions
    system_prompt = f"""You are Kwangwoon University Assistant, a helpful AI that provides accurate information about Kwangwoon University in Seoul, South Korea.
    - Answer questions based only on the provided information
    - If you don't know the answer, say so honestly and suggest checking the university website
    - Format responses in short, clear paragraphs with markdown formatting
    - For URLs, make them clickable
    - Keep responses concise and to the point
    - Maintain a friendly, helpful tone
    - Use emojis to make responses more engaging!
    - Use a language that matches the user's language
    
    Knowledge base: {json.dumps(information)}
    """

    # Convert chat history to a plain text conversation
    conversation_history = ""
    for entry in chat_history:
        if entry["role"] == "user":
            conversation_history += f"User: {entry['content']}\n"
        else:
            conversation_history += f"Assistant: {entry['content']}\n"

    # Build complete prompt with history and system instructions
    complete_prompt = f"{system_prompt}\n\nPrevious conversation:\n{conversation_history}\n\nUser: {message}\nAssistant:"

    # Use the standard generate_content method instead of chat
    try:
        response = await gemini.generate_content_async(complete_prompt)
        return format_response(response.text)
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return format_response(
            "I apologize, but I encountered an error processing your request. Please try again later."
        )


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
    print(asyncio.run(generate_response("Hello, how are you?", [])))
    create_tuned_model()
