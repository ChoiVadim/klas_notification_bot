import os
import textwrap
import google.generativeai as genai

import telegramify_markdown


async def generate_response(message: str):
    genai.configure(api_key=os.getenv("GEMINI_API_TOKEN"))

    gemini = genai.GenerativeModel("gemini-2.0-flash")

    information = """
    Kwangwoon University is a university in Seoul, South Korea. 
    University website: https://www.kw.ac.kr/
    
    Some common questions:
    [
        {
            question: "How do I apply for lectures?",
            answer: "There are 2 different periods of application for classes. 1st one consists of 3 days for different departments. Only 2-4 year students can apply during this period. 2nd one is for 1st year students and lasts for 1 day. You can apply for lectures via Kwangwoon Class Registration program. <a href='https://klas.kw.ac.kr/std/cps/atnlc/LctreReqstNewProgPage.do' target='_blank'>Download here!</a>"
        },
        {
            question: "Can you apply for part payment, what are the conditions?",
            answer: "Part payment is available only if you have to pay more than 1,000,000 KRW. The sum is divided by 1,000,000 KRW; e.g. If your tuition is 1,500,000 this term, the payment is divided into two parts: 1,000,000 KRW and 500,000 KRW. The first part is paid before the semester starts, the second part is paid next month."
        },
        {
            question: "How to pay tuition?",
            answer: "online bank transfer"
        },
        {
            question: "Why are there already subjects saying '1 year only'?",
            answer: "Some subjects are meant for 1 years only, so you can apply for them only during "
        },
        {
            question: "What papers do one require to get part-work permit?",
            answer: "check immigration office website or Kwangwoon news feed"
        },
        {
            question: "Many questions about lecture registration",
            answer: "there is PDF document for that"
        },
        {
            question: "There is a compulsory Korean lectures for foreigners, can I cancel them?",
            answer: "If you have 5th level of Korean or more, attend the office"
        },
        {
            question: "Visa related questions",
            answer: "Kwangwoon newsfeed"
        },
        {
            question: "Credits related questions",
            answer: "If you have high average grade, you’re able to apply for 21 credit, otherwise – 18 credits. 1 hour a week lecture – 1 credit, practical lectures – 2 credits, 3 hours a week lectures – 3 credits"
        },
        {
            question: "Lectures for foreigners tend to be easier and contain less study material",
            answer: ""
        },
        {
            question: "This one is compulsory for graduation, better to take this one first year first term",
            answer: ""
        },
        {
            question: "How do I register subjects on MacOS?",
            answer: "There is no available program for MacOS, find a Windows PC (ask friend or PC)"
        },
        {
            question: "Can I listen to the lectures form other departments?",
            answer: "Yes, they will appear as at your record. Kinda same as . And if you take 2nd major or minor later, they will change to /"
        },
        {
            question: "Are there any special lectures to help foreigners with TOPIK exam?",
            answer: "Yes, sometimes 2 weeks before TOPIK the university holds small term courses to prepare for TOPIK. One should check the newsfeed"
        },
        {
            question: "What do I do if I’ve missed some lectures due to illness?",
            answer: "You gotta have a paper from the doctor which confirms you were ill. Bring it to the office of your department"
        },
        {
            question: "Do foreigners need to listen to lectures?",
            answer: "They are obligatory for Koreans, foreigners are allowed to skip them"
        },
        {
            question: "Do I need to pay ?",
            answer: "Not really but you get some benefits during events"
        },
        {
            question: "How to sign up for library application?",
            answer: "Use your student ID and password is your birthdate"
        },
        {
            question: "TOPIK fee refund and TOPIK level scholarship",
            answer: "You can get a refund of TOPIK fee once a semester, check the newsfeed; There is also a scholarship for TOPIK level: 600k won for the first time you increase your level 3->4 and so on, and 300k the second time you increase it 4->5 and so on). Check for  news at  tab."
        },
        {
            question: "You can receive your TOPIK fee (55000 won) once a semester via international affairs office. Check for  news at  tab.",
            answer: "You can receive your TOPIK fee (55000 won) once a semester via international affairs office. Check for  news at  tab."
        },
        {
            question: "Graduation conditions for foreigners: you need to have a valid TOPIK of 4 or higher, so make sure to pass the TOPIK 6 months before graduation. Most of the departments require just to have an appropriate total number of credits, either 133 or 130; 60 or 45 for major credits and 30 for elective courses. But departments from (, , , ) also need to make a graduation project. Keep that in mind!",
            answer: "Most of the departments require just to have an appropriate total number of credits, either 133 or 130; 60 or 45 for major credits and 30 for elective courses. But departments from (, , , ) also need to make a graduation project. Keep that in mind!"
        },
        {
            question: "You can go for double major(45-60, depends on the major requirements) or minor (21). To be able to register for that, you must have 3.0 or higher GPA, be 2-4 year student. Check for the  news at  tab on the website.",
            answer: "To be able to register for that, you must have 3.0 or higher GPA, be 2-4 year student. Check for the  news at  tab on the website."
        },
    ];
    """

    prompt = f"""System: You are a helpful assistant. Answer the user's question about university
    Information about the university: {information}
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
