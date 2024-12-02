import asyncio
import logging

from app.bot import bot
from app.config import settings

from app.utils.encryption import decrypt_password
from app.database.database import get_all_users
from app.services.kw import KwangwoonUniversityApi


# Define time thresholds in hours and their corresponding emoji indicators
TIME_THRESHOLDS = {
    1: "🚨",  # Critical
    2: "⚠️",  # Warning
    3: "⏰",  # Alert
    6: "📢",  # Notice
    12: "ℹ️",  # Info
    24: "📅",  # Day notice
}


async def send_notification(message: str, user_id: str, urgency_level: int):
    try:
        emoji = TIME_THRESHOLDS.get(urgency_level, "📌")
        prefix = f"{emoji} {urgency_level} hour{'s' if urgency_level > 1 else ''} remaining!\n\n"
        postfix = "🚨 Don't forget to do it! 🚨"
        await bot.send_message(chat_id=user_id, text=prefix + message + postfix)
    except Exception as e:
        print(f"Error sending notification: {e}")


async def start_notification_service():
    # Creates a task that runs independently
    notification_task = asyncio.create_task(check_todos())
    notification_task.set_name("notification_checker")

    try:
        await notification_task
    except Exception as e:
        logging.error(f"Notification task failed: {e}")


async def check_todos():
    notification_tracker = {}

    while True:
        users = await get_all_users()

        for user in users:
            await asyncio.sleep(0)
            user_id = user.user_id
            if user_id not in notification_tracker:
                notification_tracker[user_id] = {}

            async with KwangwoonUniversityApi() as kw:
                await kw.login(user.username, decrypt_password(user.encrypted_password))
                todo_list = await kw.get_todo_list()

                threshold_messages = {
                    threshold: "" for threshold in TIME_THRESHOLDS.keys()
                }

                if not todo_list:
                    logging.info(f"No todo list found for user {user_id}")
                    continue

                for subject in todo_list:
                    subject_name = subject.get("name", "Unknown Subject")

                    # Assignment type emojis
                    type_emojis = {
                        "lectures": "📚",
                        "homeworks": "📝",
                        "quizzes": "🧠",
                        "team_projects": "🚧",
                    }

                    # Check each type of assignment
                    for assignment_type, emoji in type_emojis.items():
                        assignments = subject["todo"].get(assignment_type, [])
                        if assignments:
                            for assignment in assignments:
                                # Create unique assignment identifier
                                assignment_id = f"{subject_name}_{assignment_type}_{assignment.get('title', '')}"

                                # Initialize assignment tracker if not exists
                                if assignment_id not in notification_tracker[user_id]:
                                    notification_tracker[user_id][assignment_id] = set()

                                left_time = assignment["left_time"].seconds
                                days_left = assignment["left_time"].days
                                hours_left = left_time // 3600
                                title = assignment["title"]

                                if abs(days_left) > 0:
                                    continue

                                for threshold in TIME_THRESHOLDS.keys():
                                    if (
                                        hours_left <= threshold
                                        and hours_left
                                        > max(
                                            [
                                                t
                                                for t in TIME_THRESHOLDS.keys()
                                                if t < threshold
                                            ],
                                            default=0,
                                        )
                                        and threshold
                                        not in notification_tracker[user_id][
                                            assignment_id
                                        ]
                                    ):  # Check if notification wasn't sent

                                        threshold_messages[threshold] += (
                                            f"{emoji} {subject_name}\n"
                                            f"Type: {assignment_type.title()}\n"
                                            f"Title: {title}\n"
                                            f"Time left: {hours_left} hour{'s' if hours_left != 1 else ''}"
                                            f" and {left_time % 3600 // 60} minutes\n\n"
                                        )
                                        # Mark this threshold as notified for this assignment
                                        notification_tracker[user_id][
                                            assignment_id
                                        ].add(threshold)

                # Send notifications for each threshold that has messages
                for threshold, message in threshold_messages.items():
                    if message:
                        await send_notification(message, user_id, threshold)
                        await asyncio.sleep(1)

            # Clean up old assignments from tracker
            current_assignments = {
                f"{subject['name']}_{type_}_{assignment.get('title', '')}"
                for subject in todo_list
                for type_ in type_emojis.keys()
                for assignment in subject["todo"].get(type_, [])
            }

            notification_tracker[user_id] = {
                assignment_id: thresholds
                for assignment_id, thresholds in notification_tracker[user_id].items()
                if assignment_id in current_assignments
            }

        await asyncio.sleep(settings.NOTIFICATION_CHECK_INTERVAL)
