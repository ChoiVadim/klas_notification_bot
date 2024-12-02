import asyncio


async def check_todos():
    while True:
        print("Checking todos...")
        # Heavy processing here
        for i in range(1000000):  # Simulate heavy work
            _ = i * i
        await asyncio.sleep(15 * 60)  # 15 minutes


async def handle_message():
    for i in range(10):
        print("Bot received a message!")
        await asyncio.sleep(1)


async def main():
    todo_task = asyncio.create_task(check_todos())
    bot_task = asyncio.create_task(handle_message())

    await asyncio.gather(todo_task, bot_task)


asyncio.run(main())
